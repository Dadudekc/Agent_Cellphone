### New Agent Quickstart (3 steps)

[Back to Index](00_INDEX.md)

Run all commands from `D:\Agent_Cellphone`.

1) Calibrate (5‑agent default) and verify for your ID (example: Agent‑5)
```powershell
# Capture input box (hover over your Cursor input box for ~6s when prompted)
python overnight_runner/tools/capture_coords.py --layout 5-agent --agent Agent-5 --delay 6

# Verify message lands
python src/agent_cell_phone.py --layout 5-agent --agent Agent-5 --msg "[VERIFY] Live calibration: Agent-5" --tag verify
```

2) Start overnight runner (captain Agent‑3; 5‑minute cadence; 5‑agent)
```powershell
python overnight_runner/runner.py --layout 5-agent --captain Agent-3 --resume-agents Agent-1,Agent-2,Agent-4,Agent-5 \
  --duration-min 480 --interval-sec 300 --sender Agent-3 --plan autonomous-dev \
  --initial-wait-sec 60 --phase-wait-sec 15 --stagger-ms 2500 --jitter-ms 1000 \
  --comm-root D:/repositories/communications/overnight_YYYYMMDD_ --create-comm-folders
```

Optional (denser 3‑minute cadence, include self each cycle):
```powershell
python overnight_runner/runner.py --layout 5-agent --captain Agent-3 --resume-agents Agent-1,Agent-2,Agent-3,Agent-4,Agent-5 \
  --duration-min 240 --interval-sec 180 --sender Agent-3 --plan autonomous-dev \
  --initial-wait-sec 10 --phase-wait-sec 5 --stagger-ms 1500 --jitter-ms 600 \
  --comm-root D:/repositories/communications/overnight_YYYYMMDD_
```

3) (Optional) Start file‑inbox listener for silent JSON messaging
```powershell
python overnight_runner/listener.py --agent Agent-5 --env-file .env --devlog-embed --devlog-username "Agent Devlog"
```

Optional: Enable Discord devlogs
```powershell
@"
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/XXX/YYY
DEVLOG_USERNAME=Agent Devlog
"@ | Set-Content -Path .env -Encoding UTF8
python scripts/devlog_test.py
```

Tips
- Open each repo’s `TASK_LIST.md`, pick one high‑leverage item, update status as you work
- Prefer reuse/refactor; avoid duplication, stubs, or shims
- Commit small, verifiable edits; add tests/build steps where practical



[Back to Index](00_INDEX.md)
