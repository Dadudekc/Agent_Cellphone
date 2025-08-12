### Ops Runbooks

Overnight runner
- Cadence: 5‑min; slower pacing to avoid thrash
- Start/stop: see `04_OVERNIGHT_RUNNER.md`
- Logs: `D:\repositories\communications\overnight_YYYYMMDD_`

Inbox listeners
- Verify watcher running; check recent `sync_*.json`
- Paths: `...\agent_workspaces\Agent-X\inbox`

Incidents
- Pause runner; capture logs; revert last change if needed
- Notify captain; file a task in the relevant repo `TASK_LIST.md`



[Back to Index](00_INDEX.md)



