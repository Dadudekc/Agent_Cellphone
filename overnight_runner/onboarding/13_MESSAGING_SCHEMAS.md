### Messaging Schemas

Unified inbox schema (recommended)
```json
{
  "type": "sync|ping|resume|verify|task|note|fsm_request|fsm_update|ui_request",
  "from": "Agent-3",
  "to": "Agent-2",
  "timestamp": "2025-08-11T08:00:00",
  "topic": "short topic",
  "summary": "human-readable summary",
  "details": { }
}
```

FSM request
```json
{
  "type": "fsm_request",
  "from": "Agent-3",
  "to": "Agent-5",
  "workflow": "default",
  "agents": ["Agent-1","Agent-2","Agent-4"]
}
```

FSM update
```json
{
  "type": "fsm_update",
  "from": "Agent-2",
  "to": "Agent-5",
  "task_id": "task-123",
  "state": "in_progress|blocked|done",
  "summary": "brief result",
  "evidence": { "commit": "...", "tests": "..." },
  "captain": "Agent-3"
}
```

UI request (Agent-5 UI orchestration)
```json
{
  "type": "ui_request",
  "from": "Agent-3",
  "to": "Agent-5",
  "intent": "open_new_chat_and_check_inbox",
  "task_id": "task-123",
  "payload": { "message": "New fsm_update posted.", "post_transition": "completed" }
}
```

FSM task assignment (emitted by Agent-5)
```json
{
  "type": "task",
  "from": "Agent-5",
  "to": "Agent-2",
  "timestamp": "2025-08-11T08:05:00",
  "task_id": "task-123",
  "repo": "unified-workspace",
  "intent": "add unit tests for API client retry/backoff",
  "acceptance_criteria": "Small, verifiable edit with tests/build evidence.",
  "evidence_required": "Link to commit/PR and test/build output."
}
```

### Messaging Schemas (File Inbox)

Filename pattern
- `msg_YYYYMMDD_HHMMSS_From_To.json`

Common fields
- `type`: sync | task | ack | note
- `from`: Agent-X
- `to`: Agent-Y | captain
- `timestamp`: ISO8601
- `topic`: short subject
- `summary`: 1–2 lines
- `details`: optional object
- `repos_updated`: optional array of { name, path, changes[], status }

Notes
- `[RESUME]`, `[VERIFY]`, etc. are ACP UI tags, not file‑inbox `type`s. For the inbox channel, prefer `sync`, `task`, `ack`, `note`.

Example
```json
{
  "type": "sync",
  "from": "Agent-4",
  "to": "Agent-3",
  "timestamp": "2025-08-11T08:00:00",
  "topic": "10-min sync",
  "summary": "Docs updated; tests added.",
  "repos_updated": [
    {"name": "unified-workspace", "changes": ["APIClient tests"], "status": "ok"}
  ]
}
```



[Back to Index](00_INDEX.md)


