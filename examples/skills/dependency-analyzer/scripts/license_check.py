#!/usr/bin/env python3
"""
License compliance checker for project dependencies.
Validates against a policy file defining allowed/blocked licenses.
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


# Common license SPDX identifiers and their risk levels
LICENSE_CATEGORIES = {
    "permissive": [
        "MIT", "Apache-2.0", "BSD-2-Clause", "BSD-3-Clause", "ISC",
        "Unlicense", "CC0-1.0", "0BSD", "WTFPL"
    ],
    "weak_copyleft": [
        "LGPL-2.1", "LGPL-3.0", "MPL-2.0", "EPL-1.0", "EPL-2.0"
    ],
    "strong_copyleft": [
        "GPL-2.0", "GPL-3.0", "AGPL-3.0"
    ],
    "problematic": [
        "SSPL-1.0", "BSL-1.1", "Elastic-2.0", "BUSL-1.1"
    ]
}

DEFAULT_POLICY = {
    "allowed": ["permissive", "weak_copyleft"],
    "blocked": ["AGPL-3.0", "SSPL-1.0", "GPL-3.0"],
    "review_required": ["strong_copyleft", "problematic"],
    "exceptions": {}  # package_name: reason
}


def load_policy(policy_path: Path | None) -> dict:
    """Load license policy from file or use defaults."""
    if policy_path and policy_path.exists():
        with open(policy_path) as f:
            return json.load(f)
    return DEFAULT_POLICY


def get_npm_licenses(path: Path) -> list[dict]:
    """Extract licenses from npm packages."""
    packages = []

    try:
        result = subprocess.run(
            ["npm", "ls", "--all", "--json"],
            cwd=path,
            capture_output=True,
            text=True,
            timeout=60
        )

        if result.stdout:
            data = json.loads(result.stdout)

            def extract_deps(deps: dict, depth: int = 0):
                for name, info in deps.items():
                    if isinstance(info, dict):
                        packages.append({
                            "name": name,
                            "version": info.get("version", "unknown"),
                            "license": info.get("license", "UNKNOWN"),
                            "depth": depth
                        })
                        if "dependencies" in info:
                            extract_deps(info["dependencies"], depth + 1)

            if "dependencies" in data:
                extract_deps(data["dependencies"])

    except (subprocess.TimeoutExpired, json.JSONDecodeError, FileNotFoundError):
        pass

    return packages


def categorize_license(license_id: str) -> str:
    """Categorize a license by its SPDX identifier."""
    license_upper = license_id.upper().strip()

    for category, licenses in LICENSE_CATEGORIES.items():
        if any(license_upper == lic.upper() for lic in licenses):
            return category

    return "unknown"


def check_compliance(packages: list[dict], policy: dict) -> dict[str, Any]:
    """Check packages against license policy."""
    results = {
        "compliant": [],
        "blocked": [],
        "review_required": [],
        "unknown": [],
        "exceptions_used": []
    }

    blocked_licenses = set(l.upper() for l in policy.get("blocked", []))
    exceptions = policy.get("exceptions", {})

    for pkg in packages:
        name = pkg["name"]
        license_id = pkg.get("license", "UNKNOWN")

        # Check if package has an exception
        if name in exceptions:
            results["exceptions_used"].append({
                **pkg,
                "reason": exceptions[name]
            })
            continue

        # Check if explicitly blocked
        if license_id.upper() in blocked_licenses:
            results["blocked"].append(pkg)
            continue

        # Categorize and check
        category = categorize_license(license_id)

        if category == "unknown":
            results["unknown"].append(pkg)
        elif category in policy.get("review_required", []):
            results["review_required"].append(pkg)
        elif category in policy.get("allowed", []) or category == "permissive":
            results["compliant"].append(pkg)
        else:
            results["review_required"].append(pkg)

    return results


def generate_report(results: dict, format: str = "text") -> str:
    """Generate compliance report."""

    if format == "json":
        return json.dumps(results, indent=2)

    lines = []

    # Summary
    total = sum(len(v) for v in results.values())
    blocked_count = len(results["blocked"])
    review_count = len(results["review_required"])
    unknown_count = len(results["unknown"])

    status = "✅ COMPLIANT" if blocked_count == 0 else "❌ NON-COMPLIANT"

    lines.append(f"License Compliance: {status}")
    lines.append(f"Total packages: {total}")
    lines.append("")

    if results["blocked"]:
        lines.append("## ❌ BLOCKED LICENSES (Must Replace)")
        lines.append("")
        for pkg in results["blocked"]:
            lines.append(f"  - {pkg['name']}@{pkg['version']}: {pkg['license']}")
        lines.append("")

    if results["review_required"]:
        lines.append("## ⚠️ REVIEW REQUIRED")
        lines.append("")
        for pkg in results["review_required"][:20]:
            lines.append(f"  - {pkg['name']}@{pkg['version']}: {pkg['license']}")
        if len(results["review_required"]) > 20:
            lines.append(f"  ... and {len(results['review_required']) - 20} more")
        lines.append("")

    if results["unknown"]:
        lines.append("## ❓ UNKNOWN LICENSES")
        lines.append("")
        for pkg in results["unknown"][:10]:
            lines.append(f"  - {pkg['name']}@{pkg['version']}: {pkg['license']}")
        if len(results["unknown"]) > 10:
            lines.append(f"  ... and {len(results['unknown']) - 10} more")
        lines.append("")

    if results["exceptions_used"]:
        lines.append("## 📋 EXCEPTIONS APPLIED")
        lines.append("")
        for pkg in results["exceptions_used"]:
            lines.append(f"  - {pkg['name']}: {pkg['reason']}")
        lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Check license compliance")
    parser.add_argument("--path", default=".", help="Project path")
    parser.add_argument("--policy", help="Policy JSON file path")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    parser.add_argument("--fail-on-blocked", action="store_true",
                        help="Exit with error if blocked licenses found")
    args = parser.parse_args()

    path = Path(args.path).resolve()
    policy_path = Path(args.policy) if args.policy else None

    policy = load_policy(policy_path)
    packages = get_npm_licenses(path)

    if not packages:
        print("No packages found or unable to analyze")
        sys.exit(0)

    results = check_compliance(packages, policy)
    print(generate_report(results, args.format))

    if args.fail_on_blocked and results["blocked"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
