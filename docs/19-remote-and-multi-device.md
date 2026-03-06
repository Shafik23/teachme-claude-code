# Remote Control, Slack, and Multi-Device Access

Claude Code can be accessed from multiple surfaces beyond the terminal: your phone, browser, Slack, and the Desktop app. This guide covers the ways to work with Claude Code from anywhere.

## Remote Control

Remote Control connects [claude.ai/code](https://claude.ai/code) or the Claude mobile app ([iOS](https://apps.apple.com/us/app/claude-by-anthropic/id6473753684), [Android](https://play.google.com/store/apps/details?id=com.anthropic.claude)) to a Claude Code session running on your machine. Start a task at your desk, then pick it up from your phone.

Your session runs locally the entire time — your filesystem, MCP servers, tools, and project configuration all stay available. The web and mobile interfaces are just a window into that local session.

### Starting a Remote Control Session

```bash
# Start a new remote session
claude remote-control

# With a custom name
claude remote-control "My Feature Work"

# With verbose logging
claude remote-control --verbose

# With sandboxing enabled
claude remote-control --sandbox
```

From an existing session, use the slash command:

```
/remote-control
/rc  # shorthand
```

### Connecting from Another Device

Once a session is active, connect via:

- **Session URL**: Displayed in the terminal, opens the session on claude.ai/code
- **QR code**: Press spacebar in the terminal to show a QR code for your phone
- **Session list**: Open claude.ai/code and find the session by name (shows a green status dot when online)

### Enable for All Sessions

Run `/config` and set **Enable Remote Control for all sessions** to `true` to automatically start Remote Control with every session.

### Key Points

- **Outbound only**: No inbound ports opened on your machine — all traffic flows through the Anthropic API over TLS
- **Auto-reconnect**: If your laptop sleeps or network drops, the session reconnects automatically
- **Sync**: The conversation stays in sync across all connected devices — send messages from terminal, browser, and phone interchangeably
- **One session at a time**: Each Claude Code instance supports one remote session

### Remote Control vs Claude Code on the Web

| Feature | Remote Control | Claude Code on the Web |
|---------|---------------|----------------------|
| **Where it runs** | Your machine | Anthropic cloud |
| **Local files/tools** | Full access | Cloud repo only |
| **Best for** | Continuing local work remotely | Kicking off tasks without local setup |

## Claude Code in Slack

Mention `@Claude` in a Slack channel with a coding task, and Claude creates a Claude Code session on the web automatically. Useful for delegating development work directly from team conversations.

### Setup

1. Install the Claude app from the [Slack App Marketplace](https://slack.com/marketplace/A08SF47R6P4)
2. Connect your Claude account in the App Home tab
3. Connect a GitHub repository to Claude Code on the web
4. Invite Claude to channels: `/invite @Claude`

### Routing Modes

| Mode | Behavior |
|------|----------|
| **Code only** | All @mentions route to Claude Code sessions |
| **Code + Chat** | Claude routes coding tasks to Claude Code, general questions to Chat |

### How It Works

1. @mention Claude with a coding request in a channel or thread
2. Claude detects coding intent and creates a web session
3. Status updates post to your Slack thread as work progresses
4. On completion, Claude @mentions you with a summary and action buttons
5. Click **View Session** to see the full transcript or **Create PR** to open a pull request

### Tips

- Include file names, error messages, and repo names for better results
- Use threads so Claude can gather full conversation context
- Use **Retry as Code** if Claude responds as chat when you wanted a code session
- Use **Change Repo** if Claude selected the wrong repository

## Desktop App

The Desktop app provides a standalone interface for Claude Code outside your IDE or terminal. Review diffs visually, run multiple sessions side by side, and kick off cloud sessions.

### Download

- [macOS](https://claude.ai/api/desktop/darwin/universal/dmg/latest/redirect) (Intel and Apple Silicon)
- [Windows x64](https://claude.ai/api/desktop/win32/x64/exe/latest/redirect)
- [Windows ARM64](https://claude.ai/api/desktop/win32/arm64/exe/latest/redirect) (remote sessions only)

### Hand Off from Terminal

Use `/desktop` in a terminal session to hand it off to the Desktop app for visual diff review.

## Teleport: Web to Terminal

Use `/teleport` in the terminal to resume a remote session from claude.ai/code in your local terminal. This is useful when you started a task on the web and want to continue locally.

## Chrome Extension (Beta)

Control your browser directly from Claude Code for testing, scraping, or web automation:

1. Install from: https://claude.ai/chrome
2. Use `/browser` to manage the integration

## Mobile App

Use `/mobile` inside Claude Code to display a download QR code for the Claude app on [iOS](https://apps.apple.com/us/app/claude-by-anthropic/id6473753684) or [Android](https://play.google.com/store/apps/details?id=com.anthropic.claude).

## Related

- [Headless Mode](./15-headless-and-automation.md) - CI/CD and scripting
- [Agent Teams](./18-agent-teams.md) - Multi-agent coordination
- [Configuration](./04-configuration.md) - Settings and permissions
