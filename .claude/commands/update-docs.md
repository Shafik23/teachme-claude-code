---
description: Search the web for current Claude Code features, update all documentation, and push to GitHub
allowed-tools: WebSearch, WebFetch, Read, Edit, Write, Glob, Grep, Bash(git:*), Bash(gh:*)
---

# Documentation Auto-Updater

You are updating the Claude Code educational documentation in this repository. Follow these steps methodically.

**CRITICAL: You MUST use ONLY the built-in `WebSearch` and `WebFetch` tools for web searches and fetching. DO NOT use any MCP tools like firecrawl, mcp__firecrawl-mcp__*, or any other MCP-based web scraping tools. Use ONLY the native Claude Code WebSearch and WebFetch tools.**

## Step 1: Search for Current Claude Code Information

Use the built-in `WebSearch` tool (NOT firecrawl or any MCP tools) to search for the latest Claude Code features and documentation. Run these searches:

1. Search: "Claude Code CLI features 2025"
2. Search: "Claude Code slash commands reference"
3. Search: "Claude Code MCP servers integrations"
4. Search: "Claude Code hooks PreToolUse PostToolUse"
5. Search: "Claude Code Agent SDK Python TypeScript"
6. Search: "Claude Code changelog latest updates"
7. Search: "Claude Code configuration settings"

## Step 2: Fetch Official Documentation

Use the built-in `WebFetch` tool (NOT firecrawl or any MCP tools) to fetch content from these official sources:

1. https://code.claude.com/docs/en/overview - Main overview
2. https://code.claude.com/docs/en/slash-commands - Slash commands reference
3. https://code.claude.com/docs/en/hooks - Hooks documentation
4. https://code.claude.com/docs/en/mcp - MCP documentation
5. https://github.com/anthropics/claude-code - GitHub README

## Step 3: Read Current Documentation

Read all documentation files in this repository to understand what's currently documented:

```
docs/01-getting-started.md
docs/02-core-features.md
docs/03-slash-commands.md
docs/04-configuration.md
docs/05-tips-and-tricks.md
docs/06-mcp-servers.md
docs/07-hooks.md
docs/08-ide-integrations.md
docs/09-skills.md
docs/10-plugins.md
docs/11-subagents.md
docs/12-agent-sdk.md
docs/13-best-practices.md
docs/14-checkpoints-and-rewind.md
docs/15-headless-and-automation.md
docs/16-background-tasks.md
```

## Step 4: Compare and Identify Updates

Compare the fetched information against current documentation. Look for:

### New Features
- New slash commands not documented
- New hooks or hook events
- New MCP servers or integrations
- New configuration options
- New CLI flags or arguments
- New SDK capabilities

### Changed Features
- Updated command syntax
- Changed default behaviors
- Modified configuration schemas
- Updated hook signatures

### Removed/Deprecated Features
- Commands that no longer exist
- Deprecated configuration options
- Removed integrations

## Step 5: Apply Updates

For each update identified, edit the appropriate documentation file:

### Mapping of Topics to Files

| Topic | File |
|-------|------|
| Installation, first run | docs/01-getting-started.md |
| File operations, git, testing, web | docs/02-core-features.md |
| Slash commands | docs/03-slash-commands.md |
| Settings, permissions, CLAUDE.md | docs/04-configuration.md |
| Keyboard shortcuts, vim mode | docs/05-tips-and-tricks.md |
| MCP servers, integrations | docs/06-mcp-servers.md |
| Hooks system | docs/07-hooks.md |
| VS Code, JetBrains | docs/08-ide-integrations.md |
| Skills framework | docs/09-skills.md |
| Plugins system | docs/10-plugins.md |
| Subagents | docs/11-subagents.md |
| Agent SDK | docs/12-agent-sdk.md |
| Best practices | docs/13-best-practices.md |
| Checkpoints, rewind | docs/14-checkpoints-and-rewind.md |
| Headless mode, CI/CD | docs/15-headless-and-automation.md |
| Background tasks | docs/16-background-tasks.md |

### Update Guidelines

1. **Maintain existing style** - Match the Markdown formatting and table styles already in use
2. **Be precise** - Only update what has actually changed
3. **Preserve structure** - Don't reorganize sections unless necessary
4. **Add sources** - Include official documentation links where helpful
5. **Keep practical** - Ensure examples are copy-pasteable

## Step 6: Commit and Push to GitHub

After making updates, commit and push the changes:

1. **Check what changed**:
   ```bash
   git status
   git diff
   ```

2. **Stage all documentation changes**:
   ```bash
   git add docs/ examples/ README.md
   ```

3. **Create a descriptive commit**:
   ```bash
   git commit -m "docs: auto-update documentation with latest Claude Code features

   - Updated from official Anthropic documentation
   - Synced with current Claude Code capabilities

   🤖 Generated with [Claude Code](https://claude.com/claude-code)

   Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
   ```

4. **Push to GitHub**:
   ```bash
   git push
   ```

If there are no changes to commit, skip this step and note that documentation is already current.

## Step 7: Summary Report

After completing all steps, provide a summary:

```
## Documentation Update Summary

### Sources Checked
- [List URLs fetched]

### Updates Made
- [List specific changes by file]

### New Features Added
- [List new features documented]

### Deprecations Noted
- [List any deprecations found]

### No Changes Needed
- [List sections that were already current]

### Git Status
- Commit: [commit hash]
- Pushed to: [branch name]
```

## Important Notes

- Always verify information from official Anthropic sources before updating
- If information conflicts between sources, prefer docs.anthropic.com
- Do not remove documented features unless confirmed deprecated
- For uncertain changes, note them in the summary for manual review
- Only commit if actual changes were made to documentation
