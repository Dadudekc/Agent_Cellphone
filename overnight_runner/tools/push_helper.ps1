param(
  [Parameter(Mandatory=$true)] [string]$RepoPath,
  [Parameter(Mandatory=$true)] [string]$Message,
  [string]$Branch,
  [string]$CommsRoot = "D:/repositories/communications/overnight_$(Get-Date -Format 'yyyyMMdd')_"
)

function New-BranchName {
  param([string]$Prefix = 'chore/autonomous')
  $ts = Get-Date -Format 'yyyyMMdd_HHmmss'
  return "$Prefix-$ts"
}

try {
  if (-not (Test-Path -LiteralPath $RepoPath)) { throw "RepoPath not found: $RepoPath" }
  Set-Location -LiteralPath $RepoPath

  # Stage changes
  git add -A | Out-Null
  $status = git status --porcelain
  if (-not $status) {
    Write-Host "No changes to commit in $RepoPath"
    exit 0
  }

  # Commit
  git commit -m $Message | Out-Null

  # Branch
  if (-not $Branch) { $Branch = New-BranchName }
  git checkout -B $Branch | Out-Null

  # Push (may fail if no permissions)
  try {
    git push -u origin $Branch
    Write-Host "✅ Pushed branch $Branch with message:`n$Message"
    exit 0
  }
  catch {
    Write-Warning "Push failed. Writing patch to comms folder instead."
    if (-not (Test-Path -LiteralPath $CommsRoot)) { New-Item -ItemType Directory -Force -Path $CommsRoot | Out-Null }
    $stamp = Get-Date -Format 'yyyyMMdd_HHmmss'
    $patchPath = Join-Path $CommsRoot ("${($RepoPath | Split-Path -Leaf)}_$Branch_$stamp.patch")
    git diff HEAD > $patchPath
    Write-Host "📝 Wrote patch: $patchPath"
    exit 0
  }
}
catch {
  Write-Error $_
  exit 1
}














