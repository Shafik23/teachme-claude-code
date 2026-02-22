# Agent Teams

Agent teams allow you to spawn multiple Claude Code agents that work on different parts of a task simultaneously. A lead agent coordinates the work, assigns subtasks, and merges results.

## Overview

Agent teams extend the [subagent](./11-subagents.md) model by adding coordination between multiple agents. Instead of a single Claude delegating to isolated subagents, teams support:

- **Shared task lists**: All teammates see the same task board
- **Direct messaging**: Teammates can communicate with each other
- **Parallel work**: Multiple agents edit code simultaneously using [worktree isolation](./17-git-worktrees.md)
- **Coordinated shutdown**: The lead agent manages the team lifecycle

## Enabling Agent Teams

Agent teams require an environment variable:

```bash
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
claude
```

## How Teams Work

### Team Lifecycle

1. **Create**: The lead agent creates a team with a name and description
2. **Spawn**: The lead spawns teammates, each with a role and instructions
3. **Assign**: Tasks are created and assigned to teammates
4. **Work**: Teammates work independently, communicating as needed
5. **Complete**: When all tasks are done, the lead shuts down teammates
6. **Cleanup**: The team and task list are removed

### Teammate Behavior

- Teammates go **idle** after each turn — this is normal, not an error
- Sending a message to an idle teammate **wakes them up**
- Messages between teammates are automatically delivered
- Each teammate can have its own tools, model, and permissions

## Display Modes

Control how teammates appear with the `--teammate-mode` flag:

| Mode | Behavior |
|------|----------|
| `auto` (default) | Automatically chooses based on environment |
| `in-process` | Teammates run within the same process |
| `tmux` | Each teammate gets its own tmux pane |

```bash
claude --teammate-mode tmux
```

## Task Coordination

Teams share a task list that all members can access:

- **Create tasks**: Any teammate can add tasks with `TaskCreate`
- **Claim tasks**: Teammates pick up unassigned tasks with `TaskUpdate`
- **Track progress**: Tasks have states: pending, in-progress, completed
- **Order matters**: Prefer tasks in ID order (lower IDs first)

## Communication

### Direct Messages

Teammates communicate using direct messages:

```
# Lead sends to a specific teammate
SendMessage → recipient: "frontend-dev", content: "Start on the login form"

# Teammate replies
SendMessage → recipient: "team-lead", content: "Login form is done"
```

### Broadcasts (Use Sparingly)

Send a message to all teammates at once:

```
# Only for critical team-wide announcements
SendMessage → type: "broadcast", content: "Blocking bug found, pause all work"
```

Broadcasts are expensive — each one sends a separate message to every teammate.

## Example: Full-Stack Feature

A typical team for implementing a full-stack feature:

1. **Lead agent**: Coordinates work, creates tasks, reviews results
2. **Backend agent**: Implements API endpoints and database changes
3. **Frontend agent**: Builds UI components and client-side logic
4. **Test agent**: Writes and runs tests for both frontend and backend

Each agent works in its own [worktree](./17-git-worktrees.md) to avoid file conflicts.

## Best Practices

### 1. Clear Task Descriptions

Give each task enough context that the assigned teammate can work independently.

### 2. Use Worktree Isolation

Spawn teammates with `isolation: "worktree"` when they need to edit files, so their changes don't conflict.

### 3. Prefer Direct Messages Over Broadcasts

Only broadcast for truly critical, team-wide issues.

### 4. Shut Down Gracefully

When work is complete, send shutdown requests to all teammates before cleaning up the team.

## Related

- [Subagents](./11-subagents.md) - Single-agent delegation
- [Git Worktrees](./17-git-worktrees.md) - Worktree isolation for parallel work
- [Background Tasks](./16-background-tasks.md) - Running tasks in the background
