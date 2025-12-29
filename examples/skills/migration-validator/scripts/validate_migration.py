#!/usr/bin/env python3
"""
Database migration validator.
Analyzes SQL migrations for safety, performance, and reversibility.
"""

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any


class Severity(Enum):
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


@dataclass
class Issue:
    severity: Severity
    category: str
    message: str
    file: str
    line: int | None = None
    sql: str | None = None
    suggestion: str | None = None


@dataclass
class MigrationAnalysis:
    file: str
    issues: list[Issue] = field(default_factory=list)
    operations: list[str] = field(default_factory=list)
    tables_affected: set[str] = field(default_factory=set)
    has_down: bool = False
    is_reversible: bool = True


# Dangerous SQL patterns and their risk levels
DANGEROUS_PATTERNS = [
    {
        "pattern": r"\bDROP\s+TABLE\b",
        "severity": Severity.ERROR,
        "category": "data_loss",
        "message": "DROP TABLE will permanently delete all data",
        "suggestion": "Consider renaming table first, then dropping after verification period"
    },
    {
        "pattern": r"\bDROP\s+COLUMN\b",
        "severity": Severity.ERROR,
        "category": "data_loss",
        "message": "DROP COLUMN will permanently delete column data",
        "suggestion": "Mark column as deprecated, stop writing, then drop after data migration"
    },
    {
        "pattern": r"\bTRUNCATE\b",
        "severity": Severity.ERROR,
        "category": "data_loss",
        "message": "TRUNCATE will delete all rows without logging",
        "suggestion": "Use DELETE with WHERE clause or backup data first"
    },
    {
        "pattern": r"\bDROP\s+DATABASE\b",
        "severity": Severity.ERROR,
        "category": "data_loss",
        "message": "DROP DATABASE is extremely dangerous",
        "suggestion": "This should never be in a migration file"
    },
    {
        "pattern": r"ALTER\s+TABLE\s+\w+\s+ADD\s+(?:COLUMN\s+)?\w+.*NOT\s+NULL(?!\s+DEFAULT)",
        "severity": Severity.ERROR,
        "category": "breaking_change",
        "message": "Adding NOT NULL column without DEFAULT will fail on tables with data",
        "suggestion": "Add DEFAULT value or make nullable, then backfill, then add NOT NULL"
    },
    {
        "pattern": r"\bRENAME\s+TABLE\b|\bALTER\s+TABLE\s+\w+\s+RENAME\s+TO\b",
        "severity": Severity.WARNING,
        "category": "breaking_change",
        "message": "Renaming table will break existing queries",
        "suggestion": "Create new table, migrate data, update code, then drop old table"
    },
    {
        "pattern": r"ALTER\s+TABLE\s+\w+\s+RENAME\s+COLUMN\b",
        "severity": Severity.WARNING,
        "category": "breaking_change",
        "message": "Renaming column will break existing queries",
        "suggestion": "Add new column, backfill, update code, then drop old column"
    },
    {
        "pattern": r"ALTER\s+TABLE\s+\w+\s+ALTER\s+COLUMN\s+\w+\s+TYPE\b",
        "severity": Severity.WARNING,
        "category": "locking",
        "message": "Changing column type may require table rewrite and acquire locks",
        "suggestion": "Test on production-size data first; consider using pg_repack for large tables"
    },
    {
        "pattern": r"\bCREATE\s+INDEX\b(?!\s+CONCURRENTLY)",
        "severity": Severity.WARNING,
        "category": "locking",
        "message": "CREATE INDEX without CONCURRENTLY blocks writes",
        "suggestion": "Use CREATE INDEX CONCURRENTLY to avoid blocking"
    },
    {
        "pattern": r"\bCREATE\s+UNIQUE\s+INDEX\b(?!\s+CONCURRENTLY)",
        "severity": Severity.WARNING,
        "category": "locking",
        "message": "CREATE UNIQUE INDEX without CONCURRENTLY blocks writes",
        "suggestion": "Use CREATE UNIQUE INDEX CONCURRENTLY"
    },
    {
        "pattern": r"\bADD\s+CONSTRAINT\b.*\bFOREIGN\s+KEY\b",
        "severity": Severity.WARNING,
        "category": "locking",
        "message": "Adding foreign key constraint validates existing rows and acquires lock",
        "suggestion": "Add constraint as NOT VALID, then validate separately"
    },
    {
        "pattern": r"\bADD\s+CONSTRAINT\b.*\bCHECK\b",
        "severity": Severity.INFO,
        "category": "locking",
        "message": "Adding CHECK constraint validates existing rows",
        "suggestion": "For large tables, add as NOT VALID first, then VALIDATE CONSTRAINT"
    },
    {
        "pattern": r"\bUPDATE\b.*\bSET\b(?!.*\bWHERE\b)",
        "severity": Severity.WARNING,
        "category": "performance",
        "message": "UPDATE without WHERE clause will update all rows",
        "suggestion": "Add WHERE clause or batch the update"
    },
    {
        "pattern": r"\bDELETE\s+FROM\b(?!.*\bWHERE\b)",
        "severity": Severity.WARNING,
        "category": "performance",
        "message": "DELETE without WHERE clause will delete all rows",
        "suggestion": "Add WHERE clause or use TRUNCATE if intentional"
    },
    {
        "pattern": r"\bLOCK\s+TABLE\b",
        "severity": Severity.WARNING,
        "category": "locking",
        "message": "Explicit table lock may cause deadlocks",
        "suggestion": "Review lock mode and ensure proper ordering"
    }
]

# Patterns indicating irreversible operations
IRREVERSIBLE_PATTERNS = [
    r"\bDROP\s+(?:TABLE|COLUMN|INDEX|CONSTRAINT|DATABASE)\b",
    r"\bTRUNCATE\b",
    r"\bDELETE\s+FROM\b",
    r"\bUPDATE\b.*\bSET\b",
]


def extract_sql_from_file(file_path: Path) -> list[tuple[str, int]]:
    """Extract SQL statements from various migration formats."""
    content = file_path.read_text(errors="ignore")
    statements = []

    ext = file_path.suffix.lower()

    if ext == ".sql":
        # Raw SQL file
        lines = content.split("\n")
        current_stmt = []
        start_line = 1

        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if stripped and not stripped.startswith("--"):
                if not current_stmt:
                    start_line = i
                current_stmt.append(line)

                if stripped.endswith(";"):
                    statements.append(("\n".join(current_stmt), start_line))
                    current_stmt = []

        if current_stmt:
            statements.append(("\n".join(current_stmt), start_line))

    elif ext in [".js", ".ts"]:
        # Knex.js / TypeORM style migrations
        # Extract SQL from template literals and .raw() calls
        raw_patterns = [
            r'\.raw\s*\(\s*[`\'"]([^`\'"]+)[`\'"]\s*\)',
            r'knex\.schema\.raw\s*\(\s*[`\'"]([^`\'"]+)[`\'"]\s*\)',
            r'`([^`]*(?:CREATE|ALTER|DROP|INSERT|UPDATE|DELETE)[^`]*)`',
        ]

        for pattern in raw_patterns:
            for match in re.finditer(pattern, content, re.IGNORECASE | re.DOTALL):
                sql = match.group(1)
                # Approximate line number
                line_num = content[:match.start()].count("\n") + 1
                statements.append((sql, line_num))

        # Also extract table operations from schema builder
        schema_patterns = [
            (r'\.createTable\s*\(\s*[\'"](\w+)[\'"]', "CREATE TABLE"),
            (r'\.dropTable\s*\(\s*[\'"](\w+)[\'"]', "DROP TABLE"),
            (r'\.renameTable\s*\(\s*[\'"](\w+)[\'"]', "RENAME TABLE"),
            (r'\.table\s*\(\s*[\'"](\w+)[\'"].*\.dropColumn', "DROP COLUMN"),
        ]

        for pattern, op_type in schema_patterns:
            for match in re.finditer(pattern, content, re.IGNORECASE):
                table = match.group(1)
                line_num = content[:match.start()].count("\n") + 1
                statements.append((f"{op_type} {table}", line_num))

    elif ext == ".py":
        # Alembic / Django migrations
        op_patterns = [
            (r'op\.execute\s*\(\s*[\'"]([^\'"]+)[\'"]', None),
            (r'op\.drop_table\s*\(\s*[\'"](\w+)[\'"]', "DROP TABLE"),
            (r'op\.drop_column\s*\(\s*[\'"](\w+)[\'"]', "DROP COLUMN"),
            (r'op\.create_index\s*\(\s*[\'"](\w+)[\'"]', "CREATE INDEX"),
            (r'migrations\.RunSQL\s*\(\s*[\'"]([^\'"]+)[\'"]', None),
        ]

        for pattern, op_type in op_patterns:
            for match in re.finditer(pattern, content):
                sql = match.group(1)
                if op_type:
                    sql = f"{op_type} {sql}"
                line_num = content[:match.start()].count("\n") + 1
                statements.append((sql, line_num))

    return statements


def extract_tables(sql: str) -> set[str]:
    """Extract table names from SQL statement."""
    tables = set()

    patterns = [
        r'\bFROM\s+(\w+)',
        r'\bJOIN\s+(\w+)',
        r'\bINTO\s+(\w+)',
        r'\bUPDATE\s+(\w+)',
        r'\bTABLE\s+(\w+)',
        r'\bON\s+(\w+)',
    ]

    for pattern in patterns:
        for match in re.finditer(pattern, sql, re.IGNORECASE):
            tables.add(match.group(1).lower())

    return tables


def analyze_migration(file_path: Path, level: str = "strict") -> MigrationAnalysis:
    """Analyze a single migration file."""
    analysis = MigrationAnalysis(file=str(file_path.name))

    statements = extract_sql_from_file(file_path)

    for sql, line_num in statements:
        sql_upper = sql.upper()

        # Track operations and tables
        for op in ["CREATE", "ALTER", "DROP", "INSERT", "UPDATE", "DELETE", "TRUNCATE"]:
            if op in sql_upper:
                analysis.operations.append(op)

        analysis.tables_affected.update(extract_tables(sql))

        # Check against dangerous patterns
        for pattern_info in DANGEROUS_PATTERNS:
            if re.search(pattern_info["pattern"], sql, re.IGNORECASE):
                # Skip warnings in permissive mode
                if level == "permissive" and pattern_info["severity"] == Severity.WARNING:
                    continue

                analysis.issues.append(Issue(
                    severity=pattern_info["severity"],
                    category=pattern_info["category"],
                    message=pattern_info["message"],
                    file=str(file_path.name),
                    line=line_num,
                    sql=sql[:200] + "..." if len(sql) > 200 else sql,
                    suggestion=pattern_info["suggestion"]
                ))

        # Check reversibility
        for pattern in IRREVERSIBLE_PATTERNS:
            if re.search(pattern, sql, re.IGNORECASE):
                analysis.is_reversible = False
                break

    # Check for down migration
    parent = file_path.parent
    down_patterns = [
        file_path.stem + ".down.sql",
        file_path.stem.replace(".up", ".down") + file_path.suffix,
    ]

    for pattern in down_patterns:
        if (parent / pattern).exists():
            analysis.has_down = True
            break

    # Also check for down() function in JS/TS/Python files
    if file_path.suffix in [".js", ".ts", ".py"]:
        content = file_path.read_text(errors="ignore")
        if re.search(r'\bdef\s+downgrade\b|\bexports\.down\b|\basync\s+down\b|\.down\s*=', content):
            analysis.has_down = True

    return analysis


def format_report(analyses: list[MigrationAnalysis], format: str = "text") -> str:
    """Format analysis report."""
    all_issues = []
    for analysis in analyses:
        all_issues.extend(analysis.issues)

    if format == "json":
        return json.dumps({
            "migrations": [
                {
                    "file": a.file,
                    "issues": [
                        {
                            "severity": i.severity.value,
                            "category": i.category,
                            "message": i.message,
                            "line": i.line,
                            "sql": i.sql,
                            "suggestion": i.suggestion
                        }
                        for i in a.issues
                    ],
                    "operations": a.operations,
                    "tables_affected": list(a.tables_affected),
                    "has_down": a.has_down,
                    "is_reversible": a.is_reversible
                }
                for a in analyses
            ],
            "summary": {
                "total_migrations": len(analyses),
                "errors": len([i for i in all_issues if i.severity == Severity.ERROR]),
                "warnings": len([i for i in all_issues if i.severity == Severity.WARNING]),
            }
        }, indent=2)

    # Text format
    lines = ["=" * 60, "MIGRATION VALIDATION REPORT", "=" * 60, ""]

    errors = [i for i in all_issues if i.severity == Severity.ERROR]
    warnings = [i for i in all_issues if i.severity == Severity.WARNING]

    if not all_issues:
        lines.append("✅ All migrations passed validation!")
        return "\n".join(lines)

    # Summary
    lines.append(f"Analyzed {len(analyses)} migration(s)")
    lines.append(f"Found {len(errors)} error(s), {len(warnings)} warning(s)")
    lines.append("")

    # Errors
    if errors:
        lines.append("## ❌ ERRORS (Must Fix Before Deploy)")
        lines.append("")
        for issue in errors:
            lines.append(f"**{issue.file}:{issue.line or '?'}** [{issue.category}]")
            lines.append(f"  {issue.message}")
            if issue.sql:
                lines.append(f"  ```sql")
                lines.append(f"  {issue.sql}")
                lines.append(f"  ```")
            if issue.suggestion:
                lines.append(f"  💡 {issue.suggestion}")
            lines.append("")

    # Warnings
    if warnings:
        lines.append("## ⚠️  WARNINGS (Review Before Deploy)")
        lines.append("")
        for issue in warnings:
            lines.append(f"**{issue.file}:{issue.line or '?'}** [{issue.category}]")
            lines.append(f"  {issue.message}")
            if issue.suggestion:
                lines.append(f"  💡 {issue.suggestion}")
            lines.append("")

    # Migration status
    lines.append("## Migration Status")
    lines.append("")
    for analysis in analyses:
        status = "✅" if not analysis.issues else "❌" if any(i.severity == Severity.ERROR for i in analysis.issues) else "⚠️"
        reversible = "↩️" if analysis.is_reversible else "⛔"
        down = "✓" if analysis.has_down else "✗"
        lines.append(f"{status} {analysis.file} | down: {down} | reversible: {reversible}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Validate database migrations")
    parser.add_argument("--path", required=True, help="Migration files path")
    parser.add_argument("--level", choices=["strict", "permissive"], default="strict")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    parser.add_argument("--fail-on-warning", action="store_true")
    args = parser.parse_args()

    path = Path(args.path)

    # Find migration files
    migration_files = []
    extensions = [".sql", ".js", ".ts", ".py"]

    if path.is_file():
        migration_files.append(path)
    else:
        for ext in extensions:
            migration_files.extend(path.rglob(f"*{ext}"))

    # Filter out down migrations and test files
    migration_files = [
        f for f in migration_files
        if ".down." not in f.name
        and "_test" not in f.name
        and ".test." not in f.name
        and "node_modules" not in str(f)
    ]

    if not migration_files:
        print("No migration files found", file=sys.stderr)
        sys.exit(0)

    # Analyze each migration
    analyses = [analyze_migration(f, args.level) for f in sorted(migration_files)]

    print(format_report(analyses, args.format))

    # Exit code
    all_issues = [i for a in analyses for i in a.issues]
    has_errors = any(i.severity == Severity.ERROR for i in all_issues)
    has_warnings = any(i.severity == Severity.WARNING for i in all_issues)

    if has_errors:
        sys.exit(1)
    if args.fail_on_warning and has_warnings:
        sys.exit(1)


if __name__ == "__main__":
    main()
