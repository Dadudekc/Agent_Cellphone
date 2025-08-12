Param(
  [string]$Root = 'D:\repositories',
  [string]$Out
)
$ErrorActionPreference = 'Stop'
$dateSuffix = Get-Date -Format 'yyyyMMdd'
if (-not $Out -or [string]::IsNullOrWhiteSpace($Out)) {
  $Out = "D:\\repositories\\communications\\overnight_${dateSuffix}_"
}
$files = Get-ChildItem -Path $Root -Filter 'TASK_LIST.md' -File -Recurse -ErrorAction SilentlyContinue
$rows = @()
foreach ($f in $files) {
  $repo = Split-Path -Parent $f.FullName
  $readme = Test-Path (Join-Path $repo 'README.md')
  $validate = Test-Path (Join-Path $repo 'validate.ps1')
  $rows += [pscustomobject]@{ repo=$repo; readme=$readme; validate=$validate; tasklist=$f.FullName }
}
$csv = Join-Path $Out ('tasklist_scan_' + (Get-Date -Format 'yyyyMMdd_HHmmss') + '.csv')
$rows | Export-Csv -Path $csv -NoTypeInformation -Encoding UTF8
Write-Output $csv




