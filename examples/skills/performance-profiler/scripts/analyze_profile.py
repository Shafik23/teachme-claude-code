#!/usr/bin/env python3
"""
Profile analyzer for Python cProfile output.
Identifies performance bottlenecks and provides recommendations.
"""

import argparse
import pstats
import sys
from io import StringIO
from pathlib import Path
from dataclasses import dataclass
from typing import Any


@dataclass
class FunctionStats:
    name: str
    filename: str
    line_number: int
    total_calls: int
    total_time: float
    cumulative_time: float
    time_per_call: float
    callers: list[str]
    callees: list[str]


def load_profile(profile_path: Path) -> pstats.Stats:
    """Load a profile file."""
    return pstats.Stats(str(profile_path))


def get_top_functions(stats: pstats.Stats, n: int = 20, sort_by: str = "cumulative") -> list[dict]:
    """Get top N functions by specified metric."""
    stream = StringIO()
    stats.stream = stream
    stats.sort_stats(sort_by)
    stats.print_stats(n)

    # Parse the output
    functions = []
    output = stream.getvalue()

    for line in output.split("\n"):
        # Match lines like: ncalls tottime percall cumtime percall filename:lineno(function)
        parts = line.split()
        if len(parts) >= 6 and ":" in parts[-1]:
            try:
                ncalls = parts[0].split("/")[0]  # Handle recursive calls like "3/1"
                tottime = float(parts[1])
                cumtime = float(parts[3])
                location = parts[-1]

                functions.append({
                    "calls": int(ncalls) if ncalls.isdigit() else ncalls,
                    "total_time": tottime,
                    "cumulative_time": cumtime,
                    "location": location
                })
            except (ValueError, IndexError):
                continue

    return functions


def find_bottlenecks(stats: pstats.Stats) -> list[dict]:
    """Identify performance bottlenecks."""
    bottlenecks = []

    # Get functions sorted by cumulative time
    stream = StringIO()
    stats.stream = stream
    stats.sort_stats("cumulative")
    stats.print_stats(50)

    output = stream.getvalue()
    lines = output.split("\n")

    total_time = 0.0
    function_times = []

    for line in lines:
        parts = line.split()
        if len(parts) >= 6 and ":" in parts[-1]:
            try:
                cumtime = float(parts[3])
                location = parts[-1]

                if cumtime > 0:
                    function_times.append((cumtime, location))
                    total_time = max(total_time, cumtime)
            except (ValueError, IndexError):
                continue

    # Identify bottlenecks (functions taking >10% of total time)
    for cumtime, location in function_times:
        percentage = (cumtime / total_time * 100) if total_time > 0 else 0
        if percentage > 10:
            bottlenecks.append({
                "location": location,
                "time": cumtime,
                "percentage": percentage,
                "severity": "high" if percentage > 30 else "medium"
            })

    return bottlenecks


def analyze_call_patterns(stats: pstats.Stats) -> list[dict]:
    """Analyze call patterns for potential issues."""
    issues = []

    stream = StringIO()
    stats.stream = stream
    stats.sort_stats("calls")
    stats.print_stats(100)

    output = stream.getvalue()

    for line in output.split("\n"):
        parts = line.split()
        if len(parts) >= 6 and ":" in parts[-1]:
            try:
                ncalls_str = parts[0]
                location = parts[-1]

                # Check for recursive calls (format: "total/primitive")
                if "/" in ncalls_str:
                    total, primitive = ncalls_str.split("/")
                    if int(total) > int(primitive) * 10:
                        issues.append({
                            "type": "deep_recursion",
                            "location": location,
                            "calls": ncalls_str,
                            "message": "Deep recursion detected - consider iterative approach"
                        })

                # Check for functions called many times
                ncalls = int(ncalls_str.split("/")[0])
                if ncalls > 100000:
                    issues.append({
                        "type": "high_call_count",
                        "location": location,
                        "calls": ncalls,
                        "message": f"Called {ncalls:,} times - consider caching or batching"
                    })

            except (ValueError, IndexError):
                continue

    return issues


def generate_recommendations(bottlenecks: list[dict], issues: list[dict]) -> list[str]:
    """Generate optimization recommendations."""
    recommendations = []

    for bn in bottlenecks:
        loc = bn["location"]
        pct = bn["percentage"]

        if "database" in loc.lower() or "query" in loc.lower() or "sql" in loc.lower():
            recommendations.append(
                f"Database bottleneck at {loc} ({pct:.1f}%): "
                "Consider query optimization, indexing, or caching"
            )
        elif "json" in loc.lower():
            recommendations.append(
                f"JSON processing at {loc} ({pct:.1f}%): "
                "Consider streaming JSON parsing or using orjson/ujson"
            )
        elif "http" in loc.lower() or "request" in loc.lower():
            recommendations.append(
                f"HTTP bottleneck at {loc} ({pct:.1f}%): "
                "Consider connection pooling, async requests, or caching"
            )
        elif "file" in loc.lower() or "read" in loc.lower() or "write" in loc.lower():
            recommendations.append(
                f"I/O bottleneck at {loc} ({pct:.1f}%): "
                "Consider async I/O, buffering, or memory mapping"
            )
        else:
            recommendations.append(
                f"CPU bottleneck at {loc} ({pct:.1f}%): "
                "Profile this function for optimization opportunities"
            )

    for issue in issues:
        if issue["type"] == "deep_recursion":
            recommendations.append(
                f"Deep recursion at {issue['location']}: "
                "Convert to iterative with explicit stack to avoid stack overflow"
            )
        elif issue["type"] == "high_call_count":
            recommendations.append(
                f"High call count at {issue['location']}: "
                "Consider memoization, caching, or loop optimization"
            )

    return recommendations


def format_report(
    top_functions: list[dict],
    bottlenecks: list[dict],
    issues: list[dict],
    recommendations: list[str],
    format: str = "text"
) -> str:
    """Format the analysis report."""

    if format == "json":
        import json
        return json.dumps({
            "top_functions": top_functions,
            "bottlenecks": bottlenecks,
            "issues": issues,
            "recommendations": recommendations
        }, indent=2)

    lines = ["=" * 60, "PERFORMANCE ANALYSIS REPORT", "=" * 60, ""]

    # Top functions
    lines.append("## Top Functions by Cumulative Time")
    lines.append("")
    lines.append(f"{'Location':<50} {'Time (s)':<10} {'Calls':<10}")
    lines.append("-" * 70)

    for func in top_functions[:15]:
        loc = func["location"][:48]
        lines.append(f"{loc:<50} {func['cumulative_time']:<10.4f} {func['calls']}")

    lines.append("")

    # Bottlenecks
    if bottlenecks:
        lines.append("## 🔥 Performance Bottlenecks")
        lines.append("")
        for bn in bottlenecks:
            severity_icon = "🔴" if bn["severity"] == "high" else "🟡"
            lines.append(f"{severity_icon} {bn['location']}")
            lines.append(f"   Time: {bn['time']:.4f}s ({bn['percentage']:.1f}% of total)")
        lines.append("")

    # Issues
    if issues:
        lines.append("## ⚠️  Potential Issues")
        lines.append("")
        for issue in issues:
            lines.append(f"- {issue['type']}: {issue['location']}")
            lines.append(f"  {issue['message']}")
        lines.append("")

    # Recommendations
    if recommendations:
        lines.append("## 💡 Recommendations")
        lines.append("")
        for i, rec in enumerate(recommendations, 1):
            lines.append(f"{i}. {rec}")
        lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Analyze Python profile data")
    parser.add_argument("--input", required=True, help="Profile file (.prof)")
    parser.add_argument("--top", type=int, default=20, help="Number of top functions")
    parser.add_argument("--sort", choices=["cumulative", "time", "calls"], default="cumulative")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    args = parser.parse_args()

    profile_path = Path(args.input)
    if not profile_path.exists():
        print(f"Profile file not found: {profile_path}", file=sys.stderr)
        sys.exit(1)

    try:
        stats = load_profile(profile_path)
    except Exception as e:
        print(f"Error loading profile: {e}", file=sys.stderr)
        sys.exit(1)

    top_functions = get_top_functions(stats, args.top, args.sort)
    bottlenecks = find_bottlenecks(stats)
    issues = analyze_call_patterns(stats)
    recommendations = generate_recommendations(bottlenecks, issues)

    print(format_report(top_functions, bottlenecks, issues, recommendations, args.format))


if __name__ == "__main__":
    main()
