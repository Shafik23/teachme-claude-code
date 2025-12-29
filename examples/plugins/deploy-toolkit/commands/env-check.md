---
description: Verify environment configuration and readiness for deployment
argument-hint: <environment>
allowed-tools: Bash(printenv), Read, Glob, Grep
---

# Environment Check Command

Verify the **$ARGUMENTS** environment is properly configured for deployment.

## Checks to Perform

### 1. Required Environment Variables

Check that all required variables are set:

| Variable | Required For | Description |
|----------|--------------|-------------|
| `DATABASE_URL` | All | Database connection string |
| `API_KEY` | All | External API authentication |
| `JWT_SECRET` | All | Token signing secret |
| `SENTRY_DSN` | staging, prod | Error tracking |
| `REDIS_URL` | staging, prod | Cache connection |

### 2. Configuration Files

Verify these files exist and are valid:
- `.env.$ARGUMENTS` or environment-specific config
- `docker-compose.$ARGUMENTS.yml` (if using Docker)
- Kubernetes manifests (if using K8s)

### 3. Service Connectivity

Test connections to:
- Database (can connect, migrations current)
- Redis/Cache (if applicable)
- External APIs (authentication works)
- Message queue (if applicable)

### 4. Resource Availability

Check:
- Disk space on deployment target
- Memory allocation
- CPU limits configured

### 5. Security

Verify:
- No secrets in code/config files
- HTTPS configured (staging/prod)
- CORS settings appropriate for environment

## Output Format

```
Environment Check: $ARGUMENTS
================================

[✓] Environment Variables
    - DATABASE_URL: Set
    - API_KEY: Set
    - JWT_SECRET: Set

[✓] Configuration Files
    - .env.staging: Found
    - docker-compose.staging.yml: Found

[✓] Service Connectivity
    - Database: Connected
    - Redis: Connected

[!] Warnings
    - SENTRY_DSN not set (recommended for staging)

[✗] Errors
    - None

Status: READY FOR DEPLOYMENT
```

## Exit Codes

- `0`: All checks passed, ready for deployment
- `1`: Warnings present, deployment possible but review recommended
- `2`: Errors present, deployment blocked
