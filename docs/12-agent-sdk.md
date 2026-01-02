# Claude Agent SDK

The **Claude Agent SDK** (formerly Claude Code SDK) lets you build AI agents programmatically in Python and TypeScript. It provides the same tools, agent loop, and context management that power Claude Code, as a library.

## Why Use the Agent SDK?

| Client SDK | Agent SDK |
|------------|-----------|
| You implement tool execution | Claude handles tools autonomously |
| You manage the message loop | Built-in agent loop |
| Direct API access | Production-ready agent framework |

```python
# Client SDK: You implement the tool loop
response = client.messages.create(...)
while response.stop_reason == "tool_use":
    result = your_tool_executor(response.tool_use)
    response = client.messages.create(tool_result=result, ...)

# Agent SDK: Claude handles tools autonomously
async for message in query(prompt="Fix the bug in auth.py"):
    print(message)
```

## Installation

### 1. Install Claude Code (runtime)

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

The Python SDK automatically bundles the Claude Code CLI—no separate installation required.

### 2. Install the SDK

```bash
# Python
pip install claude-agent-sdk

# TypeScript
npm install @anthropic-ai/claude-agent-sdk
```

### 3. Set API key

```bash
export ANTHROPIC_API_KEY=your-api-key
```

Also supports third-party API providers:
- **Amazon Bedrock**: `CLAUDE_CODE_USE_BEDROCK=1`
- **Google Vertex AI**: `CLAUDE_CODE_USE_VERTEX=1`
- **Microsoft Azure Foundry**: `CLAUDE_CODE_USE_FOUNDRY=1`

The Python SDK automatically bundles the Claude Code CLI—no separate installation required.

## Quick Start

### Python

The Python SDK provides two main APIs:

1. **`query()`** - Simple text generation (no tools)
2. **`ClaudeSDKClient`** - Full agentic API with tools, sessions, and hooks

Note: The SDK no longer reads from filesystem settings (CLAUDE.md, settings.json, slash commands, etc.) by default. Use `setting_sources=["project"]` to load project configurations.

```python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions

async def main():
    async for message in query(
        prompt="Find and fix the bug in auth.py",
        options=ClaudeAgentOptions(allowed_tools=["Read", "Edit", "Bash"])
    ):
        print(message)

asyncio.run(main())
```

For custom tools defined as Python functions, use `ClaudeSDKClient` which implements them as in-process MCP servers.

### TypeScript

```typescript
import { query } from '@anthropic-ai/claude-agent-sdk';

for await (const message of query({
  prompt: 'Find all TODO comments and summarize them',
  options: { allowedTools: ['Read', 'Glob', 'Grep'] }
})) {
  console.log(message);
}
```

## Built-in Tools

Your agent has these tools out of the box:

| Tool | Description |
|------|-------------|
| `Read` | Read any file in the working directory |
| `Write` | Create new files |
| `Edit` | Make precise edits to existing files |
| `Bash` | Run terminal commands, scripts, git operations |
| `Glob` | Find files by pattern (`**/*.ts`, `src/**/*.py`) |
| `Grep` | Search file contents with regex |
| `WebSearch` | Search the web for current information |
| `WebFetch` | Fetch and parse web page content |

## Agent Options

```python
from claude_agent_sdk import ClaudeAgentOptions

options = ClaudeAgentOptions(
    # Tools the agent can use
    allowed_tools=["Read", "Edit", "Bash", "Glob", "Grep"],

    # Working directory
    cwd="/path/to/project",

    # Load project settings (.claude/settings.json, CLAUDE.md, etc.)
    setting_sources=["project"],

    # Custom system prompt additions
    system_prompt_suffix="Focus on security best practices.",

    # Max turns before stopping
    max_turns=50,
)
```

## Using Claude Code Features

The SDK supports Claude Code's configuration:

```python
options = ClaudeAgentOptions(
    setting_sources=["project"]  # Load .claude/ configs
)
```

This enables:

| Feature | Location |
|---------|----------|
| Skills | `.claude/skills/*/SKILL.md` |
| Slash commands | `.claude/commands/*.md` |
| Memory | `CLAUDE.md` |
| MCP servers | `.mcp.json` |

## Example Agents

### Bug Fixer

```python
async for msg in query(
    prompt="Find and fix the failing test in tests/auth_test.py",
    options=ClaudeAgentOptions(
        allowed_tools=["Read", "Edit", "Bash"],
        cwd="/path/to/project"
    )
):
    if hasattr(msg, "result"):
        print(msg.result)
```

### Code Reviewer

```python
async for msg in query(
    prompt="""Review the changes in the last commit for:
    - Security vulnerabilities
    - Performance issues
    - Code style violations
    Output as markdown.""",
    options=ClaudeAgentOptions(
        allowed_tools=["Read", "Bash", "Glob", "Grep"]
    )
):
    print(msg)
```

### Research Agent

```python
async for msg in query(
    prompt="Research the latest React 19 features and summarize",
    options=ClaudeAgentOptions(
        allowed_tools=["WebSearch", "WebFetch"]
    )
):
    print(msg)
```

### Migration Agent

```python
# Fan out to process many files
import asyncio

files = ["src/auth.py", "src/users.py", "src/api.py"]

async def migrate_file(file):
    async for msg in query(
        prompt=f"Migrate {file} from Flask to FastAPI",
        options=ClaudeAgentOptions(allowed_tools=["Read", "Edit"])
    ):
        pass

await asyncio.gather(*[migrate_file(f) for f in files])
```

## Hooks

Intercept and modify agent behavior:

```python
from claude_agent_sdk import ClaudeAgentOptions

def pre_tool_hook(tool_name, tool_input):
    if tool_name == "Bash" and "rm -rf" in tool_input.get("command", ""):
        return {"allow": False, "message": "Blocked dangerous command"}
    return {"allow": True}

options = ClaudeAgentOptions(
    hooks={
        "PreToolUse": pre_tool_hook
    }
)
```

## Sessions

Resume conversations:

```python
from claude_agent_sdk import query, ClaudeAgentOptions

# First session
session_id = None
async for msg in query(prompt="Analyze the auth module"):
    if hasattr(msg, "session_id"):
        session_id = msg.session_id
    print(msg)

# Resume later
async for msg in query(
    prompt="Now fix the issues you found",
    options=ClaudeAgentOptions(session_id=session_id)
):
    print(msg)
```

## Error Handling

```python
from claude_agent_sdk import query, AgentError

try:
    async for msg in query(prompt="Fix the bug"):
        print(msg)
except AgentError as e:
    print(f"Agent failed: {e}")
```

## Resources

- [Agent SDK Documentation](https://docs.claude.com/en/api/agent-sdk/overview)
- [Python SDK GitHub](https://github.com/anthropics/claude-agent-sdk-python)
- [TypeScript SDK GitHub](https://github.com/anthropics/claude-agent-sdk-typescript)
- [Example Agents](https://github.com/anthropics/claude-agent-sdk-demos)
