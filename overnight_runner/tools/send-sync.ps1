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




