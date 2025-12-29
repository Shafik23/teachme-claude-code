# IDE Integrations

Claude Code integrates with popular IDEs for a seamless development experience.

## VS Code

### Installation

1. Open VS Code
2. Press `Cmd+Shift+X` (Mac) or `Ctrl+Shift+X` (Windows/Linux)
3. Search for "Claude Code"
4. Click Install

Or install from: [VS Code Marketplace](https://marketplace.visualstudio.com/items?itemName=anthropic.claude-code)

### Features

| Feature | Description |
|---------|-------------|
| **Graphical Chat Panel** | Native chat interface in VS Code |
| **Inline Diffs** | See proposed changes highlighted in editor |
| **File References** | @-mention files with specific line ranges |
| **Plan Review** | Review changes before accepting |
| **Auto-Accept Mode** | Skip confirmation for trusted operations |
| **Multiple Conversations** | Separate tabs for different tasks |
| **History Access** | Browse and resume past conversations |

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Alt+K` | Insert @-mention file reference |
| `Cmd+Esc` (Mac) / `Ctrl+Esc` | Toggle focus editor ↔ Claude |
| `Cmd+Shift+Esc` / `Ctrl+Shift+Esc` | Open in new tab |

### Commands

Open Command Palette (`Cmd+Shift+P` / `Ctrl+Shift+P`):

- `Claude Code: Open in Side Bar`
- `Claude Code: Open in Terminal`
- `Claude Code: Open in New Tab`
- `Claude Code: Open in New Window`
- `Claude Code: Insert @-Mention Reference`
- `Claude Code: New Conversation`

### Settings

Access via `Preferences > Settings > Claude Code`:

| Setting | Description |
|---------|-------------|
| Selected Model | Choose default Claude model |
| Use Terminal | Launch in terminal mode |
| Initial Permission Mode | Default permission behavior |
| Preferred Location | Sidebar or panel |
| Autosave | Save files before Claude reads/writes |
| Use Ctrl+Enter | Send with Ctrl+Enter instead of Enter |

### Tips

1. **Select code, then chat** - Claude sees your selection as context
2. **Use @-mentions** - Reference specific files: `@src/api/routes.ts:10-50`
3. **Review diffs** - Click through inline changes before accepting
4. **Split view** - Keep Claude panel open alongside code

---

## JetBrains IDEs

### Supported IDEs

- IntelliJ IDEA
- PyCharm
- Android Studio
- WebStorm
- PhpStorm
- GoLand
- Rider
- CLion
- RubyMine

### Installation

1. Open your JetBrains IDE
2. Go to `Settings/Preferences > Plugins`
3. Search for "Claude Code"
4. Click Install
5. Restart IDE

Or install from: [JetBrains Marketplace](https://plugins.jetbrains.com/plugin/27310-claude-code-beta-)

### Features

| Feature | Description |
|---------|-------------|
| **Quick Launch** | Open Claude with keyboard shortcut |
| **IDE Diff Viewer** | See changes in native diff tool |
| **Selection Context** | Selected code auto-shared with Claude |
| **File References** | Shortcut to reference files |
| **Diagnostic Sharing** | Share IDE errors with Claude |

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Cmd+Esc` (Mac) / `Ctrl+Esc` | Open/focus Claude Code |
| `Cmd+Option+K` (Mac) / `Ctrl+Alt+K` | Insert file reference |
| `Option+Enter` (Mac) | Multi-line prompt input |

### Configuration

Settings → Tools → Claude Code [Beta]:

**General:**
- Custom Claude command path
- Option+Enter for multiline (macOS)

**ESC Key Configuration:**
- Configure ESC behavior for interrupting operations

### Tips

1. **Use IDE diagnostics** - Claude sees errors highlighted by your IDE
2. **Select code first** - Selected code provides context
3. **Use refactoring together** - Combine Claude with IDE refactoring tools

---

## Terminal Integration

### Checking IDE Status

```bash
/ide
```

### Launching from Terminal

```bash
# Open project in VS Code with Claude
code . && claude

# Open in JetBrains with Claude
idea . && claude
```

### Terminal Setup

For better multiline input:

```bash
/terminal-setup
```

This enables `Shift+Enter` for newlines in supported terminals.

---

## Best Practices

### 1. Use the Right Interface

| Task | Best Interface |
|------|----------------|
| Quick questions | Terminal |
| Code review with diffs | VS Code/JetBrains |
| Complex refactoring | IDE with diff view |
| Scripting/automation | Terminal with pipes |

### 2. Leverage IDE Features

- **Breakpoints** - Debug issues, then ask Claude about them
- **Git integration** - Use IDE git view alongside Claude
- **Terminal** - Run Claude terminal in IDE's integrated terminal

### 3. Keyboard-First Workflow

Learn the shortcuts for your IDE:

```
Cmd+Esc     → Focus Claude
Alt+K       → @-mention file
Cmd+Shift+P → Command palette
```

### 4. Multiple Conversations

- Keep separate conversations for different features
- Use tabs to organize work streams
- Resume conversations when returning to tasks

---

## Troubleshooting

### Extension Not Loading

1. Check VS Code version (requires latest)
2. Reload window: `Cmd+Shift+P` → "Reload Window"
3. Check extension logs in Output panel

### Plugin Not Working (JetBrains)

1. Verify IDE version compatibility
2. Check `Settings > Plugins > Installed`
3. Restart IDE after installation

### Can't Connect to Claude

1. Run `/doctor` in terminal to check installation
2. Verify authentication: `/login`
3. Check network connectivity

### Diff View Not Showing

1. Ensure Claude is proposing file changes
2. Check IDE diff viewer settings
3. Try terminal mode to verify functionality
