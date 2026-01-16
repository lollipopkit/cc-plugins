English | [简体中文](README.zh-CN.md)

# issue-loop

A Claude Code plugin that drives a task/issue to a merge-ready PR through an iterative loop:

1. Implement minimal fix
2. Commit
3. Open or update PR
4. Wait for AI/bot review comments
5. Apply feedback
6. Repeat until merge-ready

## Installation

```bash
/plugin marketplace add lollipopkit/cc-plugins
/plugin install issue-loop@lk-ccp
```

## Components

- Skill: `skills/issue-loop/SKILL.md`
- Agent: `agents/issue-loop-runner.md`
- Commands:
  - `/issue-loop` – start or resume the workflow
  - `/issue-loop-enable` – create/update `.claude/issue-loop.local.md`
- Hook:
  - `hooks/hooks.json` – Stop hook that can send IM notifications using a user-provided command template

## Configuration

Create `.claude/issue-loop.local.md` in your project root.

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
llm_command_template: "" # e.g. llm_script.sh "$ISSUE_LOOP_PROMPT"  OR  ccpxy "$ISSUE_LOOP_PROMPT"

# Notifications (optional)
notify_enabled: false
notify_shell: "auto"            # auto|bash|fish
notify_on_stop: true
notify_command_template: ""      # executed with selected shell; can reference env vars below
---

Additional instructions for issue-loop can go here.
```

### Templates and environment variables

`llm_command_template`:

- Intended to run a non-interactive LLM tool.
- The runner will export `ISSUE_LOOP_PROMPT` before execution.
- The command should output a Markdown checklist so it can be parsed deterministically.

Expected output format:

```markdown
## Review Checklist
- [ ] path/to/file.ts:123 - Describe the exact change to make
- [ ] path/to/file.ts - Describe the change (line optional)
- [ ] (general) Non-file guidance (use sparingly)
```

Parse with: `python3 "$CLAUDE_PLUGIN_ROOT/scripts/parse-review-checklist.py"` (or `python3 issue-loop/scripts/parse-review-checklist.py` while developing)

Examples:

- `llm_script.sh "$ISSUE_LOOP_PROMPT"`
- `ccpxy gpt -- -p "$ISSUE_LOOP_PROMPT"` (if `ccpxy` is only available in fish, set `llm_shell: "fish"`)

Note on `ccpxy`: in your fish config, `ccpxy` treats the first non-option argument as a profile name (e.g. `gpt`, `g3p`, `g3f`, `gc`, `glm`, `c`). Do not set `llm_command_template` to `ccpxy "$ISSUE_LOOP_PROMPT"`, because the prompt would be interpreted as a profile.

Note on `claude` CLI: non-interactive mode is `-p/--print`, so the template should generally include `-p` and pass the prompt as the final argument.

`notify_command_template`:

- Executed by the Stop hook script `scripts/issue-loop-notify.sh`.
- The hook exports:
  - `ISSUE_LOOP_MESSAGE` (short message)
  - `ISSUE_LOOP_PROJECT_DIR`
  - `ISSUE_LOOP_EVENT_NAME`
  - `ISSUE_LOOP_REASON`
  - `ISSUE_LOOP_TRANSCRIPT_PATH`
  - `ISSUE_LOOP_EVENT_JSON_B64` (base64-encoded hook input JSON)
