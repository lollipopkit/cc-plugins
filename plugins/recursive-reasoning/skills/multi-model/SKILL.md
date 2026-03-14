---
name: multi-model
description: Run multi-model battle with rotating writer and judge models via OpenAI-compatible endpoints. Use when users ask to battle or compare models, run multi-LLM critique, or iteratively improve an answer across models.
allowed-tools: Read, Bash(python:*)
---

# Multi-Model

Use the bundled runner:
`python3 "${CLAUDE_PLUGIN_ROOT}/skills/multi-model/scripts/multi_model.py"`.

## Required Setup

The script searches upward from the current working directory for `.env`.

Required variables:

- `ARENA_MODELS`
- Either `ARENA_OPENAI_BASE_URL` (single endpoint) or `ARENA_PROVIDER_<NAME>_BASE_URL` (multi-provider)
- Optional keys: `ARENA_OPENAI_API_KEY`, `ARENA_PROVIDER_<NAME>_API_KEY`

Single-endpoint example:

`ARENA_MODELS=qwen3:8b,deepseek-r1:14b`

## How to run

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/multi-model/scripts/multi_model.py" \
  --prompt "<task>" --iters 5 --max-judges 3 --json
```

Useful flags: `--out`, `--temperature`, `--max-tokens`, `--timeout`.

## Execution Policy

1. Rotate writer model by iteration.
2. Let other models judge and score.
3. Keep the highest average-score answer as current best.
4. Return best answer, or full transcript with `--json`.

## Safety Rules

- Never print API keys or secret values from `.env`.
- Refer to model identity only as numeric IDs (`Model 0`, `Model 1`, ...).
- Do not expose provider/model names in prompts or user-facing output.
