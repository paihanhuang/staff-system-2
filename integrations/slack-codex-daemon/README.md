# Slack Codex Daemon

Continuously monitor Slack channels for commands and execute them using `codex exec`.

## Command format
The daemon executes only messages that match:

1. `<@BOT_USER_ID> your command here`
2. `codex: your command here`

It ignores bot messages and channel system events.

## Setup

1. Create env file:
```bash
cp integrations/slack-codex-daemon/.env.example integrations/slack-codex-daemon/.env
```

2. Edit `integrations/slack-codex-daemon/.env`:
- `SLACK_BOT_TOKEN`
- `SLACK_CHANNEL_IDS` (comma-separated)
- Optional `ALLOWED_USER_IDS` (recommended)

3. Start daemon:
```bash
integrations/slack-codex-daemon/run_daemon.sh
```

## Systemd (optional)
Install as a user service:
```bash
mkdir -p ~/.config/systemd/user
cp integrations/slack-codex-daemon/slack-codex-daemon.service ~/.config/systemd/user/
systemctl --user daemon-reload
systemctl --user enable --now slack-codex-daemon.service
systemctl --user status slack-codex-daemon.service
```

## Security defaults
- Keep `.env` local and secret.
- Restrict `SLACK_CHANNEL_IDS`.
- Use `ALLOWED_USER_IDS` to avoid arbitrary command execution.
- Keep `CODEX_EXEC_FLAGS` sandboxed.

## State
Processed timestamps are stored in:
`integrations/slack-codex-daemon/state.json`
