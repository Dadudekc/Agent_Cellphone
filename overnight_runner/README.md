### Overnight Runner – Autonomous Multi‑Agent Coordination

This directory contains a small, opinionated toolkit to coordinate 4‑agent autonomous work sessions using the Agent Cell Phone (ACP) and an optional file‑inbox channel.

#### Components
- `runner.py`: schedules recurring prompts (resume/task/coordinate/sync/verify) to specific agents at a fixed cadence.
- `listener.py`: tails an agent’s `inbox/` folder for JSON messages and pushes them into the internal pipeline (Phase‑2 scaffold).
- ACP (already in `src/agent_cell_phone.py`): performs the visible UI typing to each agent’s Cursor input box based on calibrated coordinates.

#### What’s new (v2, captain‑less FSM mode)
- Captain‑less, FSM‑led cadence: no captain prompts; FSM assigns tasks from contracts and agents report back via inbox.
- Listener supports optional Discord devlogs via `.env` (no token, webhook only).
- Pacing controls to suppress noise (resume cooldown, active grace window, skip kickoff/assignments).

#### Prerequisites
- Run commands from `D:\Agent_Cellphone` so imports and paths resolve correctly.
- Calibrate coordinates once per layout/window move.
- Keep Cursor windows visible for ACP to click/type.

#### One‑time setup
1) Create `.env` in repo root:
```env
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/.../...
DEVLOG_USERNAME=Agent Devlog
```
2) Install dependencies:
```powershell
pip install -r requirements.txt
```
3) Calibrate agent coordinates (see below) once per layout/move.

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

#### Quick start (captain‑less FSM run)
Terminal A (listener + devlogs):
```powershell
python overnight_runner/listener.py --agent Agent-5 --env-file .env --devlog-embed --devlog-username "Agent Devlog" | cat
```
Terminal B (30–120 min cadence, captain‑less, FSM‑enabled, contracts‑tailored):
```powershell
$env:ACP_DEFAULT_NEW_CHAT='1'; $env:ACP_AUTO_ONBOARD='1'; $env:ACP_SINGLE_MESSAGE='1'; $env:ACP_MESSAGE_VERBOSITY='extensive'; $env:ACP_NEW_CHAT_INTERVAL_SEC='1800'

python overnight_runner/runner.py --layout 5-agent --agents Agent-1,Agent-2,Agent-3,Agent-4 \
  --duration-min 60 --interval-sec 1200 --sender Agent-3 --plan contracts \
  --fsm-enabled --fsm-agent Agent-5 --fsm-workflow default \
  --contracts-file D:/repositories/communications/overnight_YYYYMMDD_/Agent-5/contracts.json \
  --suppress-resume --skip-assignments --skip-captain-kickoff --skip-captain-fsm-feed \
  --resume-cooldown-sec 3600 --active-grace-sec 1200 \
  --initial-wait-sec 10 --phase-wait-sec 8 --stagger-ms 2500 --jitter-ms 800 \
  --comm-root D:/repositories/communications/overnight_YYYYMMDD_ --create-comm-folders | cat
```
What happens:
- Listener tails `agent_workspaces/Agent-5/inbox`, updates `state.json`, and posts Discord devlogs on task/sync/verify/fsm_update.
- Runner drops `fsm_request_*.json` each cycle; FSM assigns small, verifiable tasks round‑robin to Agents 1–4.
- Agents work and send `fsm_update` with state, summary, evidence (links/logs) back to Agent‑5 inbox.

Key flags:
- `--plan autonomous-dev`: rotates prompts that foster autonomous progress + peer coordination.
- `--resume-agents`: who receives each cycle’s prompts (captain receives kickoff only).
- `--stagger-ms`, `--jitter-ms`: spacing between per‑agent sends to avoid rapid focus switches.
- `--initial-wait-sec`, `--phase-wait-sec`: give time for kickoff/preamble/assignments to settle.
- Captain‑less pacing flags:
- `--suppress-resume`, `--resume-cooldown-sec`, `--active-grace-sec`, `--skip-assignments`, `--skip-captain-kickoff`, `--skip-captain-fsm-feed`.

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
- Discord not posting: ensure `.env` `DISCORD_WEBHOOK_URL` is set (no quotes/trailing spaces). Test with: `python scripts/devlog_test.py`.
- PowerShell pager noise: avoid piping to `cat` if commands appear stuck; re‑run without `| cat`.

#### If the system looks “broken” or updates seem lost
1) Sync code and deps:
```powershell
git fetch --all --prune
git pull --rebase origin main
pip install -r requirements.txt
```
2) Re‑verify coordinates (see calibration above) and `.env`.
3) Run the listener test post:
```powershell
python scripts/devlog_test.py
```
4) Start listener and cadence again (Quick start above).

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


