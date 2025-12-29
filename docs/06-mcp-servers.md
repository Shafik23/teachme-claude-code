# MCP Servers (Model Context Protocol)

MCP enables Claude Code to connect to external tools and data sources through the open Model Context Protocol standard.

## What You Can Do with MCP

- **Issue Trackers**: Implement features from JIRA, Linear, GitHub Issues
- **Monitoring**: Analyze data from Sentry, Datadog, Statsig
- **Databases**: Query PostgreSQL, MySQL, MongoDB directly
- **Design Tools**: Work with Figma designs and design systems
- **Communication**: Automate Gmail, Slack workflows
- **Custom Tools**: Connect to your company's internal APIs

## Installing MCP Servers

### HTTP Servers (Recommended)

```bash
# Notion integration
claude mcp add --transport http notion https://mcp.notion.com/mcp

# Sentry error tracking
claude mcp add --transport http sentry https://mcp.sentry.dev/mcp

# GitHub
claude mcp add --transport http github https://mcp.github.com/mcp
```

### SSE Servers

```bash
claude mcp add --transport sse asana https://mcp.asana.com/sse
```

### Local Stdio Servers

For servers that run as local processes:

```bash
# Airtable
claude mcp add --transport stdio airtable \
  --env AIRTABLE_API_KEY=your_key \
  -- npx -y airtable-mcp-server

# File system access
claude mcp add --transport stdio filesystem \
  -- npx -y @anthropic/mcp-server-filesystem ~/Documents
```

## Managing MCP Servers

```bash
# List all configured servers
claude mcp list

# Get details for a server
claude mcp get github

# Remove a server
claude mcp remove github

# In-session management
/mcp
```

## Configuration Scopes

### Local Scope (Default)
Private to you in current project. Stored in project's `.claude.json`.

```bash
claude mcp add github https://mcp.github.com/mcp
```

### Project Scope
Shared with team via `.mcp.json` (commit to git).

```bash
claude mcp add --scope project github https://mcp.github.com/mcp
```

### User Scope
Available across all your projects. Stored in `~/.claude.json`.

```bash
claude mcp add --scope user github https://mcp.github.com/mcp
```

## Configuration Files

### Project `.mcp.json`

```json
{
  "mcpServers": {
    "github": {
      "type": "http",
      "url": "https://mcp.github.com/mcp"
    },
    "database": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-server-postgres"],
      "env": {
        "DATABASE_URL": "${DATABASE_URL}"
      }
    }
  }
}
```

### Environment Variables

Use environment variables for secrets:

```json
{
  "mcpServers": {
    "api-server": {
      "type": "http",
      "url": "${API_BASE_URL:-https://api.example.com}/mcp",
      "headers": {
        "Authorization": "Bearer ${API_KEY}"
      }
    }
  }
}
```

Syntax:
- `${VAR}` - Use environment variable
- `${VAR:-default}` - Use default if not set

## Popular MCP Servers

### Development Tools

| Server | Purpose |
|--------|---------|
| GitHub | Issues, PRs, repos |
| GitLab | GitLab integration |
| Linear | Issue tracking |
| Jira | Atlassian issues |

### Databases

| Server | Purpose |
|--------|---------|
| PostgreSQL | Query Postgres |
| MySQL | Query MySQL |
| MongoDB | Query MongoDB |
| SQLite | Local databases |

### Monitoring

| Server | Purpose |
|--------|---------|
| Sentry | Error tracking |
| Datadog | Monitoring |
| PagerDuty | Incident management |

### Productivity

| Server | Purpose |
|--------|---------|
| Notion | Docs and wikis |
| Slack | Team messaging |
| Gmail | Email automation |
| Google Drive | File access |

### Design

| Server | Purpose |
|--------|---------|
| Figma | Design files |

## Using MCP in Sessions

Once configured, Claude automatically has access to MCP tools:

```
> Check the latest errors in Sentry for our production environment

> Create a GitHub issue for the bug we just discussed

> Query the database to find all users who signed up last week

> Send a Slack message to #engineering about the deployment
```

## Troubleshooting

### Check Server Status

```
/mcp
```

### Server Not Connecting

1. Verify the URL is correct
2. Check authentication credentials
3. Ensure network access to the server
4. Check server-specific requirements

### Permission Issues

Some MCP servers require OAuth. Follow the authentication prompts when first using the server.

### Debug Mode

```bash
claude --verbose
```

## Security Considerations

1. **Store secrets in environment variables**, not in `.mcp.json`
2. **Review MCP servers** before adding them
3. **Use project scope** for team-approved servers only
4. **Audit MCP access** regularly with `claude mcp list`

## Creating Custom MCP Servers

You can create custom MCP servers to expose your own tools:

```typescript
// Basic MCP server structure
import { Server } from "@modelcontextprotocol/sdk";

const server = new Server({
  name: "my-custom-server",
  version: "1.0.0",
});

server.tool("my-tool", "Description of what it does", async (params) => {
  // Tool implementation
  return { result: "..." };
});

server.start();
```

See the [MCP SDK documentation](https://github.com/anthropics/mcp) for full details.
