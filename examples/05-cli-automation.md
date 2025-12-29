# Example: CLI Automation

This example shows how to use Claude Code in scripts and automation workflows.

## Basic Patterns

### One-Shot Commands

```bash
# Generate code
claude -p "Write a Python script to convert CSV to JSON"

# Explain code
claude -p "Explain what this function does" < complex_function.py

# Quick questions
claude -p "What's the difference between let and const in JavaScript?"
```

### Pipe Patterns

```bash
# Analyze logs
tail -100 /var/log/app.log | claude -p "Summarize any errors"

# Generate commit messages
git diff --staged | claude -p "Write a concise commit message"

# Explain diffs
git diff HEAD~1 | claude -p "What changed in the last commit?"

# Review PRs
gh pr diff 123 | claude -p "Review this PR for issues"
```

## Git Automation

### Smart Commit Messages

```bash
#!/bin/bash
# smart-commit.sh

DIFF=$(git diff --staged)
if [ -z "$DIFF" ]; then
    echo "No staged changes"
    exit 1
fi

MESSAGE=$(echo "$DIFF" | claude -p "Write a commit message following conventional commits format. Be concise.")

echo "Proposed commit message:"
echo "$MESSAGE"
echo ""
read -p "Use this message? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    git commit -m "$MESSAGE"
fi
```

### PR Description Generator

```bash
#!/bin/bash
# pr-description.sh

BASE=${1:-main}
BRANCH=$(git branch --show-current)

COMMITS=$(git log $BASE..$BRANCH --oneline)
DIFF=$(git diff $BASE..$BRANCH --stat)

claude -p "Generate a PR description with:
- Summary of changes
- List of commits
- Testing notes

Commits:
$COMMITS

Files changed:
$DIFF"
```

## Log Analysis

### Error Monitoring

```bash
#!/bin/bash
# monitor-errors.sh

tail -f /var/log/app.log | while read line; do
    if echo "$line" | grep -q "ERROR"; then
        echo "$line" | claude -p "Analyze this error and suggest a fix" >> error_analysis.log
    fi
done
```

### Daily Log Summary

```bash
#!/bin/bash
# daily-summary.sh

LOG_FILE="/var/log/app.log"
TODAY=$(date +%Y-%m-%d)

grep "$TODAY" "$LOG_FILE" | claude -p "Summarize today's logs:
- Total requests
- Error rate
- Slowest endpoints
- Notable events"
```

## Code Generation

### Generate Tests

```bash
#!/bin/bash
# generate-tests.sh

FILE=$1
claude -p "Write unit tests for this file using Jest" < "$FILE" > "${FILE%.ts}.test.ts"
```

### Generate Documentation

```bash
#!/bin/bash
# generate-docs.sh

for file in src/**/*.ts; do
    claude -p "Add JSDoc comments to all exported functions" < "$file" > "$file.tmp"
    mv "$file.tmp" "$file"
done
```

## CI/CD Integration

### GitHub Actions Example

```yaml
# .github/workflows/claude-review.yml
name: Claude Code Review

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Install Claude Code
        run: npm install -g @anthropic-ai/claude-code

      - name: Get PR diff
        run: |
          git diff origin/${{ github.base_ref }}...HEAD > pr.diff

      - name: Run Claude Review
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          cat pr.diff | claude -p "Review for bugs and security issues. Output as GitHub review comments JSON." > review.json

      - name: Post Review Comments
        uses: actions/github-script@v7
        with:
          script: |
            const review = require('./review.json');
            // Post comments to PR...
```

## Database Operations

### Query Generator

```bash
#!/bin/bash
# query.sh

SCHEMA=$(cat schema.sql)
QUESTION=$1

claude -p "Given this schema:
$SCHEMA

Write a SQL query to: $QUESTION"
```

### Migration Generator

```bash
#!/bin/bash
# migrate.sh

CURRENT=$(cat migrations/latest.sql)
CHANGE=$1

claude -p "Current schema:
$CURRENT

Generate a migration to: $CHANGE

Include both UP and DOWN migrations."
```

## Batch Processing

### Process Multiple Files

```bash
#!/bin/bash
# batch-analyze.sh

for file in src/**/*.js; do
    echo "Analyzing $file..."
    claude -p "List potential bugs in this code" < "$file" > "reports/$(basename $file).md"
done
```

### Parallel Processing

```bash
#!/bin/bash
# parallel-analyze.sh

find src -name "*.ts" | parallel -j 4 'claude -p "Analyze for security issues" < {} > reports/{/.}.security.md'
```

## Cron Jobs

### Daily Code Health Check

```bash
# Add to crontab: 0 9 * * * /path/to/health-check.sh

#!/bin/bash
# health-check.sh

cd /path/to/project

REPORT=$(claude -p "Analyze this codebase for:
- TODO comments that need attention
- Outdated dependencies
- Code smell patterns
- Security concerns

Be concise.")

echo "$REPORT" | mail -s "Daily Code Health Report" team@example.com
```

## Pro Tips

1. **Use `-p` for non-interactive** - Single prompt, single response
2. **Pipe for context** - `cat file | claude -p "..."`
3. **Save outputs** - Redirect to files for records
4. **Combine with Unix tools** - grep, awk, sed work great
5. **Rate limit in loops** - Add `sleep` to avoid API limits
6. **Handle errors** - Check exit codes and empty responses
