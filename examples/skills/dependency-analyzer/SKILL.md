---
name: dependency-analyzer
description: Deep analysis of project dependencies - security vulnerabilities, license compliance, bundle size impact, staleness, and circular dependencies. Use when auditing dependencies, before major upgrades, or when asked about dependency health.
allowed-tools: Read, Bash(node:*), Bash(python3:*), Bash(npm:*), Bash(pip:*), Glob, Grep
---

# Dependency Analyzer

Comprehensive dependency analysis for Node.js and Python projects.

## Quick Analysis

Run the analysis script for an instant health report:

```bash
python3 ${SKILL_DIR}/scripts/analyze_deps.py --path .
```

## Analysis Dimensions

### 1. Security Vulnerabilities

Check for known CVEs:

```bash
# Node.js
npm audit --json | python3 ${SKILL_DIR}/scripts/parse_audit.py

# Python
pip-audit --format=json 2>/dev/null || safety check --json
```

### 2. License Compliance

Run license check:

```bash
python3 ${SKILL_DIR}/scripts/license_check.py --path . --policy ${SKILL_DIR}/rules/license-policy.json
```

Blocked licenses (see @rules/license-policy.json):
- GPL-3.0 (viral, requires source disclosure)
- AGPL-3.0 (network copyleft)
- SSPL (MongoDB's restrictive license)

### 3. Bundle Size Impact

For frontend projects:

```bash
node ${SKILL_DIR}/scripts/bundle-impact.js
```

### 4. Dependency Freshness

Check for outdated packages:

```bash
python3 ${SKILL_DIR}/scripts/staleness_report.py --path .
```

### 5. Circular Dependencies

Detect import cycles:

```bash
python3 ${SKILL_DIR}/scripts/circular_deps.py --path . --ext ts,js
```

## Report Format

Generate full report:

```bash
python3 ${SKILL_DIR}/scripts/analyze_deps.py --path . --format markdown > dependency-report.md
```

## Configuration

See @rules/config.json for thresholds:
- Max vulnerability severity to allow
- Staleness thresholds (days since last update)
- Bundle size budgets
- Allowed/blocked licenses
