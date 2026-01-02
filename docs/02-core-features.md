# Core Features

## File Operations

### Reading Files

Claude can read any file in your project:

```
> Show me the contents of config.json
> What's in the src/utils directory?
```

### Editing Files

Claude makes surgical edits while preserving your code style:

```
> Add error handling to the fetchData function in api.js
> Rename the variable 'x' to 'userCount' in statistics.py
```

### Creating Files

```
> Create a new React component called UserProfile
> Generate a .gitignore for a Node.js project
```

## Terminal Integration

Claude can run shell commands on your behalf:

```
> Run the test suite
> Install axios and lodash
> Show me the git log for the last week
```

## Git Operations

### Commits

```
> Commit these changes with an appropriate message
```

### Branch Management

```
> Create a new branch called feature/user-auth
> What branches exist and which one am I on?
```

### Conflict Resolution

```
> Help me resolve the merge conflicts in app.js
```

## Code Analysis

### Understanding Code

```
> Explain how the authentication flow works
> What does this regex do: ^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$
```

### Finding Issues

```
> Are there any potential bugs in the checkout function?
> Review this code for security vulnerabilities
```

### Refactoring

```
> Refactor the UserService class to use dependency injection
> Convert this callback-based code to async/await
```

## Testing

### Writing Tests

```
> Write unit tests for the calculateTotal function
> Add integration tests for the API endpoints
```

### Running Tests

```
> Run the tests and fix any failures
```

## Documentation

### Code Comments

```
> Add JSDoc comments to the public methods in UserController
```

### README Generation

```
> Generate a README for this project
```

## Image Processing

Claude can analyze images and screenshots:

```
> Look at screenshot.png and implement this UI design
> What's shown in this architecture diagram?
```

Paste images directly with `Ctrl+V` (Mac/Linux) or `Alt+V` (Windows).

## Extended Thinking

For complex problems, Claude uses extended thinking:

```
> Design a caching strategy for our API that handles:
> - High read volume
> - Eventual consistency requirements
> - Multi-region deployment
```

Enable always-on thinking in settings for complex codebases.

## Plan Mode

Review changes before implementation:

```
> /plan Refactor the database layer to use connection pooling
```

Claude will:
1. Analyze the current implementation
2. Propose a detailed plan
3. Wait for your approval before making changes
4. Ask clarifying questions if needed

Toggle with `Shift+Tab` or `Alt+M`. When rejecting a plan, you can now provide feedback telling Claude what to change.

## Subagents

Claude can delegate specialized tasks:

```
> Use a subagent to research the best practices for rate limiting
> Spawn an agent to analyze performance bottlenecks
```

Claude can dynamically choose the model used by subagents and resume subagents when needed. The Explore subagent (powered by Haiku) efficiently searches through your codebase to save context. Background agents can run in parallel while you continue working on other tasks.

## LSP Integration

Claude Code includes Language Server Protocol (LSP) support for code intelligence:

- **Go to definition**: Find where symbols are defined
- **Find references**: Find all usages of a symbol
- **Hover documentation**: Get type info and docs
- **Document symbols**: Get all symbols in a file
- **Workspace symbols**: Search across the codebase
- **Go to implementation**: Find implementations of interfaces
- **Call hierarchy**: Find incoming/outgoing calls

## Web Capabilities

### Search

```
> Search for the latest React 19 features
```

### Fetch Documentation

```
> Fetch the axios documentation and show me how to handle retries
```

## Context Management

### Add Directories

```
/add-dir ../shared-lib
```

### View Context Usage

```
/context
```

### Compact Conversation

```
/compact focus on the authentication module
```
