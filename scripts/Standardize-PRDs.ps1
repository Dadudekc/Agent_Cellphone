param(
    [string]$Root = 'D:\repos',
    [switch]$DryRun
)

$ErrorActionPreference = 'Stop'

function Write-Log {
    param([string]$Message)
    Write-Host "[$(Get-Date -Format 'u')] $Message"
}

$summary = @()

# Discover git repositories under the root
$repos = Get-ChildItem -Path $Root -Directory -Recurse -Depth 3 -ErrorAction SilentlyContinue |
    Where-Object { Test-Path (Join-Path $_.FullName '.git') }

foreach ($repo in $repos) {
    try {
        $repoPath = $repo.FullName
        $repoName = Split-Path $repoPath -Leaf
        $docsDir = Join-Path $repoPath 'docs'

        if (-not (Test-Path $docsDir)) {
            if ($DryRun) {
                Write-Log "Would create docs dir in $repoName"
            } else {
                New-Item -ItemType Directory -Path $docsDir | Out-Null
            }
        }

        $canonicalPath = Join-Path $docsDir 'PRD.md'
        $canonicalExists = Test-Path $canonicalPath
        $canonicalHasMarker = $false

        if ($canonicalExists) {
            $canonContent = Get-Content -Path $canonicalPath -Raw -ErrorAction SilentlyContinue
            if ($null -ne $canonContent -and $canonContent -match 'x-standard-prd:\s*v1') {
                $canonicalHasMarker = $true
            }
        }

        if ($canonicalHasMarker) {
            $summary += "SKIP: $repoName (already standardized)"
            continue
        }

        $candidates = Get-ChildItem -Path $repoPath -Recurse -File -Include 'PRD.md','prd.md','*PRD*.md','*prd*.md' -ErrorAction SilentlyContinue |
            Where-Object { $_.FullName -ne $canonicalPath }

        $now = Get-Date -Format 'yyyy-MM-dd'

        $yaml = @(
            '---'
            "title: $repoName Product Requirements Document"
            "repository: $repoPath"
            'owner: Unknown'
            'status: Draft'
            'version: 1.0'
            "last_updated: $now"
            'x-standard-prd: v1'
            '---'
            ''
        )

        $skeleton = @(
            '## Overview','- TBD','',
            '## Problem Statement','- TBD','',
            '## Goals','- TBD','',
            '## Non-Goals','- TBD','',
            '## Target Users','- TBD','',
            '## Scope','- In Scope: TBD','- Out of Scope: TBD','',
            '## Requirements','### Functional','- TBD','',
            '### Non-Functional','- TBD','',
            '## Success Metrics','- TBD','',
            '## Milestones & Timeline','- TBD','',
            '## Assumptions','- TBD','',
            '## Risks & Mitigations','- TBD','',
            '## Open Questions','- TBD','',
            '## Appendix','- TBD',''
        )

        $legacyParts = foreach ($cand in $candidates) {
            try {
                $content = Get-Content -Path $cand.FullName -Raw -ErrorAction SilentlyContinue
                if ($content.Trim().Length -gt 0) {
                    "## Legacy Content from: $($cand.FullName)",'', $content,'','---',''
                }
            } catch { }
        }

        $newContent = ($yaml + $skeleton + $legacyParts) -join "`r`n"

        if (-not $DryRun) {
            if ($canonicalExists -and -not $canonicalHasMarker) {
                $backupPath = "$canonicalPath.backup.$(Get-Date -Format 'yyyyMMddHHmmss').md"
                Copy-Item -Path $canonicalPath -Destination $backupPath -Force -ErrorAction SilentlyContinue
            }
            Set-Content -Path $canonicalPath -Value $newContent -Encoding UTF8
        }

        $summary += if ($DryRun) {
            "WOULD UPDATE: $repoName -> docs\PRD.md"
        } else {
            "UPDATED: $repoName -> docs\PRD.md"
        }
    }
    catch {
        $summary += "ERROR: $($repo.FullName) -> $($_.Exception.Message)"
    }
}

$summary | ForEach-Object { Write-Log $_ }
