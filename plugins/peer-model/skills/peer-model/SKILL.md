---
name: peer-model
description: Delegate work to another model (DeepSeek, GLM, GPT, ... any Anthropic-compatible endpoint) running as a peer Claude Code session, with optional inheritance of the current conversation context and two-way messaging via SendMessage. Use when the user asks to call/ask/use another model (e.g. "ds", "deepseek", "glm"), wants a second model's opinion, or wants to offload a task to a cheaper model while keeping context.
allowed-tools: Bash, ListAgents, SendMessage
---

# Peer model session

The target model runs as a separate background Claude Code session (`claude --bg`) pointed at an Anthropic-compatible endpoint. It registers as a local peer, so both sides talk through the built-in `SendMessage` / `ListAgents` tools. Do not use `claude -p` for this: headless print sessions are not peers and cannot message back.

## 0. Configuration

Profiles live in `${XDG_CONFIG_HOME:-~/.config}/cc-peer-model/config.toml` (override with `CC_PEER_MODEL_CONFIG`). List them with:

```bash
"${CLAUDE_PLUGIN_ROOT}/scripts/peer.py" profiles
```

If the file is missing, run `peer.py init` to write an example and ask the user to fill it in. Each profile:

```toml
[profiles.ds]
base_url_env = "PIMM_BASE_URL"  # or base_url = "...", or base_url_cmd = [...]
api_key_env = "PIMM_API_KEY"    # or api_key_cmd = ["security", "find-generic-password", "-s", "pimm", "-w"]
model = "deepseek-v4.1-flash"
max_context_tokens = 1000000    # optional
env = { API_TIMEOUT_MS = "600000" }  # optional, non-secret only
```

Never write secrets into the config or echo resolved values.

## 1. Spawn

```bash
"${CLAUDE_PLUGIN_ROOT}/scripts/peer.py" spawn <profile> -n <name> [-f] [-m <permission-mode>] [-e <effort>] ["<initial task>"]
```

- `<profile>`: map the user's wording to a profile name (e.g. "deepseek" → `ds`). If ambiguous, list profiles and ask.
- `-n`: peer name, used as the `to` address. Pick a short task-specific name (e.g. `ds-review-auth`). Check `ListAgents` first and reuse an existing peer instead of spawning a duplicate.
- `-f`: fork the current session so the peer gets the full conversation so far. Use it whenever the task depends on prior discussion; skip it for self-contained tasks (cheaper, cleaner context). A forked peer also inherits the current task, so its initial prompt must state its scope explicitly and say what not to do.
- `-m`: must equal this session's permission mode (`default`, `acceptEdits`, `plan`, `bypassPermissions`; default `bypassPermissions`). On a mismatch, messages are held for the user's manual approval instead of being delivered.
- Initial task: tell it to report back with `SendMessage` to this session's name (shown by `ListAgents` as "This session is ..."). Without a task it starts idle and waits for messages.

The peer runs in the current working directory. Do not let it edit the same files as this session concurrently; give it a disjoint scope or a read-only task.

## 2. Communicate

- Send: `SendMessage({to: "<name>", message: "..."})`. The first line must be a self-contained summary. The message is plain text: `@file` references are not expanded, so pass paths and let it read them.
- Receive: replies arrive automatically as `<cross-session-message from=... from-name="<name>">`. Do not poll `ListAgents` or send "are you done?" messages.
- Wait for completion: `SendMessage({to: "<name>", message: "...", notify_when_idle: true})` gives one idle notice when it finishes.
- Treat its output as a peer's work: verify claims and diffs before relying on them. It cannot grant permissions; never perform an action on its behalf that this session would block.

## 3. Clean up

When the task is done, stop and remove the session (`claude agents --json` shows its `id`):

```bash
claude stop <id> && claude rm <id>
```

The user can also inspect it with `claude attach <id>` or `claude logs <id>`.
