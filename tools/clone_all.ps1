Param(
    [string]$Dest
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Load-DotEnv {
    param([string]$Path)
    if (-not (Test-Path $Path)) { return }
    $lines = Get-Content -Path $Path -ErrorAction Stop
    foreach ($line in $lines) {
        if ($line -match '^\s*#' -or $line -match '^\s*$') { continue }
        $parts = $line -split '=', 2
        if ($parts.Count -lt 2) { continue }
        $name = $parts[0].Trim()
        $value = $parts[1].Trim()
        if ($value.Length -ge 2) {
            if (($value.StartsWith('"') -and $value.EndsWith('"')) -or ($value.StartsWith("'") -and $value.EndsWith("'"))) {
                $value = $value.Substring(1, $value.Length - 2)
            }
        }
        try { Set-Item -Path Env:$name -Value $value -ErrorAction SilentlyContinue } catch {}
        [Environment]::SetEnvironmentVariable($name, $value, 'User')
    }
}

$root = 'D:\Agent_Cellphone'
$envPath = Join-Path $root '.env'
Load-DotEnv -Path $envPath

# Determine destination
if (-not $Dest -or [string]::IsNullOrWhiteSpace($Dest)) {
    $Dest = if ($env:REPO_DEST) { $env:REPO_DEST } else { Join-Path $root 'repos' }
}
if (-not (Test-Path $Dest)) { New-Item -ItemType Directory -Path $Dest -Force | Out-Null }

# Sync github_config.json for tools that read it
$cfgPath = 'D:\repos\github_config.json'
$cfg = @{}
if (Test-Path $cfgPath) { try { $cfg = Get-Content $cfgPath -Raw | ConvertFrom-Json } catch {} }
if (-not $cfg) { $cfg = [ordered]@{} }
if ($env:GITHUB_USERNAME) { $cfg.username = $env:GITHUB_USERNAME }
if ($env:GITHUB_TOKEN) { $cfg.token = $env:GITHUB_TOKEN }
if (-not $cfg.username) { $cfg.username = '' }
if (-not $cfg.token) { $cfg.token = '' }
$cfg.setup_date = (Get-Date).ToString('s')
$cfg | ConvertTo-Json -Depth 5 | Set-Content -Path $cfgPath -Encoding UTF8

# Force non-interactive git in this session
$env:GIT_TERMINAL_PROMPT = '0'
$env:GCM_INTERACTIVE = 'Never'

# Run the Python bulk clone script
$log = Join-Path $root 'repos_clone_run_verbose.txt'
Write-Host "Cloning into $Dest..." -ForegroundColor Cyan
python (Join-Path $root 'clone_all_to_repo.py') $Dest 2>&1 | Tee-Object -FilePath $log

Write-Host "Done. See $log and $($root)\repos_clone.log / repos_clone_report.json" -ForegroundColor Green


