# Skills

Skills are markdown-based files that teach Claude how to do something specific. Unlike slash commands that you invoke explicitly, Skills are **model-invoked** — Claude automatically uses them when your request matches the Skill's description.

## How Skills Work

1. **Discovery**: Claude loads only the name and description of available Skills at startup
2. **Activation**: When your request semantically matches a Skill's description, Claude asks permission to use it
3. **Execution**: Claude follows the Skill's instructions, loading referenced files as needed

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

### Required Frontmatter

| Field | Description | Constraints |
|-------|-------------|-------------|
| `name` | Unique identifier | Lowercase, hyphens, max 64 chars |
| `description` | What it does and when to use it | Max 1024 chars |

### Optional Frontmatter

| Field | Description | Example |
|-------|-------------|---------|
| `allowed-tools` | Tools Claude can use without asking | `Read, Grep, Bash(npm:*)` |
| `model` | Override the conversation model | `claude-sonnet-4-20250514` |

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

## Skills vs Slash Commands

| Aspect | Skills | Slash Commands |
|--------|--------|----------------|
| Invocation | Automatic (Claude decides) | Explicit (`/command`) |
| Discovery | Semantic matching | User types `/` |
| Best for | Complex workflows, domain expertise | Quick actions, frequent tasks |
| Context | Can load multiple files | Single markdown file |

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
