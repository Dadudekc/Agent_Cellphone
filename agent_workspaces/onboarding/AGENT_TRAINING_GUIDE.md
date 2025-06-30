# Agent Training Guide

## Status Reporting (Dream.OS Protocol)

**You MUST update your `status.json` after every action, state change, or message.**

- Use the provided `update_status` helper function.
- Always set a clear `message` for the user when waiting, busy, or on error.
- This enables real-time UI, monitoring, and agent-to-agent coordination.

Example:
```python
def update_status(agent_id, status, current_task, message=""):
    import os, json, datetime
    path = os.path.join(os.getcwd(), "status.json")
    data = {
        "agent_id": agent_id,
        "status": status,
        "current_task": current_task,
        "message": message,
        "last_updated": datetime.datetime.utcnow().isoformat() + "Z"
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
```

**Status values:**
- `ready` – idle, waiting for task
- `busy` – working on a task
- `paused` – waiting for input or paused
- `offline` – agent is stopped
- `error` – encountered a problem

**Message discipline:**
- Use the `message` field to communicate with the user (e.g., "Waiting for user input", "Paused for review", "Task complete!")
- Keep messages short and clear

---

(Review the onboarding checklist and summary for the full protocol.) 