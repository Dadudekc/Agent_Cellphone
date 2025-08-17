# Agent Cellphone Auto Mode Startup Script
Write-Host "🚀 Starting Agent Cellphone Auto Mode..." -ForegroundColor Green
Write-Host ""
Write-Host "🎯 Replacing 'Overnight System' with clear 'Auto Mode'" -ForegroundColor Cyan
Write-Host "📚 Comprehensive setup guide and automation" -ForegroundColor Cyan
Write-Host "🤖 4 specialized coordination agents" -ForegroundColor Cyan
Write-Host "🔗 Discord integration and democratic coordination" -ForegroundColor Cyan
Write-Host "📈 Auto-scaling up to 100 repositories" -ForegroundColor Cyan
Write-Host ""

# Change to project directory
Set-Location $PSScriptRoot\..

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"

# Start Auto Mode
Write-Host "Starting Auto Mode System..." -ForegroundColor Green
python AUTO_MODE_IMPLEMENTATION.py

Write-Host ""
Write-Host "Press any key to continue..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")


