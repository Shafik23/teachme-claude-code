# Subagents

Subagents are specialized AI agents that Claude can delegate tasks to. Each subagent operates with its own context and can have specific Skills and tool access.

## Built-in Subagents

Claude Code includes several built-in subagents:

| Agent | Purpose | When Used |
|-------|---------|-----------|
| **Explore** | Codebase exploration | Finding files, understanding structure |
| **Plan** | Architecture planning | Designing implementation approaches |
| **Verify** | Verification tasks | Checking work, validating changes |

## How Subagents Work

1. Claude recognizes a task that matches a subagent's specialty
2. Claude asks permission to delegate
3. The subagent runs with its own context
4. Results return to the main conversation

## Creating Custom Subagents

### File Location

```
~/.claude/agents/           # Personal (all projects)
  agent-name/
    AGENT.md                # Required

.claude/agents/             # Project (this repo)
  agent-name/
    AGENT.md                # Required
```

### AGENT.md Format

```yaml
---
name: code-reviewer
description: Review code for quality, security, and best practices
skills: code-review, security-check
allowed-tools: Read, Grep, Glob
---

# Code Reviewer Agent

You are a code review specialist. When reviewing code:

1. Check for security vulnerabilities
2. Identify performance issues
3. Suggest improvements
4. Note any style inconsistencies

Provide feedback with file:line references.
```

### Frontmatter Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Unique identifier |
| `description` | Yes | What the agent does |
| `skills` | No | Skills this agent can use |
| `allowed-tools` | No | Tools available to this agent |
| `model` | No | Override model for this agent |

## Example Subagents

### Documentation Writer

```yaml
---
name: doc-writer
description: Generate and update documentation
allowed-tools: Read, Write, Glob
---

# Documentation Writer

Generate clear, comprehensive documentation:

## For Functions/Methods
- Purpose
- Parameters with types
- Return value
- Usage example
- Edge cases

## For Modules/Classes
- Overview
- Public API
- Dependencies
- Usage patterns

## Style
- Use active voice
- Include code examples
- Keep paragraphs short
```

### Test Generator

```yaml
---
name: test-generator
description: Generate comprehensive test suites
skills: test-writer
allowed-tools: Read, Write, Glob, Bash(npm test:*)
---

# Test Generator

Generate thorough tests:

1. Identify all functions/methods to test
2. For each, create tests for:
   - Happy path
   - Edge cases (null, empty, boundary)
   - Error conditions
3. Use existing test patterns in the codebase
4. Run tests to verify they pass
```

### Security Auditor

```yaml
---
name: security-auditor
description: Audit code for security vulnerabilities
allowed-tools: Read, Grep, Glob
---

# Security Auditor

Perform security analysis:

## Check For
- SQL injection
- XSS vulnerabilities
- Command injection
- Hardcoded secrets
- Insecure dependencies
- Authentication issues
- Authorization bypasses
- Data exposure

## Output Format
For each finding:
- **Severity**: Critical/High/Medium/Low
- **Location**: file:line
- **Issue**: Description
- **Fix**: Recommended remediation
```

### Refactoring Assistant

```yaml
---
name: refactorer
description: Safely refactor code while preserving behavior
skills: code-review
allowed-tools: Read, Edit, Glob, Bash(npm test:*)
---

# Refactoring Assistant

Refactor code safely:

## Process
1. Understand current behavior
2. Identify test coverage
3. Plan changes
4. Make incremental edits
5. Run tests after each change
6. Verify behavior preserved

## Principles
- Small, focused changes
- One refactoring at a time
- Tests must pass at each step
- Preserve public interfaces
```

## Using Subagents

### Automatic Delegation

Claude automatically suggests using subagents when appropriate:

```
> Review the authentication module for security issues

Claude: I'd like to use the security-auditor agent for this task.
        It specializes in security analysis. Proceed?
```

### Explicit Invocation

```
/agents
```

Lists available agents and lets you invoke one directly.

### In Prompts

```
> Use the doc-writer agent to document the API module
```

## Subagent Skills

Subagents can leverage Skills for specialized knowledge:

```yaml
---
name: api-developer
description: Build and maintain REST APIs
skills: api-design, openapi-spec, error-handling
---
```

The agent automatically has access to the named Skills.

## Tool Restrictions

Limit what a subagent can do:

```yaml
---
name: reader-only
description: Analyze code without making changes
allowed-tools: Read, Grep, Glob
---

# Read-Only Analyzer

Analyze code and provide insights without modifying any files.
```

## Subagent Priority

Like Skills, subagents have priority:

1. **Enterprise** (highest)
2. **Personal** (`~/.claude/agents/`)
3. **Project** (`.claude/agents/`)
4. **Plugin** (lowest)

## Subagents in Plugins

```
my-plugin/
├── agents/
│   ├── reviewer/
│   │   └── AGENT.md
│   └── deployer/
│       └── AGENT.md
```

Plugin agents are namespaced: `my-plugin:reviewer`

## Best Practices

### 1. Single Responsibility

Each agent should do one thing well:

```yaml
# Good - focused
description: Review Python code for PEP 8 compliance

# Bad - too broad
description: Help with Python development
```

### 2. Clear Instructions

Be specific about how the agent should work:

```yaml
---
name: migrator
description: Handle database migrations
---

# Database Migrator

## Before Any Migration
1. Backup current schema
2. Check for pending changes
3. Verify rollback exists

## Migration Process
1. Run in transaction
2. Verify data integrity
3. Update schema version

## On Failure
1. Rollback immediately
2. Report what failed
3. Do not retry automatically
```

### 3. Appropriate Tool Access

Only grant tools the agent needs:

```yaml
# Read-only analysis
allowed-tools: Read, Grep, Glob

# Can run tests
allowed-tools: Read, Grep, Glob, Bash(npm test:*)

# Full access (use sparingly)
# (omit allowed-tools for full access)
```

### 4. Leverage Skills

Combine with Skills for deep expertise:

```yaml
---
name: frontend-expert
description: Frontend development specialist
skills: react-patterns, css-architecture, accessibility
---
```

## Debugging Subagents

### Check Available Agents

```
/agents
```

### Debug Loading

```bash
claude --debug
```

### Verify File Location

```bash
ls ~/.claude/agents/
ls .claude/agents/
```

## Example: Full Agent Suite

A project might have:

```
.claude/agents/
├── code-reviewer/
│   └── AGENT.md      # PR reviews
├── test-writer/
│   └── AGENT.md      # Test generation
├── doc-updater/
│   └── AGENT.md      # Documentation
└── deploy-checker/
    └── AGENT.md      # Pre-deploy verification
```

This gives Claude specialized helpers for common tasks while keeping the main conversation focused.

## Ready-to-Use Examples

See [examples/agents/](../examples/agents/) for complete, working subagents:

| Agent | Description |
|-------|-------------|
| [code-reviewer](../examples/agents/code-reviewer/) | Thorough code review with severity levels |
| [documentation-writer](../examples/agents/documentation-writer/) | README, API docs, code comments |
| [bug-hunter](../examples/agents/bug-hunter/) | Systematic debugging and investigation |

Install one:
```bash
cp -r examples/agents/code-reviewer ~/.claude/agents/
```
