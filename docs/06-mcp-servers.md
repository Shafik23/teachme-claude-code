# MCP Servers (Model Context Protocol)

MCP enables Claude Code to connect to external tools and data sources through the open Model Context Protocol standard.

## What You Can Do with MCP

- **Issue Trackers**: Implement features from JIRA, Linear, GitHub Issues
- **Monitoring**: Analyze data from Sentry, Datadog, Statsig
- **Databases**: Query PostgreSQL, MySQL, MongoDB directly
- **Design Tools**: Work with Figma designs and design systems
- **Communication**: Automate Gmail, Slack workflows
- **Browser Control**: Control your browser with Claude in Chrome (Beta)
- **Custom Tools**: Connect to your company's internal APIs

## Remote MCP Support

Remote MCP servers offer a lower maintenance alternative to local servers. Just add the vendor's URL—no manual setup required. Vendors handle updates, scaling, and availability.

Claude Code features native OAuth support for remote MCP servers, ensuring secure connections. Simply authenticate once, and Claude Code handles the rest.

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

### Remote HTTP Servers (Quick Setup)

| Server | Command |
|--------|---------|
| **Linear** | `claude mcp add --transport http linear https://mcp.linear.app/mcp` |
| **Notion** | `claude mcp add --transport http notion https://mcp.notion.com/mcp` |
| **Sentry** | `claude mcp add --transport http sentry https://mcp.sentry.dev/mcp` |
| **Figma** | `claude mcp add --transport http figma https://mcp.figma.com/mcp` |
| **Stripe** | `claude mcp add --transport http stripe https://mcp.stripe.com` |
| **PayPal** | `claude mcp add --transport http paypal https://mcp.paypal.com/mcp` |
| **Vercel** | `claude mcp add --transport http vercel https://mcp.vercel.com` |
| **Netlify** | `claude mcp add --transport http netlify https://netlify-mcp.netlify.app/mcp` |
| **Cloudflare** | `claude mcp add --transport http cloudflare https://bindings.mcp.cloudflare.com/mcp` |
| **Monday** | `claude mcp add --transport http monday https://mcp.monday.com/mcp` |
| **Canva** | `claude mcp add --transport http canva https://mcp.canva.com/mcp` |
| **Hugging Face** | `claude mcp add --transport http hugging-face https://huggingface.co/mcp` |
| **Honeycomb** | `claude mcp add --transport http honeycomb https://mcp.honeycomb.io/mcp` |
| **Intercom** | `claude mcp add --transport http intercom https://mcp.intercom.com/mcp` |
| **Square** | `claude mcp add --transport sse square https://mcp.squareup.com/sse` |

### Development & DevOps

| Server | Purpose |
|--------|---------|
| GitHub | Issues, PRs, repos, code reviews |
| Linear | Modern issue tracking |
| Jira/Atlassian | Enterprise issues and Confluence |
| Sentry | Error monitoring and debugging |
| Honeycomb | Observability and SLOs |
| Vercel | Deploy and manage websites |
| Netlify | Build and deploy web apps |
| Cloudflare | CDN, compute, storage |

### Databases

| Server | Purpose |
|--------|---------|
| PostgreSQL | Query Postgres databases |
| CData Connect | 270+ enterprise data sources |
| Snowflake | Data warehouse queries |
| Databricks | Unity Catalog and Mosaic AI |

### Productivity & Business

| Server | Purpose |
|--------|---------|
| Notion | Docs, wikis, databases |
| Monday | Project management |
| Asana | Task and project coordination |
| Clockwise | Calendar and scheduling |
| Zapier | Workflow automation |

### Design & Content

| Server | Purpose |
|--------|---------|
| Figma | Design files and systems |
| Canva | Create and edit designs |
| BioRender | Scientific templates |
| Cloudinary | Image and video management |

### Finance & Payments

| Server | Purpose |
|--------|---------|
| Stripe | Payment processing |
| PayPal | Payments platform |
| Ramp | Financial data and analytics |

Find hundreds more at [github.com/modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers)

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

## MCP Resources

MCP servers can expose resources you can reference with `@` mentions:

```bash
# Reference resources in prompts
> Can you analyze @github:issue://123 and suggest a fix?
> Compare @postgres:schema://users with @docs:file://database/user-model
```

Resources are automatically fetched and included as attachments.

---

## MCP Prompts as Slash Commands

MCP servers can expose prompts as slash commands:

```bash
/mcp__github__list_prs
/mcp__jira__create_issue "Bug title" high
```

Use `/` to see available MCP commands from connected servers.

---

## Plugin-Provided MCP Servers

Plugins can bundle MCP servers that start automatically when enabled:

```json
{
  "mcpServers": {
    "plugin-api": {
      "command": "${CLAUDE_PLUGIN_ROOT}/servers/api-server",
      "args": ["--port", "8080"]
    }
  }
}
```

Plugin MCP servers use `${CLAUDE_PLUGIN_ROOT}` for relative paths.

---

## Security Considerations

1. **Store secrets in environment variables**, not in `.mcp.json`
2. **Review MCP servers** before adding them
3. **Use project scope** for team-approved servers only
4. **Audit MCP access** regularly with `claude mcp list`
5. **Be careful with untrusted content** - MCP servers that fetch external data may expose you to prompt injection

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
