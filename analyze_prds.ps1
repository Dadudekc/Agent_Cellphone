# Comprehensive PRD Analysis Script for Dadudekc Workspace
# Analyzes all repositories for PRD status

$workspacePath = "D:\repos\Dadudekc"
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

Write-Host "Starting comprehensive PRD analysis of $workspacePath" -ForegroundColor Green
Write-Host "Timestamp: $timestamp" -ForegroundColor Yellow
Write-Host "=" * 80 -ForegroundColor Cyan

# Get all repositories
$repos = Get-ChildItem -Path $workspacePath -Directory
Write-Host "Found $($repos.Count) repositories" -ForegroundColor Green

# Initialize counters
$totalRepos = $repos.Count
$reposWithPRD = 0
$reposWithoutPRD = 0
$completePRDs = 0
$incompletePRDs = 0

# Results array
$results = @()

# Analyze each repository
for ($i = 0; $i -lt $repos.Count; $i++) {
    $repo = $repos[$i]
    $repoName = $repo.Name
    $repoPath = $repo.FullName
    
    Write-Host "[$($i+1):$totalRepos] Analyzing: $repoName" -ForegroundColor White
    
    # Initialize analysis object
    $analysis = @{
        Repository = $repoPath
        Name = $repoName
        HasPRD = $false
        HasREADME = $false
        HasRequirements = $false
        PRDStatus = "NOT_FOUND"
        READMEStatus = "NOT_FOUND"
        RequirementsStatus = "NOT_FOUND"
        Files = @()
        PRDContent = $null
        READMEContent = $null
        RequirementsContent = $null
    }
    
    try {
        # Get all files in repository
        $files = Get-ChildItem -Path $repoPath -Recurse -File | ForEach-Object { 
            $_.FullName.Replace($repoPath, "").TrimStart("\") 
        }
        $analysis.Files = $files
        
        # Check for PRD.md
        $prdPath = Join-Path $repoPath "PRD.md"
        if (Test-Path $prdPath) {
            $analysis.HasPRD = $true
            $analysis.PRDStatus = "EXISTS"
            try {
                $content = Get-Content $prdPath -Raw -Encoding UTF8
                if ($content.Length -gt 500) {
                    $analysis.PRDContent = $content.Substring(0, 500) + "..."
                } else {
                    $analysis.PRDContent = $content
                }
                
                # Check for placeholders
                if ($content -match "placeholder|TODO|FIXME|\[.*\]") {
                    $analysis.PRDStatus = "INCOMPLETE_PLACEHOLDERS"
                } else {
                    $analysis.PRDStatus = "COMPLETE"
                }
            } catch {
                $analysis.PRDContent = "Error reading PRD: $($_.Exception.Message)"
            }
        }
        
        # Check for README.md
        $readmePath = Join-Path $repoPath "README.md"
        if (Test-Path $readmePath) {
            $analysis.HasREADME = $true
            $analysis.READMEStatus = "EXISTS"
            try {
                $content = Get-Content $readmePath -Raw -Encoding UTF8
                if ($content.Length -gt 500) {
                    $analysis.READMEContent = $content.Substring(0, 500) + "..."
                } else {
                    $analysis.READMEContent = $content
                }
            } catch {
                $analysis.READMEContent = "Error reading README: $($_.Exception.Message)"
            }
        }
        
        # Check for requirements.txt
        $reqPath = Join-Path $repoPath "requirements.txt"
        if (Test-Path $reqPath) {
            $analysis.HasRequirements = $true
            $analysis.RequirementsStatus = "EXISTS"
            try {
                $content = Get-Content $reqPath -Raw -Encoding UTF8
                if ($content.Length -gt 500) {
                    $analysis.RequirementsContent = $content.Substring(0, 500) + "..."
                } else {
                    $analysis.RequirementsContent = $content
                }
            } catch {
                $analysis.RequirementsContent = "Error reading requirements: $($_.Exception.Message)"
            }
        }
        
        # Update counters
        if ($analysis.HasPRD) {
            $reposWithPRD++
            if ($analysis.PRDStatus -eq "COMPLETE") {
                $completePRDs++
            } elseif ($analysis.PRDStatus -eq "INCOMPLETE_PLACEHOLDERS") {
                $incompletePRDs++
            }
        } else {
            $reposWithoutPRD++
        }
        
    } catch {
        $analysis.Error = $_.Exception.Message
    }
    
    # Add to results
    $results += $analysis
    
    # Print status
    $statusIcon = if ($analysis.HasPRD) { "✅" } else { "❌" }
    Write-Host "    $statusIcon PRD: $($analysis.PRDStatus)" -ForegroundColor $(if ($analysis.HasPRD) { "Green" } else { "Red" })
}

# Generate summary
Write-Host "`n" + ("=" * 80) -ForegroundColor Cyan
Write-Host "ANALYSIS SUMMARY" -ForegroundColor Green
Write-Host "=" * 80 -ForegroundColor Cyan

Write-Host "Total Repositories: $totalRepos" -ForegroundColor White
Write-Host "With PRD: $reposWithPRD ($([math]::Round($reposWithPRD/$totalRepos*100, 1))%)" -ForegroundColor Green
Write-Host "Without PRD: $reposWithoutPRD ($([math]::Round($reposWithoutPRD/$totalRepos*100, 1))%)" -ForegroundColor Red
Write-Host "Complete PRDs: $completePRDs" -ForegroundColor Green
Write-Host "Incomplete PRDs: $incompletePRDs" -ForegroundColor Yellow

# Save detailed results
$outputFile = "comprehensive_prd_analysis_$(Get-Date -Format 'yyyyMMdd_HHmmss').json"
$results | ConvertTo-Json -Depth 10 | Out-File $outputFile -Encoding UTF8
Write-Host "`nDetailed results saved to: $outputFile" -ForegroundColor Green

# List repositories without PRDs
Write-Host "`nRepositories WITHOUT PRDs:" -ForegroundColor Red
Write-Host "-" * 40 -ForegroundColor Red
foreach ($repo in $results) {
    if (-not $repo.HasPRD) {
        Write-Host "❌ $($repo.Name)" -ForegroundColor Red
    }
}

# List repositories with incomplete PRDs
Write-Host "`nRepositories with INCOMPLETE PRDs (placeholders):" -ForegroundColor Yellow
Write-Host "-" * 50 -ForegroundColor Yellow
foreach ($repo in $results) {
    if ($repo.PRDStatus -eq "INCOMPLETE_PLACEHOLDERS") {
        Write-Host "⚠️  $($repo.Name)" -ForegroundColor Yellow
    }
}

Write-Host "`nAnalysis complete!" -ForegroundColor Green
