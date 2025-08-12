### Calibration (5‑Agent default)

[Back to Index](00_INDEX.md)

Step 1 – capture input box position (PowerShell)
```powershell
python overnight_runner/tools/capture_coords.py --layout 5-agent --agent Agent-5 --delay 6
```

Step 1 (bash)
```bash
python overnight_runner/tools/capture_coords.py --layout 5-agent --agent Agent-5 --delay 6
```

Step 2 – verify delivery (PowerShell)
```powershell
python src/agent_cell_phone.py --layout 5-agent --agent Agent-5 --msg "[VERIFY] Live calibration: Agent-5" --tag verify
```

Step 2 (bash)
```bash
python src/agent_cell_phone.py --layout 5-agent --agent Agent-5 --msg "[VERIFY] Live calibration: Agent-5" --tag verify
```

Repeat for other agents in your layout. Re‑calibrate after moving/tiling windows.

Note: Avoid long inline one‑liners in interactive shells; use the helper script `overnight_runner/tools/capture_coords.py` to prevent PSReadLine buffer issues.




[Back to Index](00_INDEX.md)
