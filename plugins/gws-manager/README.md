English | [简体中文](README.zh-CN.md)

# gws-manager

A Claude Code plugin to manage parallel development workspaces (git worktrees) and advisory locks using the [gws](https://github.com/lollipopkit/gws) CLI tool.

## Installation

```bash
/plugin marketplace add lollipopkit/cc-plugins
/plugin install gws-manager@lk-ccp
```

## Features

- **Workspace Isolation**: Easily create, list, and remove parallel development workspaces using git worktrees.
- **Advisory Locking**: Coordinate with other agents or team members using advisory locks to prevent conflicting changes.
- **Automatic Suggestions**: Suggests creating a new workspace when significant changes are detected (via PreToolUse hook).
- **Environment Doctor**: Checks for `gws` CLI availability and workspace health on session start.

## Commands

- `/gws:new` – Create a new parallel development workspace.
- `/gws:list` – List all current workspaces.
- `/gws:rm` – Remove a workspace.
- `/gws:prune` – Prune stale workspaces.
- `/gws:lock` – Acquire an advisory lock on a resource.
- `/gws:unlock` – Release an advisory lock.
- `/gws:locks` – List all active advisory locks.
- `/gws:doctor` – Run a health check on the gws environment.
- `/gws:integrate` – Install/Update gws integration in the current project.

## Components

- **Agent**: `agents/workspace-agent.md` – Specialized agent for workspace and lock management.
- **Skill**: `skills/workspace-management/SKILL.md` – Core logic for complex workspace operations.
- **Hook**: `hooks/hooks.json` – Session start health checks and workspace creation suggestions.
