Param(
  [Parameter(Mandatory)][string]$Agent,
  [Parameter(Mandatory)][string]$TaskId,
  [string]$RepoPath,
  [ValidateSet('assigned','in_progress','blocked','complete','validated','pushed')]
  [string]$Status,
  [string]$Branch,
  [string]$EndState,
  [string]$Notes,
  [string]$MetaJson = '{}'
)

$ErrorActionPreference='Stop'
$workspace = Join-Path 'D:\Agent_Cellphone\agent_workspaces' $Agent
if (-not (Test-Path $workspace)) { $workspace = Join-Path 'D:\repositories\dadudekc\Agent_Cellphone\agent_workspaces' $Agent }
if (-not (Test-Path $workspace)) { throw "Workspace not found for $Agent" }
$statePath = Join-Path $workspace 'task_state.json'

function Set-Field([psobject]$obj, [string]$name, $value) {
  $prop = $obj.PSObject.Properties[$name]
  if ($prop) { $prop.Value = $value }
  else { $obj | Add-Member -NotePropertyName $name -NotePropertyValue $value -Force }
}

function Load-State {
  if (Test-Path $statePath) { return Get-Content -Path $statePath -Raw | ConvertFrom-Json } else { return @{} }
}
function Save-State($obj) {
  $json = $obj | ConvertTo-Json -Depth 10
  $json | Out-File -FilePath $statePath -Encoding utf8
}

$state = Load-State
if (-not $state.tasks) { $state.tasks = [pscustomobject]@{} }

# Ensure a property for this TaskId exists (supports names with dashes)
$tasksObj = $state.tasks
$prop = $tasksObj.PSObject.Properties[$TaskId]
if (-not $prop) {
  $tasksObj | Add-Member -NotePropertyName $TaskId -NotePropertyValue ([pscustomobject]@{}) -Force
  $prop = $tasksObj.PSObject.Properties[$TaskId]
}

$entry = $prop.Value
$now = (Get-Date).ToString('s')
if ($RepoPath) { Set-Field $entry 'repo_path' $RepoPath }
if ($Branch) { Set-Field $entry 'branch' $Branch }
if ($EndState) { Set-Field $entry 'end_state' $EndState }
if ($Notes) { Set-Field $entry 'notes' $Notes }
if ($MetaJson) { try { Set-Field $entry 'meta' (ConvertFrom-Json $MetaJson) } catch { Set-Field $entry 'meta' (@{ raw = $MetaJson }) } }
if ($Status) {
  Set-Field $entry 'status' $Status
  switch ($Status) {
    'assigned'   { Set-Field $entry 'assigned_at' $now }
    'in_progress'{ Set-Field $entry 'started_at' $now }
    'blocked'    { Set-Field $entry 'blocked_at' $now }
    'complete'   { Set-Field $entry 'completed_at' $now }
    'validated'  { Set-Field $entry 'validated_at' $now }
    'pushed'     { Set-Field $entry 'pushed_at' $now }
  }
}

$tasksObj.PSObject.Properties[$TaskId].Value = $entry
$state.last_update = $now
Save-State $state
Write-Host "Updated task_state for $Agent::$TaskId -> $($entry.status)"
exit 0



