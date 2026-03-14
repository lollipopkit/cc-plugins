---
name: recursive-arena
description: Combine recursive outer-loop refinement with multi-model arena generation each round. Use when users request recursive arena, multi-LLM consensus with iterative refinement, or recursive plus model-battle workflows.
allowed-tools: Read, Bash(python:*)
---

# Recursive-Arena

Use the orchestrator:
`python3 "${CLAUDE_PLUGIN_ROOT}/skills/recursive-arena/scripts/recursive_arena.py"`.

## How to run

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/recursive-arena/scripts/recursive_arena.py" \
  --prompt "<task>" --iters 4 --arena-iters 3 --json
```

Common flags: `--max-judges`, `--temperature`, `--max-tokens`, `--timeout`.

## Iteration Loop

For each outer iteration:

1. Run `multi-model` to generate a best candidate.
2. Use judge summaries as critique input.
3. Refine the prompt with the current best answer.
4. Keep the global best by score and continue.

## Configuration

Reuses `multi-model` `.env` configuration:

- `ARENA_MODELS`
- `ARENA_OPENAI_BASE_URL` or `ARENA_PROVIDER_<NAME>_BASE_URL`
- Optional API keys (`ARENA_OPENAI_API_KEY`, `ARENA_PROVIDER_<NAME>_API_KEY`)

Optional orchestration env:

- `RLM_ARENA_ARENA_ITERS` default inner arena iterations
- `RLM_ARENA_MAX_JUDGES` default judge cap

## Output and Safety

- Final answer is the best outer-iteration result.
- When useful, show a compact evolution table:
  - `iteration`
  - `winner_model_id` (numeric ID only)
  - `avg_judge_score`
  - `refinement_applied`
- Never disclose provider/model names.
- Never print secrets from `.env`.
