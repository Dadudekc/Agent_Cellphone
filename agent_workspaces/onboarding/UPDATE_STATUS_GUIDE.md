# Agent Status File – Update Guide

Every agent maintains a `status.json` file inside its workspace directory:
```
agent_workspaces/Agent-X/status.json
```

## Required Keys
| Key | Description |
|-----|-------------|
| `agent_id` | Your agent identifier (`Agent-1`, `Agent-2`, …) |
| `status` | Current heartbeat state. Allowed values:<br> `ready`, `busy`, `paused`, `offline`, `error` |
| `current_task` | Short description of the task you are actively working on. Use `none` if idle. |
| `message` | (Optional) Any message you want to display to the user. |
| `last_updated` | ISO-8601 UTC timestamp you touched the file. |

Example:
```json
{
  "agent_id": "Agent-2",
  "status": "busy",
  "current_task": "Compiling daily report",
  "message": "Waiting for user input",
  "last_updated": "2025-06-30T18:27:42Z"
}
```

## **MANDATORY ONBOARDING RULE**
**After every action, state change, or message, you MUST update your `status.json` with your new status, current task, message, and timestamp.**

- This is required for all agents, at all times.
- The UI and other agents rely on this for coordination and monitoring.

## How to Update (Python Helper)
Add this function to your agent code and call it after every action:
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

## When to Update
1. **Start-up / Heartbeat** – set `status` to `ready`.
2. **Task change** – update `current_task` and set `status` to `busy`.
3. **Paused / Waiting** – set `status` to `paused`.
4. **Shut-down** – set `status` to `offline`.
5. **Any message to user** – update `message`.

## Validation
`scripts/update_agent_status.py` will fill missing keys but **will not** overwrite your `status`, `current_task`, or `message`. Keep them accurate!

---
*Document version 1.1 – onboarding rule and helper function added (June 2025)* 