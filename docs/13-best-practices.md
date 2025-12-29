# Best Practices

Official best practices from Anthropic for getting the most out of Claude Code.

*Based on [Claude Code: Best practices for agentic coding](https://www.anthropic.com/engineering/claude-code-best-practices)*

## 1. Customize Your Setup

### Create Effective CLAUDE.md Files

Place `CLAUDE.md` in your project root with:

```markdown
# Bash commands
- npm run build: Build the project
- npm run typecheck: Run the typechecker

# Code style
- Use ES modules (import/export) syntax, not CommonJS (require)
- Destructure imports when possible

# Workflow
- Be sure to typecheck when you're done making changes
- Prefer running single tests, not the whole suite
```

**Locations** (all are read automatically):
- Project root: `CLAUDE.md` (shared) or `CLAUDE.local.md` (personal)
- Parent directories (for monorepos)
- Child directories (loaded on demand)
- Home folder: `~/.claude/CLAUDE.md` (global)

**Pro tip**: Use `#` to add instructions during a session:
```
# Always run prettier after editing TypeScript files
```

### Tune Your Allowlist

Add frequently-used safe tools to avoid permission prompts:

```bash
/permissions
```

Common allowlist additions:
- `Edit` - Allow all file edits
- `Bash(git commit:*)` - Allow git commits
- `Bash(npm run:*)` - Allow npm scripts

## 2. Effective Workflows

### Explore → Plan → Code → Commit

1. **Explore**: Ask Claude to read relevant files without coding yet
   - Use subagents for complex investigations
   - "Read the auth module and understand how sessions work"

2. **Plan**: Ask for a plan using extended thinking
   - Use "think" / "think hard" / "think harder" / "ultrathink" for more thinking budget
   - "Think hard about how to refactor this safely"

3. **Code**: Implement the plan
   - Ask Claude to verify as it implements
   - Save the plan first for easy rollback

4. **Commit**: Let Claude handle git
   - "Commit with an appropriate message and create a PR"

### Test-Driven Development

1. **Write tests first**: "Write tests for user authentication, don't implement yet"
2. **Verify they fail**: "Run the tests and confirm they fail"
3. **Commit tests**: "Commit the tests"
4. **Implement**: "Write code to pass the tests, don't modify the tests"
5. **Commit code**: "Commit when all tests pass"

### Visual Iteration

1. Give Claude a way to screenshot (Puppeteer MCP, iOS Simulator MCP)
2. Provide a design mock (paste image or give path)
3. "Implement this design, screenshot the result, iterate until it matches"
4. Commit when satisfied

## 3. Be Specific

| Poor | Good |
|------|------|
| "add tests for foo.py" | "write tests for foo.py covering the logged-out edge case, avoid mocks" |
| "why is the API weird?" | "look through git history and summarize how ExecutionFactory's API evolved" |
| "add a calendar widget" | "look at HotDogWidget.php as an example, then implement a calendar widget that lets users select month and paginate years" |

## 4. Course Correct Early

- **Press Escape** to interrupt and redirect
- **Double-tap Escape** to rewind and try a different approach
- **Ask for a plan first** before any coding
- **Use /clear** between tasks to reset context

## 5. Multi-Claude Workflows

### Code + Review Pattern

1. Claude #1 writes code
2. `/clear` or new terminal
3. Claude #2 reviews the code
4. Claude #3 implements feedback

### Git Worktrees for Parallelism

```bash
# Create worktrees for parallel work
git worktree add ../project-feature-a feature-a
git worktree add ../project-feature-b feature-b

# Run Claude in each
cd ../project-feature-a && claude
cd ../project-feature-b && claude
```

Each Claude works independently on different features.

### Headless Fan-Out

Process many files in parallel:

```bash
for file in src/*.py; do
  claude -p "migrate $file from Flask to FastAPI" &
done
wait
```

## 6. Give Claude Context

### Images
- **Paste**: Cmd+Ctrl+Shift+4 (macOS screenshot to clipboard), then Ctrl+V
- **Drag and drop** into the prompt
- **File path**: "Look at mockup.png and implement this UI"

### URLs
```
Check https://docs.example.com/api and implement the new endpoint
```

Add domains to allowlist with `/permissions`.

### Files
Use tab-completion to reference files:
```
Look at src/auth/[TAB]
```

## 7. Extended Thinking Triggers

Use these phrases for more thorough reasoning:

| Phrase | Thinking Budget |
|--------|-----------------|
| "think" | Low |
| "think hard" | Medium |
| "think harder" | High |
| "ultrathink" | Maximum |

Example:
```
Think hard about the security implications of this change before implementing.
```

## 8. Checklists for Complex Tasks

For large migrations or many fixes:

1. "Run the linter and write all errors to a checklist in TODO.md"
2. "Fix each issue one by one, checking off as you go"

Claude uses the file as a working scratchpad.

## 9. Common Use Cases

### Codebase Q&A (Onboarding)
- "How does logging work in this project?"
- "How do I create a new API endpoint?"
- "What edge cases does CustomerOnboardingFlow handle?"

### Git Operations
- "Search git history for when this API changed"
- "Write a commit message for these changes"
- "Resolve the rebase conflicts"

### GitHub Integration
- "Create a PR for this feature"
- "Fix the review comments on my PR"
- "Triage the open issues and add labels"

### Jupyter Notebooks
- Open notebook side-by-side with Claude
- "Clean up this notebook before I present it"
- "Make the visualizations more aesthetically pleasing"

## 10. Safety

### Dangerous Skip Permissions

For automated workflows in containers:

```bash
claude --dangerously-skip-permissions
```

**Only use in isolated environments** (Docker without network access).

See the [reference implementation](https://github.com/anthropics/claude-code/tree/main/.devcontainer).

## Sources

- [Claude Code: Best practices for agentic coding](https://www.anthropic.com/engineering/claude-code-best-practices)
- [Claude Code Documentation](https://docs.anthropic.com/en/docs/claude-code)
