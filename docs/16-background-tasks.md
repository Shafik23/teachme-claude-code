# Background Tasks

Claude Code can run tasks in the background, allowing you to continue working while long-running operations complete.

## Background Shells

Run shell commands in the background:

```bash
# In Claude Code conversation
> Run the test suite in the background while I continue working

# Claude runs with run_in_background: true
# You can continue chatting while tests run
```

### Checking Background Tasks

Use `/bashes` to see running background shell operations:

```
/bashes

Active tasks:
  [shell-abc123] Running: npm run test:all (2m 34s)
  [agent-def456] Running: Code review analysis (1m 12s)
```

### Getting Output

```
> What's the status of the test run?

# Claude uses TaskOutput tool to check progress
```

### Killing Background Tasks

```
> Kill the test run

# Claude uses KillShell to terminate
```

## Background Agents

Launch subagents in the background:

```
> Start analyzing the dependency tree in the background,
  then help me with this other file

# Claude launches Task with run_in_background: true
# You continue working on other things
```

## Use Cases

### 1. Long Test Suites

```
> Run the full E2E test suite in the background

[Background task started]

> While that runs, let's work on the login component
```

### 2. Parallel Analysis

```
> In the background:
  - Analyze code coverage
  - Check for security vulnerabilities
  - Run performance benchmarks

Meanwhile, let's review this PR
```

### 3. Build While Coding

```
> Start the build in the background

[Building...]

> Now let's fix this type error in auth.ts

[Later]
> How did the build go?
```

## TaskOutput Options

When checking background task status:

| Option | Behavior |
|--------|----------|
| `block: true` (default) | Wait for task to complete |
| `block: false` | Return current status immediately |
| `timeout` | Max wait time in milliseconds |

## Best Practices

### 1. Use for Long Operations

Background tasks are ideal for:
- Full test suites (> 30 seconds)
- Complete builds
- Large file operations
- Comprehensive analysis

### 2. Don't Use for Quick Tasks

Skip background for:
- Single file tests
- Quick lints
- Simple git commands

### 3. Monitor Progress

Check in periodically:
```
> Quick status check on background tasks
```

### 4. Clean Up

Kill tasks you no longer need:
```
> Kill all background tasks
```

## Limitations

1. **Session-bound**: Background tasks terminate when you exit Claude Code
2. **Resource usage**: Multiple background tasks consume system resources
3. **Output buffering**: Very long outputs may be truncated

## Example Workflow

```
# Start comprehensive checks in background
> Run these in the background:
  1. npm run test:all
  2. npm run lint
  3. npm run typecheck

# Work on feature
> Now help me implement the new user dashboard

[...coding continues...]

# Check progress
> How are those background tasks doing?

# Review results when done
> Show me any failures from the tests
```
