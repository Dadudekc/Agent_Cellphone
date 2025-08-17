@echo off
echo Starting Agent-1 Rescue System...
echo This will prevent Agent-1 from stalling and maintain continuous operation
echo.

REM Change to the project directory
cd /d "%~dp0.."

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.7+ and try again
    pause
    exit /b 1
)

REM Check if required packages are installed
echo Checking required packages...
python -c "import asyncio, aiohttp" >nul 2>&1
if errorlevel 1 (
    echo Installing required packages...
    pip install aiohttp
)

REM Create logs directory if it doesn't exist
if not exist "logs" mkdir logs

REM Start the rescue system
echo Starting Agent-1 Rescue System...
echo Press Ctrl+C to stop the system
echo.
python src/agent_rescue_system.py

pause



