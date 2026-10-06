#!/usr/bin/env python3
"""Spawn a background Claude Code session backed by a configured model.

The session registers as a local peer, so it can be addressed with
SendMessage / ListAgents. Profiles are read from
$CC_PEER_MODEL_CONFIG or ${XDG_CONFIG_HOME:-~/.config}/cc-peer-model/config.toml.
"""

import argparse
import os
import stat
import subprocess
import sys
import tomllib
from pathlib import Path

EXAMPLE = """\
# Profiles for the peer-model Claude Code plugin.
# Secrets never go in this file: reference an env var or a command instead.

[profiles.ds]
base_url_env = "PIMM_BASE_URL"     # or: base_url = "https://example.com/anthropic"
api_key_env = "PIMM_API_KEY"       # or: api_key_cmd = ["security", "find-generic-password", "-s", "pimm", "-w"]
model = "deepseek-v4.1-flash"
max_context_tokens = 1000000
# Extra non-secret env vars for the spawned session:
# env = { API_TIMEOUT_MS = "600000" }
"""

# The caller's session identity and messaging credentials must not leak
# into the child; a first-party API key would override the auth token.
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
    """Read `key` literally, from `<key>_env`, or from `<key>_cmd` stdout."""
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

    env = {k: v for k, v in os.environ.items() if k not in STRIP_ENV}
    env.update({k: str(v) for k, v in p.get("env", {}).items()})
    # The Anthropic SDK appends /v1/messages itself.
    env["ANTHROPIC_BASE_URL"] = resolve(p, "base_url").rstrip("/").removesuffix("/v1")
    env["ANTHROPIC_AUTH_TOKEN"] = resolve(p, "api_key")
    for v in MODEL_VARS:
        env[f"ANTHROPIC_DEFAULT_{v}_MODEL"] = model
    if mct := p.get("max_context_tokens"):
        env["CLAUDE_CODE_MAX_CONTEXT_TOKENS"] = str(mct)

    args = ["claude", "--bg", "-n", a.name, "--permission-mode", a.mode]
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
