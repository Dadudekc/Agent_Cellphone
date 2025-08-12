Param(
  [Parameter(Mandatory)][string]$RepoPath,
  [string]$WebhookUrl = $env:DISCORD_WEBHOOK_URL
)

$ErrorActionPreference='Stop'
if (-not (Test-Path $RepoPath)) { throw "RepoPath not found: $RepoPath" }

$validator = Get-ChildItem -Path $RepoPath -Filter 'validate.ps1' -File -ErrorAction SilentlyContinue | Select-Object -First 1
$validated = $false
if ($validator) {
  Push-Location $RepoPath
  & pwsh -NoLogo -NoProfile -File $validator.FullName | Out-Null
  $validated = ($LASTEXITCODE -eq 0)
  Pop-Location
}

$extra = if ($validated) { 'validation: success' } elseif ($validator) { 'validation: failed' } else { 'validation: n/a' }

& (Join-Path $PSScriptRoot 'devlog_notify_from_repo.ps1') -RepoPath $RepoPath -Validated:($validated) -Pushed:$false -Extra $extra @(
  if ($WebhookUrl) { '-WebhookUrl'; $WebhookUrl }
) | Out-Null

Write-Host "Devlog post sent for $RepoPath (validated=$validated)"
exit 0




