# Deploy Toolkit Plugin

A comprehensive deployment automation toolkit for Claude Code.

## Features

- **Pre-deploy checks** - Automated verification before deployments
- **Multi-environment support** - Dev, staging, and production workflows
- **Rollback capability** - Quick recovery from failed deployments
- **Audit logging** - Track all deployment-related commands

## Installation

```bash
# From local directory
claude plugin add ./deploy-toolkit

# Or from git
claude plugin add https://github.com/example/deploy-toolkit.git
```

## Commands

### `/deploy-toolkit:deploy <environment>`

Deploy to specified environment:

```
/deploy-toolkit:deploy staging
/deploy-toolkit:deploy prod
```

### `/deploy-toolkit:rollback <environment> [version]`

Rollback to previous version:

```
/deploy-toolkit:rollback prod
/deploy-toolkit:rollback staging v1.2.3
```

### `/deploy-toolkit:env-check <environment>`

Verify environment configuration:

```
/deploy-toolkit:env-check prod
```

## Skills

### Pre-Deploy Check

Automatically activated when Claude detects deployment-related tasks. Performs:

- Code quality verification (lint, types, format)
- Test execution and coverage check
- Security scanning
- Build verification
- Git state validation

## Hooks

The plugin includes hooks that:

- Log all deployment commands to `~/.claude/deploy-audit.log`
- Track deployment outcomes for audit purposes

## Configuration

### Environment Variables

The plugin respects these environment variables:

| Variable | Description |
|----------|-------------|
| `DEPLOY_ENV` | Default deployment environment |
| `SKIP_TESTS` | Skip test verification (not recommended) |
| `DEPLOY_TIMEOUT` | Deployment timeout in seconds |

## Customization

### Adding New Environments

1. Create deploy script: `npm run deploy:<env-name>`
2. Add environment config to your application
3. Use: `/deploy-toolkit:deploy <env-name>`

### Modifying Checks

Edit `skills/pre-deploy-check/SKILL.md` to customize:

- Coverage thresholds
- Required checks
- Blocking vs warning issues

## Audit Log Format

```
[2024-01-15T10:30:00Z] Command: npm run deploy:staging
[2024-01-15T10:30:45Z] Exit Code: 0
[2024-01-15T14:22:00Z] Command: npm run rollback:staging
[2024-01-15T14:22:30Z] Exit Code: 0
```

## License

MIT
