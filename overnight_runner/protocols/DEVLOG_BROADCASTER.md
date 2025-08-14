### Protocol: Devlog Broadcaster (Discord)

Use when
- You want agents to broadcast meaningful updates (assignments, syncs, verifies, FSM events, validations, pushes) to a shared Discord channel.

Prereqs
- Discord webhook URL for the target channel
- Optional: `.env` file in `D:\Agent_Cellphone` with:
```
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/XXX/YYY
DEVLOG_USERNAME=Agent Devlog
```

Verify webhook (recommended)
```powershell
python scripts/devlog_test.py
```

Listener-based devlogs (automatic)
- Start the inbox listener with devlog flags. It will post concise embeds when file-inbox messages arrive (e.g., `sync`, `verify`, `task`, `fsm_update`).
```powershell
python overnight_runner/listener.py --agent Agent-5 --env-file .env --devlog-embed --devlog-username "Agent Devlog"
```

Notes
- If `--devlog-webhook` is omitted, the listener uses `DISCORD_WEBHOOK_URL` from the environment or `.env`.
- FSM bridge also emits optional summaries for task assignment and updates; failures are silent so they never break the run.

Manual repo devlogs (on validate/push)
- Post a per-repo update to the devlog channel using the provided tools.

After validate
```powershell
./overnight_runner/tools/devlog_after_validate.ps1 -RepoPath D:\repositories\<repo>
```

Custom notify (validate/push/branch/extra)
```powershell
$env:DISCORD_WEBHOOK_URL = '<webhook>'
./overnight_runner/tools/devlog_notify_from_repo.ps1 -RepoPath D:\repositories\<repo> -Validated -Pushed -Branch feat/xyz -Extra "nightly run"
```

When to broadcast
- New task assignment (captain/FSM)
- Agent sync or verify with evidence
- Validation result for a repo
- Push or PR creation with brief description and link

Troubleshooting
- No posts: ensure webhook set in `.env` or pass `--devlog-webhook` explicitly
- HTTP 403/429: the tester retries briefly; wait and retry
- Stuck output in PowerShell: avoid piping to `cat` when running long commands







