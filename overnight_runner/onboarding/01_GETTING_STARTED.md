### Getting Started

[Back to Index](00_INDEX.md)

Prerequisites (5-agent default)
- Run from `D:\Agent_Cellphone`
- Python 3.9+ installed; `pyautogui` available (`pip install -r requirements.txt` if provided)
- Cursor windows visible and focused during ACP sends

Folders
- `src/agent_cell_phone.py` – ACP visible typing
- `overnight_runner/runner.py` – cadence prompts (supports plan=contracts to drive contract/task updates)
- `overnight_runner/listener.py` – file inbox listener
- `agent_workspaces/Agent-N/inbox` – JSON inbox per agent

Sanity check (PowerShell, 5-agent)
```powershell
python src/agent_cell_phone.py --layout 5-agent --list-agents --test
python src/agent_cell_phone.py --layout 5-agent --agent Agent-5 --msg "[VERIFY] Hello" --tag verify
```

Sanity check (bash, 5-agent)
```bash
python src/agent_cell_phone.py --layout 5-agent --list-agents --test
python src/agent_cell_phone.py --layout 5-agent --agent Agent-5 --msg "[VERIFY] Hello" --tag verify
```




[Back to Index](00_INDEX.md)
