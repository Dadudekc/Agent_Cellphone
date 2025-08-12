# Agent Communication & Self-Prompting Guide

This guide explains how an agent communicates with another agent or prompts itself using the Agent Cell Phone (ACP) system. It covers two channels:

- Mechanical messaging via coordinates (PyAutoGUI) — visible typing in Cursor windows
- File inbox listener — JSON messages tailed from a folder into the message pipeline

## 1) Mechanical messaging (visible UI typing)

- Purpose: Deterministic, human-visible keystrokes across 2/4/8-agent layouts
- Component: `src/agent_cell_phone.py` (CLI and API)
- Coordinates: `src/runtime/config/cursor_agent_coords.json`

Environment assumption: Agents are Cursor-based and operate on the same repositories/files. ACP types into Cursor input boxes; use shared repo-relative paths in prompts and respect `TASK_LIST.md` and `status.json` for coordination.

### Quick start (CLI)

- Test mode (no mouse/keyboard movement):
```
python src/agent_cell_phone.py --layout 2-agent --agent Agent-2 --msg "Hello (test)" --test
```
- Live mode (moves mouse, types, presses Enter):
```
python src/agent_cell_phone.py --layout 2-agent --agent Agent-2 --msg "Hello (live)"
```

Notes:
- Self-prompting: set `--agent` to your own ID (e.g., `Agent-2`)
- Broadcast: omit `--agent` to send to all agents in the layout
- Tags: `--tag resume|sync|verify|task|reply|coordinate|onboarding|normal`

### Python API (self or other agent)

```python
from agent_cell_phone import AgentCellPhone, MsgTag

acp = AgentCellPhone('Agent-2', layout_mode='2-agent')
# Self-prompt
acp.send('Agent-2', 'Think aloud: summarize current task', MsgTag.REPLY)
# Message another agent
acp.send('Agent-3', 'Please prepare API contract for /resume', MsgTag.COORDINATE)
# Broadcast
acp.broadcast('Stand-up in 2 minutes', MsgTag.SYNC)
```

### Coordinate calibration

- Use the oneliner to capture the current cursor position for an agent input box:
```
python -c "import time, json, pyautogui; p='src/runtime/config/cursor_agent_coords.json';\
print('Hover over Agent-2 input box...'); time.sleep(5); x,y=pyautogui.position();\
import json; d=json.load(open(p,'r',encoding='utf-8')); d.setdefault('2-agent',{});\
d['2-agent'].setdefault('Agent-2',{}); d['2-agent']['Agent-2']['input_box']={'x':int(x),'y':int(y)};\
json.dump(d, open(p,'w',encoding='utf-8'), indent=2); print('Updated',p)"
```

## 2) File inbox listener (JSON pipeline)

- Purpose: Silent, scriptable inter-project messaging
- Components:
  - Listener: `src/core/inbox_listener.py`
  - Pipeline: `src/core/message_pipeline.py`
  - Router: `src/core/command_router.py` (default commands: `ping`, `resume`, `sync`)

### Folder convention

- Create an inbox folder for each agent, e.g. `agent_workspaces/Agent-2/inbox`

### Start a listener

```python
from src.core.inbox_listener import InboxListener
from src.core.message_pipeline import MessagePipeline
from src.core.command_router import CommandRouter

pipeline = MessagePipeline()
router = CommandRouter()

# Handle queued messages
item = pipeline.process_once()  # returns (to_agent, message) or None

# Start tailing the inbox
listener = InboxListener(inbox_dir='agent_workspaces/Agent-2/inbox', pipeline=pipeline)
listener.start()
```

### Send a message via file drop (from another project)

- Write a JSON file in the target inbox (unique filename):
```
{
  "from": "Agent-3",
  "to": "Agent-2",
  "message": "hello",
  "command": "ping",
  "args": {}
}
```
- The listener enqueues `(to, message)`. If you also want command handling, route it:
```python
result = router.route('ping', {"from":"Agent-3","to":"Agent-2","message":"hello"})
# result -> {"ok": True, "type": "pong", "echo": {...}}
```

## 3) Self-prompting patterns

- Mechanical: send to your own ID (`Agent-N`) with a descriptive tag (e.g., `[REPLY]`, `[TASK]`).
- File-based: drop a JSON into your own inbox with a `command` (e.g., `resume`) or a free-form `message` for journaling.

Examples:
- “Plan next 3 steps for ticket #123”
- “Summarize PRD deltas before sync”
- “Run tests and report failures by file”

## 4) Command router (built-ins)

- `ping` → `{ok: true, type: "pong"}`
- `resume` → `{ok: true, agent: <id>, action: "resume", status: "online"}`
- `sync` → `{ok: true, agent: <id>, action: "sync", status: "in-sync"}`

Add your own:
```python
from src.core.command_router import CommandRouter
router = CommandRouter()

def assign_task(payload):
    return {"ok": True, "agent": payload.get("to","unknown"), "action": "assign_task", "task": payload.get("task")}

router.register('assign_task', assign_task)
```

## 5) Best practices

- Keep coordinates fresh if windows move (use the calibration oneliner)
- Prefer file inbox for cross-repo automation; use ACP live typing for visible synchronization
- Tag messages consistently (e.g., `[COORDINATE]`, `[TASK]`, `[SYNC]`)
- Use unique JSON filenames (e.g., timestamps) to avoid collisions

## 6) Troubleshooting

- No typing? Check `cursor_agent_coords.json` and Cursor windows are visible
- Listener idle? Verify inbox path and JSON validity
- Import errors? Run from project root so `src/` is on `PYTHONPATH`
- Test-only run: add `--test` to ACP CLI to avoid moving mouse/keyboard

---
This guide complements `docs/INTER_AGENT_COMMUNICATION_GUIDE.md` and focuses on practical, minimal steps for agent-to-agent and self messaging.
