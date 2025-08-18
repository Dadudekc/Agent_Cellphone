# Batch Repository Cleanup Script
# For Dadudekc Portfolio Standardization
# Processes multiple repositories in sequence

param(
    [Parameter(Mandatory=$false)]
    [string]$BasePath = "D:\repos\Dadudekc",
    
    [Parameter(Mandatory=$false)]
    [string]$RepositoryList = "",
    
    [Parameter(Mandatory=$false)]
    [string]$AgentNumber = "1"
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

# Function to get repository list based on agent assignment
function Get-RepositoryList {
    param([string]$AgentNum)
    
    switch ($AgentNum) {
        "1" {
            # High-Priority Repositories (Agent-1)
            return @(
                "Agent-5",
                "ai-task-organizer", 
                "network-scanner",
                "AI_Debugger_Assistant",
                "Auto_Blogger",
                "Dream.os",
                "DigitalDreamscape",
                "FocusForge",
                "FreeRideInvestor",
                "gpt_automation",
                "HCshini",
                "Hive-Mind",
                "LSTMmodel_trainer",
                "machinelearningmodelmaker",
                "MLRobotmaker",
                "organizer-validation"
            )
        }
        "2" {
            # Medium-Priority Repositories (Agent-2)
            return @(
                "agentproject",
                "basicbot",
                "bolt-project",
                "content",
                "contract-leads",
                "DaDudekC",
                "DaDudeKC-Website",
                "DreamVault",
                "FreerideinvestorWebsite",
                "FreeWork",
                "ideas",
                "IT_help_desk",
                "machinelearningproject",
                "MeTuber",
                "my-personal-templates",
                "my-resume",
                "NewSims4ModProject"
            )
        }
        "3" {
            # Lower-Priority Repositories (Agent-3)
            return @(
                "Victor.os",
                "Remaining utility projects",
                "Template repositories",
                "Documentation projects",
                "Experimental projects",
                "Legacy systems",
                "Backup repositories"
            )
        }
        "4" {
            # Remaining + Verification (Agent-4)
            return @(
                "All remaining repositories",
                "Verification tasks",
                "Final cleanup"
            )
        }
        default {
            Write-ColorOutput "Invalid agent number. Using Agent-1 list." $Yellow
            return Get-RepositoryList -AgentNum "1"
        }
    }
}

# Function to check if repository exists and is a git repo
function Test-Repository {
    param([string]$RepoPath, [string]$RepoName)
    
    if (-not (Test-Path $RepoPath)) {
        Write-ColorOutput "❌ Repository not found: $RepoName" $Red
        return $false
    }
    
    if (-not (Test-Path (Join-Path $RepoPath ".git"))) {
        Write-ColorOutput "❌ Not a git repository: $RepoName" $Red
        return $false
    }
    
    return $true
}

# Function to run cleanup on single repository
function Invoke-RepositoryCleanup {
    param([string]$RepoName)
    
    $repoPath = Join-Path $BasePath $RepoName
    
    Write-ColorOutput "`n" $White
    Write-ColorOutput "=" * 60 $Cyan
    Write-ColorOutput "🧹 CLEANING REPOSITORY: $RepoName" $Cyan
    Write-ColorOutput "=" * 60 $Cyan
    
    if (-not (Test-Repository -RepoPath $repoPath -RepoName $RepoName)) {
        return @{
            Name = $RepoName
            Status = "SKIPPED"
            BranchesRemoved = 0
            PRsMerged = 0
            Error = "Repository not found or not a git repo"
        }
    }
    
    try {
        # Check git status
        $gitStatus = git -C $repoPath status --porcelain
        $hasUncommittedChanges = [bool]$gitStatus
        
        if ($hasUncommittedChanges) {
            Write-ColorOutput "⚠️  Uncommitted changes detected in $RepoName" $Yellow
            Write-ColorOutput "  Consider committing or stashing changes before cleanup" $Yellow
        }
        
        # Count branches before cleanup
        $localBranchesBefore = (git -C $repoPath branch --format="%(refname:short)").Count
        $remoteBranchesBefore = (git -C $repoPath branch -r --format="%(refname:short)").Count
        
        # Run cleanup commands
        Write-ColorOutput "  Cleaning up branches..." $Yellow
        
        # Remove local feature branches (keep only main/master)
        $localBranches = git -C $repoPath branch --format="%(refname:short)"
        $localBranchesRemoved = 0
        foreach ($branch in $localBranches) {
            if ($branch -notin @("main", "master")) {
                try {
                    git -C $repoPath branch -D $branch | Out-Null
                    $localBranchesRemoved++
                }
                catch {
                    Write-ColorOutput "    Failed to delete local branch: $branch" $Red
                }
            }
        }
        
        # Remove remote feature branches (keep only origin/main, origin/master)
        $remoteBranches = git -C $repoPath branch -r --format="%(refname:short)"
        $remoteBranchesRemoved = 0
        foreach ($branch in $remoteBranches) {
            if ($branch -notin @("origin/main", "origin/master")) {
                try {
                    $branchName = $branch.Replace("origin/", "")
                    git -C $repoPath push origin --delete $branchName | Out-Null
                    $remoteBranchesRemoved++
                }
                catch {
                    Write-ColorOutput "    Failed to delete remote branch: $branchName" $Red
                }
            }
        }
        
        $totalBranchesRemoved = $localBranchesRemoved + $remoteBranchesRemoved
        
        # Standardize repository
        Write-ColorOutput "  Standardizing repository..." $Yellow
        
        # Ensure we're on main branch
        $currentBranch = git -C $repoPath branch --show-current
        if ($currentBranch -ne "main") {
            git -C $repoPath checkout main | Out-Null
        }
        
        # Pull latest changes
        git -C $repoPath pull origin main | Out-Null
        
        # Check if master exists and sync it
        $hasMaster = git -C $repoPath branch -r | Select-String "origin/master"
        if ($hasMaster) {
            git -C $repoPath checkout master | Out-Null
            git -C $repoPath pull origin master | Out-Null
            git -C $repoPath merge main | Out-Null
            git -C $repoPath push origin master | Out-Null
            git -C $repoPath checkout main | Out-Null
        }
        
        # Verify cleanup
        $localBranchesAfter = (git -C $repoPath branch --format="%(refname:short)").Count
        $remoteBranchesAfter = (git -C $repoPath branch -r --format="%(refname:short)").Count
        
        $cleanupSuccess = ($localBranchesAfter -le 2) -and ($remoteBranchesAfter -le 2)
        
        # Create cleanup report
        $reportPath = Join-Path $repoPath "cleanup_report.txt"
        $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
        
        @"
Repository: $RepoName
Cleanup Date: $timestamp
Agent: Agent-$AgentNumber
Branches Removed: $totalBranchesRemoved
PRs Merged: 0 (manual review required)
Status: $(if ($cleanupSuccess) { "CLEANED" } else { "PARTIAL" })
Cleanup Script: batch_cleanup_script.ps1
"@ | Out-File -FilePath $reportPath -Encoding UTF8
        
        Write-ColorOutput "✓ Repository cleanup completed for $RepoName" $Green
        Write-ColorOutput "  Branches removed: $totalBranchesRemoved" $White
        Write-ColorOutput "  Status: $(if ($cleanupSuccess) { "CLEANED" } else { "PARTIAL" })" $White
        
        return @{
            Name = $RepoName
            Status = if ($cleanupSuccess) { "CLEANED" } else { "PARTIAL" }
            BranchesRemoved = $totalBranchesRemoved
            PRsMerged = 0
            Error = $null
        }
    }
    catch {
        Write-ColorOutput "❌ Error cleaning up $RepoName: $_" $Red
        return @{
            Name = $RepoName
            Status = "ERROR"
            BranchesRemoved = 0
            PRsMerged = 0
            Error = $_.Exception.Message
        }
    }
}

# Function to create summary report
function New-SummaryReport {
    param(
        [array]$Results,
        [string]$AgentNum,
        [string]$BasePath
    )
    
    $timestamp = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
    $summaryPath = Join-Path $BasePath "cleanup_summary_Agent-$AgentNum`_$timestamp.txt"
    
    $totalRepos = $Results.Count
    $cleanedRepos = ($Results | Where-Object { $_.Status -eq "CLEANED" }).Count
    $partialRepos = ($Results | Where-Object { $_.Status -eq "PARTIAL" }).Count
    $errorRepos = ($Results | Where-Object { $_.Status -eq "ERROR" }).Count
    $skippedRepos = ($Results | Where-Object { $_.Status -eq "SKIPPED" }).Count
    $totalBranchesRemoved = ($Results | Measure-Object -Property BranchesRemoved -Sum).Sum
    
    $summary = @"
=== REPOSITORY CLEANUP SUMMARY ===
Date: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
Agent: Agent-$AgentNumber
Base Path: $BasePath

=== OVERALL STATISTICS ===
Total Repositories Processed: $totalRepos
Successfully Cleaned: $cleanedRepos
Partially Cleaned: $partialRepos
Errors: $errorRepos
Skipped: $skippedRepos
Total Branches Removed: $totalBranchesRemoved

=== DETAILED RESULTS ===
"@
    
    foreach ($result in $Results) {
        $summary += "`n$($result.Name):"
        $summary += "  Status: $($result.Status)"
        $summary += "  Branches Removed: $($result.BranchesRemoved)"
        $summary += "  PRs Merged: $($result.PRsMerged)"
        if ($result.Error) {
            $summary += "  Error: $($result.Error)"
        }
    }
    
    $summary += "`n`n=== RECOMMENDATIONS ==="
    if ($errorRepos -gt 0) {
        $summary += "`n- Review repositories with errors for manual cleanup"
    }
    if ($partialRepos -gt 0) {
        $summary += "`n- Verify partially cleaned repositories meet standards"
    }
    if ($skippedRepos -gt 0) {
        $summary += "`n- Check skipped repositories for git initialization"
    }
    
    $summary | Out-File -FilePath $summaryPath -Encoding UTF8
    
    Write-ColorOutput "`n📊 Summary report created: $summaryPath" $Green
    return $summaryPath
}

# Main execution
function Main {
    Write-ColorOutput "🚀 Batch Repository Cleanup Script for Dadudekc Portfolio" $Cyan
    Write-ColorOutput "Agent: Agent-$AgentNumber" $White
    Write-ColorOutput "Base Path: $BasePath" $White
    Write-ColorOutput "=" * 60 $Cyan
    
    # Get repository list
    if ($RepositoryList) {
        $repositories = $RepositoryList -split ","
        Write-ColorOutput "Using custom repository list: $RepositoryList" $Yellow
    } else {
        $repositories = Get-RepositoryList -AgentNum $AgentNumber
        Write-ColorOutput "Using Agent-$AgentNumber repository list" $Yellow
    }
    
    Write-ColorOutput "`nRepositories to process:" $Cyan
    foreach ($repo in $repositories) {
        Write-ColorOutput "  - $repo" $White
    }
    
    $continue = Read-Host "`nContinue with cleanup? (y/N)"
    if ($continue -ne "y" -and $continue -ne "Y") {
        Write-ColorOutput "Batch cleanup cancelled by user." $Yellow
        exit 0
    }
    
    # Process repositories
    $results = @()
    $startTime = Get-Date
    
    foreach ($repo in $repositories) {
        $result = Invoke-RepositoryCleanup -RepoName $repo
        $results += $result
        
        # Brief pause between repositories
        Start-Sleep -Seconds 2
    }
    
    $endTime = Get-Date
    $duration = $endTime - $startTime
    
    # Create summary report
    $summaryPath = New-SummaryReport -Results $results -AgentNum $AgentNumber -BasePath $BasePath
    
    # Final summary
    Write-ColorOutput "`n" $White
    Write-ColorOutput "=" * 60 $Cyan
    Write-ColorOutput "🎉 BATCH CLEANUP COMPLETED!" $Cyan
    Write-ColorOutput "=" * 60 $Cyan
    
    $totalRepos = $results.Count
    $cleanedRepos = ($results | Where-Object { $_.Status -eq "CLEANED" }).Count
    $totalBranchesRemoved = ($results | Measure-Object -Property BranchesRemoved -Sum).Sum
    
    Write-ColorOutput "Total Repositories: $totalRepos" $White
    Write-ColorOutput "Successfully Cleaned: $cleanedRepos" $Green
    Write-ColorOutput "Total Branches Removed: $totalBranchesRemoved" $White
    Write-ColorOutput "Duration: $($duration.ToString('hh\:mm\:ss'))" $White
    Write-ColorOutput "Summary Report: $summaryPath" $Cyan
    
    Write-ColorOutput "`nNext Steps:" $Yellow
    Write-ColorOutput "1. Review summary report for any issues" $White
    Write-ColorOutput "2. Manually review repositories with errors" $White
    Write-ColorOutput "3. Verify cleanup meets standards" $White
    Write-ColorOutput "4. Submit daily report to coordinator" $White
}

# Execute main function
Main
