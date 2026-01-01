# Getting Started with Claude Code

## Installation

### Option 1: Native Install (Recommended)

```bash
# macOS, Linux, or WSL
curl -fsSL https://claude.ai/install.sh | bash
```

### Option 2: Homebrew (macOS)

```bash
brew install --cask claude-code
```

### Option 3: Windows

**PowerShell:**
```powershell
irm https://claude.ai/install.ps1 | iex
```

**CMD:**
```cmd
curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
```

### Option 4: npm (Cross-platform)

Requires Node.js 18+:

```bash
npm install -g @anthropic-ai/claude-code
```

## First Launch

After installation, start Claude Code:

```bash
cd your-project
claude
```

On first run, you'll authenticate with your [Claude.ai](https://claude.ai/) account (recommended) or [Claude Console](https://console.anthropic.com/) account.

## Basic Usage

### Interactive Mode

Simply type your request in natural language:

```
> Create a Python function that calculates fibonacci numbers
```

Claude will:
1. Understand your request
2. Ask clarifying questions if needed
3. Write the code
4. Ask permission before creating/modifying files

### Non-Interactive Mode

Use the `-p` flag for single prompts:

```bash
# Quick questions
claude -p "What does the main() function in app.py do?"

# Generate code
claude -p "Write a bash script to backup my documents folder"

# Pipe input
cat error.log | claude -p "Explain this error and suggest a fix"
```

## Your First Project

Let's walk through a simple example:

### 1. Start Claude Code in your project

```bash
cd my-project
claude
```

### 2. Ask Claude to understand your codebase

```
> Give me an overview of this project's structure
```

### 3. Make a change

```
> Add input validation to the login function in auth.js
```

### 4. Review and approve

Claude will show you the proposed changes and ask for permission before applying them.

## Understanding Permissions

Claude operates with a permission system:

| Action | Permission Required |
|--------|---------------------|
| Read files | Usually auto-approved |
| Write/edit files | Asks permission |
| Run shell commands | Asks permission |
| Delete files | Always asks |

You can configure these in settings (see [04-configuration.md](./04-configuration.md)).

## Session Management

### Resume Previous Sessions

```bash
# Open session picker
claude --resume

# Resume by session ID
claude --resume abc123

# Resume by number (e.g., most recent)
claude --resume 1

# Resume named session (use /rename to name sessions)
claude --resume my-feature-work

# Fork a session with custom ID
claude --resume abc123 --fork-session --session-id new-session-id
```

The `/resume` screen shows sessions grouped by branch with search, preview (P), and rename (R) shortcuts.

### Continue Last Session

```bash
claude --continue
```

### Clear Conversation

In interactive mode:
```
/clear
```

### Exit

```
/exit
```
Or press `Ctrl+D`

## Getting Help

```bash
# CLI help
claude --help

# In-session help
/help
```

## Next Steps

- Learn about [Core Features](./02-core-features.md)
- Explore [Slash Commands](./03-slash-commands.md)
- Configure your [Settings](./04-configuration.md)
