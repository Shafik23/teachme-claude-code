---
name: code-explainer
description: Explain code with visual diagrams, analogies, and step-by-step walkthroughs. Use when the user asks "how does this work?", "explain this code", "what does this do?", or wants to understand unfamiliar code.
allowed-tools: Read, Glob, Grep
---

# Code Explainer

When explaining code, follow this structure:

## 1. Start with the Big Picture

Give a one-sentence summary of what the code accomplishes:
> "This function handles user authentication by validating credentials against the database and creating a session token."

## 2. Use an Analogy

Compare the code to something from everyday life:
> "Think of this like a hotel check-in: you show your ID (credentials), the front desk verifies it (database lookup), and you get a room key (session token)."

## 3. Draw a Diagram

Use ASCII art to visualize the flow:

```
┌─────────┐     ┌──────────┐     ┌──────────┐
│  User   │────▶│ Validate │────▶│ Database │
│ Request │     │  Input   │     │  Lookup  │
└─────────┘     └──────────┘     └────┬─────┘
                                      │
                    ┌─────────────────┘
                    ▼
              ┌──────────┐     ┌──────────┐
              │  Create  │────▶│  Return  │
              │  Token   │     │ Response │
              └──────────┘     └──────────┘
```

## 4. Walk Through Step-by-Step

Number each significant step:
1. **Line 5-8**: Extract username and password from request
2. **Line 10-15**: Validate input format (check for empty values, SQL injection)
3. **Line 17-22**: Query database for matching user
4. **Line 24-30**: Compare password hashes
5. **Line 32-38**: Generate JWT token with user claims

## 5. Highlight Key Concepts

Call out patterns, algorithms, or techniques:
- **Pattern used**: Repository pattern for database access
- **Security measure**: Bcrypt for password hashing (cost factor 12)
- **Error handling**: Early returns for validation failures

## 6. Note the Gotchas

Warn about common mistakes or non-obvious behavior:
> "Note: The token expiry is set to 24 hours by default. If you need longer sessions, modify the `TOKEN_EXPIRY` constant, but be aware this affects security."

## Style Guidelines

- Use simple language, avoid jargon unless explaining it
- Keep code snippets short (5-10 lines max)
- Reference line numbers when discussing specific parts
- If the code is complex, break explanation into multiple sections
