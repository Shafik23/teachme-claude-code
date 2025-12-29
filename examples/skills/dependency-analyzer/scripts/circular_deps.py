#!/usr/bin/env python3
"""
Detect circular dependencies in TypeScript/JavaScript/Python codebases.
Uses static analysis of import statements.
"""

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Generator


# Import patterns for different languages
IMPORT_PATTERNS = {
    "ts": [
        r'import\s+.*?\s+from\s+[\'"]([^\'"]+)[\'"]',
        r'import\s*\([\'"]([^\'"]+)[\'"]\)',
        r'require\s*\([\'"]([^\'"]+)[\'"]\)',
        r'export\s+.*?\s+from\s+[\'"]([^\'"]+)[\'"]',
    ],
    "js": [
        r'import\s+.*?\s+from\s+[\'"]([^\'"]+)[\'"]',
        r'import\s*\([\'"]([^\'"]+)[\'"]\)',
        r'require\s*\([\'"]([^\'"]+)[\'"]\)',
        r'export\s+.*?\s+from\s+[\'"]([^\'"]+)[\'"]',
    ],
    "py": [
        r'^from\s+([\w.]+)\s+import',
        r'^import\s+([\w.]+)',
    ]
}


def find_files(path: Path, extensions: list[str]) -> Generator[Path, None, None]:
    """Find all files with given extensions."""
    for ext in extensions:
        yield from path.rglob(f"*.{ext}")


def extract_imports(file_path: Path, lang: str) -> list[str]:
    """Extract import paths from a file."""
    imports = []
    patterns = IMPORT_PATTERNS.get(lang, [])

    try:
        content = file_path.read_text(encoding="utf-8", errors="ignore")

        for pattern in patterns:
            for match in re.finditer(pattern, content, re.MULTILINE):
                import_path = match.group(1)
                imports.append(import_path)

    except Exception:
        pass

    return imports


def resolve_import(import_path: str, from_file: Path, project_root: Path) -> Path | None:
    """Resolve an import path to an actual file."""
    # Skip external modules
    if not import_path.startswith(".") and not import_path.startswith("@/"):
        return None

    from_dir = from_file.parent

    # Handle relative imports
    if import_path.startswith("."):
        resolved = (from_dir / import_path).resolve()
    elif import_path.startswith("@/"):
        # Common alias for src/
        resolved = (project_root / "src" / import_path[2:]).resolve()
    else:
        return None

    # Try different extensions
    for ext in ["", ".ts", ".tsx", ".js", ".jsx", "/index.ts", "/index.tsx", "/index.js"]:
        candidate = Path(str(resolved) + ext)
        if candidate.exists() and candidate.is_file():
            return candidate

    return None


def build_dependency_graph(path: Path, extensions: list[str]) -> dict[Path, set[Path]]:
    """Build a graph of file dependencies."""
    graph = defaultdict(set)

    lang_map = {"ts": "ts", "tsx": "ts", "js": "js", "jsx": "js", "py": "py"}

    for file_path in find_files(path, extensions):
        # Skip node_modules, __pycache__, etc.
        if any(p in file_path.parts for p in ["node_modules", "__pycache__", ".git", "dist", "build"]):
            continue

        ext = file_path.suffix[1:]  # Remove the dot
        lang = lang_map.get(ext, "js")

        imports = extract_imports(file_path, lang)

        for imp in imports:
            resolved = resolve_import(imp, file_path, path)
            if resolved:
                graph[file_path].add(resolved)

    return graph


def find_cycles(graph: dict[Path, set[Path]]) -> list[list[Path]]:
    """Find all cycles in the dependency graph using DFS."""
    cycles = []
    visited = set()
    rec_stack = set()
    path = []

    def dfs(node: Path):
        visited.add(node)
        rec_stack.add(node)
        path.append(node)

        for neighbor in graph.get(node, set()):
            if neighbor not in visited:
                dfs(neighbor)
            elif neighbor in rec_stack:
                # Found a cycle
                cycle_start = path.index(neighbor)
                cycle = path[cycle_start:] + [neighbor]
                cycles.append(cycle)

        path.pop()
        rec_stack.remove(node)

    for node in graph:
        if node not in visited:
            dfs(node)

    return cycles


def format_cycle(cycle: list[Path], project_root: Path) -> str:
    """Format a cycle for display."""
    rel_paths = [str(p.relative_to(project_root)) for p in cycle]
    return " → ".join(rel_paths)


def main():
    parser = argparse.ArgumentParser(description="Detect circular dependencies")
    parser.add_argument("--path", default=".", help="Project path")
    parser.add_argument("--ext", default="ts,tsx,js,jsx",
                        help="File extensions to analyze (comma-separated)")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    args = parser.parse_args()

    path = Path(args.path).resolve()
    extensions = [e.strip() for e in args.ext.split(",")]

    print(f"Scanning for circular dependencies in {path}...", file=sys.stderr)

    graph = build_dependency_graph(path, extensions)
    cycles = find_cycles(graph)

    # Deduplicate cycles (same cycle can be found starting from different nodes)
    unique_cycles = []
    seen = set()
    for cycle in cycles:
        # Normalize cycle by starting from the lexicographically smallest element
        min_idx = cycle.index(min(cycle[:-1], key=str))
        normalized = tuple(cycle[min_idx:-1]) + tuple(cycle[:min_idx]) + (cycle[min_idx],)
        if normalized not in seen:
            seen.add(normalized)
            unique_cycles.append(cycle)

    if args.format == "json":
        import json
        result = {
            "total_files": len(graph),
            "cycles_found": len(unique_cycles),
            "cycles": [
                [str(p.relative_to(path)) for p in cycle]
                for cycle in unique_cycles
            ]
        }
        print(json.dumps(result, indent=2))
    else:
        print(f"\nAnalyzed {len(graph)} files")
        print(f"Found {len(unique_cycles)} circular dependency chain(s)\n")

        if unique_cycles:
            print("Circular Dependencies:")
            print("=" * 60)
            for i, cycle in enumerate(unique_cycles, 1):
                print(f"\n{i}. {format_cycle(cycle, path)}")

            print("\n" + "=" * 60)
            print("Recommendations:")
            print("- Extract shared code into a separate module")
            print("- Use dependency injection to break cycles")
            print("- Consider lazy imports for complex cycles")
        else:
            print("✅ No circular dependencies found!")

    sys.exit(1 if unique_cycles else 0)


if __name__ == "__main__":
    main()
