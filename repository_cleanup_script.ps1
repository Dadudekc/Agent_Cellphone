# Repository Cleanup Automation Script
# For Dadudekc Portfolio Standardization
# Usage: .\repository_cleanup_script.ps1 [REPO_NAME]

param(
    [Parameter(Mandatory=$true)]
    [string]$RepositoryName,
    
    [Parameter(Mandatory=$false)]
    [string]$BasePath = "D:\repos\Dadudekc"
)

# Colors for output
$Red = "Red"
$Green = "Green"
$Yellow = "Yellow"
$Cyan = "Cyan"
$White = "White"

# Function to write colored output
function Write-ColorOutput {
    param(
        [string]$Message,
        [string]$Color = $White
    )
    Write-Host $Message -ForegroundColor $Color
}

# Function to check if git is available
function Test-GitAvailable {
    try {
        $null = git --version
        return $true
    }
    catch {
        return $false
    }
}

# Function to check if GitHub CLI is available
function Test-GitHubCLIAvailable {
    try {
        $null = gh --version
        return $true
    }
    catch {
        return $false
    }
}

# Function to create cleanup report
function New-CleanupReport {
    param(
        [string]$RepoPath,
        [string]$RepoName,
        [int]$BranchesRemoved,
        [int]$PRsMerged,
        [string]$Status
    )
    
    $reportPath = Join-Path $RepoPath "cleanup_report.txt"
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    
    @"
Repository: $RepoName
Cleanup Date: $timestamp
Branches Removed: $BranchesRemoved
PRs Merged: $PRsMerged
Status: $Status
Cleanup Script: repository_cleanup_script.ps1
"@ | Out-File -FilePath $reportPath -Encoding UTF8
    
    Write-ColorOutput "✓ Cleanup report created: $reportPath" $Green
}

# Function to analyze repository status
function Analyze-Repository {
    param([string]$RepoPath)
    
    Write-ColorOutput "`n🔍 Analyzing repository: $RepositoryName" $Cyan
    
    # Check git status
    Write-ColorOutput "Checking git status..." $Yellow
    $gitStatus = git -C $RepoPath status --porcelain
    if ($gitStatus) {
        Write-ColorOutput "⚠️  Uncommitted changes detected:" $Yellow
        $gitStatus | ForEach-Object { Write-ColorOutput "  $_" $Yellow }
    } else {
        Write-ColorOutput "✓ No uncommitted changes" $Green
    }
    
    # Check branches
    Write-ColorOutput "`nChecking branches..." $Yellow
    $localBranches = git -C $RepoPath branch --format="%(refname:short)")
    $remoteBranches = git -C $RepoPath branch -r --format="%(refname:short)")
    
    Write-ColorOutput "Local branches:" $Cyan
    $localBranches | ForEach-Object { Write-ColorOutput "  $_" $White }
    
    Write-ColorOutput "`nRemote branches:" $Cyan
    $remoteBranches | ForEach-Object { Write-ColorOutput "  $_" $White }
    
    return @{
        LocalBranches = $localBranches
        RemoteBranches = $remoteBranches
        HasUncommittedChanges = [bool]$gitStatus
    }
}

# Function to cleanup branches
function Remove-ExtraBranches {
    param(
        [string]$RepoPath,
        [array]$LocalBranches,
        [array]$RemoteBranches
    )
    
    Write-ColorOutput "`n🧹 Cleaning up branches..." $Cyan
    
    $branchesRemoved = 0
    
    # Remove local feature branches (keep only main/master)
    foreach ($branch in $LocalBranches) {
        if ($branch -notin @("main", "master")) {
            try {
                Write-ColorOutput "  Deleting local branch: $branch" $Yellow
                git -C $RepoPath branch -D $branch
                $branchesRemoved++
                Write-ColorOutput "    ✓ Deleted" $Green
            }
            catch {
                Write-ColorOutput "    ❌ Failed to delete: $branch" $Red
            }
        }
    }
    
    # Remove remote feature branches (keep only origin/main, origin/master)
    foreach ($branch in $RemoteBranches) {
        if ($branch -notin @("origin/main", "origin/master")) {
            try {
                $branchName = $branch.Replace("origin/", "")
                Write-ColorOutput "  Deleting remote branch: $branchName" $Yellow
                git -C $RepoPath push origin --delete $branchName
                $branchesRemoved++
                Write-ColorOutput "    ✓ Deleted" $Green
            }
            catch {
                Write-ColorOutput "    ❌ Failed to delete: $branch" $Red
            }
        }
    }
    
    return $branchesRemoved
}

# Function to handle PRs
function Handle-PullRequests {
    param([string]$RepoPath)
    
    Write-ColorOutput "`n📋 Handling Pull Requests..." $Cyan
    
    if (-not (Test-GitHubCLIAvailable)) {
        Write-ColorOutput "⚠️  GitHub CLI not available. Manual PR review required." $Yellow
        return 0
    }
    
    $prsMerged = 0
    
    try {
        # List open PRs
        $openPRs = gh -R $RepoPath pr list --state open --json number,title,headRefName
        if ($openPRs) {
            Write-ColorOutput "Open PRs found:" $Yellow
            $openPRs | ForEach-Object { 
                Write-ColorOutput "  PR #$($_.number): $($_.title) (from $($_.headRefName))" $White 
            }
            
            # For now, just list them - agents should review manually
            Write-ColorOutput "`n⚠️  Manual PR review required. Please review each PR individually." $Yellow
        } else {
            Write-ColorOutput "✓ No open PRs found" $Green
        }
        
        # List merged PRs
        $mergedPRs = gh -R $RepoPath pr list --state merged --json number,title,headRefName
        if ($mergedPRs) {
            Write-ColorOutput "`nMerged PRs:" $Cyan
            $mergedPRs | ForEach-Object { 
                Write-ColorOutput "  PR #$($_.number): $($_.title) (from $($_.headRefName))" $White 
            }
            
            # Delete merged PR branches
            foreach ($pr in $mergedPRs) {
                try {
                    Write-ColorOutput "  Deleting merged PR branch: $($pr.headRefName)" $Yellow
                    git -C $RepoPath push origin --delete $pr.headRefName
                    $prsMerged++
                    Write-ColorOutput "    ✓ Deleted" $Green
                }
                catch {
                    Write-ColorOutput "    ❌ Failed to delete: $($pr.headRefName)" $Red
                }
            }
        }
    }
    catch {
        Write-ColorOutput "⚠️  Error handling PRs: $_" $Red
    }
    
    return $prsMerged
}

# Function to standardize repository
function Standardize-Repository {
    param([string]$RepoPath)
    
    Write-ColorOutput "`n🔧 Standardizing repository..." $Cyan
    
    try {
        # Ensure we're on main branch
        $currentBranch = git -C $RepoPath branch --show-current
        if ($currentBranch -ne "main") {
            Write-ColorOutput "  Switching to main branch..." $Yellow
            git -C $RepoPath checkout main
        }
        
        # Pull latest changes
        Write-ColorOutput "  Pulling latest changes..." $Yellow
        git -C $RepoPath pull origin main
        
        # Check if master exists and sync it
        $hasMaster = git -C $RepoPath branch -r | Select-String "origin/master"
        if ($hasMaster) {
            Write-ColorOutput "  Syncing master branch..." $Yellow
            git -C $RepoPath checkout master
            git -C $RepoPath pull origin master
            git -C $RepoPath merge main
            git -C $RepoPath push origin master
            git -C $RepoPath checkout main
        }
        
        Write-ColorOutput "✓ Repository standardized" $Green
    }
    catch {
        Write-ColorOutput "❌ Error standardizing repository: $_" $Red
    }
}

# Function to verify cleanup
function Verify-Cleanup {
    param([string]$RepoPath)
    
    Write-ColorOutput "`n✅ Verifying cleanup..." $Cyan
    
    $localBranches = git -C $RepoPath branch --format="%(refname:short)")
    $remoteBranches = git -C $RepoPath branch -r --format="%(refname:short)")
    
    $allowedLocal = $localBranches | Where-Object { $_ -in @("main", "master") }
    $allowedRemote = $remoteBranches | Where-Object { $_ -in @("origin/main", "origin/master") }
    
    if ($localBranches.Count -eq $allowedLocal.Count -and $remoteBranches.Count -eq $allowedRemote.Count) {
        Write-ColorOutput "✓ Repository cleanup verified successfully!" $Green
        Write-ColorOutput "  Only main/master branches remain" $Green
        return $true
    } else {
        Write-ColorOutput "❌ Repository cleanup incomplete!" $Red
        Write-ColorOutput "  Local branches: $($localBranches.Count) (expected: $($allowedLocal.Count))" $Red
        Write-ColorOutput "  Remote branches: $($remoteBranches.Count) (expected: $($allowedRemote.Count))" $Red
        return $false
    }
}

# Main execution
function Main {
    Write-ColorOutput "🚀 Repository Cleanup Script for Dadudekc Portfolio" $Cyan
    Write-ColorOutput "Repository: $RepositoryName" $White
    Write-ColorOutput "Base Path: $BasePath" $White
    Write-ColorOutput "=" * 50 $Cyan
    
    # Check prerequisites
    if (-not (Test-GitAvailable)) {
        Write-ColorOutput "❌ Git is not available. Please install Git first." $Red
        exit 1
    }
    
    $repoPath = Join-Path $BasePath $RepositoryName
    if (-not (Test-Path $repoPath)) {
        Write-ColorOutput "❌ Repository not found: $repoPath" $Red
        exit 1
    }
    
    if (-not (Test-Path (Join-Path $repoPath ".git"))) {
        Write-ColorOutput "❌ Not a git repository: $repoPath" $Red
        exit 1
    }
    
    # Check GitHub CLI
    $hasGitHubCLI = Test-GitHubCLIAvailable
    Write-ColorOutput "GitHub CLI available: $hasGitHubCLI" $White
    
    # Analyze repository
    $analysis = Analyze-Repository -RepoPath $repoPath
    
    # Handle uncommitted changes
    if ($analysis.HasUncommittedChanges) {
        Write-ColorOutput "`n⚠️  WARNING: Uncommitted changes detected!" $Yellow
        Write-ColorOutput "Please commit or stash changes before proceeding." $Yellow
        Write-ColorOutput "You can run: git add . && git commit -m 'Save work before cleanup'" $White
        $continue = Read-Host "Continue anyway? (y/N)"
        if ($continue -ne "y" -and $continue -ne "Y") {
            Write-ColorOutput "Cleanup cancelled by user." $Yellow
            exit 0
        }
    }
    
    # Handle PRs
    $prsMerged = Handle-PullRequests -RepoPath $repoPath
    
    # Cleanup branches
    $branchesRemoved = Remove-ExtraBranches -RepoPath $repoPath -LocalBranches $analysis.LocalBranches -RemoteBranches $analysis.RemoteBranches
    
    # Standardize repository
    Standardize-Repository -RepoPath $repoPath
    
    # Verify cleanup
    $cleanupSuccess = Verify-Cleanup -RepoPath $repoPath
    
    # Create cleanup report
    $status = if ($cleanupSuccess) { "CLEANED" } else { "PARTIAL" }
    New-CleanupReport -RepoPath $repoPath -RepoName $RepositoryName -BranchesRemoved $branchesRemoved -PRsMerged $prsMerged -Status $status
    
    # Summary
    Write-ColorOutput "`n" $White
    Write-ColorOutput "=" * 50 $Cyan
    Write-ColorOutput "📊 CLEANUP SUMMARY" $Cyan
    Write-ColorOutput "=" * 50 $Cyan
    Write-ColorOutput "Repository: $RepositoryName" $White
    Write-ColorOutput "Branches Removed: $branchesRemoved" $White
    Write-ColorOutput "PRs Merged: $prsMerged" $White
    Write-ColorOutput "Status: $status" $White
    Write-ColorOutput "=" * 50 $Cyan
    
    if ($cleanupSuccess) {
        Write-ColorOutput "🎉 Repository cleanup completed successfully!" $Green
    } else {
        Write-ColorOutput "⚠️  Repository cleanup completed with issues. Manual review required." $Yellow
    }
}

# Execute main function
Main
