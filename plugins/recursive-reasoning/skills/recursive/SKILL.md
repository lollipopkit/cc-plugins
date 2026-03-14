---
name: recursive
description: Recursive master-orchestration for complex multi-step tasks. Decompose work, delegate execution to sub-agents, and iterate until verified. Use when users request recursive reasoning, multi-pass refinement, or explicit plan-execute-verify loops.
allowed-tools: Read, Task, mcp__seq-think__sequentialthinking
---

# Recursive

Act as the master orchestrator. Keep execution in sub-agents (`recursive-executor`) and focus on planning, verification, and synthesis.

## Workflow

1. Plan with `mcp__seq-think__sequentialthinking`.
2. Split the task into 2-6 ordered steps with dependencies and acceptance criteria.
3. Delegate one step at a time with `Task` (parallelize only independent steps).
4. Verify each result for correctness, completeness, and constraint compliance.
5. If a step fails, re-delegate with concrete fixes and retry criteria.
6. Synthesize verified outputs into the final response.

## Operating Rules

- Pass only the minimum context required for each sub-task.
- Keep a short reflection log: what failed, what changed, what now works.
- Stop when all steps pass, or when two consecutive retries on the same step bring no material improvement.
- Prioritize final answer quality over exposing internal chain-of-thought.

## Response Style

- Default: return final answer first, then a brief verification summary when useful.
- If the user asks for process details, provide a compact table: `step | owner | status | retries`.
