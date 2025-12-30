# Learn Claude Code

Welcome! This repository is your guide to mastering **Claude Code** - Anthropic's agentic coding tool that lives in your terminal.

## What is Claude Code?

Claude Code is an AI-powered pair programmer that helps you:

- **Build features from descriptions** - Describe what you want in plain English; Claude plans, writes code, and verifies it works
- **Debug and fix issues** - Paste an error or describe a bug; Claude analyzes your codebase and implements fixes
- **Navigate any codebase** - Ask questions about unfamiliar code and get thoughtful answers
- **Automate tedious tasks** - Fix lint issues, resolve merge conflicts, write release notes in a single command

## Quick Start

```bash
# Install Claude Code
curl -fsSL https://claude.ai/install.sh | bash

# Or via npm (requires Node.js 18+)
npm install -g @anthropic-ai/claude-code

# Or via Homebrew
brew install --cask claude-code
```

Then simply run:

```bash
claude
```

## Repository Contents

### Getting Started
| File | Description |
|------|-------------|
| [01-getting-started.md](./docs/01-getting-started.md) | Installation, first steps, and basic usage |
| [02-core-features.md](./docs/02-core-features.md) | Essential features and capabilities |
| [03-slash-commands.md](./docs/03-slash-commands.md) | Complete slash command reference |
| [04-configuration.md](./docs/04-configuration.md) | Settings, permissions, and customization |
| [05-tips-and-tricks.md](./docs/05-tips-and-tricks.md) | Power user tips and keyboard shortcuts |

### Integrations
| File | Description |
|------|-------------|
| [06-mcp-servers.md](./docs/06-mcp-servers.md) | Model Context Protocol integrations |
| [07-hooks.md](./docs/07-hooks.md) | Automation with lifecycle hooks |
| [08-ide-integrations.md](./docs/08-ide-integrations.md) | VS Code and JetBrains setup |

### Advanced Features
| File | Description |
|------|-------------|
| [09-skills.md](./docs/09-skills.md) | Model-invoked specialized capabilities |
| [10-plugins.md](./docs/10-plugins.md) | Package and distribute extensions |
| [11-subagents.md](./docs/11-subagents.md) | Delegate to specialized AI agents |

### SDK and Automation
| File | Description |
|------|-------------|
| [12-agent-sdk.md](./docs/12-agent-sdk.md) | Build agents programmatically with Python/TypeScript |
| [13-best-practices.md](./docs/13-best-practices.md) | Official Anthropic best practices guide |
| [14-checkpoints-and-rewind.md](./docs/14-checkpoints-and-rewind.md) | Undo changes with automatic checkpoints |
| [15-headless-and-automation.md](./docs/15-headless-and-automation.md) | CI/CD integration and scripting |
| [16-background-tasks.md](./docs/16-background-tasks.md) | Run long operations in background |

### Examples
| File | Description |
|------|-------------|
| [examples/](./examples/) | Practical workflow examples |

## Key Concepts

### 1. Conversational Coding
Talk to Claude like a colleague. Instead of writing code yourself, describe what you need:

```
> Add a function to validate email addresses in utils.js
```

### 2. Permission System
Claude asks before making changes. You control what it can do:
- **Normal mode** - Claude asks permission for each action
- **Plan mode** - Claude analyzes but doesn't modify
- **Auto-accept mode** - Claude proceeds without asking (use carefully!)

### 3. Context Awareness
Claude reads your codebase, understands project structure, and follows your patterns.

### 4. Tool Access
Claude can:
- Read and write files
- Run shell commands
- Search the web
- Execute tests
- Manage git operations

## Philosophy

Claude Code follows the Unix philosophy - it's composable and scriptable:

```bash
# Pipe logs to Claude for analysis
tail -f app.log | claude -p "Alert me if you see any anomalies"

# Generate commit messages
git diff | claude -p "Write a commit message for these changes"

# Code review from CLI
claude -p "Review the changes in this PR" < pr_diff.txt
```

## Keeping Documentation Current

This repository includes a command that automatically syncs documentation with the official Claude Code website:

```bash
cd teachme-claude-code
claude

> /update-docs
```

This will search the web for current Claude Code features, update all documentation files, and push changes to GitHub.

## Learn More

- [Official Documentation](https://docs.anthropic.com/en/docs/claude-code)
- [Anthropic Discord](https://discord.gg/anthropic)
- [Report Issues](https://github.com/anthropics/claude-code/issues)

---

*This repository was created by Claude Code to teach you about... Claude Code!*
