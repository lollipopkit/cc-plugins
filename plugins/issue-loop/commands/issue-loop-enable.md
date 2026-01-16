---
name: issue-loop-enable
description: Quickly enable issue-loop for this repo by creating or updating `.claude/issue-loop.local.md`.
allowed-tools: ["Read", "Write", "Edit", "AskUserQuestion"]
---

Enable issue-loop for the current project.

Steps:

1. Ensure a `.claude/` directory exists in the project root.
2. If `.claude/issue-loop.local.md` exists, update frontmatter keys:
   - `enabled: true`
3. If it does not exist, create it with a minimal template and safe defaults.
4. Ask user for:
   - `review_mode` (default: `github`)
   - `llm_command_template` (optional)
   - `llm_shell` (auto|bash|fish)
   - `notify_enabled` (true/false)
   - `notify_command_template` (optional)
   - `notify_shell` (auto|bash|fish)
5. Remind that hook config is loaded at session start; restart Claude Code for hook changes to take effect.

Notes:

- `llm_command_template` may reference `$ISSUE_LOOP_PROMPT`.
- `notify_command_template` may reference `$ISSUE_LOOP_MESSAGE` and `$ISSUE_LOOP_EVENT_JSON_B64`.
