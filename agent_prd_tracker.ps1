param(
	[string]$Root = 'D:\repos',
	[switch]$DryRun
)

$ErrorActionPreference = 'Stop'
$TrackerFile = 'docs\prd_tracker.json'

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
	Set-Content -Path $path -Value $json -Encoding UTF8
}

$repos = Get-ChildItem -Path $Root -Directory -Recurse -Depth 3 -ErrorAction SilentlyContinue |
	Where-Object { Test-Path (Join-Path $_.FullName '.git') }

foreach ($repo in $repos) {
	try {
		$repoPath = $repo.FullName
		$repoName = Split-Path $repoPath -Leaf
		$docsDir = Join-Path $repoPath 'docs'

		if (-not (Test-Path $docsDir)) {
			if (-not $DryRun) { New-Item -ItemType Directory -Path $docsDir | Out-Null }
		}

		$trackerPath = Join-Path $repoPath $TrackerFile
		$tracker = Load-Tracker $trackerPath

		$entry = $tracker | Where-Object { $_.repo -eq $repoName }
		if (-not $entry) {
			$entry = @{
				repo        = $repoName
				path        = $repoPath
				assigned_to = 'Unassigned'
				status      = 'In Progress'
				checklist   = @(
					'Repo inspected',
					'README reviewed',
					'Unique PRD draft started',
					'Legacy content integrated',
					'Final PRD committed'
				)
				completed   = @()
				progress    = 0
				last_update = (Get-Date).ToString('u')
			}
			$tracker += $entry
			Write-Log "PRD tracker created for $repoName"
		}

		if (-not $DryRun) { Save-Tracker $trackerPath $tracker }
	}
	catch {
		Write-Log "ERROR: $($repo.FullName) -> $($_.Exception.Message)"
	}
}

Write-Log 'PRD tracker pass complete'
