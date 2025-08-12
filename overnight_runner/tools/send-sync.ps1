Param(
  [Parameter(Mandatory=$true)][string]$To,
  [Parameter(Mandatory=$true)][ValidateSet('sync','task','ack','note','resume','verify','ping')][string]$Type,
  [Parameter(Mandatory=$true)][string]$Topic,
  [Parameter(Mandatory=$true)][string]$Summary,
  [string]$From='Agent-3',
  [string]$PayloadPath
)

$ErrorActionPreference = 'Stop'

function Get-InboxPath {
  param([string]$Agent)
  $candidates = @(
    (Join-Path -Path (Get-Location) -ChildPath ("agent_workspaces\$Agent\inbox")),
    "D:\\Agent_Cellphone\\agent_workspaces\$Agent\inbox",
    "D:\\repositories\\dadudekc\\Agent_Cellphone\\agent_workspaces\$Agent\inbox"
  )
  foreach ($p in $candidates) {
    if (Test-Path -LiteralPath $p) { return $p }
  }
  # Attempt to create relative inbox if agent_workspaces exists
  $base = Join-Path -Path (Get-Location) -ChildPath 'agent_workspaces'
  if (Test-Path -LiteralPath $base) {
    $inbox = Join-Path -Path $base -ChildPath ("$Agent\inbox")
    New-Item -ItemType Directory -Force -Path $inbox | Out-Null
    return $inbox
  }
  throw "Inbox not found for $Agent"
}

function Read-DetailsJson {
  param([string]$Path)
  if (-not $Path) { return [pscustomobject]@{} }
  if (-not (Test-Path -LiteralPath $Path)) { return [pscustomobject]@{} }
  try {
    $raw = Get-Content -LiteralPath $Path -Encoding UTF8 -Raw
    $obj = ConvertFrom-Json -InputObject $raw -ErrorAction Stop
    if ($null -eq $obj) { return [pscustomobject]@{} }
    return $obj
  }
  catch { return [pscustomobject]@{} }
}

$inbox = Get-InboxPath -Agent $To
$now = Get-Date
$ts = $now.ToString('yyyyMMdd_HHmmss')
$detailsObj = Read-DetailsJson -Path $PayloadPath

$payload = [pscustomobject]@{
  type      = $Type
  from      = $From
  to        = $To
  timestamp = $now.ToString('o')
  topic     = $Topic
  summary   = $Summary
  details   = $detailsObj
}

$json = $payload | ConvertTo-Json -Depth 10
$outfile = Join-Path -Path $inbox -ChildPath ("msg_{0}_{1}_to_{2}.json" -f $ts,$From,$To)
Set-Content -LiteralPath $outfile -Value $json -Encoding utf8
Write-Host "Wrote: $outfile"
exit 0

Param(
  [Parameter(Mandatory=$true)] [string]$To,
  [Parameter(Mandatory=$true)] [ValidateSet('sync','task','ack','note','verify','resume')] [string]$Type,
  [Parameter(Mandatory=$true)] [string]$Topic,
  [Parameter(Mandatory=$true)] [string]$Summary,
  [string]$PayloadPath,
  [string]$From = 'Agent-4'
)
$ErrorActionPreference = 'Stop'
$cands = @('D:\Agent_Cellphone\agent_workspaces', 'D:\repositories\dadudekc\Agent_Cellphone\agent_workspaces')
$root = $cands | Where-Object { Test-Path $_ } | Select-Object -First 1
if (-not $root) { throw 'agent_workspaces root not found' }
$inbox = Join-Path (Join-Path $root $To) 'inbox'
if (-not (Test-Path $inbox)) { throw "inbox not found: $inbox" }
$now=Get-Date
$msg = [pscustomobject]@{ type=$Type; from=$From; to=$To; timestamp=$now.ToString('o'); topic=$Topic; summary=$Summary }
if ($PayloadPath -and (Test-Path $PayloadPath)) { $msg | Add-Member -NotePropertyName details -NotePropertyValue (Get-Content $PayloadPath -Raw | ConvertFrom-Json) }
$json = $msg | ConvertTo-Json -Depth 6
$file = Join-Path $inbox ("msg_" + $now.ToString('yyyyMMdd_HHmmss') + "_${From}_to_${To}.json")
$json | Out-File -FilePath $file -Encoding utf8
Write-Output $file




