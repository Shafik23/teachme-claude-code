#!/usr/bin/env python3
"""
Architecture enforcement tool.
Validates code against defined architectural rules.
"""

import argparse
import json
import re
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class Violation:
    """Represents an architecture violation."""
    rule: str
    severity: str  # error, warning
    file: str
    line: int | None
    message: str
    suggestion: str | None = None


class ArchitectureEnforcer:
    def __init__(self, config: dict, project_path: Path):
        self.config = config
        self.project_path = project_path
        self.violations: list[Violation] = []

    def check_layers(self) -> list[Violation]:
        """Check that layer dependencies are respected."""
        violations = []
        layers = self.config.get("layers", {})

        if not layers:
            return violations

        # Build a map of paths to layers
        path_to_layer = {}
        for layer_name, layer_config in layers.items():
            patterns = layer_config.get("paths", [f"src/{layer_name}/**/*"])
            for pattern in patterns:
                path_to_layer[pattern] = layer_name

        # Analyze imports in each layer
        for layer_name, layer_config in layers.items():
            allowed = set(layer_config.get("can_import", []))
            allowed.add(layer_name)  # Can always import from same layer

            layer_paths = layer_config.get("paths", [f"src/{layer_name}"])

            for layer_path in layer_paths:
                base_path = self.project_path / layer_path.replace("/**/*", "")
                if not base_path.exists():
                    continue

                for file_path in base_path.rglob("*.ts"):
                    if "node_modules" in str(file_path):
                        continue

                    imports = self._extract_imports(file_path)

                    for imp, line_num in imports:
                        imported_layer = self._resolve_layer(imp, file_path, layers)
                        if imported_layer and imported_layer not in allowed:
                            violations.append(Violation(
                                rule="layer_dependency",
                                severity="error",
                                file=str(file_path.relative_to(self.project_path)),
                                line=line_num,
                                message=f"Layer '{layer_name}' cannot import from '{imported_layer}'",
                                suggestion=f"Move shared code to a common layer or inject the dependency"
                            ))

        return violations

    def check_boundaries(self) -> list[Violation]:
        """Check that module boundaries are respected."""
        violations = []
        boundaries = self.config.get("boundaries", {})

        if not boundaries:
            return violations

        for module_path, boundary_config in boundaries.items():
            public_exports = set(boundary_config.get("public", []))
            module_dir = self.project_path / module_path

            if not module_dir.exists():
                continue

            # Find all files that import from this module
            for ts_file in self.project_path.rglob("*.ts"):
                if str(module_path) in str(ts_file):
                    continue  # Skip files within the module
                if "node_modules" in str(ts_file):
                    continue

                imports = self._extract_imports(ts_file)

                for imp, line_num in imports:
                    if module_path in imp:
                        # Check if importing from public interface
                        imported_file = imp.split(module_path)[-1].lstrip("/")
                        is_public = any(
                            imported_file == pub or imported_file.startswith(pub.replace("*", ""))
                            for pub in public_exports
                        )

                        if not is_public and imported_file:
                            violations.append(Violation(
                                rule="module_boundary",
                                severity="error",
                                file=str(ts_file.relative_to(self.project_path)),
                                line=line_num,
                                message=f"Cannot import private module '{imp}' from '{module_path}'",
                                suggestion=f"Import from '{module_path}/index' or add to public exports"
                            ))

        return violations

    def check_naming(self) -> list[Violation]:
        """Check naming conventions."""
        violations = []
        naming_rules = self.config.get("naming", {})

        for pattern, rules in naming_rules.items():
            for file_path in self.project_path.glob(pattern):
                if "node_modules" in str(file_path):
                    continue

                file_name = file_path.stem

                # Check file naming
                if "file_pattern" in rules:
                    regex = rules["file_pattern"]
                    if not re.match(regex, file_name):
                        violations.append(Violation(
                            rule="naming_convention",
                            severity="warning",
                            file=str(file_path.relative_to(self.project_path)),
                            line=None,
                            message=f"File name '{file_name}' doesn't match pattern '{regex}'",
                            suggestion=rules.get("suggestion")
                        ))

                # Check export naming
                if "export_pattern" in rules:
                    content = file_path.read_text(errors="ignore")
                    exports = re.findall(r'export\s+(?:const|class|function|interface|type)\s+(\w+)', content)

                    regex = rules["export_pattern"]
                    for export_name in exports:
                        if not re.match(regex, export_name):
                            violations.append(Violation(
                                rule="naming_convention",
                                severity="warning",
                                file=str(file_path.relative_to(self.project_path)),
                                line=None,
                                message=f"Export '{export_name}' doesn't match pattern '{regex}'",
                                suggestion=rules.get("suggestion")
                            ))

        return violations

    def check_direction(self) -> list[Violation]:
        """Check dependency direction (e.g., UI should depend on Domain, not vice versa)."""
        violations = []
        direction_rules = self.config.get("dependency_direction", {})

        for rule in direction_rules:
            from_pattern = rule["from"]
            cannot_import = rule["cannot_import"]

            for file_path in self.project_path.glob(from_pattern):
                if "node_modules" in str(file_path):
                    continue

                imports = self._extract_imports(file_path)

                for imp, line_num in imports:
                    for forbidden in cannot_import:
                        if forbidden in imp:
                            violations.append(Violation(
                                rule="dependency_direction",
                                severity="error",
                                file=str(file_path.relative_to(self.project_path)),
                                line=line_num,
                                message=f"'{from_pattern}' cannot depend on '{forbidden}'",
                                suggestion=rule.get("suggestion", "Invert the dependency using interfaces")
                            ))

        return violations

    def _extract_imports(self, file_path: Path) -> list[tuple[str, int]]:
        """Extract imports with line numbers."""
        imports = []
        try:
            lines = file_path.read_text(errors="ignore").split("\n")
            for i, line in enumerate(lines, 1):
                match = re.search(r'(?:import|from)\s+[\'"]([^\'"]+)[\'"]', line)
                if match:
                    imports.append((match.group(1), i))
        except Exception:
            pass
        return imports

    def _resolve_layer(self, import_path: str, from_file: Path, layers: dict) -> str | None:
        """Resolve which layer an import belongs to."""
        for layer_name, layer_config in layers.items():
            patterns = layer_config.get("paths", [f"src/{layer_name}"])
            for pattern in patterns:
                # Simple check - could be more sophisticated
                layer_dir = pattern.replace("/**/*", "").replace("src/", "")
                if layer_dir in import_path:
                    return layer_name
        return None

    def generate_graph(self, output_path: Path):
        """Generate a DOT graph of dependencies."""
        graph = defaultdict(set)

        for ts_file in self.project_path.rglob("*.ts"):
            if "node_modules" in str(ts_file):
                continue

            rel_path = str(ts_file.relative_to(self.project_path))
            imports = self._extract_imports(ts_file)

            for imp, _ in imports:
                if imp.startswith("."):
                    # Resolve relative import
                    resolved = (ts_file.parent / imp).resolve()
                    try:
                        rel_resolved = str(resolved.relative_to(self.project_path))
                        graph[rel_path].add(rel_resolved)
                    except ValueError:
                        pass

        # Generate DOT format
        lines = ["digraph dependencies {", "  rankdir=LR;"]

        for from_file, to_files in graph.items():
            for to_file in to_files:
                lines.append(f'  "{from_file}" -> "{to_file}";')

        lines.append("}")

        output_path.write_text("\n".join(lines))
        print(f"Graph written to {output_path}")

    def run_all_checks(self) -> list[Violation]:
        """Run all architecture checks."""
        violations = []
        violations.extend(self.check_layers())
        violations.extend(self.check_boundaries())
        violations.extend(self.check_naming())
        violations.extend(self.check_direction())
        return violations


def format_report(violations: list[Violation], format: str = "text") -> str:
    """Format violations report."""
    if format == "json":
        return json.dumps([
            {
                "rule": v.rule,
                "severity": v.severity,
                "file": v.file,
                "line": v.line,
                "message": v.message,
                "suggestion": v.suggestion
            }
            for v in violations
        ], indent=2)

    if not violations:
        return "✅ No architecture violations found!"

    lines = [f"Found {len(violations)} architecture violation(s):", ""]

    errors = [v for v in violations if v.severity == "error"]
    warnings = [v for v in violations if v.severity == "warning"]

    if errors:
        lines.append(f"## Errors ({len(errors)})")
        lines.append("")
        for v in errors:
            loc = f"{v.file}:{v.line}" if v.line else v.file
            lines.append(f"❌ [{v.rule}] {loc}")
            lines.append(f"   {v.message}")
            if v.suggestion:
                lines.append(f"   💡 {v.suggestion}")
            lines.append("")

    if warnings:
        lines.append(f"## Warnings ({len(warnings)})")
        lines.append("")
        for v in warnings:
            loc = f"{v.file}:{v.line}" if v.line else v.file
            lines.append(f"⚠️  [{v.rule}] {loc}")
            lines.append(f"   {v.message}")
            if v.suggestion:
                lines.append(f"   💡 {v.suggestion}")
            lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Enforce architecture rules")
    parser.add_argument("--config", required=True, help="Architecture config JSON")
    parser.add_argument("--path", default=".", help="Project path")
    parser.add_argument("--check", choices=["layers", "boundaries", "naming", "direction", "all"],
                        default="all", help="Which check to run")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    parser.add_argument("--graph", action="store_true", help="Generate dependency graph")
    parser.add_argument("--output", help="Output file for graph")
    parser.add_argument("--fail-on-violation", action="store_true")
    args = parser.parse_args()

    config_path = Path(args.config)
    if not config_path.exists():
        print(f"Config file not found: {config_path}", file=sys.stderr)
        sys.exit(1)

    with open(config_path) as f:
        config = json.load(f)

    project_path = Path(args.path).resolve()
    enforcer = ArchitectureEnforcer(config, project_path)

    if args.graph:
        output = Path(args.output) if args.output else Path("dependencies.dot")
        enforcer.generate_graph(output)
        sys.exit(0)

    if args.check == "all":
        violations = enforcer.run_all_checks()
    elif args.check == "layers":
        violations = enforcer.check_layers()
    elif args.check == "boundaries":
        violations = enforcer.check_boundaries()
    elif args.check == "naming":
        violations = enforcer.check_naming()
    elif args.check == "direction":
        violations = enforcer.check_direction()
    else:
        violations = []

    print(format_report(violations, args.format))

    if args.fail_on_violation and any(v.severity == "error" for v in violations):
        sys.exit(1)


if __name__ == "__main__":
    main()
