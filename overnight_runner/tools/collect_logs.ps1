Param(
  [Parameter(Mandatory)][string]$CommsRoot,
  [string]$ZipPath
)

$ErrorActionPreference='Stop'
if (-not (Test-Path $CommsRoot)) { throw "Comms root not found: $CommsRoot" }
if (-not $ZipPath) { $date=(Get-Date).ToString('yyyyMMdd_HHmmss'); $ZipPath = Join-Path $env:TEMP "overnight_logs_${date}.zip" }
Add-Type -AssemblyName 'System.IO.Compression.FileSystem'
if (Test-Path $ZipPath) { Remove-Item $ZipPath -Force }
[System.IO.Compression.ZipFile]::CreateFromDirectory($CommsRoot, $ZipPath)
Write-Host "Created: $ZipPath"
exit 0





