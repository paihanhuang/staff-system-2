#!/usr/bin/env python3
"""Poll Slack channels for @codex commands and execute via codex exec."""

from __future__ import annotations

import json
import os
import re
import shlex
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any


MENTION_RE = re.compile(r"^\s*<@([A-Z0-9]+)>\s+(.*)$", re.DOTALL)
PREFIX_RE = re.compile(r"^\s*codex\s*:\s*(.*)$", re.IGNORECASE | re.DOTALL)


@dataclass
class Config:
    slack_bot_token: str
    channel_ids: list[str]
    workspace_dir: str
    poll_interval_seconds: int
    codex_exec_flags: list[str]
    codex_timeout_seconds: int
    allowed_user_ids: set[str]
    state_file: Path
    start_from_latest: bool


def load_env_file(path: Path) -> None:
    if not path.exists():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


def get_required(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise ValueError(f"Missing required environment variable: {name}")
    return value


def parse_config() -> Config:
    channels_raw = get_required("SLACK_CHANNEL_IDS")
    channel_ids = [c.strip() for c in channels_raw.split(",") if c.strip()]
    if not channel_ids:
        raise ValueError("SLACK_CHANNEL_IDS must contain at least one channel ID")

    flags = shlex.split(os.getenv("CODEX_EXEC_FLAGS", "--full-auto"))
    allowed_users = {
        x.strip()
        for x in os.getenv("ALLOWED_USER_IDS", "").split(",")
        if x.strip()
    }
    state_file = Path(os.getenv("DAEMON_STATE_FILE", "integrations/slack-codex-daemon/state.json"))
    start_from_latest = os.getenv("START_FROM_LATEST", "true").lower() in {"1", "true", "yes"}

    return Config(
        slack_bot_token=get_required("SLACK_BOT_TOKEN"),
        channel_ids=channel_ids,
        workspace_dir=os.getenv("WORKSPACE_DIR", str(Path.cwd())),
        poll_interval_seconds=int(os.getenv("POLL_INTERVAL_SECONDS", "15")),
        codex_exec_flags=flags,
        codex_timeout_seconds=int(os.getenv("CODEX_TIMEOUT_SECONDS", "1800")),
        allowed_user_ids=allowed_users,
        state_file=state_file,
        start_from_latest=start_from_latest,
    )


def slack_api(token: str, method: str, data: dict[str, Any]) -> dict[str, Any]:
    body = urllib.parse.urlencode(data).encode("utf-8")
    req = urllib.request.Request(
        f"https://slack.com/api/{method}",
        data=body,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/x-www-form-urlencoded",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f"Slack API HTTP error on {method}: {exc.code}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Slack API network error on {method}: {exc.reason}") from exc

    if not payload.get("ok", False):
        raise RuntimeError(f"Slack API {method} failed: {payload.get('error', 'unknown_error')}")
    return payload


def read_state(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def write_state(path: Path, state: dict[str, str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, indent=2, sort_keys=True), encoding="utf-8")


def get_latest_ts(config: Config, channel_id: str) -> str:
    payload = slack_api(
        config.slack_bot_token,
        "conversations.history",
        {"channel": channel_id, "limit": 1, "inclusive": "true"},
    )
    messages = payload.get("messages", [])
    if not messages:
        return "0"
    return messages[0].get("ts", "0")


def extract_command(message: dict[str, Any], bot_user_id: str) -> str | None:
    text = message.get("text", "")
    mention = MENTION_RE.match(text)
    if mention and mention.group(1) == bot_user_id:
        return mention.group(2).strip()

    prefixed = PREFIX_RE.match(text)
    if prefixed:
        return prefixed.group(1).strip()
    return None


def run_codex_command(config: Config, command: str) -> str:
    output_file = Path("/tmp/slack_codex_last_message.txt")
    if output_file.exists():
        output_file.unlink()

    cmd = [
        "codex",
        "exec",
        *config.codex_exec_flags,
        "-C",
        config.workspace_dir,
        "-o",
        str(output_file),
        command,
    ]
    proc = subprocess.run(
        cmd,
        text=True,
        capture_output=True,
        timeout=config.codex_timeout_seconds,
        check=False,
    )

    if output_file.exists():
        result = output_file.read_text(encoding="utf-8").strip()
    else:
        result = proc.stdout.strip() or proc.stderr.strip()

    if proc.returncode != 0:
        err = proc.stderr.strip() or proc.stdout.strip() or "unknown failure"
        return f"Command failed (exit {proc.returncode}).\n{err}"
    return result or "Completed with no output."


def post_reply(config: Config, channel_id: str, thread_ts: str, text: str) -> None:
    chunks = chunk_text(text, 3500)
    for chunk in chunks:
        slack_api(
            config.slack_bot_token,
            "chat.postMessage",
            {"channel": channel_id, "thread_ts": thread_ts, "text": chunk},
        )


def chunk_text(text: str, size: int) -> list[str]:
    text = text.strip()
    if len(text) <= size:
        return [text]
    parts: list[str] = []
    start = 0
    while start < len(text):
        parts.append(text[start : start + size])
        start += size
    return parts


def should_process_message(config: Config, message: dict[str, Any]) -> bool:
    if message.get("subtype"):
        return False
    if message.get("bot_id"):
        return False
    user = message.get("user")
    if not user:
        return False
    if config.allowed_user_ids and user not in config.allowed_user_ids:
        return False
    return True


def main() -> int:
    env_path = Path(os.getenv("DAEMON_ENV_FILE", "integrations/slack-codex-daemon/.env"))
    load_env_file(env_path)
    config = parse_config()

    auth = slack_api(config.slack_bot_token, "auth.test", {})
    bot_user_id = auth.get("user_id")
    if not bot_user_id:
        raise RuntimeError("Could not determine bot user_id via auth.test")

    state = read_state(config.state_file)
    if config.start_from_latest:
        for channel_id in config.channel_ids:
            if channel_id not in state:
                state[channel_id] = get_latest_ts(config, channel_id)
        write_state(config.state_file, state)

    while True:
        for channel_id in config.channel_ids:
            last_ts = state.get(channel_id, "0")
            payload = slack_api(
                config.slack_bot_token,
                "conversations.history",
                {
                    "channel": channel_id,
                    "oldest": last_ts,
                    "inclusive": "false",
                    "limit": 50,
                },
            )
            messages = payload.get("messages", [])
            messages.sort(key=lambda m: float(m.get("ts", "0")))

            for message in messages:
                ts = message.get("ts", "0")
                state[channel_id] = ts
                if not should_process_message(config, message):
                    continue

                command = extract_command(message, bot_user_id)
                if not command:
                    continue

                thread_ts = message.get("thread_ts") or ts
                try:
                    result = run_codex_command(config, command)
                except subprocess.TimeoutExpired:
                    result = f"Command timed out after {config.codex_timeout_seconds} seconds."
                except Exception as exc:  # pragma: no cover
                    result = f"Daemon execution error: {exc}"

                post_reply(config, channel_id, thread_ts, result)
                write_state(config.state_file, state)

            write_state(config.state_file, state)
        time.sleep(config.poll_interval_seconds)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        raise SystemExit(0)
    except Exception as exc:  # pragma: no cover
        print(f"FATAL: {exc}", file=sys.stderr)
        raise SystemExit(1)
