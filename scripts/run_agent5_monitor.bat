@echo off
REM Agent-5 Monitor Runner for Windows
REM ===================================
REM This script runs the Agent-5 production monitor

echo 🤖 Starting Agent-5 Production Monitor...
echo.

REM Set environment variables
set AGENT_STALL_SEC=1200
set AGENT_CHECK_SEC=5
set AGENT_FILE_ROOT=agent_workspaces
set AGENT_FSM_ENABLED=1
set AGENT_RESCUE_COOLDOWN_SEC=300
set AGENT_ACTIVE_GRACE_SEC=300

echo 📊 Configuration:
echo    Stall threshold: %AGENT_STALL_SEC% seconds
echo    Check interval: %AGENT_CHECK_SEC% seconds
echo    File root: %AGENT_FILE_ROOT%
echo    FSM enabled: %AGENT_FSM_ENABLED%
echo    Rescue cooldown: %AGENT_RESCUE_COOLDOWN_SEC% seconds
echo    Active grace: %AGENT_ACTIVE_GRACE_SEC% seconds
echo.

REM Run the monitor
python -m src.agent_monitors.agent5_monitor

echo.
echo ✅ Agent-5 Monitor stopped.
pause
