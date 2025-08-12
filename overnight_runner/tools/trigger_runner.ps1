Param(
  [string]$Captain='Agent-3',
  [string]$ResumeAgents='Agent-1,Agent-2,Agent-4',
  [int]$DurationMin=15,
  [int]$IntervalSec=300,
  [string]$CommsRoot
)

$ErrorActionPreference='Stop'
if (-not $CommsRoot) { $date=(Get-Date).ToString('yyyyMMdd'); $CommsRoot = "D:/repositories/communications/overnight_${date}_" }
python overnight_runner/runner.py --layout 4-agent --captain $Captain --resume-agents $ResumeAgents --duration-min $DurationMin --interval-sec $IntervalSec --sender $Captain --plan autonomous-dev --comm-root $CommsRoot --create-comm-folders
exit $LASTEXITCODE





