### Protocol: Trigger Overnight Runner (Safe Defaults)

Use when
- Kicking off a short autonomous cycle to validate pipelines.

Steps
```powershell
# Easiest entry point with sane defaults and new‑chat throttling
./overnight_runner/tools/trigger_runner.ps1 -Layout '5-agent' -Agents 'Agent-1,Agent-2,Agent-3,Agent-4' `
  -Sender 'Agent-3' -Plan 'single-repo-beta' -AssignRoot 'D:/repositories' -DurationMin 480 -IntervalSec 300 `
  -FsmEnabled -FsmAgent 'Agent-5' -FsmWorkflow 'default' -NewChatIntervalSec 3600 -DefaultNewChat -NewWindow
```

Behavior:
- Only triggers Ctrl+T on first contact per agent (or when rescuing a stall/focus change).
- Subsequent prompts type into the regular input area to avoid double‑onboarding tabs.





