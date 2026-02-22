# Git Worktrees

Git worktrees let you have multiple working copies of a repository checked out simultaneously, each on a different branch. Claude Code has first-class worktree support, making it easy to run parallel tasks without them interfering with each other.

## Why Worktrees Matter for Claude Code

When you run multiple Claude sessions against the same directory, they compete over the same files. One session's edits can break another's work mid-flight. Worktrees solve this by giving each session its own isolated copy of the repo that shares the same `.git` directory.

Common use cases:
- Work on two features simultaneously in separate terminals
- Let a subagent make changes without touching your working tree
- Run agent teams where each teammate edits files independently
- Keep your main branch clean while Claude experiments on a side branch

## Built-in Worktree Command

Claude Code provides a `/worktree` slash command that creates a worktree inside `.claude/worktrees/` and switches your session into it.

### Basic Usage

```
> /worktree
```

This creates a new worktree with a random name and a new branch based on HEAD. Your session's working directory moves into the worktree immediately.

### Named Worktrees

```
> /worktree my-feature
```

Creates a worktree at `.claude/worktrees/my-feature` with a corresponding branch.

### What Happens Under the Hood

1. A new directory is created at `.claude/worktrees/<name>/`
2. A new git branch is created from the current HEAD
3. The session's working directory switches to the new worktree
4. When the session ends, you're prompted to keep or remove the worktree

### Cleanup

When your session ends, Claude Code asks whether to keep or remove the worktree. If you keep it, the worktree and its branch remain for you to merge, inspect, or continue later.

You can also manage worktrees manually:

```bash
# List active worktrees
git worktree list

# Remove a specific worktree
git worktree remove .claude/worktrees/my-feature

# Clean up stale worktree references
git worktree prune
```

## Manual Worktrees for Multi-Claude Workflows

You can also create worktrees manually with standard git commands and run separate Claude sessions in each:

```bash
# Create worktrees on feature branches
git worktree add ../project-feature-auth feature-auth
git worktree add ../project-feature-dashboard feature-dashboard

# Run Claude in each (separate terminals)
cd ../project-feature-auth && claude
cd ../project-feature-dashboard && claude
```

Each Claude instance has its own files to edit and its own branch to commit to. When both are done, merge the branches normally.

### Choosing a Location

| Approach | Location | Best For |
|----------|----------|----------|
| `/worktree` command | `.claude/worktrees/` inside the repo | Session-scoped work, subagent isolation |
| Manual `git worktree add` | Sibling directory (e.g., `../project-feature`) | Long-lived parallel features |

## Subagent Worktree Isolation

When Claude spawns a subagent via the Task tool, it can set `isolation: "worktree"` to give that subagent its own copy of the repository. The subagent works in a temporary worktree so its file edits never touch your main working tree.

### How It Works

1. Claude spawns a subagent with `isolation: "worktree"`
2. A temporary worktree is created with a new branch
3. The subagent runs entirely within that worktree
4. If the subagent makes no changes, the worktree is automatically cleaned up
5. If the subagent makes changes, the worktree path and branch name are returned in the result

### When to Use It

- **Experimental changes**: Let a subagent try something without risk to your working tree
- **Parallel editing**: Multiple subagents can edit the same files on different branches
- **Code review**: A reviewer subagent can check out a PR branch in isolation

### Example: Parallel Refactoring

Claude might spawn two subagents in parallel, each in its own worktree:

```
Subagent A (worktree) → refactors the auth module on branch refactor-auth
Subagent B (worktree) → refactors the billing module on branch refactor-billing
```

Neither subagent's changes affect the other or your main working directory. After both complete, you can review and merge each branch.

## Agent Teams and Worktrees

When using [agent teams](./12-agent-sdk.md), worktree isolation becomes especially valuable. Each teammate can be spawned with `isolation: "worktree"` so they edit files independently without stepping on each other.

This is the recommended pattern for teams where multiple agents need to modify code simultaneously.

## WorktreeCreate and WorktreeRemove Hooks

Claude Code fires [hook events](./07-hooks.md) when worktrees are created and removed, allowing you to customize behavior.

### WorktreeCreate

Runs when a worktree is created (via `/worktree` or subagent isolation).

```json
{
  "hooks": {
    "WorktreeCreate": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "cd $WORKTREE_PATH && npm install"
          }
        ]
      }
    ]
  }
}
```

Use cases:
- Install dependencies in the new worktree
- Copy environment files (`.env`) into the worktree
- Initialize local configuration

### WorktreeRemove

Runs when a worktree is removed.

```json
{
  "hooks": {
    "WorktreeRemove": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "echo 'Worktree removed' >> ~/.claude/worktree-log.txt"
          }
        ]
      }
    ]
  }
}
```

Use cases:
- Clean up resources tied to the worktree
- Log worktree lifecycle events
- Archive or back up changes before removal

### Non-Git VCS Support

The `WorktreeCreate` and `WorktreeRemove` hooks also enable worktree-like isolation for non-git version control systems. If you're not in a git repository, Claude Code delegates to these hooks instead of using `git worktree`, letting you implement custom isolation logic for Mercurial, Perforce, or any other VCS.

## Tips

- **Don't forget to merge**: Worktree branches won't merge themselves. After work completes, review and merge the branch.
- **Shared `.git` directory**: All worktrees share the same `.git` database. Commits made in any worktree are visible to all others via standard git commands.
- **Branch exclusivity**: Git requires each worktree to be on a different branch. You can't check out the same branch in two worktrees simultaneously.
- **Disk space**: Worktrees are lightweight because they share the object database, but each has its own copy of the working files.
- **Dependencies**: If your project has a `node_modules/` or similar dependency directory, each worktree needs its own. Use a `WorktreeCreate` hook to automate this.
