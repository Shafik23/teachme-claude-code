# Tips and Tricks

## Keyboard Shortcuts

### Essential Controls

| Shortcut | Action |
|----------|--------|
| `Ctrl+C` | Cancel current operation |
| `Ctrl+D` | Exit Claude Code |
| `Ctrl+L` | Clear screen (keeps history) |
| `Ctrl+R` | Search command history |
| `Up/Down` | Navigate previous prompts |

### Advanced Controls

| Shortcut | Action |
|----------|--------|
| `Ctrl+O` | Toggle verbose output (transcript mode) |
| `Shift+Tab` or `Alt+M` | Toggle permission modes |
| `Option+P` (Mac) / `Alt+P` | Switch model while typing |
| `Alt+T` | Toggle thinking mode |
| `Esc + Esc` | Rewind code/conversation |
| `Ctrl+G` | Edit prompt in system text editor |
| `Alt+Y` | Yank-pop (cycle through kill ring after Ctrl+Y) |
| `?` | Show all shortcuts |

### Image Handling

| Shortcut | Action |
|----------|--------|
| `Ctrl+V` (Mac/Linux) | Paste image from clipboard |
| `Alt+V` (Windows) | Paste image from clipboard |

### Multiline Input

| Method | How |
|--------|-----|
| Backslash | `\ + Enter` |
| Option key (Mac) | `Option+Enter` |
| After setup | `Shift+Enter` (run `/terminal-setup` first) |
| Control sequence | `Ctrl+J` |

## Quick Prefixes

| Prefix | Action |
|--------|--------|
| `/` | Run slash command |
| `!` | Run bash command directly |
| `@` | Reference a file (autocomplete) |
| `&` | Start background task (Claude Code Web) |

## Productivity Tips

### 1. Be Specific

Instead of:
```
> Fix the bug
```

Try:
```
> Fix the null pointer exception in UserService.getUser() when userId is undefined
```

### 2. Provide Context

```
> I'm building a REST API with Express and TypeScript.
> Add rate limiting middleware that:
> - Limits to 100 requests per minute per IP
> - Returns 429 status when exceeded
> - Logs rate limit violations
```

### 3. Use File References

```
> Look at @src/api/routes.ts and add a new endpoint for user preferences
```

### 4. Chain Operations

```
> Update the database schema, generate migrations, and update the TypeScript types
```

### 5. Ask for Explanations

```
> Explain what you changed and why
```

### 6. Request Reviews

```
> Review my changes for potential issues before I commit
```

## CLI Power Moves

### Pipe Operations

```bash
# Analyze logs
tail -f app.log | claude -p "Alert me about errors"

# Generate commit messages
git diff --staged | claude -p "Write a commit message"

# Explain complex output
kubectl describe pod my-pod | claude -p "What's wrong with this pod?"

# Code review
git diff main..feature | claude -p "Review these changes"
```

### Quick Queries

```bash
# One-off questions
claude -p "What's the syntax for Python list comprehensions?"

# File analysis
claude -p "Summarize what this code does" < complex_file.py

# Generate code
claude -p "Write a bash script to find large files" > find_large.sh
```

### Session Continuation

```bash
# Resume last session
claude --resume

# Continue specific session
claude --resume abc123
```

## Vim Mode

Enable with `/vim` for powerful text editing:

### Mode Switching
- `Esc` - Normal mode
- `i`, `a`, `o` - Insert mode variants
- `I`, `A`, `O` - Insert at line positions

### Navigation
- `h/j/k/l` - Movement
- `w/e/b` - Word movement
- `0/$` - Line start/end
- `gg/G` - Document start/end

### Editing
- `x` - Delete character
- `dd` - Delete line
- `cc` - Change line
- `yy` - Yank (copy) line
- `p` - Paste
- `.` - Repeat last change

## Context Management

### Compact Strategically

```
/compact focus on authentication code
```

### Add Related Directories

```
/add-dir ../shared-types
/add-dir ../api-docs
```

### Check Context Usage

```
/context
```

## Model Selection

### Use the Right Model

- **Claude Opus 4** - Complex reasoning, architecture decisions
- **Claude Sonnet 4** - Balanced speed and capability (default)
- **Claude Haiku** - Quick tasks, simple edits

Switch mid-session:
```
/model
```

Or use prefix:
```
Option+P (Mac) / Alt+P (Windows/Linux)
```

## Background Tasks

Run long operations in background:

```
> Run the full test suite in the background
```

Or press `Ctrl+B` to background a running command.

Check background tasks:
```
/bashes
```

## Debugging Tips

### Check Installation Health

```
/doctor
```

### View Token Usage

```
/cost
```

### Export Conversation

```
/export debug-session.md
```

### Report Issues

```
/bug
```

## Security Best Practices

1. **Never auto-allow sensitive operations**
   ```json
   {
     "deny": ["Read(.env*)", "Read(**/*.key)"]
   }
   ```

2. **Use sandbox mode for untrusted code**
   ```
   /sandbox
   ```

3. **Review before committing**
   ```
   > Show me all changes before we commit
   ```

4. **Request security reviews**
   ```
   /security-review
   ```

## Memory Best Practices

### Good CLAUDE.md Content

```markdown
# Project Memory

## Build Commands
- `npm run dev` - Development server
- `npm test` - Run tests
- `npm run build` - Production build

## Code Style
- Use TypeScript strict mode
- Prefer composition over inheritance
- Keep components under 200 lines

## Don't Touch
- `legacy/` - Old code pending migration
- `generated/` - Auto-generated files
```

### Memory Updates

During session, tell Claude to update your memory:
```
> Always format with prettier after editing TS files - update CLAUDE.md
```

Or use:
```
/memory
```

## LSP Integration

Claude Code includes Language Server Protocol support for code intelligence:

- **Go to definition**: Find where symbols are defined
- **Find references**: Find all usages of a symbol
- **Hover documentation**: Get type info and docs
- **Workspace symbols**: Search across the codebase

This works automatically with supported language servers.
