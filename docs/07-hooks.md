# Hooks

Hooks are user-defined shell commands, LLM prompts, or subagents that execute at specific points in Claude Code's lifecycle. They provide deterministic control over Claude Code's behavior, ensuring certain actions always happen rather than relying on the LLM to choose to run them.

## Hook Events

| Event | When It Runs | Common Uses |
|-------|--------------|-------------|
| `PreToolUse` | Before a tool executes | Block dangerous commands, validate inputs, modify tool input |
| `PostToolUse` | After a tool executes | Auto-format, logging, notifications |
| `PostToolUseFailure` | After a tool call fails | Error handling, retry logic |
| `PermissionRequest` | When permission dialog appears | Auto-approve/deny based on rules, process 'always allow' suggestions |
| `UserPromptSubmit` | When user submits a prompt | Add context, validate input |
| `Notification` | When Claude sends notification | Custom notification handling |
| `Stop` | When Claude finishes responding | Post-response actions, quality gates |
| `SubagentStart` | When a subagent begins | Initialize subagent context |
| `SubagentStop` | When a subagent completes | Handle subagent results (includes agent_id and agent_transcript_path) |
| `TeammateIdle` | When an agent team teammate goes idle | Coordinate team workflows |
| `TaskCompleted` | When a task is marked as completed | Post-completion actions |
| `ConfigChange` | When a config file changes during session | Audit, block unauthorized changes |
| `WorktreeCreate` | When a worktree is created | Custom VCS worktree behavior |
| `WorktreeRemove` | When a worktree is removed | Worktree cleanup |
| `PreCompact` | Before conversation compaction | Pre-compaction logic |
| `SessionStart` | When session begins or resumes | Initialize environment, set env vars |
| `SessionEnd` | When session ends | Cleanup actions, logging session statistics |

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
            "command": "your-command-here",
            "timeout": 60,
            "once": true
          }
        ]
      }
    ]
  }
}
```

### Hook Options

| Option | Description |
|--------|-------------|
| `type` | `"command"` for bash commands, `"prompt"` for LLM evaluation, `"agent"` for multi-turn subagent verification |
| `command` | The bash command to execute (for `type: "command"`) |
| `prompt` | The prompt for LLM evaluation (for `type: "prompt"` or `type: "agent"`) |
| `model` | Override model for prompt/agent hooks (default: Haiku) |
| `timeout` | Max execution time in seconds (default: 600, max: 600) |
| `once` | If `true`, hook only runs once per session |

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

Hooks receive JSON on stdin with context about the event. The environment variable `$CLAUDE_TOOL_OUTPUT` contains the output from the tool's execution (only for the PostToolUse event).

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
| `SubagentStart` | Blocks subagent start, shows stderr to Claude |
| `SubagentStop` | Blocks stoppage, shows stderr to subagent |
| `SessionStart` | Shows stderr to user only |
| `SessionEnd` | Shows stderr to user only |

## JSON Output

For advanced control, output JSON:

```json
{
  "allow": true,
  "message": "Approved with note"
}
```

### Modifying Tool Input (PreToolUse)

PreToolUse hooks can modify the tool input before execution:

```json
{
  "allow": true,
  "updatedInput": {
    "command": "npm test -- --coverage"
  }
}
```

This is useful for:
- Adding flags or options to commands
- Rewriting file paths
- Injecting environment-specific settings

## Prompt-Based Hooks

Use an LLM (Haiku) to evaluate hooks with context-aware decisions:

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Evaluate if Claude should stop: $ARGUMENTS. Check if all tasks are complete.",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

Prompt-based hooks work especially well with `Stop` and `SubagentStop` events for intelligent, context-aware decisions about whether Claude should continue working. Use `$ARGUMENTS` as a placeholder for the hook input JSON. You can specify a different model with the `model` field if you need more capability than the default (Haiku).

## Agent-Based Hooks

When verification requires inspecting files or running commands, use `type: "agent"` hooks. Unlike prompt hooks which make a single LLM call, agent hooks spawn a subagent that can read files, search code, and use other tools to verify conditions before returning a decision.

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "agent",
            "prompt": "Verify that all unit tests pass. Run the test suite and check the results. $ARGUMENTS",
            "timeout": 120
          }
        ]
      }
    ]
  }
}
```

Agent hooks use the same `"ok"` / `"reason"` response format as prompt hooks, but with a longer default timeout of 60 seconds and up to 50 tool-use turns. Use prompt hooks when the hook input data alone is enough to make a decision. Use agent hooks when you need to verify something against the actual state of the codebase.

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
| `CLAUDE_TOOL_OUTPUT` | (PostToolUse only) The output from the tool's execution |

### SessionStart Hook Input

The SessionStart hook receives JSON input with:

```json
{
  "agent_type": "my-agent"
}
```

The `agent_type` field is populated if `--agent` was specified on the command line.

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
