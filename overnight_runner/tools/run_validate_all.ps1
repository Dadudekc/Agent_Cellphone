Param(
  [string]$ReposRoot = 'D:\repositories',
  [switch]$WriteSummary,
  [string]$SummaryPath
)

$ErrorActionPreference='Stop'
$results = @()
$validators = Get-ChildItem -Path $ReposRoot -Filter 'validate.ps1' -File -Recurse -ErrorAction SilentlyContinue
foreach ($v in $validators) {
  $repo = Split-Path -Parent $v.FullName
  Push-Location $repo
  & pwsh -NoLogo -NoProfile -File $v.FullName | Out-Null
  $code = $LASTEXITCODE
  Pop-Location
  $results += [pscustomobject]@{ repo=$repo; exit=$code }
}

if ($WriteSummary) {
  if (-not $SummaryPath) { $date=(Get-Date).ToString('yyyyMMdd_HHmmss'); $SummaryPath = "D:\\repositories\\communications\\overnight_${date}_validate_summary.txt" }
  $lines = $results | ForEach-Object { "${($_.exit -eq 0 ? 'OK ' : 'ERR')} `t$($_.repo)" }
  $lines -join [Environment]::NewLine | Out-File -FilePath $SummaryPath -Encoding utf8
  Write-Host "Summary written: $SummaryPath"
}

$failed = $results | Where-Object { $_.exit -ne 0 }
if ($failed) { exit 1 } else { exit 0 }





