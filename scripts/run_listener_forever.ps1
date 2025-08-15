Param(
    [string]$Agent = 'Agent-5'
)

$ErrorActionPreference = 'SilentlyContinue'
Set-Location -Path 'D:\Agent_Cellphone'

if (-not (Test-Path -Path 'logs')) { New-Item -ItemType Directory -Path 'logs' | Out-Null }

while ($true) {
    try {
        python overnight_runner/listener.py --agent $Agent --env-file .env --devlog-embed --devlog-username "Agent Devlog" 2>&1 |
            Tee-Object -FilePath 'logs/listener.log' -Append | Out-Host
    } catch {
        # swallow and retry
    }
    Start-Sleep -Seconds 5
}




