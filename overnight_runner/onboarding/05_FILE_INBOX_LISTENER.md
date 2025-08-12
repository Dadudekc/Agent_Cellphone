### File Inbox Listener

[Back to Index](00_INDEX.md)

Start listener
```powershell
python overnight_runner/listener.py --agent Agent-3
```

Send JSON message (PowerShell, unified tool)
```powershell
./overnight_runner/tools/send-sync.ps1 -To Agent-3 -Type sync -Topic "10-min sync" -Summary "What changed, TODO, next" -From Agent-3
```

Schema
```json
{
  "type": "sync",
  "from": "Agent-1",
  "to": "Agent-3",
  "timestamp": "2025-08-11T08:00:00",
  "topic": "10-min sync",
  "summary": "free-form text",
  "details": {},
  "repos_updated": []
}
```

Additional examples (only schema-supported types shown)
```json
{ "type":"sync", "from":"Agent-3", "to":"Agent-1", "timestamp":"2025-08-11T08:00:00", "topic":"10-min sync", "summary":"changed/TODO/next.", "details":{} }
{ "type":"task", "from":"Agent-3", "to":"Agent-2", "timestamp":"2025-08-11T08:00:00", "topic":"task", "summary":"Implement one concrete improvement.", "details":{ "scope":"tests" } }
{ "type":"note", "from":"Agent-3", "to":"Agent-4", "timestamp":"2025-08-11T08:00:00", "topic":"custom", "summary":"Custom note with metadata", "details":{ "priority":"low" } }
{ "type":"ack", "from":"Agent-3", "to":"Agent-4", "timestamp":"2025-08-11T08:00:00", "topic":"ack", "summary":"Received and processing.", "details":{} }
```

Note: ACP UI tags like `[RESUME]` and `[VERIFY]` are not inbox `type`s. Use `sync`, `task`, `ack`, or `note` for file‑inbox messages.




[Back to Index](00_INDEX.md)
