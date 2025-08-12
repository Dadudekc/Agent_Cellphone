### Protocol: Trigger Overnight Runner (Safe Defaults)

Use when
- Kicking off a short autonomous cycle to validate pipelines.

Steps
```powershell
./overnight_runner/tools/trigger_runner.ps1 -Captain Agent-3 -ResumeAgents 'Agent-1,Agent-2,Agent-4' -DurationMin 10 -IntervalSec 300
```





