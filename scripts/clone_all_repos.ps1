Param()

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Ensure-GitAvailable {
	try {
		git --version | Out-Null
	} catch {
		throw "Git does not appear to be installed or is not on PATH. Please install Git and retry."
	}
}

function Read-GitHubConfig {
	$scriptRoot = $PSScriptRoot
	$configPath = Join-Path $scriptRoot 'config' | Join-Path -ChildPath 'github_config.json'
	if (-not (Test-Path -Path $configPath)) {
		throw "Config file not found at: $configPath"
	}
	$config = Get-Content -Raw -Path $configPath | ConvertFrom-Json
	if (-not $config.username) { throw "Missing 'username' in github_config.json" }
	if (-not $config.token) { throw "Missing 'token' in github_config.json" }
	return $config
}

function Get-GitHubHeaders([string] $token) {
	return @{ Authorization = "token $token"; 'User-Agent' = 'projectscanner' }
}

function Test-GitHubToken([string] $baseApi, [hashtable] $headers) {
	try {
		$me = Invoke-RestMethod -Method Get -Uri ("{0}/user" -f $baseApi) -Headers $headers
		return $me
	} catch {
		throw "Failed to validate GitHub token: $($_.Exception.Message)"
	}
}

function Get-AllRepos([string] $baseApi, [hashtable] $headers) {
	$all = @()
	$page = 1
	$perPage = 100
	$affiliation = 'owner,collaborator,organization_member'
	while ($true) {
		$uri = "{0}/user/repos?per_page={1}&page={2}&affiliation={3}" -f $baseApi, $perPage, $page, $affiliation
		$batch = Invoke-RestMethod -Method Get -Uri $uri -Headers $headers
		if (-not $batch -or $batch.Count -eq 0) { break }
		$all += $batch
		$page += 1
	}
	return $all
}

function New-ReposRoot {
	$scriptRoot = $PSScriptRoot
	$reposRoot = Join-Path $scriptRoot 'repos'
	if (-not (Test-Path -Path $reposRoot)) {
		[void](New-Item -ItemType Directory -Path $reposRoot)
	}
	return $reposRoot
}

function Get-AuthenticatedCloneUrl([string] $cloneUrl, [string] $username, [string] $token) {
	# Builds https://username:token@host/owner/repo.git
	$u = [Uri]$cloneUrl
	$authPart = "{0}:{1}" -f $username, $token
	$rebuilt = "https://{0}@{1}{2}" -f $authPart, $u.Authority, $u.AbsolutePath
	return $rebuilt
}

function Clone-Or-UpdateRepo($repo, [string] $reposRoot, [string] $username, [string] $token) {
	$fullName = $repo.full_name  # owner/repo
	$owner, $name = $fullName -split '/'
	$ownerDir = Join-Path $reposRoot $owner
	if (-not (Test-Path -Path $ownerDir)) {
		[void](New-Item -ItemType Directory -Path $ownerDir)
	}
	$targetDir = Join-Path $ownerDir $name
	if (Test-Path -Path $targetDir) {
		if (Test-Path -Path (Join-Path $targetDir '.git')) {
			Write-Host ("[skip] {0} already cloned → {1}" -f $fullName, $targetDir)
			return
		} else {
			throw "Target path exists but is not a git repo: $targetDir"
		}
	}
	$authUrl = Get-AuthenticatedCloneUrl -cloneUrl $repo.clone_url -username $username -token $token
	Write-Host ("[clone] {0}" -f $fullName)
	$null = git clone --recurse-submodules --progress `
		"$authUrl" `
		"$targetDir"
}

try {
	Ensure-GitAvailable
	$config = Read-GitHubConfig
	$baseApi = if ($config.PSObject.Properties.Name -contains 'api_base' -and $config.api_base) { $config.api_base } else { 'https://api.github.com' }
	$headers = Get-GitHubHeaders -token $config.token
	$me = Test-GitHubToken -baseApi $baseApi -headers $headers
	Write-Host ("Authenticated as: {0}" -f $me.login)
	$repos = Get-AllRepos -baseApi $baseApi -headers $headers
	Write-Host ("Discovered {0} repositories" -f $repos.Count)
	$reposRoot = New-ReposRoot
	foreach ($repo in $repos) {
		try {
			Clone-Or-UpdateRepo -repo $repo -reposRoot $reposRoot -username $config.username -token $config.token
		} catch {
			Write-Warning ("[error] {0}: {1}" -f $repo.full_name, $_.Exception.Message)
		}
	}
	Write-Host "All done."
} catch {
	Write-Error $_
	exit 1
}
