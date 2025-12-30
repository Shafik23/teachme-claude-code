# Slash Commands Reference

Slash commands control Claude Code behavior. Type `/` to see available commands.

## Navigation & Session

| Command | Description |
|---------|-------------|
| `/help` | Show help information |
| `/exit` | Exit Claude Code |
| `/clear` | Clear conversation history |
| `/resume [session]` | Resume a previous conversation by ID, name, or pick from list |
| `/rename <name>` | Rename current session for easier identification (enables named resume) |
| `/export [filename]` | Export conversation to file or clipboard |

## Configuration

| Command | Description |
|---------|-------------|
| `/config` | Open settings interface (Config tab) |
| `/settings` | Alias for `/config` |
| `/model` | Select or change AI model |
| `/permissions` | View or update permissions |
| `/privacy-settings` | View and update privacy settings |
| `/statusline` | Configure status line display |
| `/output-style [style]` | Set output style (Concise, Normal, Explanatory) |
| `/theme` | Open theme picker (Ctrl+T to toggle syntax highlighting) |

## Context Management

| Command | Description |
|---------|-------------|
| `/add-dir` | Add additional working directories |
| `/context` | Visualize current context window usage |
| `/compact [instructions]` | Compact conversation with optional focus instructions |

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
| `/cost` | Show token usage statistics for current session |
| `/stats` | Visualize daily usage, streaks, and favorite model |
| `/status` | Show version, model, account, and connectivity info |
| `/usage` | Show plan usage limits and rate limit status |
| `/doctor` | Check installation health and diagnose issues |
| `/bug` | Report bugs to Anthropic |
| `/release-notes` | View release notes for current version |

## Advanced

| Command | Description |
|---------|-------------|
| `/vim` | Enter vim mode for editing |
| `/sandbox` | Enable sandboxed bash tool with filesystem and network isolation |
| `/bashes` | List and manage background shell tasks |
| `/terminal-setup` | Install Shift+Enter key binding for multiline input (iTerm2, VSCode, Kitty, Alacritty, Zed, Warp, WezTerm) |
| `/security-review` | Security review of pending changes |

## Account

| Command | Description |
|---------|-------------|
| `/login` | Switch Anthropic accounts |
| `/logout` | Sign out from account |

---

## MCP Slash Commands

MCP servers can expose prompts as slash commands. These follow the pattern:

```
/mcp__<server-name>__<prompt-name> [arguments]
```

Examples:
```bash
/mcp__github__list_prs
/mcp__github__pr_review 456
/mcp__jira__create_issue "Bug title" high
```

MCP commands are dynamically discovered from connected servers. Use `/mcp` to manage connections.

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

### Frontmatter Options

| Field | Description | Default |
|-------|-------------|---------|
| `allowed-tools` | Tools the command can use | Inherits from conversation |
| `argument-hint` | Arguments hint shown in autocomplete | None |
| `description` | Brief description of command | First line of prompt |
| `model` | Override model for this command | Inherits from conversation |
| `disable-model-invocation` | Prevent SlashCommand tool from calling this | false |

---

## Plugin Commands

Plugins can provide custom slash commands that integrate with Claude Code.

- **Namespaced**: Use `/plugin-name:command-name` to avoid conflicts
- **Automatically available**: Commands appear in `/help` when plugin is enabled
- **Fully integrated**: Support all command features (arguments, frontmatter, bash execution)

---

## SlashCommand Tool

Claude can invoke custom slash commands programmatically via the `SlashCommand` tool. To encourage this, reference commands by name in your prompts or `CLAUDE.md`:

```
Run /write-unit-test when you are about to start writing tests.
```

### Disable SlashCommand Tool

To prevent Claude from executing slash commands via the tool:

```
/permissions
# Add to deny rules: SlashCommand
```

---

## Skills vs Slash Commands

| Aspect | Slash Commands | Skills |
|--------|----------------|--------|
| **Invocation** | Explicit (`/command`) | Automatic (Claude decides) |
| **Discovery** | User types `/` | Semantic matching |
| **Best for** | Quick actions, frequent tasks | Complex workflows, domain expertise |
| **Structure** | Single .md file | Directory with SKILL.md + resources |
