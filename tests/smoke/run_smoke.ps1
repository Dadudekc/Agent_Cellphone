Param(
  [string]$CommsRoot
)

$ErrorActionPreference = 'Stop'
function Step($name, [scriptblock]$action){
  Write-Host "==> $name" -ForegroundColor Cyan
  & $action
}

Step 'Python version' { python --version | Out-Host }

Step 'Compile core python files' {
  python -m py_compile `
    overnight_runner/runner.py `
    overnight_runner/listener.py `
    overnight_runner/tools/capture_coords.py
}

Step 'Import GUI components' {
  python -c "import sys,os; sys.path.insert(0, os.getcwd()); import gui.components.agent_panel as ap; print('AgentPanel import OK')" | Out-Host
}

Step 'Generate contracts (dry run, max 1 per agent)' {
  if (-not $CommsRoot -or [string]::IsNullOrWhiteSpace($CommsRoot)){
    $d = Get-Date -Format 'yyyyMMdd'
    $CommsRoot = "D:/repos/communications/overnight_${d}_"
  }
  pwsh -NoLogo -NoProfile -File overnight_runner/tools/generate-contracts.ps1 `
    -Root 'D:\repos' `
    -ToAgents 'Agent-1,Agent-2' `
    -From 'Agent-5' `
    -OutComms $CommsRoot `
    -MaxPerAgent 1 `
    -DryRun | Out-Host
}

Step 'Runner one-cycle test (no typing)' {
  python overnight_runner/runner.py `
    --layout 5-agent `
    --captain Agent-5 `
    --resume-agents Agent-1,Agent-2,Agent-3,Agent-4 `
    --iterations 1 `
    --interval-sec 1 `
    --sender Agent-3 `
    --plan contracts `
    --fsm-enabled --fsm-agent Agent-5 --fsm-workflow default `
    --test | Out-Host
}

Write-Host "Smoke tests completed." -ForegroundColor Green




