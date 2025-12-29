---
name: performance-profiler
description: Profile application performance - CPU, memory, async operations, and database queries. Identifies bottlenecks, memory leaks, and slow operations. Use when investigating performance issues, optimizing code, or when the user mentions slowness, memory leaks, or performance problems.
allowed-tools: Read, Bash(python3:*), Bash(node:*), Bash(npm:*), Glob, Grep
---

# Performance Profiler

Profile and analyze application performance issues.

## Quick Profile

### Node.js Application

```bash
# CPU profiling
node --prof app.js
node --prof-process isolate-*.log > profile.txt

# Or use the helper script
node ${SKILL_DIR}/scripts/profile-node.js --entry app.js --duration 30
```

### Python Application

```bash
python3 -m cProfile -o profile.prof app.py
python3 ${SKILL_DIR}/scripts/analyze_profile.py --input profile.prof
```

## Analysis Tools

### 1. CPU Hotspots

Find functions consuming the most CPU:

```bash
python3 ${SKILL_DIR}/scripts/analyze_profile.py --input profile.prof --top 20
```

### 2. Memory Analysis

Detect memory leaks and high allocations:

```bash
# Node.js
node --expose-gc ${SKILL_DIR}/scripts/memory-snapshot.js --entry app.js

# Python
python3 -m tracemalloc ${SKILL_DIR}/scripts/memory_trace.py --target app.py
```

### 3. Async Operation Analysis

Find slow promises, unresolved async operations:

```bash
node ${SKILL_DIR}/scripts/async-tracker.js --entry app.js
```

### 4. Database Query Analysis

Profile slow queries:

```bash
python3 ${SKILL_DIR}/scripts/query_analyzer.py --log queries.log --threshold 100
```

## Bottleneck Detection

Run comprehensive analysis:

```bash
python3 ${SKILL_DIR}/scripts/find_bottlenecks.py --path . --type nodejs
```

This checks for:
- Synchronous operations in async code
- N+1 query patterns
- Missing connection pooling
- Unbounded loops/recursion
- Memory-intensive operations

## Flame Graph Generation

```bash
# Record profile
node --perf-basic-prof app.js &
perf record -F 99 -p $! -g -- sleep 30

# Generate flame graph
perf script | ${SKILL_DIR}/scripts/stackcollapse-perf.pl | \
  ${SKILL_DIR}/scripts/flamegraph.pl > flame.svg
```

## Recommendations Engine

Get optimization suggestions:

```bash
python3 ${SKILL_DIR}/scripts/recommend.py --profile profile.prof --source src/
```

Analyzes profile data and source code to suggest:
- Caching opportunities
- Parallelization candidates
- Algorithm improvements
- Resource pooling
