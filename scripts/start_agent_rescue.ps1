# Agent-1 Rescue System Startup Script
# This script prevents Agent-1 from stalling and maintains continuous operation

Write-Host "🚀 Starting Agent-1 Rescue System..." -ForegroundColor Green
Write-Host "This will prevent Agent-1 from stalling and maintain continuous operation" -ForegroundColor Yellow
Write-Host ""

# Change to the project directory
Set-Location $PSScriptRoot\..

# Check if Python is available
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Error: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.7+ and try again" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if required packages are installed
Write-Host "Checking required packages..." -ForegroundColor Cyan
try {
    python -c "import asyncio, aiohttp" 2>$null
    Write-Host "✓ Required packages are installed" -ForegroundColor Green
} catch {
    Write-Host "Installing required packages..." -ForegroundColor Yellow
    pip install aiohttp
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Failed to install required packages" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
}

# Create logs directory if it doesn't exist
if (!(Test-Path "logs")) {
    New-Item -ItemType Directory -Path "logs" | Out-Null
    Write-Host "✓ Created logs directory" -ForegroundColor Green
}

# Start the rescue system
Write-Host "Starting Agent-1 Rescue System..." -ForegroundColor Green
Write-Host "Press Ctrl+C to stop the system" -ForegroundColor Yellow
Write-Host ""

try {
    python src/agent_rescue_system.py
} catch {
    Write-Host "❌ Error running rescue system: $_" -ForegroundColor Red
}

Read-Host "Press Enter to exit"



