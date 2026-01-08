# Configuration

## Configuration Files

Claude Code uses a hierarchy of settings files:

| Scope | Location | Purpose |
|-------|----------|---------|
| User | `~/.claude/settings.json` | Personal global settings |
| Project (shared) | `.claude/settings.json` | Team settings (commit to git) |
| Project (local) | `.claude/settings.local.json` | Personal project settings |

Higher scopes override lower ones.

## Key Settings

### Permissions

Control what Claude can do without asking:

```json
{
  "permissions": {
    "allow": [
      "Read",
      "Glob",
      "Grep",
      "Bash(npm run:*)",
      "Bash(git diff:*)",
      "Bash(git status)"
    ],
    "deny": [
      "Read(.env)",
      "Read(secrets/**)",
      "Bash(rm -rf:*)"
    ]
  }
}
```

### Permission Patterns

```
Tool                    - Allow all uses of tool
Tool(pattern:*)         - Allow with prefix match
Tool(*:suffix)          - Allow with suffix match
Tool(exact-match)       - Allow exact match only
```

Examples:
```json
{
  "allow": [
    "Bash(npm run:*)",        // npm run test, npm run build, etc.
    "Bash(npm *)",            // npm install, npm update, etc. (wildcard patterns)
    "Bash(git:*)",            // All git commands
    "Edit(src/**)",           // Edit files in src/
    "Read(*.md)"              // Read markdown files
  ]
}
```

### Environment Variables

Set environment variables for Claude sessions:

```json
{
  "env": {
    "NODE_ENV": "development",
    "DEBUG": "true",
    "API_URL": "http://localhost:3000"
  }
}
```

### Model Selection

Override the default model:

```json
{
  "model": "claude-opus-4-5-20251101"
}
```

### Extended Thinking

Enable extended thinking by default:

```json
{
  "alwaysThinkingEnabled": true
}
```

### Output Style

Set default output verbosity:

```json
{
  "outputStyle": "Explanatory"
}
```

Options: `"Concise"`, `"Normal"`, `"Explanatory"`

### Response Language

Configure Claude's response language:

```json
{
  "language": "japanese"
}
```

### Respect Gitignore

Control whether the @-mention file picker respects `.gitignore`:

```json
{
  "respectGitignore": true
}
```

### Sandbox Mode

Enable sandboxed bash execution:

```json
{
  "sandbox": {
    "enabled": true,
    "autoAllowBashIfSandboxed": true
  }
}
```

## CLAUDE.md Memory Files

Claude reads `CLAUDE.md` files to understand your project:

### Project Memory

Create `CLAUDE.md` in your project root:

```markdown
# Project: My Awesome App

## Tech Stack
- React 18 with TypeScript
- Express.js backend
- PostgreSQL database

## Conventions
- Use functional components with hooks
- Follow Airbnb style guide
- Write tests for all new features

## Important Commands
- `npm run dev` - Start development server
- `npm test` - Run test suite
- `npm run lint` - Check code style

## Architecture Notes
- API routes are in `src/api/`
- Components are in `src/components/`
- Database models are in `src/models/`
```

### User Memory

Create `~/.claude/CLAUDE.md` for global preferences:

```markdown
# My Preferences

## Coding Style
- I prefer explicit types over inference
- Use early returns for cleaner code
- Keep functions under 50 lines

## Communication
- Be concise in explanations
- Show code examples
- Explain trade-offs
```

### Import Other Files

CLAUDE.md files can import other files:

```markdown
# Project Memory

## Additional Context
@path/to/coding-standards.md
@path/to/api-guidelines.md
```

### Rules Directory

For project-specific rules, create files in `.claude/rules/`:

```
.claude/rules/
  security.md       # Security guidelines
  style.md          # Code style rules
  testing.md        # Testing requirements
  api-patterns.md   # API design patterns
```

Files in this directory are automatically loaded and provide structured guidance to Claude. Each file can focus on a specific aspect of your project's requirements.

**Best Practices for Rules:**
- Keep each rule file focused on one topic
- Use clear, actionable language
- Include examples where helpful
- Update rules as project conventions evolve

### Dynamic Memory Updates

During a session, ask Claude to update your CLAUDE.md:

```
> Always run prettier after editing TypeScript files - add this to CLAUDE.md
```

Or use the `/memory` command to edit memory files directly.

## Default Permission Modes

Set how Claude handles permissions:

```json
{
  "permissions": {
    "defaultMode": "normal"
  }
}
```

Options:
- `"normal"` - Ask for each action
- `"plan"` - Analyze only, don't modify
- `"acceptEdits"` - Auto-approve file edits

## Additional Directories

Allow Claude to access directories outside the project:

```json
{
  "permissions": {
    "additionalDirectories": [
      "../shared-lib",
      "~/templates"
    ]
  }
}
```

## Attribution

Customize commit and PR attribution:

```json
{
  "attribution": {
    "commit": "Co-Authored-By: Claude <noreply@anthropic.com>",
    "pr": "Generated with Claude Code"
  }
}
```

## MCP Tool Permissions

Use wildcards for MCP tool permissions:

```json
{
  "permissions": {
    "allow": [
      "mcp__github",
      "mcp__github__*",
      "mcp__server__*",
      "mcp__linear__get_issue"
    ]
  }
}
```

The `mcp__server__*` wildcard syntax allows or denies all tools from a specific MCP server.

## Complete Example

```json
{
  "permissions": {
    "allow": [
      "Read",
      "Glob",
      "Grep",
      "Bash(npm:*)",
      "Bash(git:*)",
      "Bash(docker compose:*)",
      "mcp__github__*"
    ],
    "deny": [
      "Read(.env*)",
      "Read(**/*.key)",
      "Bash(rm -rf:*)"
    ],
    "additionalDirectories": ["../shared"],
    "defaultMode": "normal"
  },
  "env": {
    "NODE_ENV": "development"
  },
  "model": "claude-sonnet-4-20250514",
  "alwaysThinkingEnabled": false,
  "outputStyle": "Normal",
  "sandbox": {
    "enabled": false
  }
}
```
