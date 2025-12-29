---
name: architecture-enforcer
description: Enforce architectural boundaries and coding standards via static analysis. Validates layer dependencies, module boundaries, naming conventions, and structural rules. Use when checking architecture compliance, during code review, or when asked about architecture violations.
allowed-tools: Read, Bash(python3:*), Bash(node:*), Glob, Grep
---

# Architecture Enforcer

Enforce architectural rules through static analysis. Define rules once, validate continuously.

## Quick Check

Run all architecture validations:

```bash
python3 ${SKILL_DIR}/scripts/enforce.py --config ${SKILL_DIR}/rules/architecture.json --path .
```

## Rule Types

### 1. Layer Dependencies

Ensure proper layering (e.g., controllers → services → repositories):

```bash
python3 ${SKILL_DIR}/scripts/enforce.py --check layers --path .
```

See @rules/architecture.json for layer definitions.

### 2. Module Boundaries

Prevent unauthorized cross-module imports:

```bash
python3 ${SKILL_DIR}/scripts/enforce.py --check boundaries --path .
```

### 3. Naming Conventions

Validate file and export naming:

```bash
python3 ${SKILL_DIR}/scripts/enforce.py --check naming --path .
```

### 4. Dependency Direction

Ensure dependencies flow in the correct direction (e.g., UI → Domain, not Domain → UI):

```bash
python3 ${SKILL_DIR}/scripts/enforce.py --check direction --path .
```

## Configuration

Edit @rules/architecture.json to define your architecture:

```json
{
  "layers": {
    "controllers": {"can_import": ["services", "models", "utils"]},
    "services": {"can_import": ["repositories", "models", "utils"]},
    "repositories": {"can_import": ["models", "utils"]}
  },
  "boundaries": {
    "src/auth": {"public": ["index.ts"], "private": ["**/*"]},
    "src/payments": {"public": ["index.ts"], "private": ["**/*"]}
  }
}
```

## CI Integration

Add to your CI pipeline:

```yaml
- name: Architecture Check
  run: |
    python3 scripts/enforce.py --config .architecture.json --path . --fail-on-violation
```

## Generating Dependency Graph

Visualize the actual dependency structure:

```bash
python3 ${SKILL_DIR}/scripts/enforce.py --graph --path . --output deps.dot
dot -Tpng deps.dot -o deps.png
```
