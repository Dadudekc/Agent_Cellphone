Param(
  [Parameter(Mandatory=$true)] [string]$To,
  [Parameter(Mandatory=$true)] [string]$Msg,
  [ValidateSet('resume','task','coordinate','sync','verify','note')] [string]$Tag = 'note',
  [string]$Layout = '4-agent'
)

$ErrorActionPreference = 'Stop'

# Ensure we run from repo root for relative paths
$repoRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location -LiteralPath $repoRoot | Out-Null

& python src/agent_cell_phone.py --layout $Layout --agent $To --msg $Msg --tag $Tag
exit $LASTEXITCODE



