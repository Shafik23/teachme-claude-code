# Skills

Skills extend what Claude can do. Create a `SKILL.md` file with instructions, and Claude adds it to its toolkit. Claude uses skills when relevant, or you can invoke one directly with `/skill-name`.

> **Custom slash commands have been merged into skills.** A file at `.claude/commands/review.md` and a skill at `.claude/skills/review/SKILL.md` both create `/review` and work the same way. Your existing `.claude/commands/` files keep working. Skills add optional features: a directory for supporting files, frontmatter to control invocation, and the ability for Claude to load them automatically when relevant.

Skills follow the [Agent Skills](https://agentskills.io) open standard, which works across multiple AI tools.

## Bundled Skills

Bundled skills ship with Claude Code and are available in every session. Unlike built-in commands which execute fixed logic, bundled skills are prompt-based: they give Claude a detailed playbook and let it orchestrate work using its tools (spawning parallel agents, reading files, adapting to your codebase).

| Skill | Description |
|-------|-------------|
| `/simplify` | Reviews recently changed files for code reuse, quality, and efficiency, then fixes issues. Spawns three review agents in parallel (code reuse, code quality, efficiency). Pass optional text to focus: `/simplify focus on memory efficiency` |
| `/batch <instruction>` | Orchestrates large-scale changes across a codebase in parallel. Researches the codebase, decomposes work into 5-30 independent units, and spawns one background agent per unit in isolated git worktrees. Each agent implements, tests, and opens a PR. Requires a git repository |
| `/debug [description]` | Troubleshoots your current Claude Code session by reading the session debug log. Optionally describe the issue to focus the analysis |

Claude Code also includes a bundled developer platform skill that activates automatically when your code imports the Anthropic SDK.

## How Skills Work

1. **Discovery**: Claude loads only the name and description of available Skills at startup (descriptions are always in context)
2. **Activation**: When your request semantically matches a Skill's description, Claude loads the full skill content
3. **Execution**: Claude follows the Skill's instructions, loading referenced files as needed
4. **Direct invocation**: You can also invoke any user-invocable skill with `/skill-name`

**Hot-Reload**: Skills created or modified in `~/.claude/skills` or `.claude/skills` are immediately available without restarting your session.

## Creating a Skill

### File Location

```
~/.claude/skills/           # Personal Skills (all projects)
  skill-name/
    SKILL.md                # Required

.claude/skills/             # Project Skills (this repo only)
  skill-name/
    SKILL.md                # Required
```

### SKILL.md Format

```yaml
---
name: explaining-code
description: Explains code with visual diagrams and analogies. Use when explaining how code works or when the user asks "how does this work?"
---

# Explaining Code

When explaining code, always:

1. **Start with an analogy** - Compare to something from everyday life
2. **Draw a diagram** - Use ASCII art to show flow or relationships
3. **Walk through step-by-step** - Explain what happens in order
4. **Highlight gotchas** - Note common mistakes or misconceptions
```

### Frontmatter Reference

All fields are optional. Only `description` is recommended so Claude knows when to use the skill.

| Field | Required | Description |
|-------|----------|-------------|
| `name` | No | Display name for the skill. If omitted, uses the directory name. Lowercase, hyphens, max 64 chars |
| `description` | Recommended | What the skill does and when to use it. Claude uses this to decide when to apply the skill |
| `argument-hint` | No | Hint shown during autocomplete (e.g., `[issue-number]`) |
| `disable-model-invocation` | No | Set to `true` to prevent Claude from auto-loading. Users must invoke manually with `/name` |
| `user-invocable` | No | Set to `false` to hide from the `/` menu. Use for background knowledge only |
| `allowed-tools` | No | Tools Claude can use without asking (supports YAML-style lists) |
| `model` | No | Override the conversation model |
| `context` | No | Set to `fork` to run in a forked subagent context |
| `agent` | No | Which subagent type to use when `context: fork` is set (e.g., `Explore`, `Plan`) |
| `hooks` | No | Hooks scoped to this skill's lifecycle |

**YAML-style allowed-tools:**
```yaml
---
name: my-skill
description: Example with YAML tools list
allowed-tools:
  - Read
  - Grep
  - Bash(npm:*)
---
```

### String Substitutions

Skills support dynamic values:

| Variable | Description |
|----------|-------------|
| `$ARGUMENTS` | All arguments passed when invoking the skill |
| `$ARGUMENTS[N]` | Access a specific argument by 0-based index |
| `$N` | Shorthand for `$ARGUMENTS[N]` (e.g., `$0`, `$1`) |
| `${CLAUDE_SESSION_ID}` | The current session ID |

### Dynamic Context Injection

The `` !`command` `` syntax runs shell commands before the skill content is sent to Claude:

```yaml
---
name: pr-summary
description: Summarize changes in a pull request
context: fork
agent: Explore
---

## Pull request context
- PR diff: !`gh pr diff`
- Changed files: !`gh pr diff --name-only`

Summarize this pull request...
```

### Controlling Invocation

| Frontmatter | You can invoke | Claude can invoke |
|:--|:--|:--|
| (default) | Yes | Yes |
| `disable-model-invocation: true` | Yes | No |
| `user-invocable: false` | No | Yes |

## Example: Code Review Skill

```yaml
---
name: code-review
description: Review code for quality, security, and best practices. Use when reviewing PRs, checking code quality, or when the user asks for a code review.
allowed-tools: Read, Grep, Glob
---

# Code Review

When reviewing code, check for:

## Security
- Input validation
- SQL injection / XSS vulnerabilities
- Hardcoded secrets
- Authentication/authorization issues

## Quality
- Error handling
- Edge cases
- Code duplication
- Naming clarity

## Performance
- N+1 queries
- Unnecessary computations
- Memory leaks

## Output Format

Provide feedback as:
1. **Critical** - Must fix before merge
2. **Important** - Should fix
3. **Suggestions** - Nice to have

Include file:line references for each issue.
```

## Multi-File Skills (Progressive Disclosure)

For complex Skills, split content across files. Keep SKILL.md under 500 lines and reference supporting files:

```
pdf-processor/
├── SKILL.md              # Overview (Claude loads this first)
├── FORMS.md              # Form field documentation
├── REFERENCE.md          # Detailed API docs
└── scripts/
    └── fill_form.py      # Utility script
```

In SKILL.md, reference the files:

```markdown
---
name: pdf-processor
description: Process PDF files - extract text, fill forms, merge documents. Use when working with PDFs.
---

# PDF Processor

For form field mappings, see @FORMS.md
For API details, see @REFERENCE.md

## Quick Start
...
```

Claude loads referenced files only when needed for the task.

## Tool Restrictions

Limit what Claude can do when a Skill is active:

```yaml
---
name: safe-reader
description: Read and analyze files without modifications
allowed-tools: Read, Grep, Glob
---

# Safe File Reader

This Skill provides read-only access to analyze code...
```

## Skill Priority

When multiple Skills have the same name, priority determines which is used:

1. **Enterprise** (highest)
2. **Personal** (`~/.claude/skills/`)
3. **Project** (`.claude/skills/`)
4. **Plugin** (lowest)

## Writing Good Descriptions

The description is critical — it determines when Claude activates the Skill.

### Bad Description

```yaml
description: Helps with documents
```

Too vague. Won't match specific requests.

### Good Description

```yaml
description: Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.
```

Specific triggers: "PDF", "forms", "extract", "merge documents"

## Managing Skills

```bash
# View available Skills in session
/agents

# List Skill files
ls ~/.claude/skills/
ls .claude/skills/
```

## Troubleshooting

### Skill Not Triggering

- Make description more specific with trigger words
- Check that SKILL.md is in correct location
- Verify YAML frontmatter syntax (spaces, not tabs)

### Skill Not Loading

```bash
# Debug mode shows loading errors
claude --debug
```

### Multiple Skills Conflict

Make descriptions distinct:

```yaml
# Instead of two "data analysis" skills:
description: Analyze Excel spreadsheets and CRM data exports...
description: Analyze application logs and performance metrics...
```

## Complete Example: Test Writer

```yaml
---
name: test-writer
description: Write comprehensive unit tests. Use when creating tests, improving test coverage, or when the user asks to "write tests" or "add tests".
allowed-tools: Read, Write, Glob, Bash(npm test:*)
---

# Test Writer

## Framework Detection

First, detect the test framework:
- Look for jest.config.* → Jest
- Look for vitest.config.* → Vitest
- Look for *.spec.ts with @angular → Angular Testing
- Look for pytest.ini or conftest.py → Pytest

## Test Structure

For each function/method, write tests covering:

1. **Happy path** - Normal expected input
2. **Edge cases** - Empty, null, boundary values
3. **Error cases** - Invalid input, exceptions

## Naming Convention

Follow existing patterns in the codebase. If none exist:
- Jest/Vitest: `describe('functionName', () => { it('should...') })`
- Pytest: `def test_function_name_condition():`

## After Writing

Run the tests to verify they pass:
```bash
npm test -- --testPathPattern="new-test-file"
```
```

## Skills vs Legacy Slash Commands

> Slash commands have been merged into skills. Both `.claude/commands/` and `.claude/skills/` now create the same result. Skills are recommended for new work since they support directories with supporting files.

| Aspect | Skills | Legacy Commands (`.claude/commands/`) |
|--------|--------|----------------|
| Location | `.claude/skills/<name>/SKILL.md` | `.claude/commands/<name>.md` |
| Supporting files | Directory with templates, scripts, etc. | Single markdown file only |
| Invocation control | `disable-model-invocation`, `user-invocable` | `disable-model-invocation` only |
| Dynamic context | `` !`command` `` syntax | `` !`command` `` syntax |

## Ready-to-Use Examples

See the [examples/skills/](../examples/skills/) directory for complete, working skills:

| Skill | Description |
|-------|-------------|
| [code-explainer](../examples/skills/code-explainer/) | Explains code with diagrams and analogies |
| [test-writer](../examples/skills/test-writer/) | Writes comprehensive unit tests |
| [git-assistant](../examples/skills/git-assistant/) | Helps with git operations |
| [api-designer](../examples/skills/api-designer/) | Designs RESTful APIs |

Install one:
```bash
cp -r examples/skills/code-explainer ~/.claude/skills/
```
