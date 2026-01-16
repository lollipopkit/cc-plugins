---
name: dev-loop
description: Start or resume the dev-loop workflow (create branch → fix → commit → PR → wait for AI review → apply comments → repeat).
allowed-tools: ["Read", "Write", "Edit", "Grep", "Glob", "Bash", "AskUserQuestion", "TodoWrite", "Task"]
argument-hint: "--issue <github-url|number|text|file> [--base main]"
---

Run the dev-loop workflow using the plugin components in this plugin.

Behavior:

1. Determine the issue source:
   - If the argument looks like a GitHub URL or issue/PR number, use `gh` to fetch title/body, labels, repo, and existing PR linkage.
   - If the argument looks like a local file path, read it and treat it as the issue/task description.
   - Otherwise, treat it as a free-form text task.
2. Read settings from `.claude/dev-loop.local.md` if present.
3. Invoke the loop agent `dev-loop-runner` to execute the full fix/review cycle.

Rules:

- Always start by creating a new branch based on the issue content.
- Avoid destructive operations.
- If review comments request changes that look incorrect or out-of-scope, ask the user before proceeding.
- Prefer using `gh` for GitHub workflows when available.
