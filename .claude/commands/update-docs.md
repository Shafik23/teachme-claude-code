---
description: Search the web for current Claude Code features, update all documentation, and push to GitHub
allowed-tools: WebSearch, WebFetch, Read, Edit, Write, Glob, Grep, Bash(git:*), Bash(gh:*)
---

# Documentation Auto-Updater

You are updating the Claude Code educational documentation in this repository. Follow these steps methodically.

**CRITICAL: You MUST use ONLY the built-in `WebSearch` and `WebFetch` tools for web searches and fetching. DO NOT use any MCP tools like firecrawl, mcp__firecrawl-mcp__*, or any other MCP-based web scraping tools. Use ONLY the native Claude Code WebSearch and WebFetch tools.**

**IMPORTANT: Only make changes if there are SIGNIFICANT updates from Anthropic's official documentation.** Do NOT make changes for:
- Minor wording differences that don't change meaning
- Features already documented (even if phrased differently)
- Information that is essentially the same but formatted differently
- Speculative features mentioned in blog posts but not in official docs

If after research you find the documentation is already up-to-date, simply report "Documentation is current - no updates needed" and skip the commit step. Avoid unnecessary commits.

## Step 1: Search for Current Claude Code Information

Use the built-in `WebSearch` tool (NOT firecrawl or any MCP tools) to search for the latest Claude Code features and documentation. Run these searches:

1. Search: "Claude Code CLI features" (add the current year to the query)
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

Use Glob to find all `docs/*.md` files, then read every file found. This ensures newly added documentation is always included without needing to update this list.

## Step 4: Compare and Identify Updates

Compare the fetched information against current documentation. **Be conservative** - only flag items that represent genuinely new or changed functionality, not minor variations.

### Criteria for Making Updates

**DO update for:**
- Entirely new slash commands not documented at all
- New hooks or hook events with new names/functionality
- New MCP server integrations not listed
- New CLI flags or arguments with new functionality
- Breaking changes to existing features
- Deprecated/removed features that are still documented

**DO NOT update for:**
- Features already covered (even if official docs phrase them differently)
- Minor additions to existing feature descriptions
- Third-party blog posts or tutorials (only use official Anthropic sources)
- Features you're uncertain about

### What Qualifies as Significant

Ask yourself: "Would a user be missing important functionality if this isn't documented?" If the answer is no, skip it.

## Step 5: Apply Updates

For each update identified, edit the appropriate documentation file:

### Mapping Updates to Files

Choose the appropriate file based on each file's title (the `# heading` on line 1) and existing content. You already read all the docs in Step 3, so use that knowledge to place updates in the right file. If a topic doesn't fit any existing file, create a new numbered file following the existing naming convention (e.g., `docs/18-new-topic.md`) and add it to `README.md`.

### Update Guidelines

1. **Maintain existing style** - Match the Markdown formatting and table styles already in use
2. **Be precise** - Only update what has actually changed
3. **Preserve structure** - Don't reorganize sections unless necessary
4. **Add sources** - Include official documentation links where helpful
5. **Keep practical** - Ensure examples are copy-pasteable

## Step 6: Commit and Push to GitHub (Only If Significant Changes)

**STOP HERE if you haven't made any significant changes.** Check `git status` first - if there are no changes or only trivial changes, do NOT commit. Report that documentation is current instead.

After making **significant** updates, commit and push:

1. **Check what changed**:
   ```bash
   git status
   git diff
   ```

   **If `git status` shows no changes, STOP and report "Documentation is current - no updates needed"**

2. **Review the diff** - Are these changes truly significant? If not, revert and skip the commit.

3. **Stage documentation changes**:
   ```bash
   git add docs/ examples/ README.md
   ```

4. **Create a descriptive commit**:
   ```bash
   git commit -m "docs: auto-update documentation with latest Claude Code features

   - Updated from official Anthropic documentation
   - Synced with current Claude Code capabilities

   🤖 Generated with [Claude Code](https://claude.com/claude-code)

   Co-Authored-By: Claude <noreply@anthropic.com>"
   ```

5. **Push to GitHub**:
   ```bash
   git push
   ```

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

- **Prefer no changes over unnecessary changes** - It's better to report "no updates needed" than to make trivial edits
- Always verify information from official Anthropic sources before updating
- If information conflicts between sources, prefer docs.anthropic.com or code.claude.com
- Do not remove documented features unless confirmed deprecated
- For uncertain changes, note them in the summary for manual review
- **Only commit if there are genuinely significant changes** - avoid commit noise
