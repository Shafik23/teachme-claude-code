#!/usr/bin/env python3
"""
Comprehensive dependency analyzer for Node.js and Python projects.
Analyzes security, licenses, staleness, and provides actionable recommendations.
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any
import re


def detect_project_type(path: Path) -> list[str]:
    """Detect project types based on manifest files."""
    types = []
    if (path / "package.json").exists():
        types.append("nodejs")
    if (path / "requirements.txt").exists() or (path / "pyproject.toml").exists():
        types.append("python")
    if (path / "go.mod").exists():
        types.append("go")
    if (path / "Cargo.toml").exists():
        types.append("rust")
    return types or ["unknown"]


def analyze_nodejs(path: Path) -> dict[str, Any]:
    """Analyze Node.js dependencies."""
    results = {
        "type": "nodejs",
        "dependencies": {"production": 0, "development": 0},
        "vulnerabilities": {"critical": 0, "high": 0, "moderate": 0, "low": 0},
        "outdated": [],
        "large_packages": [],
        "issues": [],
        "recommendations": []
    }

    pkg_path = path / "package.json"
    if not pkg_path.exists():
        return results

    with open(pkg_path) as f:
        pkg = json.load(f)

    deps = pkg.get("dependencies", {})
    dev_deps = pkg.get("devDependencies", {})
    results["dependencies"]["production"] = len(deps)
    results["dependencies"]["development"] = len(dev_deps)

    # Check for problematic patterns
    all_deps = {**deps, **dev_deps}
    for name, version in all_deps.items():
        # Detect loose versioning
        if version.startswith("*") or version == "latest":
            results["issues"].append({
                "severity": "high",
                "package": name,
                "issue": f"Unpinned version: {version}",
                "recommendation": f"Pin to specific version or use ^ for minor updates"
            })

        # Detect git dependencies
        if "git" in version or "github" in version:
            results["issues"].append({
                "severity": "medium",
                "package": name,
                "issue": "Git dependency - not from npm registry",
                "recommendation": "Publish to npm or use specific commit hash"
            })

    # Run npm audit
    try:
        audit_result = subprocess.run(
            ["npm", "audit", "--json"],
            cwd=path,
            capture_output=True,
            text=True,
            timeout=60
        )
        if audit_result.stdout:
            audit_data = json.loads(audit_result.stdout)
            vulns = audit_data.get("metadata", {}).get("vulnerabilities", {})
            results["vulnerabilities"] = {
                "critical": vulns.get("critical", 0),
                "high": vulns.get("high", 0),
                "moderate": vulns.get("moderate", 0),
                "low": vulns.get("low", 0)
            }
    except (subprocess.TimeoutExpired, json.JSONDecodeError, FileNotFoundError):
        results["issues"].append({
            "severity": "info",
            "package": "npm",
            "issue": "Could not run npm audit",
            "recommendation": "Run `npm audit` manually"
        })

    # Check for outdated packages
    try:
        outdated_result = subprocess.run(
            ["npm", "outdated", "--json"],
            cwd=path,
            capture_output=True,
            text=True,
            timeout=60
        )
        if outdated_result.stdout:
            outdated = json.loads(outdated_result.stdout)
            for pkg_name, info in outdated.items():
                current = info.get("current", "?")
                latest = info.get("latest", "?")
                # Check if major version differs
                current_major = current.split(".")[0] if current != "?" else "0"
                latest_major = latest.split(".")[0] if latest != "?" else "0"

                results["outdated"].append({
                    "package": pkg_name,
                    "current": current,
                    "latest": latest,
                    "major_update": current_major != latest_major
                })
    except (subprocess.TimeoutExpired, json.JSONDecodeError, FileNotFoundError):
        pass

    # Generate recommendations
    total_vulns = sum(results["vulnerabilities"].values())
    if total_vulns > 0:
        results["recommendations"].append(
            f"Run `npm audit fix` to address {total_vulns} vulnerabilities"
        )

    major_updates = [o for o in results["outdated"] if o["major_update"]]
    if major_updates:
        results["recommendations"].append(
            f"{len(major_updates)} packages have major updates available - review changelogs before upgrading"
        )

    return results


def analyze_python(path: Path) -> dict[str, Any]:
    """Analyze Python dependencies."""
    results = {
        "type": "python",
        "dependencies": {"direct": 0, "transitive": 0},
        "vulnerabilities": {"critical": 0, "high": 0, "moderate": 0, "low": 0},
        "outdated": [],
        "issues": [],
        "recommendations": []
    }

    # Parse requirements.txt
    req_path = path / "requirements.txt"
    if req_path.exists():
        with open(req_path) as f:
            lines = [l.strip() for l in f if l.strip() and not l.startswith("#")]

        results["dependencies"]["direct"] = len(lines)

        for line in lines:
            # Check for unpinned dependencies
            if ">=" in line or line.isalpha() or (not "==" in line and not line.startswith("-")):
                pkg_name = re.split(r'[<>=!]', line)[0].strip()
                if pkg_name and not pkg_name.startswith("-"):
                    results["issues"].append({
                        "severity": "medium",
                        "package": pkg_name,
                        "issue": f"Unpinned or loosely pinned: {line}",
                        "recommendation": "Pin to exact version with =="
                    })

    # Try pip-audit for vulnerabilities
    try:
        audit_result = subprocess.run(
            ["pip-audit", "--format=json", "-r", str(req_path)],
            cwd=path,
            capture_output=True,
            text=True,
            timeout=120
        )
        if audit_result.stdout:
            vulns = json.loads(audit_result.stdout)
            for vuln in vulns:
                severity = vuln.get("vulns", [{}])[0].get("severity", "unknown").lower()
                if severity in results["vulnerabilities"]:
                    results["vulnerabilities"][severity] += 1
    except (subprocess.TimeoutExpired, json.JSONDecodeError, FileNotFoundError):
        results["recommendations"].append(
            "Install pip-audit (`pip install pip-audit`) for vulnerability scanning"
        )

    return results


def generate_report(results: list[dict], format: str = "text") -> str:
    """Generate analysis report."""
    if format == "json":
        return json.dumps(results, indent=2)

    if format == "markdown":
        lines = ["# Dependency Analysis Report", ""]
        lines.append(f"Generated: {datetime.now().isoformat()}")
        lines.append("")

        for project in results:
            lines.append(f"## {project['type'].title()} Dependencies")
            lines.append("")

            # Summary
            deps = project["dependencies"]
            total_deps = sum(deps.values())
            lines.append(f"**Total Dependencies:** {total_deps}")
            lines.append("")

            # Vulnerabilities
            vulns = project["vulnerabilities"]
            total_vulns = sum(vulns.values())
            if total_vulns > 0:
                lines.append("### Security Vulnerabilities")
                lines.append("")
                lines.append("| Severity | Count |")
                lines.append("|----------|-------|")
                for sev, count in vulns.items():
                    if count > 0:
                        emoji = {"critical": "🔴", "high": "🟠", "moderate": "🟡", "low": "🔵"}.get(sev, "⚪")
                        lines.append(f"| {emoji} {sev.title()} | {count} |")
                lines.append("")

            # Issues
            if project["issues"]:
                lines.append("### Issues Found")
                lines.append("")
                for issue in project["issues"]:
                    emoji = {"high": "🔴", "medium": "🟠", "low": "🟡", "info": "🔵"}.get(issue["severity"], "⚪")
                    lines.append(f"- {emoji} **{issue['package']}**: {issue['issue']}")
                    lines.append(f"  - *Recommendation:* {issue['recommendation']}")
                lines.append("")

            # Outdated
            if project.get("outdated"):
                lines.append("### Outdated Packages")
                lines.append("")
                lines.append("| Package | Current | Latest | Major Update |")
                lines.append("|---------|---------|--------|--------------|")
                for pkg in project["outdated"][:10]:  # Top 10
                    major = "⚠️ Yes" if pkg["major_update"] else "No"
                    lines.append(f"| {pkg['package']} | {pkg['current']} | {pkg['latest']} | {major} |")
                if len(project["outdated"]) > 10:
                    lines.append(f"| ... and {len(project['outdated']) - 10} more | | | |")
                lines.append("")

            # Recommendations
            if project["recommendations"]:
                lines.append("### Recommendations")
                lines.append("")
                for rec in project["recommendations"]:
                    lines.append(f"- {rec}")
                lines.append("")

        return "\n".join(lines)

    # Plain text format
    lines = ["=" * 60, "DEPENDENCY ANALYSIS REPORT", "=" * 60, ""]

    for project in results:
        lines.append(f"Project Type: {project['type']}")
        lines.append(f"Dependencies: {sum(project['dependencies'].values())}")

        vulns = project["vulnerabilities"]
        total_vulns = sum(vulns.values())
        lines.append(f"Vulnerabilities: {total_vulns} ({vulns['critical']} critical, {vulns['high']} high)")

        if project["issues"]:
            lines.append(f"Issues: {len(project['issues'])}")

        lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Analyze project dependencies")
    parser.add_argument("--path", default=".", help="Project path")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    args = parser.parse_args()

    path = Path(args.path).resolve()
    project_types = detect_project_type(path)

    results = []
    for ptype in project_types:
        if ptype == "nodejs":
            results.append(analyze_nodejs(path))
        elif ptype == "python":
            results.append(analyze_python(path))

    print(generate_report(results, args.format))


if __name__ == "__main__":
    main()
