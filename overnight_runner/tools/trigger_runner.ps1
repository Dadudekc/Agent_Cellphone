Param(
    [string]$Layout = '5-agent',
    [string]$Agents = 'Agent-1,Agent-2,Agent-3,Agent-4',
    [string]$SenderAgent = 'Agent-3',
    [int]$IntervalSec = 300,
    [int]$InitialWaitSec = 300,
    [int]$DurationMin = 480,
    [string]$Plan = 'single-repo-beta',
    [string]$AssignRoot = 'D:/repositories',
    [switch]$FsmEnabled,
    [string]$FsmAgent = 'Agent-5',
    [string]$FsmWorkflow = 'default',
    [int]$NewChatIntervalSec = 3600,
    [switch]$DefaultNewChat,
    [switch]$NewWindow,
    [switch]$PlanRepoGitSetup
)

$ErrorActionPreference = 'Stop'

$venvPy = Join-Path $PSScriptRoot '..' '..' '.venv' 'Scripts' 'python.exe' | Resolve-Path
$env:REPOS_ROOT = $env:REPOS_ROOT -as [string]; if (-not $env:REPOS_ROOT) { $env:REPOS_ROOT = 'D:/repositories' }

$env:ACP_AUTO_ONBOARD='1'
$env:ACP_SINGLE_MESSAGE='1'
$env:ACP_MESSAGE_VERBOSITY='extensive'
if ($DefaultNewChat) { $env:ACP_DEFAULT_NEW_CHAT='1' } else { Remove-Item Env:ACP_DEFAULT_NEW_CHAT -ErrorAction SilentlyContinue }
$env:ACP_NEW_CHAT_INTERVAL_SEC = [string]$NewChatIntervalSec

$argsList = @(
    'overnight_runner/runner.py',
    '--layout', $Layout,
    '--agents', $Agents,
    '--sender', $SenderAgent,
    '--interval-sec', $IntervalSec,
    '--initial-wait-sec', $InitialWaitSec,
    '--duration-min', $DurationMin,
    '--plan', $Plan,
    '--assign-root', $AssignRoot,
    '--per-agent-cooldown-sec', '300',
    '--resume-cooldown-sec', '600',
    '--new-chat-interval-sec', [string]$NewChatIntervalSec
)
if ($PlanRepoGitSetup) { $argsList = $argsList -replace ('--plan\s+\S+'), '--plan repo-git-setup' }
if ($FsmEnabled) { $argsList += @('--fsm-enabled', '--fsm-agent', $FsmAgent, '--fsm-workflow', $FsmWorkflow) }
if ($DefaultNewChat) { $argsList += '--default-new-chat' }

if ($NewWindow) {
    $cmd = "`$env:ACP_AUTO_ONBOARD='1'; `$env:ACP_SINGLE_MESSAGE='1'; `$env:ACP_MESSAGE_VERBOSITY='extensive'; `$env:ACP_NEW_CHAT_INTERVAL_SEC='$NewChatIntervalSec';"
    if ($DefaultNewChat) { $cmd += " `$env:ACP_DEFAULT_NEW_CHAT='1';" }
    $argStr = ($argsList -join ' ')
    Start-Process pwsh -ArgumentList "-NoProfile -Command $cmd `"$($venvPy.Path)`" $argStr"
} else {
    & $venvPy.Path @argsList
}

 
