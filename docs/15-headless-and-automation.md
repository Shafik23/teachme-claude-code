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
export CLAUDE_CODE_MODEL=claude-sonnet-4  # Override model
export CLAUDE_CODE_MAX_TURNS=50          # Limit iterations
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
