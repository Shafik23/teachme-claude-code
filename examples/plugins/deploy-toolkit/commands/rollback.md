---
description: Rollback deployment to previous version
argument-hint: <environment> [version]
allowed-tools: Bash(git:*), Bash(npm:*), Bash(docker:*), Read
---

# Rollback Command

Rollback the **$1** environment to a previous version.

If a specific version is provided ($2), rollback to that version.
Otherwise, rollback to the immediately previous deployment.

## Safety Checks

Before rolling back:

1. **Confirm Environment**
   - Verify target environment is correct
   - For production, require explicit confirmation

2. **Verify Target Version**
   - Check that the target version exists
   - Confirm it was previously deployed successfully
   - Review what changes will be reverted

## Rollback Process

### Step 1: Identify Target Version

```bash
# List recent deployments
npm run deployments:list --env=$1

# If no version specified, use previous
# If version specified, verify it exists
```

### Step 2: Execute Rollback

```bash
# Trigger rollback
npm run rollback:$1 --version=${2:-previous}
```

### Step 3: Verify Rollback

1. Check application health endpoint
2. Verify the correct version is running
3. Monitor error rates
4. Check key functionality

## Output

Provide:
- Previous version (what was running)
- Rolled back to version
- Rollback duration
- Health check status
- Any warnings or issues detected

## Emergency Rollback

For critical issues, use fast rollback:
```bash
npm run rollback:emergency --env=$1
```

This skips some verification steps for speed.
