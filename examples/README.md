# Examples

This directory contains ready-to-use examples of Claude Code extensibility features.

## Skills

Skills are model-invoked capabilities that Claude automatically uses when your request matches the skill's description.

| Skill | Description | Use When |
|-------|-------------|----------|
| [code-explainer](./skills/code-explainer/) | Explains code with diagrams and analogies | "How does this work?", "Explain this code" |
| [test-writer](./skills/test-writer/) | Writes comprehensive unit tests | "Write tests", "Add test coverage" |
| [git-assistant](./skills/git-assistant/) | Helps with git operations | Commits, branches, merges, conflicts |
| [api-designer](./skills/api-designer/) | Designs RESTful APIs | "Design an API", "Create endpoints" |

### Installing a Skill

```bash
# Copy to your personal skills (available in all projects)
cp -r examples/skills/code-explainer ~/.claude/skills/

# Or copy to project skills (shared with team)
cp -r examples/skills/test-writer .claude/skills/
```

---

## Plugins

Plugins package multiple features (commands, skills, hooks) into a distributable unit.

### [deploy-toolkit](./plugins/deploy-toolkit/)

A complete deployment automation plugin with:

- **Commands:**
  - `/deploy-toolkit:deploy <env>` - Deploy to environment
  - `/deploy-toolkit:rollback <env>` - Rollback deployment
  - `/deploy-toolkit:env-check <env>` - Verify environment config

- **Skills:**
  - `pre-deploy-check` - Automated deployment readiness verification

- **Hooks:**
  - Deployment audit logging

### Installing a Plugin

```bash
# Test locally
claude --plugin-dir ./examples/plugins/deploy-toolkit

# Install permanently
claude plugin add ./examples/plugins/deploy-toolkit
```

---

## Subagents

Subagents are specialized AI agents that Claude can delegate tasks to.

| Agent | Description | Use When |
|-------|-------------|----------|
| [code-reviewer](./agents/code-reviewer/) | Thorough code review specialist | PR reviews, code quality checks |
| [documentation-writer](./agents/documentation-writer/) | Technical documentation specialist | Creating/updating docs |
| [bug-hunter](./agents/bug-hunter/) | Debugging and investigation specialist | Investigating errors, debugging |

### Installing a Subagent

```bash
# Copy to your personal agents
cp -r examples/agents/code-reviewer ~/.claude/agents/

# Or copy to project agents
cp -r examples/agents/bug-hunter .claude/agents/
```

---

## Using These Examples

### 1. Copy and Customize

These examples are starting points. Copy them and customize:

```bash
# Copy a skill
cp -r examples/skills/test-writer ~/.claude/skills/my-test-writer

# Edit to match your needs
$EDITOR ~/.claude/skills/my-test-writer/SKILL.md
```

### 2. Test Before Installing

Use `--plugin-dir` to test plugins without installing:

```bash
claude --plugin-dir ./examples/plugins/deploy-toolkit
```

### 3. Combine Features

Create a plugin that includes multiple skills and agents:

```
my-team-toolkit/
├── .claude-plugin/
│   └── plugin.json
├── skills/
│   ├── code-explainer/
│   └── test-writer/
├── agents/
│   ├── code-reviewer/
│   └── bug-hunter/
└── commands/
    └── team-review.md
```

---

## Workflow Examples

The original workflow examples are also available:

| Example | Description |
|---------|-------------|
| [01-debug-workflow.md](./01-debug-workflow.md) | Debugging with Claude |
| [02-feature-workflow.md](./02-feature-workflow.md) | Building new features |
| [03-refactoring-workflow.md](./03-refactoring-workflow.md) | Safe refactoring |
| [04-code-review-workflow.md](./04-code-review-workflow.md) | PR review process |
| [05-cli-automation.md](./05-cli-automation.md) | Scripts and CI/CD |
