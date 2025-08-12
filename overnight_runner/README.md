### Overnight Runner – Autonomous Multi‑Agent Coordination

This directory contains a small, opinionated toolkit to coordinate 4‑agent autonomous work sessions using the Agent Cell Phone (ACP) and an optional file‑inbox channel.

#### Components
- `runner.py`: schedules recurring prompts (resume/task/coordinate/sync/verify) to specific agents at a fixed cadence.
- `listener.py`: tails an agent’s `inbox/` folder for JSON messages and pushes them into the internal pipeline (Phase‑2 scaffold).
- ACP (already in `src/agent_cell_phone.py`): performs the visible UI typing to each agent’s Cursor input box based on calibrated coordinates.

#### Prerequisites
- Run commands from `D:\Agent_Cellphone` so imports and paths resolve correctly.
- Calibrate coordinates once per layout/window move.
- Keep Cursor windows visible for ACP to click/type.

Conventions
- Paths in examples may use forward slashes but target Windows paths.
- Timestamps are ISO8601 (`ToString('o')`).
- Prefer the unified messaging tool `overnight_runner/tools/send-sync.ps1`.

#### Coordinate calibration (4‑agent)
1) Hover over the agent’s input box when prompted (≈6s):
```powershell
python -c "import time,json,pyautogui; p='src/runtime/config/cursor_agent_coords.json'; print('Hover over Agent-1 input box (4-agent)...'); time.sleep(6); x,y=pyautogui.position(); d=json.load(open(p,'r',encoding='utf-8')); d.setdefault('4-agent',{}); d['4-agent'].setdefault('Agent-1',{}); d['4-agent']['Agent-1']['input_box']={'x':int(x),'y':int(y)}; d['4-agent']['Agent-1']['starter_location_box']={'x':int(x),'y':int(y)}; json.dump(d, open(p,'w',encoding='utf-8'), indent=2); print('Updated',x,y)"
```
2) Verify delivery to that agent:
```powershell
python src/agent_cell_phone.py --layout 4-agent --agent Agent-1 --msg "[VERIFY] Live calibration: Agent-1" --tag verify
```

#### Start a 5‑agent captain run (autonomous‑dev plan)
Captain is `Agent-5` (FSM orchestrator). `Agent-3` acts as Coordination Manager. Cycle prompts go to the `--resume-agents` list.

- 5‑minute cadence (8 hours), FSM‑enabled:
```powershell
python overnight_runner/runner.py --layout 5-agent --captain Agent-5 --resume-agents Agent-1,Agent-2,Agent-3,Agent-4 \
  --duration-min 480 --interval-sec 300 --sender Agent-3 --plan autonomous-dev \
  --fsm-enabled --fsm-agent Agent-5 --fsm-workflow default \
  --initial-wait-sec 60 --phase-wait-sec 15 --stagger-ms 2500 --jitter-ms 1000 \
  --comm-root D:/repositories/communications/overnight_YYYYMMDD_ --create-comm-folders
```

- 3‑minute cadence (denser updates), include self in cycle:
```powershell
python overnight_runner/runner.py --layout 4-agent --captain Agent-3 --resume-agents Agent-1,Agent-2,Agent-3,Agent-4 \
  --duration-min 480 --interval-sec 180 --sender Agent-3 --plan autonomous-dev \
  --initial-wait-sec 10 --phase-wait-sec 5 --stagger-ms 1500 --jitter-ms 600 \
  --comm-root D:/repositories/communications/overnight_YYYYMMDD_
```

Key flags:
- `--plan autonomous-dev`: rotates prompts that foster autonomous progress + peer coordination.
- `--resume-agents`: who receives each cycle’s prompts (captain receives kickoff only).
- `--stagger-ms`, `--jitter-ms`: spacing between per‑agent sends to avoid rapid focus switches.
- `--initial-wait-sec`, `--phase-wait-sec`: give time for kickoff/preamble/assignments to settle.

#### Use repo task lists (anti‑duplication)
- Before coding, open each repo’s `TASK_LIST.md` to select work and update status.
- Prefer reuse/refactor across repos; avoid duplication, stubs, or shims.
- Commit small, verifiable edits; add tests/build steps where practical.

#### File‑system messaging (silent channel)
Start a listener for an agent (e.g., Agent‑3):
```powershell
python overnight_runner/listener.py --agent Agent-3
```
Send a message by dropping JSON into the inbox:
```powershell
# Path: agent_workspaces/Agent-3/inbox/sync_YYYYMMDD_HHMMSS.json
{
  "from": "Agent-3",
  "to": "Agent-3",
  "message": "Agent-3 10-min sync: what changed, open TODO, and the next verifiable action.",
  "command": "sync",
  "args": {}
}
```

#### Common pitfalls
- “File not found” when running tools: ensure you’re in `D:\Agent_Cellphone` (not `D:\repositories`).
- No typing: re‑check `src/runtime/config/cursor_agent_coords.json` and that Cursor windows are visible.
- Too chatty: increase `--interval-sec`, or raise `--stagger-ms`/`--initial-wait-sec`.

#### Quick one‑offs
- List agents in layout:
```powershell
python src/agent_cell_phone.py --layout 4-agent --list-agents --test
```
- Send a single resume to an agent:
```powershell
python src/agent_cell_phone.py --layout 4-agent --agent Agent-2 --msg "Resume autonomous development: choose the highest-leverage task and begin now." --tag resume
```

#### What the autonomous‑dev plan sends
In cycles, the runner rotates:
- `[RESUME]` resume autonomous development
- `[TASK]` implement one concrete improvement (tests/build/lint/docs/refactor)
- `[COORDINATE]` prompt a peer for a quick sanity check; incorporate feedback
- `[SYNC]` 10‑minute status: changed, open TODO, next verifiable action
- `[VERIFY]` verify outcomes (tests/build); stage diffs and summarize if blocked

This balances momentum with collaboration while avoiding duplication.


