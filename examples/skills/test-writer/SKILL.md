---
name: test-writer
description: Write comprehensive unit and integration tests. Use when the user asks to "write tests", "add test coverage", "create unit tests", or wants to test a specific function or module.
allowed-tools: Read, Write, Glob, Grep, Bash(npm test:*), Bash(pytest:*), Bash(go test:*)
---

# Test Writer

## Step 1: Detect Testing Framework

First, identify the testing framework by checking for config files:

| File | Framework |
|------|-----------|
| `jest.config.*`, `package.json` with jest | Jest (JavaScript/TypeScript) |
| `vitest.config.*` | Vitest (JavaScript/TypeScript) |
| `pytest.ini`, `conftest.py`, `pyproject.toml` | Pytest (Python) |
| `*_test.go` | Go testing |
| `*.spec.ts` with `@angular` | Angular Testing |
| `Cargo.toml` with `[dev-dependencies]` | Rust (cargo test) |

## Step 2: Analyze the Code Under Test

For each function/method, identify:

1. **Inputs**: Parameters, their types, valid ranges
2. **Outputs**: Return values, side effects
3. **Dependencies**: External services, databases, APIs
4. **Edge cases**: Null, empty, boundary values, errors

## Step 3: Write Test Cases

### Categories to Cover

#### Happy Path
Normal expected usage:
```typescript
it('should return user when valid ID provided', async () => {
  const user = await getUser(123);
  expect(user).toEqual({ id: 123, name: 'John' });
});
```

#### Edge Cases
Boundary conditions and special values:
```typescript
it('should handle empty string input', () => {
  expect(validateEmail('')).toBe(false);
});

it('should handle maximum length input', () => {
  const maxEmail = 'a'.repeat(254) + '@test.com';
  expect(() => validateEmail(maxEmail)).not.toThrow();
});
```

#### Error Cases
Invalid inputs and failure scenarios:
```typescript
it('should throw NotFoundError when user does not exist', async () => {
  await expect(getUser(99999)).rejects.toThrow(NotFoundError);
});

it('should throw ValidationError for negative ID', async () => {
  await expect(getUser(-1)).rejects.toThrow(ValidationError);
});
```

#### Async Behavior
Promises, callbacks, timeouts:
```typescript
it('should timeout after 5 seconds', async () => {
  jest.useFakeTimers();
  const promise = fetchWithTimeout('/slow-endpoint');
  jest.advanceTimersByTime(5001);
  await expect(promise).rejects.toThrow('Timeout');
});
```

## Step 4: Mock Dependencies

### Database Mocks
```typescript
const mockDb = {
  users: {
    findById: jest.fn().mockResolvedValue({ id: 1, name: 'Test' })
  }
};
```

### API Mocks
```typescript
jest.mock('../api/client', () => ({
  fetch: jest.fn().mockResolvedValue({ data: 'mocked' })
}));
```

### Time Mocks
```typescript
beforeEach(() => {
  jest.useFakeTimers();
  jest.setSystemTime(new Date('2024-01-15'));
});
```

## Step 5: Follow Project Conventions

- Match existing test file naming (`*.test.ts`, `*.spec.ts`, `*_test.go`)
- Use the same assertion style as existing tests
- Follow the project's describe/it nesting structure
- Use existing test utilities and helpers

## Step 6: Verify Tests Pass

After writing tests, run them:
```bash
# JavaScript/TypeScript
npm test -- --testPathPattern="new-test-file"

# Python
pytest path/to/test_file.py -v

# Go
go test ./path/to/package -run TestFunctionName
```

## Test Naming Convention

Use descriptive names that explain the scenario:

```typescript
// Good
it('should return empty array when no users match filter')
it('should throw AuthError when token is expired')

// Bad
it('test1')
it('works')
```

## Output

Provide the complete test file with:
1. All necessary imports
2. Setup/teardown hooks if needed
3. Organized describe blocks
4. Clear test case names
5. Meaningful assertions
