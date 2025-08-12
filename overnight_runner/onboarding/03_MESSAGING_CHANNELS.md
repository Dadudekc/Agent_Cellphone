### Messaging Channels

[Back to Index](00_INDEX.md)

Visible typing (ACP)
- Sends messages into Cursor input boxes via calibrated coordinates
- Single send:
```powershell
python src/agent_cell_phone.py --layout 4-agent --agent Agent-3 --msg "[RESUME] Resume autonomous development" --tag resume
```

File system inbox (silent)
- Each agent has `agent_workspaces/Agent-N/inbox`
- Drop JSON files in unified schema (see `13_MESSAGING_SCHEMAS.md`)
```json
{
  "type": "sync",
  "from": "Agent-3",
  "to": "Agent-3",
  "timestamp": "2025-08-11T08:00:00",
  "topic": "10-min sync",
  "summary": "What changed, open TODO, next verifiable action.",
  "details": {}
}
```

Start a listener (PowerShell)
```powershell
python overnight_runner/listener.py --agent Agent-3
```

Start a listener (bash)
```bash
python overnight_runner/listener.py --agent Agent-3
```

Send a message using the unified tool (preferred)
```powershell
./overnight_runner/tools/send-sync.ps1 -To Agent-3 -Type sync -Topic "10-min sync" -Summary "What changed, TODO, next" -From Agent-3
```




[Back to Index](00_INDEX.md)
