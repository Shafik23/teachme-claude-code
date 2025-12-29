---
name: migration-validator
description: Validate database migrations for safety, performance, and reversibility. Detects dangerous operations, missing indexes, locking issues, and data loss risks. Use when reviewing migrations, before deploying schema changes, or when asked to check migration safety.
allowed-tools: Read, Bash(python3:*), Glob, Grep
---

# Migration Validator

Analyze database migrations for production safety.

## Quick Validation

```bash
python3 ${SKILL_DIR}/scripts/validate_migration.py --path migrations/
```

## Checks Performed

### 1. Dangerous Operations

Detects operations that can cause outages:

- `DROP TABLE` / `DROP COLUMN` (data loss)
- `TRUNCATE` (data loss)
- `ALTER TABLE ... RENAME` (breaks queries)
- `NOT NULL` without default (fails on existing rows)

### 2. Locking Analysis

Identifies operations that acquire heavy locks:

- `ALTER TABLE` on large tables → `ACCESS EXCLUSIVE` lock
- `CREATE INDEX` without `CONCURRENTLY` → blocks writes
- `ADD CONSTRAINT` → table lock

### 3. Performance Risks

- Missing indexes on foreign keys
- Full table scans in migrations
- Large data transformations without batching

### 4. Reversibility

- Checks for corresponding `down` migration
- Validates `down` actually reverses `up`
- Flags irreversible operations

## Safety Levels

```bash
# Strict mode - for production
python3 ${SKILL_DIR}/scripts/validate_migration.py --path migrations/ --level strict

# Permissive mode - for development
python3 ${SKILL_DIR}/scripts/validate_migration.py --path migrations/ --level permissive
```

## CI Integration

```yaml
- name: Validate Migrations
  run: |
    python3 scripts/validate_migration.py \
      --path migrations/ \
      --level strict \
      --fail-on-warning
```

## Supported Formats

- Raw SQL files
- Knex.js migrations
- Prisma migrations
- TypeORM migrations
- Django migrations
- Alembic (Python)

## Configuration

See @rules/migration-rules.json for:
- Table size thresholds for warnings
- Allowed/blocked operations per environment
- Custom dangerous patterns
