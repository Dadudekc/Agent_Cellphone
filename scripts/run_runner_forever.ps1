Param(
    [string]$Agents = 'Agent-1,Agent-2,Agent-3,Agent-4',
    [string]$Layout = '5-agent',
    [int]$IntervalSec = 1200,
    [int]$DurationMin = 720,
    [string]$Plan = 'contracts',
    [string]$Sender = 'Agent-3',
    [string]$FsmAgent = 'Agent-5',
    [string]$Workflow = 'default'
)

$ErrorActionPreference = 'SilentlyContinue'
Set-Location -Path 'D:\Agent_Cellphone'

$env:ACP_DEFAULT_NEW_CHAT='1'
$env:ACP_AUTO_ONBOARD='1'
$env:ACP_SINGLE_MESSAGE='1'
$env:ACP_MESSAGE_VERBOSITY='extensive'
$env:ACP_NEW_CHAT_INTERVAL_SEC='1800'
$env:ACP_DISABLE_FAILSAFE='1'

if (-not (Test-Path -Path 'logs')) { New-Item -ItemType Directory -Path 'logs' | Out-Null }

while ($true) {
    try {
        python overnight_runner/runner.py --layout $Layout --agents $Agents --duration-min $DurationMin --interval-sec $IntervalSec `
            --sender $Sender --plan $Plan --fsm-enabled --fsm-agent $FsmAgent --fsm-workflow $Workflow `
            --seed-from-tasklists --skip-assignments --skip-captain-kickoff --skip-captain-fsm-feed `
            --devlog-sends --devlog-embed --devlog-username "Agent Devlog" 2>&1 |
            Tee-Object -FilePath 'logs/runner.log' -Append | Out-Host
    } catch {
        # swallow and retry
    }
    Start-Sleep -Seconds 10
}




