param(
	[string]$Root = 'D:\repos',
	[string]$MasterTracker = 'D:\repos\runtime\agent_comms\project_master_tracker.json',
	[string]$AgentName = 'Unknown-Agent',
	[string]$OldPrdTracker = 'D:\repos\runtime\agent_comms\prd_master_tracker.json',
	[string]$OldTaskTracker = 'D:\repos\runtime\agent_comms\task_master_tracker.json',
	[switch]$ImportExisting,
	[switch]$DryRun
)

$ErrorActionPreference = 'Stop'

function Write-Log {
	param([string]$Message)
	Write-Host "[$(Get-Date -Format 'u')] $Message"
}

function Load-Tracker($path) {
	if (Test-Path $path) {
		return Get-Content $path -Raw | ConvertFrom-Json
	}
	return @()
}

function Save-Tracker($path, $data) {
	$json = $data | ConvertTo-Json -Depth 8
	$folder = Split-Path $path
	if (-not (Test-Path $folder)) { New-Item -ItemType Directory -Path $folder -Force | Out-Null }
	Set-Content -Path $path -Value $json -Encoding UTF8
}

# Templates
$PrdChecklistTemplate = @(
	'Repo inspected',
	'README reviewed',
	'Unique PRD draft started',
	'Legacy content integrated',
	'Final PRD committed'
)

$TaskTemplate = @(
	'Initial project inspection',
	'Identify core objectives',
	'Map current state vs desired state',
	'List all major deliverables',
	'Break deliverables into actionable tasks',
	'Define task priorities & dependencies',
	'Assign tasks & set deadlines',
	'Track progress updates',
	'Review and adjust plan'
)

# Load unified tracker
$unified = Load-Tracker $MasterTracker
if ($null -eq $unified) { $unified = @() }

# Optional: import and merge old trackers into unified
if ($ImportExisting) {
	$oldPrd = Load-Tracker $OldPrdTracker
	$oldTasks = Load-Tracker $OldTaskTracker

	foreach ($e in $oldPrd) {
		$existing = $unified | Where-Object { $_.repo -eq $e.repo }
		if (-not $existing) {
			$existing = @{
				repo = $e.repo
				path = $e.path
				assigned_to = $e.assigned_to
				status = 'In Progress'
				prd = @{}
				tasks = @{}
				last_update = (Get-Date).ToString('u')
			}
			$unified += $existing
		}
		$existing.prd = @{
			assigned_to = $e.assigned_to
			status      = $e.status
			checklist   = $e.checklist
			completed   = $e.completed
			progress    = $e.progress
			last_update = $e.last_update
		}
	}
	foreach ($e in $oldTasks) {
		$existing = $unified | Where-Object { $_.repo -eq $e.repo }
		if (-not $existing) {
			$existing = @{
				repo = $e.repo
				path = $e.path
				assigned_to = $e.assigned_to
				status = 'In Progress'
				prd = @{}
				tasks = @{}
				last_update = (Get-Date).ToString('u')
			}
			$unified += $existing
		}
		$existing.tasks = @{
			assigned_to = $e.assigned_to
			status      = $e.status
			template    = $e.template
			tasks       = $e.tasks
			completed   = $e.completed
			progress    = $e.progress
			last_update = $e.last_update
		}
	}
}

# Discover repos
$repos = Get-ChildItem -Path $Root -Directory -Recurse -Depth 3 -ErrorAction SilentlyContinue |
	Where-Object { Test-Path (Join-Path $_.FullName '.git') }

foreach ($repo in $repos) {
	try {
		$repoPath = $repo.FullName
		$repoName = Split-Path $repoPath -Leaf

		$entry = $unified | Where-Object { $_.repo -eq $repoName }
		if (-not $entry) {
			$entry = @{
				repo        = $repoName
				path        = $repoPath
				assigned_to = $AgentName
				status      = 'In Progress'
				prd         = @{
					assigned_to = $AgentName
					status      = 'In Progress'
					checklist   = $PrdChecklistTemplate
					completed   = @()
					progress    = 0
					last_update = (Get-Date).ToString('u')
				}
				tasks       = @{
					assigned_to = $AgentName
					status      = 'In Progress'
					template    = $TaskTemplate
					tasks       = @()
					completed   = @()
					progress    = 0
					last_update = (Get-Date).ToString('u')
				}
				last_update = (Get-Date).ToString('u')
			}
			$unified += $entry
			Write-Log "Added project entry for $repoName"
		}
		else {
			# Ensure nested structures exist
			if ($null -eq $entry.prd) {
				$entry.prd = @{
					assigned_to = $AgentName
					status      = 'In Progress'
					checklist   = $PrdChecklistTemplate
					completed   = @()
					progress    = 0
					last_update = (Get-Date).ToString('u')
				}
			}
			if ($null -eq $entry.tasks) {
				$entry.tasks = @{
					assigned_to = $AgentName
					status      = 'In Progress'
					template    = $TaskTemplate
					tasks       = @()
					completed   = @()
					progress    = 0
					last_update = (Get-Date).ToString('u')
				}
			}

			# Update assignment if agent differs
			if ($entry.assigned_to -ne $AgentName) {
				Write-Log "Reassigning $repoName from $($entry.assigned_to) to $AgentName"
				$entry.assigned_to = $AgentName
			}
			$entry.prd.assigned_to = $AgentName
			$entry.tasks.assigned_to = $AgentName
			$entry.last_update = (Get-Date).ToString('u')
		}
	}
	catch {
		Write-Log "ERROR: $($repo.FullName) -> $($_.Exception.Message)"
	}
}

if (-not $DryRun) {
	Save-Tracker $MasterTracker $unified
}

Write-Log "Unified Project tracker updated at $MasterTracker"
