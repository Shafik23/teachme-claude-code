---
name: git-assistant
description: Help with git operations including commits, branches, merges, rebases, and resolving conflicts. Use when the user mentions "git", "commit", "branch", "merge", "rebase", "conflict", or needs help with version control.
allowed-tools: Bash(git:*), Read, Glob
---

# Git Assistant

## Commit Messages

### Format
Follow Conventional Commits:
```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

### Types
| Type | When to Use |
|------|-------------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `style` | Formatting, no code change |
| `refactor` | Code change that neither fixes nor adds |
| `perf` | Performance improvement |
| `test` | Adding or fixing tests |
| `chore` | Build process, dependencies |

### Examples
```bash
# Feature
git commit -m "feat(auth): add OAuth2 login support"

# Bug fix with issue reference
git commit -m "fix(api): handle null response from payment gateway

Closes #234"

# Breaking change
git commit -m "feat(api)!: change response format to JSON:API

BREAKING CHANGE: All API responses now follow JSON:API spec.
Clients need to update their parsers."
```

## Branch Operations

### Naming Convention
```
feature/description    # New features
fix/issue-number      # Bug fixes
hotfix/description    # Urgent production fixes
release/version       # Release branches
```

### Common Operations
```bash
# Create and switch to new branch
git checkout -b feature/user-profile

# Push new branch to remote
git push -u origin feature/user-profile

# Delete local branch
git branch -d feature/old-branch

# Delete remote branch
git push origin --delete feature/old-branch

# List branches with last commit
git branch -v
```

## Merging

### Fast-Forward Merge (Clean history)
```bash
git checkout main
git merge --ff-only feature/clean-branch
```

### Merge Commit (Preserve history)
```bash
git checkout main
git merge --no-ff feature/branch-name
```

### Squash Merge (Combine commits)
```bash
git checkout main
git merge --squash feature/messy-branch
git commit -m "feat: add complete user profile feature"
```

## Rebasing

### Interactive Rebase (Clean up commits)
```bash
# Rebase last 3 commits
git rebase -i HEAD~3
```

In the editor:
```
pick abc1234 First commit
squash def5678 WIP
squash ghi9012 Fix typo
```

### Rebase onto main
```bash
git checkout feature/my-branch
git rebase main
```

## Resolving Conflicts

### Step-by-Step Process

1. **Identify conflicted files**
   ```bash
   git status
   ```

2. **Open conflicted file** - Look for markers:
   ```
   <<<<<<< HEAD
   your changes
   =======
   their changes
   >>>>>>> branch-name
   ```

3. **Resolve by choosing/combining**
   - Keep yours: Remove their section and markers
   - Keep theirs: Remove your section and markers
   - Combine: Merge both changes, remove markers

4. **Mark as resolved**
   ```bash
   git add resolved-file.js
   ```

5. **Continue operation**
   ```bash
   # For merge
   git commit

   # For rebase
   git rebase --continue
   ```

### Abort if Needed
```bash
git merge --abort
# or
git rebase --abort
```

## Undoing Changes

### Unstage files
```bash
git reset HEAD file.js
```

### Discard local changes
```bash
git checkout -- file.js
# or (Git 2.23+)
git restore file.js
```

### Undo last commit (keep changes)
```bash
git reset --soft HEAD~1
```

### Undo last commit (discard changes)
```bash
git reset --hard HEAD~1
```

### Revert a pushed commit
```bash
git revert abc1234
```

## Stashing

```bash
# Save current changes
git stash push -m "WIP: user profile"

# List stashes
git stash list

# Apply and remove latest stash
git stash pop

# Apply specific stash
git stash apply stash@{2}

# Drop a stash
git stash drop stash@{0}
```

## Viewing History

```bash
# Pretty log
git log --oneline --graph --all

# Changes in last commit
git show

# Who changed what
git blame file.js

# Search commits
git log --grep="bug fix"
git log -S "functionName"  # Search code changes
```

## Safety Reminders

- Never force push to main/master
- Always pull before pushing
- Create backup branch before risky operations
- Use `git reflog` to recover lost commits
