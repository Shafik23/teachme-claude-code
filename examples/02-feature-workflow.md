# Example: Building a New Feature

This example shows how to use Claude Code to implement a new feature from scratch.

## Scenario

Add user preferences (dark mode, notifications, language) to an existing React app.

## Step 1: Describe the Feature

```
> I want to add user preferences to my React app. Users should be able to:
> - Toggle dark mode
> - Enable/disable email notifications
> - Select their preferred language
> The preferences should persist to the backend and sync across devices.
```

## Step 2: Let Claude Plan

Claude will ask clarifying questions or propose a plan:

"I'll implement this feature with the following approach:

1. Create a `UserPreferences` type with the three settings
2. Add a preferences context for app-wide access
3. Create a PreferencesPanel component
4. Add API endpoints for saving/loading preferences
5. Implement localStorage fallback for offline support

Should I proceed with this plan?"

## Step 3: Iterate on the Plan

```
> Yes, but use Zustand instead of Context for state management,
> and we already have a settings page - add it there instead of a new component.
```

## Step 4: Implementation

Claude implements step by step:

```
> Let's start with the type definitions and Zustand store
```

Watch as Claude:
1. Creates the types
2. Sets up the Zustand store
3. Asks permission for each file change

## Step 5: Review Each Change

For each change, Claude shows you what it's doing:

```typescript
// src/stores/preferences.ts
import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface Preferences {
  darkMode: boolean;
  emailNotifications: boolean;
  language: 'en' | 'es' | 'fr' | 'de';
}

interface PreferencesStore extends Preferences {
  setDarkMode: (enabled: boolean) => void;
  setEmailNotifications: (enabled: boolean) => void;
  setLanguage: (lang: Preferences['language']) => void;
}

export const usePreferences = create<PreferencesStore>()(
  persist(
    (set) => ({
      darkMode: false,
      emailNotifications: true,
      language: 'en',
      setDarkMode: (darkMode) => set({ darkMode }),
      setEmailNotifications: (emailNotifications) => set({ emailNotifications }),
      setLanguage: (language) => set({ language }),
    }),
    { name: 'user-preferences' }
  )
);
```

## Step 6: Continue Building

```
> Great, now add the UI to the existing settings page
```

```
> Add the backend API endpoints
```

```
> Write tests for the preferences store
```

## Step 7: Polish

```
> Add proper loading states and error handling
```

```
> Make sure the dark mode actually applies to the whole app
```

## Step 8: Final Review

```
> Review all the changes we made and summarize what was added
```

## Pro Tips

1. **Start with requirements** - Clear requirements = better implementation
2. **Build incrementally** - One piece at a time, verify each step
3. **Ask for alternatives** - "What's another way to do this?"
4. **Request documentation** - "Add JSDoc comments to the public API"
5. **Think about edge cases** - "What happens if the API call fails?"
