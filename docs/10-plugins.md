# Plugins

Plugins are packaged distributions of Claude Code extensions. They bundle slash commands, Skills, hooks, agents, and MCP servers into a single installable package that can be shared across teams and communities.

## Why Plugins?

| Standalone (`.claude/`) | Plugins |
|-------------------------|---------|
| `/hello` | `/my-plugin:hello` (namespaced) |
| Single project | Distribute anywhere |
| Manual file copying | One-command install |
| No versioning | Semantic versioning |

## Plugin Structure

```
my-plugin/
├── .claude-plugin/          # Required
│   └── plugin.json          # Required: manifest
├── commands/                # Slash commands
│   └── deploy.md
├── agents/                  # Subagents
│   └── reviewer.md
├── skills/                  # Skills
│   └── code-review/
│       └── SKILL.md
├── hooks/                   # Lifecycle hooks
│   └── hooks.json
├── .mcp.json               # MCP servers
├── .lsp.json               # LSP servers
└── README.md
```

**Important**: Only `plugin.json` goes in `.claude-plugin/`. Everything else is at the root.

## Creating a Plugin

### Step 1: Create Structure

```bash
mkdir -p my-plugin/.claude-plugin
mkdir -p my-plugin/commands
```

### Step 2: Create Manifest

```json
// my-plugin/.claude-plugin/plugin.json
{
  "name": "my-plugin",
  "description": "What this plugin does",
  "version": "1.0.0",
  "author": {
    "name": "Your Name"
  }
}
```

### Step 3: Add a Command

```markdown
<!-- my-plugin/commands/hello.md -->
---
description: Greet the user
---

Say hello and ask how you can help today.
```

### Step 4: Test It

```bash
claude --plugin-dir ./my-plugin
```

Then use:
```
/my-plugin:hello
```

## Plugin Manifest Reference

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Unique identifier (kebab-case) |

### Optional Fields

| Field | Type | Description |
|-------|------|-------------|
| `version` | string | Semantic version (`1.0.0`) |
| `description` | string | What the plugin does |
| `author` | object | `{name, email, url}` |
| `homepage` | string | Documentation URL |
| `repository` | string | Source code URL |
| `license` | string | License identifier |
| `keywords` | array | Discovery tags |
| `commands` | string/array | Custom command paths |
| `agents` | string/array | Custom agent paths |
| `skills` | string/array | Custom skill paths |
| `hooks` | string/object | Hook config |
| `mcpServers` | string/object | MCP config |
| `lspServers` | string/object | LSP config |
| `outputStyles` | string/array | Output style paths |

### Full Manifest Example

```json
{
  "name": "deploy-tools",
  "version": "2.1.0",
  "description": "Deployment automation for AWS and GCP",
  "author": {
    "name": "DevOps Team",
    "email": "devops@example.com"
  },
  "homepage": "https://docs.example.com/deploy-tools",
  "repository": "https://github.com/example/deploy-tools",
  "license": "MIT",
  "keywords": ["deployment", "aws", "gcp", "ci-cd"],
  "hooks": "./hooks/hooks.json",
  "mcpServers": {
    "aws": {
      "command": "npx",
      "args": ["@example/mcp-aws"]
    }
  }
}
```

## Plugin Components

### Commands

```markdown
<!-- commands/deploy.md -->
---
description: Deploy to specified environment
argument-hint: [environment]
allowed-tools: Bash(git:*), Bash(aws:*)
---

Deploy to $ARGUMENTS environment:
1. Run pre-deploy checks
2. Build the application
3. Deploy to AWS
4. Verify deployment health
```

Usage: `/deploy-tools:deploy production`

### Skills

```
skills/
└── deployment-checker/
    └── SKILL.md
```

```yaml
---
name: deployment-checker
description: Verify deployment readiness. Use before deploying or when checking if code is ready to ship.
---

# Deployment Checker

Before any deployment, verify:
1. All tests pass
2. No security vulnerabilities
3. Environment variables configured
4. Database migrations ready
```

### Agents

```markdown
<!-- agents/release-manager.md -->
---
name: release-manager
description: Manage release process end-to-end
---

# Release Manager

Handle the complete release workflow:
1. Version bump
2. Changelog generation
3. Tag creation
4. Deployment coordination
```

### Hooks

```json
// hooks/hooks.json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/lint.sh"
          }
        ]
      }
    ]
  }
}
```

Note: Use `${CLAUDE_PLUGIN_ROOT}` to reference files within the plugin.

### MCP Servers

```json
// .mcp.json
{
  "mcpServers": {
    "plugin-db": {
      "command": "${CLAUDE_PLUGIN_ROOT}/bin/db-server",
      "args": ["--config", "${CLAUDE_PLUGIN_ROOT}/config.json"]
    }
  }
}
```

## Installing Plugins

### From Directory

```bash
claude plugin add ./path/to/plugin
```

### From Git

```bash
claude plugin add https://github.com/user/plugin.git
```

### Installation Scopes

| Scope | Location | Use Case |
|-------|----------|----------|
| `user` (default) | `~/.claude/settings.json` | Personal, all projects |
| `project` | `.claude/settings.json` | Team, via git |
| `local` | `.claude/settings.local.json` | Project-specific, gitignored |

```bash
# Install for just this project
claude plugin add --scope project ./my-plugin
```

## Managing Plugins

```bash
# List installed plugins
claude plugin list

# Remove a plugin
claude plugin remove my-plugin

# In-session management
/plugin

# Discover plugins from marketplaces
/plugin discover

# Validate plugin structure
/plugin validate ./my-plugin
```

### Plugin Marketplaces

Plugins can be distributed through marketplaces. Use `extraKnownMarketplaces` in your settings for team collaboration. Add branch/tag support with fragment syntax:

```bash
claude plugin add https://github.com/user/plugin.git#v2.0
```

Auto-update toggles allow per-marketplace control over automatic updates.

## Converting Existing Config to Plugin

If you have `.claude/commands/`, `.claude/skills/`, etc:

```bash
# 1. Create plugin structure
mkdir -p my-plugin/.claude-plugin

# 2. Create manifest
cat > my-plugin/.claude-plugin/plugin.json << 'EOF'
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "Converted from .claude config"
}
EOF

# 3. Copy existing files
cp -r .claude/commands my-plugin/
cp -r .claude/skills my-plugin/
cp -r .claude/agents my-plugin/

# 4. Test
claude --plugin-dir ./my-plugin
```

## Distributing Plugins

1. **Document** - Add a README.md
2. **Version** - Use semantic versioning
3. **Host** - Push to GitHub or similar
4. **Share** - Provide install command:

```bash
claude plugin add https://github.com/yourname/your-plugin.git
```

## Plugin Development Tips

### Use Environment Variable for Paths

```json
{
  "command": "${CLAUDE_PLUGIN_ROOT}/scripts/my-script.sh"
}
```

### Namespace Everything

Commands become `/plugin-name:command`, avoiding conflicts.

### Test During Development

```bash
claude --plugin-dir ./my-plugin
```

### Debug Issues

```bash
claude --debug --plugin-dir ./my-plugin
```

## Example: Complete CI/CD Plugin

```
ci-cd-plugin/
├── .claude-plugin/
│   └── plugin.json
├── commands/
│   ├── build.md
│   ├── test.md
│   └── deploy.md
├── skills/
│   └── pipeline-debugger/
│       └── SKILL.md
├── hooks/
│   └── hooks.json
└── README.md
```

```json
// .claude-plugin/plugin.json
{
  "name": "ci-cd",
  "version": "1.0.0",
  "description": "CI/CD pipeline management",
  "keywords": ["ci", "cd", "deployment", "testing"]
}
```

```markdown
<!-- commands/build.md -->
---
description: Build the project for specified environment
argument-hint: [dev|staging|prod]
allowed-tools: Bash(npm:*), Bash(docker:*)
---

Build for $ARGUMENTS:
1. Install dependencies
2. Run linting
3. Compile/bundle
4. Build Docker image if Dockerfile exists
```

```yaml
# skills/pipeline-debugger/SKILL.md
---
name: pipeline-debugger
description: Debug CI/CD pipeline failures. Use when builds fail, deployments break, or pipeline issues occur.
allowed-tools: Read, Bash(gh:*), Bash(docker logs:*)
---

# Pipeline Debugger

When debugging pipeline failures:

1. Check recent workflow runs: `gh run list`
2. Get failure logs: `gh run view <id> --log-failed`
3. Identify root cause
4. Suggest fix
```

## Ready-to-Use Example

See [examples/plugins/deploy-toolkit/](../examples/plugins/deploy-toolkit/) for a complete, working plugin with:

- **3 Commands:** deploy, rollback, env-check
- **1 Skill:** pre-deploy-check
- **Hooks:** deployment audit logging
- **Scripts:** helper scripts for automation

Test it:
```bash
claude --plugin-dir ./examples/plugins/deploy-toolkit
```

Then try:
```
/deploy-toolkit:deploy staging
/deploy-toolkit:env-check prod
```
