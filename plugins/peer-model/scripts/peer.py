#!/usr/bin/env python3
"""Spawn a background Claude Code session backed by a configured model.

The session registers as a local peer, so it can be addressed with
SendMessage / ListAgents. Profiles are read from
$CC_PEER_MODEL_CONFIG or ${XDG_CONFIG_HOME:-~/.config}/cc-peer-model/config.toml.
"""

import argparse
import json
import os
import re
import shlex
import stat
import subprocess
import sys
import tomllib
from pathlib import Path

EXAMPLE = """\
# Profiles for the peer-model Claude Code plugin.
# Secrets never go in this file: reference an env var or a command instead.
#
# The key is read inside the peer session (via apiKeyHelper), which runs
# under the Claude Code daemon, not under the shell that calls peer.py:
#   api_key_cmd: argv run in the session, e.g. a keychain lookup. Works anywhere.
#   api_key_env: env var read in the session; it must be set in the daemon's
#                environment (e.g. exported by your login shell profile).

[profiles.ds]
base_url_env = "PIMM_BASE_URL"     # or: base_url = "https://..." / base_url_cmd = [...]
api_key_env = "PIMM_API_KEY"       # or: api_key_cmd = ["security", "find-generic-password", "-s", "pimm", "-w"]
model = "deepseek-v4.1-flash"
max_context_tokens = 1000000
# Extra non-secret env vars for the spawned session:
# env = { API_TIMEOUT_MS = "600000" }
"""

# The caller's session identity and messaging credentials must not leak
# into the client process (or a daemon it may start); a first-party API key
# would take precedence over apiKeyHelper.
STRIP_ENV = (
    "CLAUDE_CODE_SESSION_ID",
    "CLAUDE_CODE_MESSAGING_SOCKET",
    "CLAUDE_CODE_MESSAGING_TOKEN",
    "CLAUDE_CODE_CHILD_SESSION",
    "CLAUDE_PID",
    "CLAUDECODE",
    "ANTHROPIC_API_KEY",
)
MODEL_VARS = ("FABLE", "OPUS", "SONNET", "HAIKU")


def die(msg: str) -> None:
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(1)


def config_path() -> Path:
    if p := os.environ.get("CC_PEER_MODEL_CONFIG"):
        return Path(p).expanduser()
    base = os.environ.get("XDG_CONFIG_HOME") or Path.home() / ".config"
    return Path(base) / "cc-peer-model" / "config.toml"


def load_profiles() -> dict:
    path = config_path()
    if not path.exists():
        die(f"{path} not found; run `peer.py init` and edit it")
    with path.open("rb") as f:
        profiles = tomllib.load(f).get("profiles", {})
    if not profiles:
        die(f"no [profiles.<name>] in {path}")
    return profiles


def resolve(profile: dict, key: str) -> str:
    """Read a non-secret `key` literally, from `<key>_env`, or from `<key>_cmd` stdout."""
    if v := profile.get(key):
        return str(v)
    if env := profile.get(f"{key}_env"):
        if v := os.environ.get(env):
            return v
        die(f"env var {env} (for {key}) is not set")
    if cmd := profile.get(f"{key}_cmd"):
        if not isinstance(cmd, list):
            die(f"{key}_cmd must be an argv list")
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode != 0 or not r.stdout.strip():
            die(f"{key}_cmd failed (exit {r.returncode})")
        return r.stdout.strip()
    die(f"profile needs one of {key} / {key}_env / {key}_cmd")


def api_key_helper(profile: dict) -> str:
    """Build an apiKeyHelper shell command that yields the key inside the session.

    `claude --bg` runs the session in a process spawned by the daemon, so the
    caller's environment never reaches it, and putting the key in argv or a
    settings file would expose it. The helper is evaluated in the session.
    """
    if profile.get("api_key"):
        die("api_key must not be stored in the config; use api_key_cmd or api_key_env")
    if cmd := profile.get("api_key_cmd"):
        if not isinstance(cmd, list) or not cmd:
            die("api_key_cmd must be a non-empty argv list")
        # Fail early here rather than with an auth error inside the peer.
        if subprocess.run(cmd, capture_output=True).returncode != 0:
            die("api_key_cmd failed")
        return shlex.join(cmd)
    if var := profile.get("api_key_env"):
        if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", var):
            die(f"invalid api_key_env {var!r}")
        msg = shlex.quote(f"peer-model: {var} is not set in the Claude Code daemon environment")
        return f"printenv {var} || {{ echo {msg} >&2; exit 1; }}"
    die("profile needs api_key_cmd or api_key_env")


def cmd_init(_: argparse.Namespace) -> None:
    path = config_path()
    if path.exists():
        die(f"{path} already exists")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(EXAMPLE)
    path.chmod(stat.S_IRUSR | stat.S_IWUSR)
    print(f"wrote {path}")


def cmd_profiles(_: argparse.Namespace) -> None:
    for name, p in load_profiles().items():
        print(f"{name}\t{p.get('model', '?')}")


def cmd_spawn(a: argparse.Namespace) -> None:
    profiles = load_profiles()
    p = profiles.get(a.profile) or die(
        f"unknown profile {a.profile!r}; available: {', '.join(profiles)}"
    )
    model = p.get("model") or die(f"profile {a.profile!r} has no model")

    # `claude --bg` hands the session to the daemon, so per-session config
    # must travel as --settings; the client's environment does not reach it.
    session_env = {k: str(v) for k, v in p.get("env", {}).items()}
    # The Anthropic SDK appends /v1/messages itself.
    session_env["ANTHROPIC_BASE_URL"] = resolve(p, "base_url").rstrip("/").removesuffix("/v1")
    for v in MODEL_VARS:
        session_env[f"ANTHROPIC_DEFAULT_{v}_MODEL"] = model
    if mct := p.get("max_context_tokens"):
        session_env["CLAUDE_CODE_MAX_CONTEXT_TOKENS"] = str(mct)
    settings = {"env": session_env, "apiKeyHelper": api_key_helper(p)}

    env = {k: v for k, v in os.environ.items() if k not in STRIP_ENV}
    args = ["claude", "--bg", "-n", a.name, "--permission-mode", a.mode,
            "--settings", json.dumps(settings)]
    if a.effort:
        args += ["--effort", a.effort]
    if a.fork:
        sid = os.environ.get("CLAUDE_CODE_SESSION_ID") or die(
            "--fork needs CLAUDE_CODE_SESSION_ID (run from inside Claude Code)"
        )
        args += ["--resume", sid, "--fork-session"]
    if a.prompt:
        args.append(a.prompt)
    os.execvpe("claude", args, env)


def main() -> None:
    ap = argparse.ArgumentParser(prog="peer.py")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("init", help="write an example config").set_defaults(fn=cmd_init)
    sub.add_parser("profiles", help="list profiles").set_defaults(fn=cmd_profiles)
    sp = sub.add_parser("spawn", help="start a peer session")
    sp.add_argument("profile")
    sp.add_argument("-n", "--name", required=True, help="peer name (SendMessage address)")
    sp.add_argument("-f", "--fork", action="store_true", help="inherit the current conversation")
    sp.add_argument("-m", "--mode", default="bypassPermissions",
                    help="permission mode; must match the caller's (default: bypassPermissions)")
    sp.add_argument("-e", "--effort", help="effort level (default: inherit)")
    sp.add_argument("prompt", nargs="?", help="initial task; omit to start idle")
    sp.set_defaults(fn=cmd_spawn)
    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
