---
description: Deploy application to specified environment (dev, staging, prod)
argument-hint: <environment>
allowed-tools: Bash(git:*), Bash(npm:*), Bash(docker:*), Read, Glob
---

# Deploy Command

Deploy the application to the **$ARGUMENTS** environment.

## Pre-Deploy Checklist

Before deploying, verify:

1. **Git Status**
   - Working directory is clean
   - On the correct branch (main for prod, develop for staging)
   - All changes are committed and pushed

2. **Tests**
   - All tests pass: `npm test`
   - No skipped tests in CI-critical paths

3. **Build**
   - Production build succeeds: `npm run build`
   - No TypeScript errors
   - Bundle size within limits

4. **Environment**
   - Required env vars are set for target environment
   - Secrets are configured in deployment platform
   - Database migrations are ready (if any)

## Deployment Steps

### For Development (`dev`)
```bash
npm run build
npm run deploy:dev
```

### For Staging (`staging`)
```bash
npm run build
npm run test:e2e  # Run E2E tests
npm run deploy:staging
```

### For Production (`prod`)
```bash
# Require explicit confirmation
npm run build
npm run test
npm run deploy:prod
```

## Post-Deploy Verification

After deployment:
1. Check application health endpoint
2. Verify key functionality works
3. Monitor error rates for 5 minutes
4. Check logs for anomalies

## Rollback

If issues are detected:
```bash
npm run rollback:$ARGUMENTS
```

## Output

Provide:
- Deployment status (success/failure)
- Deployed version/commit hash
- Health check results
- Link to deployment logs
