Param(
  [Parameter(Mandatory)][string]$RepoPath,
  [Parameter(Mandatory)][string]$Message,
  [string]$Branch,
  [switch]$CreateBranch,
  [switch]$OpenPR,
  [string]$PRTitle,
  [string]$PRBody
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

if ($Branch) {
  if ($CreateBranch) { RunGit "checkout -B $Branch" } else { RunGit "checkout $Branch" }
}

RunGit 'add -A'
try { RunGit "commit -m `"$Message`"" } catch { Write-Host 'No changes to commit'; }
RunGit 'push -u origin HEAD'

if ($OpenPR) {
  $title = if ($PRTitle) { $PRTitle } else { $Message }
  $body = if ($PRBody) { $PRBody } else { 'Automated PR created by Agent Cellphone' }
  $psi = New-Object System.Diagnostics.ProcessStartInfo
  $psi.FileName = 'gh'
  $psi.Arguments = "pr create --fill --title `"$title`" --body `"$body`""
  $psi.WorkingDirectory = $RepoPath
  $psi.RedirectStandardOutput = $true
  $psi.RedirectStandardError = $true
  $psi.UseShellExecute = $false
  $p = [System.Diagnostics.Process]::Start($psi)
  $out = $p.StandardOutput.ReadToEnd().Trim()
  $err = $p.StandardError.ReadToEnd().Trim()
  $p.WaitForExit()
  if ($p.ExitCode -ne 0) { throw "gh pr create failed: $err" }
  Write-Host $out
}

Write-Host 'Push complete.'
exit 0




