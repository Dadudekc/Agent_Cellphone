Param(
  [string]$Root = 'D:\repositories',
  [string]$ToAgents = 'Agent-1,Agent-2,Agent-3,Agent-4',
  [string]$From = 'Agent-5',
  [string]$OutComms,
  [switch]$Send,
  [switch]$DryRun,
  [int]$MaxPerAgent = 0
)

$ErrorActionPreference = 'Stop'
$date = Get-Date -Format 'yyyyMMdd'
if (-not $OutComms -or [string]::IsNullOrWhiteSpace($OutComms)) {
  $OutComms = "D:\repositories\communications\overnight_${date}_"
}
if (-not (Test-Path -LiteralPath $OutComms)) { New-Item -ItemType Directory -Path $OutComms -Force | Out-Null }
$fsmDir = Join-Path $OutComms 'Agent-5'
if (-not (Test-Path -LiteralPath $fsmDir)) { New-Item -ItemType Directory -Path $fsmDir -Force | Out-Null }

function New-Slug([string]$text){
  return ($text.ToLower() -replace "[^a-z0-9]+","-").Trim('-')
}

# Find TASK_LIST.md files
$files = Get-ChildItem -Path $Root -Filter 'TASK_LIST.md' -File -Recurse -ErrorAction SilentlyContinue
$agents = $ToAgents.Split(',') | ForEach-Object { $_.Trim() } | Where-Object { $_ }
if (-not $agents) { $agents = @('Agent-1','Agent-2','Agent-3','Agent-4') }
$ai = 0
$assignedCounts = @{}
foreach($a in $agents){ $assignedCounts[$a] = 0 }

$contracts = @()
foreach($f in $files){
  $repoPath = Split-Path -Parent $f.FullName
  $repoName = Split-Path -Leaf $repoPath
  $lines = Get-Content -Path $f.FullName -Encoding UTF8
  foreach($line in $lines){
    if ($line -match '^- \[( |x|X)\] (.+)$'){
      $title = $Matches[2].Trim()
      $taskId = (New-Slug "$repoName-$title")
      # choose assignee honoring MaxPerAgent if provided
      $assignee = $null
      for($j=0; $j -lt $agents.Count; $j++){
        $cand = $agents[($ai + $j) % $agents.Count]
        if ($MaxPerAgent -le 0 -or $assignedCounts[$cand] -lt $MaxPerAgent){
          $assignee = $cand; $ai = $ai + $j + 1; break
        }
      }
      if (-not $assignee) { continue }
      $contract = [pscustomobject]@{
        task_id = $taskId
        repo = $repoName
        repo_path = $repoPath
        title = $title
        description = ''
        acceptance_criteria = @()
        assignee = $assignee
        state = 'ready'
        evidence = @()
        created = (Get-Date).ToString('s')
      }
      $contracts += $contract
      $assignedCounts[$assignee] = $assignedCounts[$assignee] + 1

      if ($Send -and -not $DryRun){
        $tmp = New-TemporaryFile
        $contract | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $tmp -Encoding utf8
        $topic = "contract: $taskId"
        $summary = $title
        & .\overnight_runner\tools\send-sync.ps1 -To $assignee -Type task -Topic $topic -Summary $summary -PayloadPath $tmp -From $From | Out-Host
      }
    }
  }
}

# Persist consolidated contracts under Agent-5 folder
$contractsPath = Join-Path $fsmDir 'contracts.json'
($contracts | ConvertTo-Json -Depth 8) | Set-Content -LiteralPath $contractsPath -Encoding utf8
Write-Output "Contracts: $contractsPath (`$($contracts.Count) items)"
if ($DryRun) { Write-Output '(dry run) no messages sent' }

