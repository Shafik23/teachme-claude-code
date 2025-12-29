# Checkpoints and Rewind

Claude Code automatically saves checkpoints before each change, letting you instantly rewind to previous states.

## How Checkpoints Work

1. **Automatic saving**: Before Claude modifies any file, a checkpoint is created
2. **Includes everything**: File contents, conversation state, git status
3. **Instant restore**: Jump back to any previous point

## Rewinding

### Double-Tap Escape

The fastest way to rewind:

```
Esc Esc
```

This opens the rewind interface.

### /rewind Command

```
/rewind
```

Shows a list of checkpoints to choose from.

## What You Can Restore

When rewinding, choose what to restore:

| Option | What It Does |
|--------|--------------|
| **Code only** | Restore files to previous state, keep conversation |
| **Conversation only** | Keep current files, restore conversation context |
| **Both** | Restore files AND conversation to that point |

## Use Cases

### 1. Bad Implementation

Claude implemented something wrong:

```
> Refactor the auth module

[Claude makes changes you don't like]

Esc Esc → Select checkpoint before refactoring → Restore both
```

### 2. Explore Different Approaches

Try multiple solutions:

```
> Implement caching with Redis

[Note the checkpoint]

> Actually, try with Memcached instead

Esc Esc → Restore to before Redis → Try Memcached
```

### 3. Recover from Errors

Something broke:

```
> Update the database schema

[Tests now failing]

Esc Esc → Restore code → Take different approach
```

### 4. Edit Previous Prompt

Want to modify what you asked:

```
Esc Esc → Restore conversation → Edit the prompt → Submit again
```

## Checkpoint Visibility

View recent checkpoints:

```
/rewind
```

Shows:
- Timestamp
- What changed
- Files affected
- Conversation state

## Best Practices

### Before Risky Changes

Make a mental note of the current state before asking Claude to do something significant:

```
> Before you start, note this checkpoint. Now refactor the entire API layer.
```

### Iterative Development

Use rewind as an "undo" for Claude's changes:

1. Ask Claude to try something
2. If it's not right: `Esc Esc` → restore → try again with different instructions
3. If it's good: continue

### Comparing Approaches

```
> Implement feature with approach A

[Review result]

Esc Esc → Restore →

> Implement feature with approach B

[Compare the two approaches]
```

## Rewind vs Git

| Rewind | Git |
|--------|-----|
| Instant, within session | Persists across sessions |
| Includes conversation | Code only |
| Automatic | Manual commits |
| Lost when session ends | Permanent history |

**Recommendation**: Use rewind for experimentation, commit to git when satisfied.

## Keyboard Shortcuts Summary

| Shortcut | Action |
|----------|--------|
| `Esc Esc` | Open rewind interface |
| `/rewind` | Open rewind interface |
| `Esc` (single) | Interrupt current operation |

## Tips

1. **Rewind is cheap**: Don't hesitate to try things and rewind if they don't work
2. **Commit often**: Once satisfied, commit to git so you don't lose the checkpoint
3. **Describe intent**: When trying again after rewind, be more specific about what you want differently
