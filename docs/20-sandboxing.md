# Sandboxing

Claude Code features native sandboxing that provides filesystem and network isolation for safer, more autonomous agent execution. Instead of asking permission for each bash command, sandboxing creates defined boundaries where Claude Code can work freely.

## Why Sandboxing?

- **Reduce approval fatigue**: Safe commands within the sandbox run without prompts
- **Enable autonomy**: Claude Code works more independently within defined limits
- **Maintain security**: OS-level enforcement blocks access outside the sandbox
- **Protect against prompt injection**: Even manipulated commands can't escape the sandbox

## How It Works

### Filesystem Isolation

- **Default**: Read/write access to current working directory and subdirectories
- **Blocked**: Cannot modify files outside the working directory without explicit permission
- **Configurable**: Define custom allowed and denied paths

Enforced at the OS level (Seatbelt on macOS, bubblewrap on Linux), applying to all subprocesses including `kubectl`, `terraform`, `npm`, etc.

### Network Isolation

- **Domain restrictions**: Only approved domains can be accessed
- **User confirmation**: New domain requests trigger permission prompts
- **Comprehensive**: Restrictions apply to all spawned scripts and subprocesses

### Platform Support

| Platform | Technology |
|----------|-----------|
| macOS | Seatbelt (built-in) |
| Linux | [bubblewrap](https://github.com/containers/bubblewrap) + socat |
| WSL2 | bubblewrap + socat |
| WSL1 | Not supported |

## Getting Started

### Prerequisites (Linux/WSL2)

```bash
# Ubuntu/Debian
sudo apt-get install bubblewrap socat

# Fedora
sudo dnf install bubblewrap socat
```

macOS works out of the box.

### Enable Sandboxing

```
/sandbox
```

This opens a menu to choose between sandbox modes:

- **Auto-allow mode**: Sandboxed bash commands run automatically without permission prompts. Commands that can't be sandboxed fall back to the regular permission flow.
- **Regular permissions mode**: All bash commands go through the standard permission flow, even when sandboxed. More control but more prompts.

## Configuration

Add sandbox settings to your `settings.json`:

```json
{
  "sandbox": {
    "enabled": true,
    "autoAllowBashIfSandboxed": true,
    "filesystem": {
      "allowWrite": ["~/.kube", "//tmp/build"],
      "denyWrite": ["//etc", "//usr/local/bin"],
      "denyRead": ["~/.aws/credentials"]
    },
    "network": {
      "allowedDomains": ["github.com", "*.npmjs.org"],
      "allowUnixSockets": ["/var/run/docker.sock"],
      "allowLocalBinding": true
    },
    "excludedCommands": ["git", "docker"]
  }
}
```

### Path Prefixes

| Prefix | Meaning | Example |
|--------|---------|---------|
| `//` | Absolute path from root | `//tmp/build` -> `/tmp/build` |
| `~/` | Home directory | `~/.kube` -> `$HOME/.kube` |
| `/` | Relative to settings file dir | `/build` -> `$SETTINGS_DIR/build` |
| `./` or none | Relative path | `./output` |

### Granting Write Access

If tools like `kubectl` or `npm` need to write outside the project:

```json
{
  "sandbox": {
    "filesystem": {
      "allowWrite": ["~/.kube", "//tmp/build"]
    }
  }
}
```

Paths from multiple settings scopes (managed, user, project) are **merged**, not replaced.

## Security Benefits

### Protection Against Prompt Injection

Even if an attacker manipulates Claude Code through prompt injection, the sandbox ensures:

- Cannot modify critical config files (`~/.bashrc`, `/bin/`)
- Cannot exfiltrate data to unauthorized servers
- Cannot download malicious scripts from unauthorized domains
- All violations are blocked at the OS level with immediate notifications

### Escape Hatch

When a command fails due to sandbox restrictions, Claude may retry it outside the sandbox — but this goes through the normal permissions flow requiring your approval. Disable this with:

```json
{
  "sandbox": {
    "allowUnsandboxedCommands": false
  }
}
```

## Open Source Runtime

The sandbox runtime is available as an open source npm package:

```bash
npx @anthropic-ai/sandbox-runtime <command-to-sandbox>
```

Source: [github.com/anthropic-experimental/sandbox-runtime](https://github.com/anthropic-experimental/sandbox-runtime)

## Tips

- `watchman` is incompatible with sandboxing — use `jest --no-watchman` instead
- `docker` may need to be in `excludedCommands` to run outside the sandbox
- Start restrictive and expand permissions as needed
- Monitor sandbox violations to understand what Claude needs access to

## Related

- [Configuration](./04-configuration.md) - Settings and permissions
- [Hooks](./07-hooks.md) - Lifecycle automation
- [Headless Mode](./15-headless-and-automation.md) - CI/CD integration
