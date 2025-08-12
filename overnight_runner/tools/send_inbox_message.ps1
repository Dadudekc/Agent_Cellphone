<# Deprecated: Prefer ./send-sync.ps1. This script will be removed in a future cleanup. #>

Param(
  [Parameter(Mandatory=$true)][Alias('ToAgent')][string]$To,
  [Parameter(Mandatory=$true)][ValidateSet('sync','task','ack','note','resume','verify','ping')][string]$Type,
  [Parameter(Mandatory=$true)][string]$Topic,
  [Parameter(Mandatory=$true)][string]$Summary,
  [string]$DetailsJson='{}',
  [Alias('FromAgent')][string]$From='Agent-3'
)
Write-Warning 'send_inbox_message.ps1 is deprecated. Use send-sync.ps1 instead.'

$ErrorActionPreference='Stop'
$cands=@("D:\\repositories\\dadudekc\\Agent_Cellphone\\agent_workspaces\\$To\\inbox","D:\\Agent_Cellphone\\agent_workspaces\\$To\\inbox")
$inbox=$cands | Where-Object { Test-Path -LiteralPath $_ } | Select-Object -First 1
if (-not $inbox) { throw "Inbox not found for $To" }

$now=Get-Date
$ts=$now.ToString('yyyyMMdd_HHmmss')
$detailsObj = $null
try { $detailsObj = ConvertFrom-Json -InputObject $DetailsJson } catch { $detailsObj = $null }
if (-not $detailsObj) { $detailsObj = [pscustomobject]@{} }

$payload=[pscustomobject]@{
  type=$Type
  from=$From
  to=$To
  timestamp=$now.ToString('o')
  topic=$Topic
  summary=$Summary
  details=$detailsObj
}
$json=$payload | ConvertTo-Json -Depth 10
$outfile=Join-Path -Path $inbox -ChildPath ("msg_{0}_{1}_to_{2}.json" -f $ts,$From,$To)
Set-Content -LiteralPath $outfile -Value $json -Encoding utf8
Write-Host "Wrote: $outfile"
exit 0




