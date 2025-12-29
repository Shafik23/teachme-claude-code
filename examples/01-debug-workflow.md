# Example: Debugging Workflow

This example shows how to use Claude Code to debug and fix issues.

## Scenario

You have a Node.js API that's returning 500 errors intermittently.

## Step 1: Share the Error

```
> I'm getting this error intermittently in production:

TypeError: Cannot read property 'email' of undefined
    at UserController.getProfile (/app/src/controllers/user.js:42:28)
    at processTicksAndRejections (internal/process/task_queues.js:95:5)
```

## Step 2: Let Claude Investigate

Claude will:
1. Read the relevant file (`src/controllers/user.js`)
2. Understand the code flow
3. Identify the root cause

```
> Can you look at src/controllers/user.js and figure out why this is happening?
```

## Step 3: Review the Analysis

Claude might respond:

"The issue is on line 42 in `getProfile`. The code assumes `req.user` is always present,
but if the authentication middleware fails silently, `req.user` will be undefined.

The fix should check if `req.user` exists before accessing `email`."

## Step 4: Apply the Fix

```
> Fix this issue and add proper error handling
```

Claude will propose changes:

```javascript
// Before
async getProfile(req, res) {
  const email = req.user.email;
  // ...
}

// After
async getProfile(req, res) {
  if (!req.user) {
    return res.status(401).json({ error: 'Not authenticated' });
  }
  const email = req.user.email;
  // ...
}
```

## Step 5: Verify the Fix

```
> Now run the tests to make sure we didn't break anything
```

## Step 6: Check for Similar Issues

```
> Are there other places in the codebase where we access req.user without checking?
```

Claude will search for similar patterns and suggest preventive fixes.

## Pro Tips

1. **Paste full stack traces** - More context helps Claude pinpoint issues
2. **Share relevant logs** - `cat error.log | claude -p "What's causing these errors?"`
3. **Ask for root cause** - Don't just fix symptoms, understand why
4. **Request tests** - `> Add a test case that would have caught this bug`
