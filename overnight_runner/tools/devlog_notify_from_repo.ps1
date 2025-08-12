edits.
Param(
  [Parameter(Mandatory)][string]$RepoPath,
  [switch]$Validated,
  [switch]$Pushed,
  [string]$Branch,
  [string]$Extra
)

$ErrorActionPreference='Stop'
if (-not (Test-Path $RepoPath)) { throw "RepoPath not found: $RepoPath" }

function RunGit([string]$args) {
  $psi = New-Object System.Diagnostics.ProcessStartInfo
  $psi.FileName = 'git'
  $psi.Arguments = $args
  $psi.WorkingDirectory = $RepoPath
  $psi.RedirectStandardOutput = $true
  $psi.RedirectStandardError = $true
  $psi.UseShellExecute = $false
  $p = [System.Diagnostics.Process]::Start($psi)
  $out = $p.StandardOutput.ReadToEnd().Trim()
  $err = $p.StandardError.ReadToEnd().Trim()
  $p.WaitForExit()
  if ($p.ExitCode -ne 0) { throw "git $args failed: $err" }
  return $out
}

$repoName = Split-Path -Leaf $RepoPath
$branch = if ($Branch) { $Branch } else { try { RunGit 'rev-parse --abbrev-ref HEAD' } catch { 'unknown' } }
$sha = try { RunGit 'rev-parse --short HEAD' } catch { 'unknown' }
$msg = try { RunGit 'log -1 --pretty=%s' } catch { '' }

$statusParts = @()
if ($Validated) { $statusParts += 'validated: ok' } else { $statusParts += 'validated: n/a' }
if ($Pushed) { $statusParts += 'pushed: yes' } else { $statusParts += 'pushed: no' }
if ($Extra) { $statusParts += $Extra }
$statusLine = ($statusParts -join ' | ')

$title = "${repoName}@${sha} (${branch})"
$desc = "${statusLine}`n${msg}`n${RepoPath}"

& (Join-Path $PSScriptRoot 'notify_discord.ps1') -Embed -Title $title -Description $desc | Out-Null
Write-Host "Devlog sent for $repoName @ $sha ($branch)"
exit 0




