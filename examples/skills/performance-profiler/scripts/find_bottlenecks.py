#!/usr/bin/env python3
"""
Static analysis tool to find potential performance bottlenecks in source code.
"""

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Generator


@dataclass
class Issue:
    severity: str  # high, medium, low
    category: str
    file: str
    line: int
    code: str
    message: str
    suggestion: str


# Patterns that indicate potential performance issues
PATTERNS = {
    "nodejs": [
        {
            "pattern": r"\bfs\.(readFileSync|writeFileSync|appendFileSync)\b",
            "severity": "high",
            "category": "sync_io",
            "message": "Synchronous file operation blocks the event loop",
            "suggestion": "Use async alternatives: fs.promises.readFile, fs.promises.writeFile"
        },
        {
            "pattern": r"\bchild_process\.(execSync|spawnSync)\b",
            "severity": "high",
            "category": "sync_io",
            "message": "Synchronous process execution blocks the event loop",
            "suggestion": "Use async alternatives: exec, spawn with promisify"
        },
        {
            "pattern": r"JSON\.parse\([^)]{100,}\)",
            "severity": "medium",
            "category": "cpu_intensive",
            "message": "Parsing large JSON synchronously can block",
            "suggestion": "Consider streaming JSON parser for large payloads"
        },
        {
            "pattern": r"\.forEach\(\s*async\s*\(",
            "severity": "high",
            "category": "async_antipattern",
            "message": "forEach with async doesn't await - operations run in parallel uncontrolled",
            "suggestion": "Use for...of loop or Promise.all with map"
        },
        {
            "pattern": r"await\s+\w+\s*\(\s*\).*\n.*await\s+\w+\s*\(\s*\)",
            "severity": "medium",
            "category": "sequential_await",
            "message": "Sequential awaits that could be parallel",
            "suggestion": "Use Promise.all([...]) for independent operations"
        },
        {
            "pattern": r"new\s+RegExp\([^)]+\)",
            "severity": "low",
            "category": "regex_in_loop",
            "message": "RegExp created dynamically - may be in hot path",
            "suggestion": "Move RegExp to module scope if pattern is constant"
        },
        {
            "pattern": r"while\s*\(\s*true\s*\)",
            "severity": "medium",
            "category": "infinite_loop",
            "message": "Potential infinite loop",
            "suggestion": "Ensure proper exit condition and consider setImmediate for yielding"
        },
        {
            "pattern": r"\.push\([^)]+\).*\.push\([^)]+\).*\.push\([^)]+\)",
            "severity": "low",
            "category": "array_growth",
            "message": "Multiple array pushes - consider pre-allocation",
            "suggestion": "Pre-allocate array if size is known"
        },
        {
            "pattern": r"console\.(log|info|warn|error)\(",
            "severity": "low",
            "category": "logging",
            "message": "Console logging in production code",
            "suggestion": "Use proper logging library with levels and async output"
        },
    ],
    "python": [
        {
            "pattern": r"for\s+\w+\s+in\s+range\([^)]+\):\s*\n\s+.*\.append\(",
            "severity": "medium",
            "category": "list_append_loop",
            "message": "Building list with append in loop",
            "suggestion": "Use list comprehension: [expr for x in range(...)]"
        },
        {
            "pattern": r"\+\s*=\s*['\"]",
            "severity": "medium",
            "category": "string_concat",
            "message": "String concatenation in loop creates new objects",
            "suggestion": "Use ''.join() or io.StringIO for building strings"
        },
        {
            "pattern": r"except\s*:\s*\n\s*pass",
            "severity": "medium",
            "category": "silent_exception",
            "message": "Silent exception handling hides performance issues",
            "suggestion": "Log exceptions or handle specifically"
        },
        {
            "pattern": r"import\s+\*\s+from",
            "severity": "low",
            "category": "star_import",
            "message": "Star import loads unnecessary modules",
            "suggestion": "Import only needed names"
        },
        {
            "pattern": r"\.read\(\)(?!\s*\.)",
            "severity": "medium",
            "category": "full_file_read",
            "message": "Reading entire file into memory",
            "suggestion": "Use iteration or chunked reading for large files"
        },
        {
            "pattern": r"time\.sleep\(",
            "severity": "medium",
            "category": "blocking_sleep",
            "message": "Blocking sleep in potentially async context",
            "suggestion": "Use asyncio.sleep in async code"
        },
        {
            "pattern": r"global\s+\w+",
            "severity": "low",
            "category": "global_variable",
            "message": "Global variable access is slower than local",
            "suggestion": "Pass as parameter or use local reference"
        },
    ]
}


def find_files(path: Path, project_type: str) -> Generator[Path, None, None]:
    """Find source files based on project type."""
    extensions = {
        "nodejs": [".js", ".ts", ".mjs"],
        "python": [".py"],
    }

    for ext in extensions.get(project_type, []):
        for file_path in path.rglob(f"*{ext}"):
            # Skip common non-source directories
            if any(p in file_path.parts for p in [
                "node_modules", "__pycache__", ".git", "dist", "build",
                "venv", ".venv", "env", ".env"
            ]):
                continue
            yield file_path


def analyze_file(file_path: Path, patterns: list[dict]) -> list[Issue]:
    """Analyze a single file for performance issues."""
    issues = []

    try:
        content = file_path.read_text(errors="ignore")
        lines = content.split("\n")
    except Exception:
        return issues

    for pattern_info in patterns:
        pattern = pattern_info["pattern"]

        for match in re.finditer(pattern, content, re.MULTILINE):
            # Calculate line number
            line_num = content[:match.start()].count("\n") + 1
            matched_code = match.group(0)[:100]

            issues.append(Issue(
                severity=pattern_info["severity"],
                category=pattern_info["category"],
                file=str(file_path),
                line=line_num,
                code=matched_code,
                message=pattern_info["message"],
                suggestion=pattern_info["suggestion"]
            ))

    return issues


def find_n_plus_one_patterns(path: Path, project_type: str) -> list[Issue]:
    """Look for N+1 query patterns."""
    issues = []

    # Patterns that suggest N+1 queries
    n_plus_one_patterns = {
        "nodejs": [
            # Query inside loop
            r"for\s*\([^)]+\)\s*\{[^}]*\b(findOne|findById|query|execute)\b",
            r"\.map\(\s*async[^}]+\b(findOne|findById|query|execute)\b",
            r"\.forEach\([^}]+\b(findOne|findById|query|execute)\b",
        ],
        "python": [
            r"for\s+\w+\s+in\s+\w+:[^:]+\.(get|filter|execute|query)\(",
            r"\[\s*\w+\.(get|filter)\([^]]+for\s+\w+\s+in",
        ]
    }

    for file_path in find_files(path, project_type):
        content = file_path.read_text(errors="ignore")

        for pattern in n_plus_one_patterns.get(project_type, []):
            for match in re.finditer(pattern, content, re.MULTILINE | re.DOTALL):
                line_num = content[:match.start()].count("\n") + 1
                issues.append(Issue(
                    severity="high",
                    category="n_plus_one",
                    file=str(file_path),
                    line=line_num,
                    code=match.group(0)[:80],
                    message="Potential N+1 query pattern detected",
                    suggestion="Batch queries or use eager loading/joins"
                ))

    return issues


def format_report(issues: list[Issue], format: str = "text") -> str:
    """Format the analysis report."""

    if format == "json":
        import json
        return json.dumps([
            {
                "severity": i.severity,
                "category": i.category,
                "file": i.file,
                "line": i.line,
                "code": i.code,
                "message": i.message,
                "suggestion": i.suggestion
            }
            for i in issues
        ], indent=2)

    if not issues:
        return "✅ No performance issues detected!"

    lines = ["=" * 60, "PERFORMANCE BOTTLENECK ANALYSIS", "=" * 60, ""]

    # Group by severity
    high = [i for i in issues if i.severity == "high"]
    medium = [i for i in issues if i.severity == "medium"]
    low = [i for i in issues if i.severity == "low"]

    lines.append(f"Found {len(issues)} potential issues:")
    lines.append(f"  🔴 High: {len(high)}  🟡 Medium: {len(medium)}  🔵 Low: {len(low)}")
    lines.append("")

    if high:
        lines.append("## 🔴 High Priority")
        lines.append("")
        for i in high:
            lines.append(f"**{i.file}:{i.line}** [{i.category}]")
            lines.append(f"  {i.message}")
            lines.append(f"  ```")
            lines.append(f"  {i.code}")
            lines.append(f"  ```")
            lines.append(f"  💡 {i.suggestion}")
            lines.append("")

    if medium:
        lines.append("## 🟡 Medium Priority")
        lines.append("")
        for i in medium[:10]:  # Limit to 10
            lines.append(f"**{i.file}:{i.line}** [{i.category}]")
            lines.append(f"  {i.message}")
            lines.append(f"  💡 {i.suggestion}")
            lines.append("")

        if len(medium) > 10:
            lines.append(f"... and {len(medium) - 10} more medium issues")
            lines.append("")

    if low:
        lines.append(f"## 🔵 Low Priority ({len(low)} issues)")
        lines.append("")
        lines.append("Run with --include-low to see details")
        lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Find performance bottlenecks in source code")
    parser.add_argument("--path", default=".", help="Project path")
    parser.add_argument("--type", choices=["nodejs", "python"], required=True)
    parser.add_argument("--format", choices=["text", "json"], default="text")
    parser.add_argument("--include-low", action="store_true", help="Include low severity issues")
    args = parser.parse_args()

    path = Path(args.path).resolve()
    patterns = PATTERNS.get(args.type, [])

    all_issues = []

    # Analyze each file
    for file_path in find_files(path, args.type):
        issues = analyze_file(file_path, patterns)
        all_issues.extend(issues)

    # Look for N+1 patterns
    all_issues.extend(find_n_plus_one_patterns(path, args.type))

    # Filter low severity if not requested
    if not args.include_low:
        all_issues = [i for i in all_issues if i.severity != "low"]

    # Sort by severity
    severity_order = {"high": 0, "medium": 1, "low": 2}
    all_issues.sort(key=lambda x: severity_order.get(x.severity, 3))

    print(format_report(all_issues, args.format))

    # Exit code based on high severity issues
    if any(i.severity == "high" for i in all_issues):
        sys.exit(1)


if __name__ == "__main__":
    main()
