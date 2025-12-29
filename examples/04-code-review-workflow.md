# Example: Code Review Workflow

This example shows how to use Claude Code for thorough code reviews.

## Scenario

Review a pull request before merging.

## Step 1: Get the Changes

```bash
# Fetch the PR branch
git fetch origin feature/user-auth
git diff main..origin/feature/user-auth > pr_changes.diff
```

Then in Claude:

```
> Review the changes in this PR for:
> - Security vulnerabilities
> - Performance issues
> - Code style consistency
> - Potential bugs
> - Test coverage
```

Or directly:

```bash
git diff main..origin/feature/user-auth | claude -p "Review this PR"
```

## Step 2: Deep Dive on Specific Files

```
> Look more closely at the authentication middleware changes
```

```
> Are there any SQL injection vulnerabilities in the new database queries?
```

## Step 3: Check Test Coverage

```
> What test coverage exists for the new code? What's missing?
```

Claude might respond:

"The new `AuthService` class has good unit test coverage, but I notice:

1. No tests for the password reset flow
2. Missing edge case: expired tokens
3. No integration tests for the middleware

Would you like me to write tests for these?"

## Step 4: Get Specific Feedback

```
> Generate review comments I can post on the PR
```

Claude provides formatted feedback:

**src/services/auth.js:45**
> Consider using `crypto.timingSafeEqual()` instead of `===` for token comparison to prevent timing attacks.

**src/middleware/authenticate.js:23**
> The error message "Invalid token" leaks information. Consider using a generic "Authentication failed" message.

**src/routes/user.js:67**
> Missing rate limiting on the password reset endpoint. This could be exploited for user enumeration.

## Step 5: Security-Focused Review

```
/security-review
```

Or manually:

```
> Do a security-focused review. Check for:
> - OWASP Top 10 vulnerabilities
> - Authentication/authorization issues
> - Input validation
> - Sensitive data exposure
```

## Step 6: Performance Review

```
> Are there any performance concerns with these changes?
> Look for N+1 queries, missing indexes, memory leaks.
```

## Step 7: Generate Summary

```
> Summarize your review findings with severity levels
```

Output:

```
## PR Review Summary: feature/user-auth

### Critical (Block Merge)
- [ ] Timing attack vulnerability in token comparison (auth.js:45)
- [ ] Missing rate limiting on password reset

### High Priority
- [ ] No test coverage for password reset flow
- [ ] Information leakage in error messages

### Medium Priority
- [ ] Consider adding request logging for audit trail
- [ ] Database queries could use connection pooling

### Low Priority / Suggestions
- [ ] JSDoc comments would improve maintainability
- [ ] Consider extracting magic numbers to constants

### Approved Pending
Fix critical items before merge. Other items can be follow-up PRs.
```

## Automated Review Setup

Create a custom command `.claude/commands/review-pr.md`:

```markdown
---
description: Review current PR changes
allowed-tools: Bash(git:*), Read, Grep, Glob
---

Review the changes between main and current branch:

!git diff main...HEAD --stat

Review these changes for:
1. Security vulnerabilities (OWASP Top 10)
2. Performance issues
3. Code style and consistency
4. Potential bugs
5. Test coverage gaps

Provide feedback formatted as GitHub review comments.
```

Then use: `/review-pr`

## Pro Tips

1. **Review incrementally** - Don't try to review 50 files at once
2. **Focus on high-risk areas** - Auth, payments, data access
3. **Ask for context** - "Why was this approach chosen over X?"
4. **Check the tests** - Good tests = confident merge
5. **Use security review** - `/security-review` for sensitive changes
