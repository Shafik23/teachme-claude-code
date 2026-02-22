# Headless Mode and Automation

Claude Code's headless mode (`claude -p`) enables non-interactive automation for CI/CD, scripts, and programmatic workflows.

## Basic Usage

```bash
# Single prompt, get response
claude -p "What files are in this directory?"

# With specific output format
claude -p "List all TODO comments" --output-format json
```

## Output Formats

| Format | Use Case |
|--------|----------|
| `text` (default) | Human-readable output |
| `json` | Structured data for parsing |
| `stream-json` | Streaming JSON for real-time processing |

```bash
# JSON output for parsing
claude -p "Analyze this codebase" --output-format json | jq '.result'

# Streaming for real-time
claude -p "Run tests and report" --output-format stream-json
```

## Tool Permissions

In headless mode, specify allowed tools:

```bash
claude -p "Fix the lint errors" --allowed-tools "Edit,Bash(npm run lint:*)"
```

### Skip All Permissions (Dangerous)

For fully automated environments:

```bash
claude --dangerously-skip-permissions -p "Migrate all files"
```

**Only use in isolated containers without network access.**

## CI/CD Integration

### GitHub Actions

```yaml
name: Claude Code Review

on: [pull_request]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install Claude Code
        run: npm install -g @anthropic-ai/claude-code

      - name: Review PR
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          git diff origin/${{ github.base_ref }}...HEAD | \
            claude -p "Review this diff for bugs and security issues" \
            --output-format json > review.json

      - name: Post Review
        run: |
          # Parse review.json and post comments
```

### GitLab CI

```yaml
code-review:
  script:
    - npm install -g @anthropic-ai/claude-code
    - git diff $CI_MERGE_REQUEST_DIFF_BASE_SHA | claude -p "Review for issues"
```

### Pre-commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

# Check for secrets
claude -p "Check staged files for hardcoded secrets" \
  --allowed-tools "Bash(git diff:*)" \
  --output-format json | jq -e '.has_secrets == false' || exit 1
```

## Automation Patterns

### Fan-Out (Parallel Processing)

Process many files concurrently:

```bash
#!/bin/bash

# Migrate all Python files to new framework
for file in src/**/*.py; do
  claude -p "Migrate $file from Flask to FastAPI" \
    --allowed-tools "Read,Edit" &
done
wait
```

### Pipeline Integration

Chain with other tools:

```bash
# Analyze logs and alert
tail -1000 /var/log/app.log | \
  claude -p "Summarize errors and their frequency" \
  --output-format json | \
  jq '.errors[] | select(.count > 10)' | \
  send-to-slack
```

### Scheduled Jobs (Cron)

```bash
# Daily code health check
0 9 * * * cd /app && claude -p "Check for security vulnerabilities and outdated deps" \
  --output-format json > /reports/daily-$(date +%Y%m%d).json
```

## Issue Triage

Automatically label new issues:

```bash
#!/bin/bash
# Triggered by GitHub webhook

ISSUE_BODY=$(gh issue view $ISSUE_NUMBER --json body -q '.body')

LABELS=$(echo "$ISSUE_BODY" | claude -p "
Analyze this issue and output JSON with suggested labels.
Choose from: bug, feature, documentation, security, performance
Output format: {\"labels\": [\"label1\", \"label2\"]}
" --output-format json | jq -r '.labels | join(",")')

gh issue edit $ISSUE_NUMBER --add-label "$LABELS"
```

## Commit Message Generation

```bash
#!/bin/bash
# git-commit-ai

MESSAGE=$(git diff --staged | claude -p "
Write a conventional commit message for these changes.
Format: type(scope): description
Types: feat, fix, docs, style, refactor, test, chore
")

git commit -m "$MESSAGE"
```

## Code Review Bot

```bash
#!/bin/bash
# review-pr.sh

PR_NUMBER=$1

# Get diff
gh pr diff $PR_NUMBER > /tmp/diff.patch

# Review
REVIEW=$(claude -p "
Review this PR for:
1. Security vulnerabilities
2. Performance issues
3. Code style violations
4. Test coverage gaps

Output as GitHub review comments JSON.
" < /tmp/diff.patch --output-format json)

# Post comments
echo "$REVIEW" | gh pr review $PR_NUMBER --comment -F -
```

## Verbose Mode

Debug your automation:

```bash
claude -p "Your prompt" --verbose
```

Shows:
- Tool calls being made
- Files being read/written
- Intermediate reasoning

## Environment Variables

```bash
# Required
export ANTHROPIC_API_KEY=your-key

# Optional
export ANTHROPIC_MODEL=claude-sonnet-4-5-20250929  # Override model
export ANTHROPIC_SMALL_FAST_MODEL=claude-3-5-haiku # Override small model
export ANTHROPIC_DEFAULT_SONNET_MODEL=...          # Control sonnet alias
export ANTHROPIC_DEFAULT_OPUS_MODEL=...            # Control opus alias

# Disable non-essential traffic
export CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=true

# Override shell detection
export CLAUDE_CODE_SHELL=/bin/zsh

# Bash timeout
export BASH_DEFAULT_TIMEOUT_MS=120000

# Demo mode - hide email/org from UI (useful for streaming/recording)
export IS_DEMO=true

# Disable background tasks (auto-backgrounding and Ctrl+B)
export CLAUDE_CODE_DISABLE_BACKGROUND_TASKS=true

# Override temp directory for internal temp files
export CLAUDE_CODE_TMPDIR=/custom/tmp/path

# Override file read token limit
export CLAUDE_CODE_FILE_READ_MAX_OUTPUT_TOKENS=50000

# Force plugin auto-update when main auto-updater is disabled
export FORCE_AUTOUPDATE_PLUGINS=true
```

## CLI Flags

```bash
# Override agent for session
claude --agent my-custom-agent

# Disable slash commands
claude --disable-slash-commands

# Set max budget
claude --max-budget-usd 10.00

# Limit agentic turns
claude -p --max-turns 3 "Fix lint errors"

# Custom session ID
claude --session-id my-session --resume

# Fork a session
claude --resume abc123 --fork-session --session-id new-session

# Resume sessions linked to a GitHub PR
claude --from-pr 123

# Define custom subagents via JSON
claude --agents '{"analyzer": {"prompt": "You analyze code", "tools": ["Read", "Grep"]}}'

# Output format for scripting
claude -p "Analyze this" --output-format json

# Get validated JSON output matching a schema
claude -p --json-schema '{"type":"object","properties":{"issues":{"type":"array"}}}' "Find bugs"

# Restrict which built-in tools Claude can use
claude --tools "Read,Glob,Grep"

# Automatic model fallback when default is overloaded
claude -p --fallback-model sonnet "Review this code"

# Customize system prompt (replace or append)
claude --system-prompt "You are a Python expert"
claude --append-system-prompt "Always use TypeScript"
claude -p --system-prompt-file ./custom-prompt.txt "Review this"
claude -p --append-system-prompt-file ./rules.txt "Review this"

# Load MCP servers from a config file
claude --mcp-config ./mcp.json

# Start in isolated git worktree
claude --worktree feature-auth

# Create a web session on claude.ai
claude --remote "Fix the login bug"

# Resume a web session locally
claude --teleport
```

## Error Handling

```bash
#!/bin/bash

result=$(claude -p "Fix the build" --output-format json 2>&1)
exit_code=$?

if [ $exit_code -ne 0 ]; then
  echo "Claude failed: $result"
  exit 1
fi

if echo "$result" | jq -e '.success == false' > /dev/null; then
  echo "Task failed: $(echo $result | jq -r '.error')"
  exit 1
fi
```

## Rate Limiting

For batch operations, add delays:

```bash
for file in *.py; do
  claude -p "Analyze $file"
  sleep 2  # Avoid rate limits
done
```

## Security Considerations

1. **Never expose API keys** in logs or outputs
2. **Use containers** for `--dangerously-skip-permissions`
3. **Validate outputs** before applying changes automatically
4. **Limit tools** to only what's needed

## Sources

- [Claude Code Automation Documentation](https://docs.anthropic.com/en/docs/claude-code)
- [GitHub - Claude Code Devcontainer](https://github.com/anthropics/claude-code/tree/main/.devcontainer)
