# Example: Refactoring Workflow

This example shows how to safely refactor code with Claude Code.

## Scenario

Refactor a monolithic 500-line React component into smaller, reusable pieces.

## Step 1: Analyze the Current State

```
> Analyze src/components/Dashboard.tsx and identify opportunities
> to break it into smaller components
```

Claude will read the file and provide analysis:

"The Dashboard component has several concerns that could be separated:

1. **Data fetching logic** (lines 45-120) - Could be a custom hook
2. **Chart rendering** (lines 150-250) - Could be ChartSection component
3. **Stats cards** (lines 260-340) - Could be StatsGrid component
4. **Recent activity table** (lines 350-450) - Could be ActivityTable component

The component also mixes presentation and business logic."

## Step 2: Plan the Refactor

```
> Create a refactoring plan. I want to keep backwards compatibility
> and make sure nothing breaks.
```

Claude proposes:

"Here's a safe refactoring plan:

1. Extract custom hook `useDashboardData` for data fetching
2. Create `ChartSection` component (stateless, receives data as props)
3. Create `StatsGrid` component with typed props
4. Create `ActivityTable` component
5. Simplify Dashboard to compose these pieces
6. Ensure all existing tests pass
7. Add tests for new components

Each step will be a separate commit for easy rollback."

## Step 3: Use Plan Mode

```
/plan
```

Then:

```
> Show me exactly what the refactored code will look like before making changes
```

Claude shows the proposed structure without modifying files.

## Step 4: Execute Step by Step

```
> Let's start. Extract the useDashboardData hook first.
```

Claude creates:

```typescript
// src/hooks/useDashboardData.ts
import { useState, useEffect } from 'react';
import { fetchDashboardStats, fetchRecentActivity } from '../api/dashboard';

export function useDashboardData() {
  const [stats, setStats] = useState(null);
  const [activity, setActivity] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function loadData() {
      try {
        const [statsData, activityData] = await Promise.all([
          fetchDashboardStats(),
          fetchRecentActivity(),
        ]);
        setStats(statsData);
        setActivity(activityData);
      } catch (err) {
        setError(err);
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

  return { stats, activity, loading, error, refetch: loadData };
}
```

## Step 5: Verify After Each Change

```
> Run the tests to make sure nothing broke
```

```
> Does the Dashboard still work the same way?
```

## Step 6: Continue Extraction

```
> Now extract the ChartSection component
```

```
> Extract StatsGrid next
```

```
> Finally, extract ActivityTable
```

## Step 7: Simplify the Main Component

```
> Now update Dashboard.tsx to use all the extracted pieces
```

Result:

```typescript
// src/components/Dashboard.tsx
import { useDashboardData } from '../hooks/useDashboardData';
import { ChartSection } from './ChartSection';
import { StatsGrid } from './StatsGrid';
import { ActivityTable } from './ActivityTable';
import { LoadingSpinner } from './LoadingSpinner';
import { ErrorMessage } from './ErrorMessage';

export function Dashboard() {
  const { stats, activity, loading, error } = useDashboardData();

  if (loading) return <LoadingSpinner />;
  if (error) return <ErrorMessage error={error} />;

  return (
    <div className="dashboard">
      <StatsGrid stats={stats} />
      <ChartSection data={stats.chartData} />
      <ActivityTable items={activity} />
    </div>
  );
}
```

## Step 8: Add Tests

```
> Add unit tests for each new component
```

## Step 9: Final Review

```
> Show me a summary of all files changed and lines of code before/after
```

## Pro Tips

1. **Use plan mode first** - Preview changes before applying
2. **Small steps** - One extraction at a time
3. **Test after each change** - Catch regressions early
4. **Keep old code working** - Refactor, don't rewrite
5. **Commit incrementally** - Easy rollback if needed
