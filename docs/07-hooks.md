# Hooks

Hooks are user-defined shell commands that execute at various lifecycle points, allowing you to customize and extend Claude Code's behavior.

## Hook Events

| Event | When It Runs | Common Uses |
|-------|--------------|-------------|
| `PreToolUse` | Before a tool executes | Block dangerous commands, validate inputs |
| `PostToolUse` | After a tool executes | Auto-format, logging, notifications |
| `PermissionRequest` | When permission dialog appears | Auto-approve/deny based on rules |
| `UserPromptSubmit` | When user submits a prompt | Add context, validate input |
| `Notification` | When Claude sends notification | Custom notification handling |
| `Stop` | When Claude finishes responding | Post-response actions |
| `SubagentStop` | When a subagent completes | Handle subagent results |
| `PreCompact` | Before conversation compaction | Pre-compaction logic |
| `SessionStart` | When session begins | Initialize environment, set env vars |
| `SessionEnd` | When session ends | Cleanup actions |

### Notification Matchers

Filter notifications by type:
- `permission_prompt` - Permission requests
- `idle_prompt` - When Claude is waiting (60+ seconds idle)
- `auth_success` - Authentication success
- `elicitation_dialog` - MCP tool input needed

## Basic Configuration

Add hooks to your `settings.json`:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "echo 'File modified!'"
          }
        ]
      }
    ]
  }
}
```

## Hook Structure

```json
{
  "hooks": {
    "EventName": [
      {
        "matcher": "ToolPattern",
        "hooks": [
          {
            "type": "command",
            "command": "your-command-here"
          }
        ]
      }
    ]
  }
}
```

### Matchers

- `"Bash"` - Match Bash tool
- `"Edit"` - Match Edit tool
- `"Edit|Write"` - Match multiple tools
- `"*"` - Match all tools

## Practical Examples

### 1. Auto-Format After Edits

Format TypeScript files automatically:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '.tool_input.file_path' | xargs -I {} sh -c 'echo {} | grep -q \"\\.ts$\" && npx prettier --write {}'"
          }
        ]
      }
    ]
  }
}
```

### 2. Log All Bash Commands

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '.tool_input.command' >> ~/.claude/command-log.txt"
          }
        ]
      }
    ]
  }
}
```

### 3. Block Dangerous Commands

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '.tool_input.command' | grep -qE 'rm -rf|sudo|chmod 777' && exit 1 || exit 0"
          }
        ]
      }
    ]
  }
}
```

### 4. Protect Sensitive Files

Python script (`~/.claude/hooks/protect-files.py`):

```python
#!/usr/bin/env python3
import json
import sys

data = json.load(sys.stdin)
path = data.get('tool_input', {}).get('file_path', '')

protected = ['.env', 'secrets/', 'credentials', '.key']
if any(p in path for p in protected):
    print(f"Blocked: {path} is protected", file=sys.stderr)
    sys.exit(1)
sys.exit(0)
```

Hook configuration:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write|Read",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ~/.claude/hooks/protect-files.py"
          }
        ]
      }
    ]
  }
}
```

### 5. Send Notifications

```json
{
  "hooks": {
    "Stop": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "osascript -e 'display notification \"Claude finished\" with title \"Claude Code\"'"
          }
        ]
      }
    ]
  }
}
```

### 6. Run Tests After Changes

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '.tool_input.file_path' | grep -q 'src/.*\\.ts$' && npm test --silent || true"
          }
        ]
      }
    ]
  }
}
```

## Hook Input Format

Hooks receive JSON on stdin with context about the event:

### PreToolUse / PostToolUse

```json
{
  "tool_name": "Bash",
  "tool_input": {
    "command": "npm test",
    "description": "Run test suite"
  }
}
```

### For Edit/Write tools

```json
{
  "tool_name": "Edit",
  "tool_input": {
    "file_path": "/path/to/file.ts",
    "old_string": "...",
    "new_string": "..."
  }
}
```

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success - stdout shown in verbose mode |
| 1 | Non-blocking error - stderr shown in verbose mode |
| 2 | Blocking error - stderr fed back to Claude |

### Exit Code 2 Behavior by Event

| Event | Exit Code 2 Behavior |
|-------|---------------------|
| `PreToolUse` | Blocks tool call, shows stderr to Claude |
| `PermissionRequest` | Denies permission, shows stderr to Claude |
| `PostToolUse` | Shows stderr to Claude (tool already ran) |
| `UserPromptSubmit` | Blocks prompt, erases it, shows stderr to user |
| `Stop` | Blocks stoppage, shows stderr to Claude |
| `SubagentStop` | Blocks stoppage, shows stderr to subagent |
| `SessionStart` | Shows stderr to user only |
| `SessionEnd` | Shows stderr to user only |

## JSON Output

For advanced control, output JSON:

```json
{
  "allow": true,
  "message": "Approved with note",
  "modification": "modified content"
}
```

## Prompt-Based Hooks

Use Claude to evaluate hooks:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Is this command safe? Respond with JSON: {\"allow\": true/false, \"reason\": \"...\"}"
          }
        ]
      }
    ]
  }
}
```

## Managing Hooks

```bash
# View configured hooks
/hooks

# Edit hooks
/config
```

## Environment Variables

Hooks have access to special environment variables:

| Variable | Description |
|----------|-------------|
| `CLAUDE_PROJECT_DIR` | Absolute path to project root |
| `CLAUDE_ENV_FILE` | (SessionStart only) File to persist env vars |
| `CLAUDE_CODE_REMOTE` | `"true"` if running in remote/web environment |

### Persisting Environment Variables (SessionStart)

```bash
#!/bin/bash
if [ -n "$CLAUDE_ENV_FILE" ]; then
  echo 'export NODE_ENV=production' >> "$CLAUDE_ENV_FILE"
  echo 'export API_KEY=your-key' >> "$CLAUDE_ENV_FILE"
fi
exit 0
```

Variables written to `CLAUDE_ENV_FILE` are available in all subsequent bash commands.

---

## Plugin Hooks

Plugins can provide hooks via `hooks/hooks.json`:

```json
{
  "description": "Automatic code formatting",
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/format.sh",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

Plugin hooks run alongside your custom hooks in parallel.

---

## Best Practices

1. **Keep hooks fast** - Slow hooks delay every operation
2. **Handle errors gracefully** - Don't break Claude on hook failures
3. **Log for debugging** - Write to files for troubleshooting
4. **Test thoroughly** - Hooks run on every matching operation
5. **Use specific matchers** - Avoid `*` when possible
6. **Use `$CLAUDE_PROJECT_DIR`** - Reference project scripts with absolute paths

## Debugging Hooks

1. Add logging to your hook:
   ```bash
   echo "Hook triggered: $(date)" >> ~/.claude/hook-debug.log
   ```

2. Test hook scripts manually:
   ```bash
   echo '{"tool_name":"Bash","tool_input":{"command":"npm test"}}' | your-hook-script.sh
   ```

3. Check exit codes:
   ```bash
   your-hook-script.sh; echo "Exit code: $?"
   ```
