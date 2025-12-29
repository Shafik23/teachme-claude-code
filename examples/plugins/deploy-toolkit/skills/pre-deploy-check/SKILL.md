---
name: pre-deploy-check
description: Comprehensive pre-deployment verification. Automatically used before deployments to ensure code quality, test coverage, and configuration are ready. Use when checking deployment readiness or when the user asks "is this ready to deploy?" or "can we ship this?"
allowed-tools: Read, Glob, Grep, Bash(npm:*), Bash(git:*)
---

# Pre-Deploy Check Skill

Perform comprehensive verification before any deployment.

## Check Categories

### 1. Code Quality

Run and verify:

```bash
# Linting
npm run lint

# Type checking (TypeScript)
npm run typecheck

# Format check
npm run format:check
```

All must pass with no errors.

### 2. Test Coverage

```bash
# Run tests with coverage
npm test -- --coverage
```

Requirements:
- All tests must pass
- Coverage thresholds met (typically 80%+)
- No skipped tests in critical paths
- E2E tests pass (for staging/prod)

### 3. Security Scan

```bash
# Dependency vulnerabilities
npm audit

# Code security scan (if configured)
npm run security:scan
```

Requirements:
- No high/critical vulnerabilities
- Any medium vulnerabilities reviewed

### 4. Build Verification

```bash
# Production build
npm run build
```

Verify:
- Build completes without errors
- Bundle size within limits
- No missing dependencies

### 5. Git State

```bash
git status
git log origin/main..HEAD
```

Verify:
- Working directory clean
- On correct branch
- All commits pushed
- Branch is up to date with main

### 6. Configuration

Check for environment-specific issues:
- No hardcoded URLs/secrets
- Environment variables documented
- Feature flags set correctly

## Report Format

```
Pre-Deploy Check Report
=======================
Target: production
Branch: main
Commit: abc1234

Code Quality
------------
[✓] Linting: Passed
[✓] TypeScript: No errors
[✓] Formatting: Consistent

Tests
-----
[✓] Unit Tests: 245 passed, 0 failed
[✓] Integration: 32 passed, 0 failed
[✓] Coverage: 87% (threshold: 80%)

Security
--------
[✓] npm audit: No vulnerabilities
[✓] Code scan: No issues

Build
-----
[✓] Production build: Success
[✓] Bundle size: 245KB (limit: 500KB)

Git Status
----------
[✓] Working directory: Clean
[✓] Branch: main
[✓] Remote sync: Up to date

RESULT: ✅ READY FOR DEPLOYMENT
```

## Blocking Issues

Deployment MUST NOT proceed if:
- Any tests failing
- High/critical security vulnerabilities
- Build fails
- Uncommitted changes
- Behind remote branch

## Warnings (Non-Blocking)

Flag but allow deployment:
- Coverage below ideal (but above minimum)
- Medium security vulnerabilities (reviewed)
- Large bundle size increase
- Pending deprecation warnings
