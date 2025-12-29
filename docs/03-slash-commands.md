# Slash Commands Reference

Slash commands control Claude Code behavior. Type `/` to see available commands.

## Navigation & Session

| Command | Description |
|---------|-------------|
| `/help` | Show help information |
| `/exit` | Exit Claude Code |
| `/clear` | Clear conversation history |
| `/resume [session]` | Resume a previous conversation |
| `/rename <name>` | Rename current session |

## Configuration

| Command | Description |
|---------|-------------|
| `/config` | Open settings interface |
| `/model` | Select or change AI model |
| `/permissions` | View or update permissions |
| `/privacy-settings` | View and update privacy settings |
| `/statusline` | Configure status line display |

## Context Management

| Command | Description |
|---------|-------------|
| `/add-dir` | Add additional working directories |
| `/context` | Visualize current context usage |
| `/compact [instructions]` | Compact conversation with optional focus |

## Project Tools

| Command | Description |
|---------|-------------|
| `/init` | Initialize project with CLAUDE.md |
| `/memory` | Edit CLAUDE.md memory files |
| `/review` | Request code review |
| `/todos` | List current TODO items |
| `/rewind` | Rewind conversation and/or code |

## Integrations

| Command | Description |
|---------|-------------|
| `/mcp` | Manage MCP server connections |
| `/hooks` | Manage hook configurations |
| `/ide` | Manage IDE integrations |
| `/agents` | Manage custom AI subagents |
| `/plugin` | Manage Claude Code plugins |

## GitHub

| Command | Description |
|---------|-------------|
| `/install-github-app` | Set up Claude GitHub Actions |
| `/pr-comments` | View pull request comments |

## Utilities

| Command | Description |
|---------|-------------|
| `/cost` | Show token usage statistics |
| `/stats` | Visualize daily usage and streaks |
| `/status` | Show version, model, account info |
| `/usage` | Show plan usage limits |
| `/export [filename]` | Export conversation to file |
| `/doctor` | Check installation health |
| `/bug` | Report bugs to Anthropic |
| `/release-notes` | View release notes |

## Advanced

| Command | Description |
|---------|-------------|
| `/vim` | Enter vim mode for editing |
| `/sandbox` | Enable sandboxed bash tool |
| `/bashes` | List and manage background tasks |
| `/terminal-setup` | Install Shift+Enter key binding |
| `/security-review` | Security review of pending changes |
| `/output-style [style]` | Set output style |

## Account

| Command | Description |
|---------|-------------|
| `/login` | Switch Anthropic accounts |
| `/logout` | Sign out from account |

---

## Custom Slash Commands

Create your own commands as Markdown files.

### Project Commands (Team-Shared)

Create `.claude/commands/your-command.md`:

```markdown
---
description: Run the full test suite with coverage
allowed-tools: Bash(npm run:*)
---

Run all tests with coverage reporting:
1. Run unit tests
2. Run integration tests
3. Generate coverage report
4. Summarize any failures
```

### Personal Commands (Global)

Create `~/.claude/commands/your-command.md`:

```markdown
---
description: My custom code review checklist
---

Review this code for:
- Security vulnerabilities
- Performance issues
- Code style consistency
- Test coverage gaps
```

### Command Arguments

Use `$ARGUMENTS` or positional `$1`, `$2`:

```markdown
---
argument-hint: <component-name>
description: Create a new React component
---

Create a new React component called $ARGUMENTS with:
- TypeScript types
- Unit tests
- Storybook story
```

Usage: `/create-component UserProfile`

### Advanced Features

```markdown
---
allowed-tools: Bash(git:*), Edit
model: claude-3-5-haiku-20241022
description: Quick git operations
---

# Using ! prefix for pre-execution
!git status

Based on the current git status above, help with: $ARGUMENTS
```

### Nested Commands

Organize commands in subdirectories:

```
.claude/commands/
  frontend/
    component.md    -> /frontend:component
    hook.md         -> /frontend:hook
  backend/
    endpoint.md     -> /backend:endpoint
    migration.md    -> /backend:migration
```
