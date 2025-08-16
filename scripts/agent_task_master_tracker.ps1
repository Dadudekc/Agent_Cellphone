param(
	[string]$Root = 'D:\repos',
	[string]$MasterTracker = 'D:\repos\runtime\agent_comms\task_master_tracker.json',
	[string]$AgentName = 'Unknown-Agent',
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
	$json = $data | ConvertTo-Json -Depth 5
	$folder = Split-Path $path
	if (-not (Test-Path $folder)) { New-Item -ItemType Directory -Path $folder -Force | Out-Null }
	Set-Content -Path $path -Value $json -Encoding UTF8
}

# Standard task list template — agents adapt/extend per project
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

$tracker = Load-Tracker $MasterTracker
$repos = Get-ChildItem -Path $Root -Directory -Recurse -Depth 3 -ErrorAction SilentlyContinue |
	Where-Object { Test-Path (Join-Path $_.FullName '.git') }

foreach ($repo in $repos) {
	try {
		$repoPath = $repo.FullName
		$repoName = Split-Path $repoPath -Leaf

		$entry = $tracker | Where-Object { $_.repo -eq $repoName }

		if (-not $entry) {
			$entry = @{
				repo        = $repoName
				path        = $repoPath
				assigned_to = $AgentName
				status      = 'In Progress'
				tasks       = @() # agent fills from real repo inspection
				template    = $TaskTemplate
				completed   = @()
				progress    = 0
				last_update = (Get-Date).ToString('u')
			}
			$tracker += $entry
			Write-Log "📌 Added new Task tracker for $repoName (Agent: $AgentName)"
		}
		else {
			if ($entry.assigned_to -ne $AgentName) {
				Write-Log "🔄 Reassigning $repoName from $($entry.assigned_to) to $AgentName"
				$entry.assigned_to = $AgentName
			}
			$entry.last_update = (Get-Date).ToString('u')
		}
	}
	catch {
		Write-Log "ERROR: $($repo.FullName) -> $($_.Exception.Message)"
	}
}

if (-not $DryRun) {
	Save-Tracker $MasterTracker $tracker
}

Write-Log "✅ Global Task tracker updated at $MasterTracker"
