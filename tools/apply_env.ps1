Param(
    [Parameter(Mandatory=$true)]
    [string]$EnvFile,
    [switch]$SetMachine
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

if (-not (Test-Path $EnvFile)) {
    throw "Env file not found: $EnvFile"
}

$lines = Get-Content -Path $EnvFile -ErrorAction Stop
foreach ($line in $lines) {
    if ($line -match '^\s*#' -or $line -match '^\s*$') { continue }
    $parts = $line -split '=', 2
    if ($parts.Count -lt 2) { continue }

    $name = $parts[0].Trim()
    $value = $parts[1].Trim().Trim('"','''')

    # Current session
    try { Set-Item -Path Env:$name -Value $value -ErrorAction SilentlyContinue } catch {}

    # Per-user
    [Environment]::SetEnvironmentVariable($name, $value, 'User')

    # Machine-wide (optional)
    if ($SetMachine) {
        try { [Environment]::SetEnvironmentVariable($name, $value, 'Machine') } catch {}
    }
}

Write-Host "Applied environment variables from $EnvFile" -ForegroundColor Green





