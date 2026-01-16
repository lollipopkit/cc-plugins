English | [简体中文](README.zh-CN.md)

# dev-loop

A Claude Code plugin that drives a task/issue to a merge-ready PR through an iterative loop:

1. **Create Branch**: Always start by creating a new descriptive branch based on the issue/task content.
2. **Implement Fix**: Research and implement the smallest correct fix.
3. **Commit**: Create a clear commit message.
4. **Pull Request**: Open a PR for review.
5. **Wait for Review**: Poll for review comments.
6. **Address Feedback**: Apply changes based on review comments and commit/push again.
7. **Repeat**: Iterate through cycles of review and feedback until the PR is approved or merged.

## Installation

```bash
/plugin marketplace add lollipopkit/cc-plugins
/plugin install dev-loop@lk-ccp
```

## Components

- Skill: `skills/dev-loop/SKILL.md`
- Agent: `agents/dev-loop-runner.md`
- Commands:
  - `/dev-loop` – start or resume the workflow
  - `/dev-loop-enable` – create/update `.claude/dev-loop.local.md`
- Hook:
  - `hooks/hooks.json` – Stop hook that can send IM notifications using a user-provided command template

## Configuration

Create `.claude/dev-loop.local.md` in your project root.

Minimal template:

```markdown
---
enabled: true
base_branch: "main"

# Review behavior
review_mode: "github"   # github|local-agent|custom
max_review_polls: 40
review_poll_seconds: 60

# External non-interactive LLM (optional)
llm_shell: "auto"       # auto|bash|fish
llm_command_template: "" # e.g. llm_script.sh "$DEV_LOOP_PROMPT"  OR  ccpxy "$DEV_LOOP_PROMPT"

# Notifications (optional)
notify_enabled: false
notify_shell: "auto"            # auto|bash|fish
notify_on_stop: true
notify_command_template: ""      # executed with selected shell; can reference env vars below
---

Additional instructions for dev-loop can go here.
```

### Templates and environment variables

`llm_command_template`:

- Intended to run a non-interactive LLM tool.
- The runner will export `DEV_LOOP_PROMPT` before execution.
- The command should output a Markdown checklist so it can be parsed deterministically.

Expected output format:

```markdown
## Review Checklist
- [ ] path/to/file.ts:123 - Describe the exact change to make
- [ ] path/to/file.ts - Describe the change (line optional)
- [ ] (general) Non-file guidance (use sparingly)
```

Parse with: `python3 "$CLAUDE_PLUGIN_ROOT/scripts/parse-review-checklist.py"` (or `python3 dev-loop/scripts/parse-review-checklist.py` while developing)

Examples:

- `llm_script.sh "$DEV_LOOP_PROMPT"`
- `ccpxy gpt -- -p "$DEV_LOOP_PROMPT"` (if `ccpxy` is only available in fish, set `llm_shell: "fish"`)

Note on `ccpxy`: in your fish config, `ccpxy` treats the first non-option argument as a profile name (e.g. `gpt`, `g3p`, `g3f`, `gc`, `glm`, `c`). Do not set `llm_command_template` to `ccpxy "$DEV_LOOP_PROMPT"`, because the prompt would be interpreted as a profile.

Note on `claude` CLI: non-interactive mode is `-p/--print`, so the template should generally include `-p` and pass the prompt as the final argument.

`notify_command_template`:

- Executed by the Stop hook script `scripts/dev-loop-notify.sh`.
- The hook exports:
  - `DEV_LOOP_MESSAGE` (short message)
  - `DEV_LOOP_PROJECT_DIR`
  - `DEV_LOOP_EVENT_NAME`
  - `DEV_LOOP_REASON`
  - `DEV_LOOP_TRANSCRIPT_PATH`
  - `DEV_LOOP_EVENT_JSON_B64` (base64-encoded hook input JSON)
