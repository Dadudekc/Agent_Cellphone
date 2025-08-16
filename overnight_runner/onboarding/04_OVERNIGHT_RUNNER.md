### Overnight Runner

[Back to Index](00_INDEX.md)

Captain run (autonomous‑dev, 5-agent)
```powershell
# FSM captain is Agent-5; Agent-3 acts as Coordination Manager
python overnight_runner/runner.py --layout 5-agent --captain Agent-5 --resume-agents Agent-1,Agent-2,Agent-3,Agent-4 \
  --duration-min 480 --interval-sec 300 --sender Agent-3 --plan contracts \
  --fsm-enabled --fsm-agent Agent-5 --fsm-workflow default \
  --initial-wait-sec 60 --phase-wait-sec 15 --stagger-ms 2500 --jitter-ms 1000 \
  --comm-root D:/repos/communications/overnight_YYYYMMDD_ --create-comm-folders
```

Denser cadence (3 minutes), include self (5-agent)
```powershell
python overnight_runner/runner.py --layout 5-agent --captain Agent-5 --resume-agents Agent-1,Agent-2,Agent-3,Agent-4 \
  --duration-min 240 --interval-sec 180 --sender Agent-3 --plan contracts \
  --fsm-enabled --fsm-agent Agent-5 --fsm-workflow default \
  --initial-wait-sec 10 --phase-wait-sec 5 --stagger-ms 1500 --jitter-ms 600 \
  --comm-root D:/repos/communications/overnight_YYYYMMDD_
```

Anti‑duplication
- Open each repo’s `TASK_LIST.md` first; pick/update items
- Prefer reuse/refactor; avoid duplication, stubs, or shims
- Commit small, verifiable edits; add tests/build steps

First run (end‑to‑end smoke)
```powershell
# 1) Create comms folder
$date=(Get-Date).ToString('yyyyMMdd'); $root="D:/repos/communications/overnight_${date}_"; New-Item -ItemType Directory -Path $root -Force | Out-Null
# 2) Start listener for Agent-5 (FSM orchestrator) with Discord devlogs
python overnight_runner/listener.py --agent Agent-5 --env-file .env --devlog-embed --devlog-username "Agent Devlog"
# 3) Send a sync message via tool (in another shell)
./overnight_runner/tools/send-sync.ps1 -To Agent-3 -Type sync -Topic "first sync" -Summary "smoke"
# 4) Start runner with safe defaults (short duration). First try add --test to dry-run without typing.
python overnight_runner/runner.py --layout 5-agent --captain Agent-5 --resume-agents Agent-1,Agent-2,Agent-3,Agent-4 --duration-min 10 --interval-sec 300 --sender Agent-3 --plan contracts --fsm-enabled --fsm-agent Agent-5 --fsm-workflow default --comm-root $root --create-comm-folders
```

Task state integration
```powershell
# Mark task lifecycle as you work so captain can see readiness for push
./overnight_runner/tools/task_state_manager.ps1 -Agent Agent-4 -TaskId basic-bot-quickstart -RepoPath D:\repositories\basic-bot -Branch feat/quickstart -EndState "README+validate added" -Status in_progress
./overnight_runner/tools/task_state_manager.ps1 -Agent Agent-4 -TaskId basic-bot-quickstart -Status validated
# Broadcast validation and push events to Discord devlog (optional)
./overnight_runner/tools/devlog_after_validate.ps1 -RepoPath D:\repositories\basic-bot
./overnight_runner/tools/devlog_notify_from_repo.ps1 -RepoPath D:\repositories\basic-bot -Validated -Pushed -Extra "nightly run"
```



[Back to Index](00_INDEX.md)
