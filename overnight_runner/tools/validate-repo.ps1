Param(
  [Parameter(Mandatory=$true)] [string]$Path,
  [string]$LogDir
)
$ErrorActionPreference = 'Stop'
if (-not $LogDir -or [string]::IsNullOrWhiteSpace($LogDir)) {
  $dateSuffix = Get-Date -Format 'yyyyMMdd'
  $LogDir = "D:\\repositories\\communications\\overnight_${dateSuffix}_"
}
function Out-Note($text){ Write-Host $text; $ts=(Get-Date -Format s); Add-Content -Path (Join-Path $LogDir 'captains_log.log') -Value "[$ts] validate-repo: $text" }
if (-not (Test-Path $Path)) { throw "Path not found: $Path" }
$repo = Resolve-Path $Path | Select-Object -ExpandProperty Path
$ok = $true
if (-not (Test-Path (Join-Path $repo 'README.md'))) { Out-Note 'README.md missing'; $ok=$false }
if (-not (Test-Path (Join-Path $repo 'TASK_LIST.md'))) { Out-Note 'TASK_LIST.md missing'; $ok=$false }
$val = Join-Path $repo 'validate.ps1'
if (Test-Path $val) {
  & pwsh -NoLogo -NoProfile -File $val
  if ($LASTEXITCODE -ne 0) { Out-Note "validate.ps1 failed with $LASTEXITCODE"; $ok=$false }
} else { Out-Note 'validate.ps1 missing'; $ok=$false }

$summary = [pscustomobject]@{ repo=$repo; ok=$ok; time=(Get-Date).ToString('s') }
$json = $summary | ConvertTo-Json -Depth 4
$outfile = Join-Path $LogDir ("validate_" + (Get-Date -Format 'yyyyMMdd_HHmmss') + '.json')
$json | Out-File -FilePath $outfile -Encoding utf8
if (-not $ok) { exit 1 } else { exit 0 }




