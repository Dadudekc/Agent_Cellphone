@echo off
title Continuous Agents 1-4 Runner
color 0A
cls

echo.
echo  ██████╗ ██████╗ ███████╗███╗   ██╗████████╗██╗██╗   ██╗ ██████╗ ██╗   ██╗███████╗
echo  ██╔══██╗██╔══██╗██╔════╝████╗  ██║╚══██╔══╝██║██║   ██║██╔═══██╗██║   ██║██╔════╝
echo  ██████╔╝██████╔╝█████╗  ██╔██╗ ██║   ██║   ██║██║   ██║██║   ██║██║   ██║█████╗  
echo  ██╔══██╗██╔══██╗██╔══╝  ██║╚██╗██║   ██║   ██║╚██╗ ██╔╝██║   ██║╚██╗ ██╔╝██╔══╝  
echo  ██████╔╝██║  ██║███████╗██║ ╚████║   ██║   ██║ ╚████╔╝ ╚██████╔╝ ╚████╔╝ ███████╗
echo  ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═══╝   ╚═════╝   ╚═══╝  ╚══════╝
echo.
echo  █████╗  ██████╗ ███████╗███╗   ██╗████████╗███████╗     ██████╗ ██████╗ ████████╗
echo  ██╔══██╗██╔════╝ ██╔════╝████╗  ██║╚══██╔══╝██╔════╝    ██╔═══██╗██╔══██╗╚══██╔══╝
echo  ███████║██║  ███╗█████╗  ██╔██╗ ██║   ██║   █████╗      ██║   ██║██████╔╝   ██║   
echo  ██╔══██║██║   ██║██╔══╝  ██║╚██╗██║   ██║   ██╔══╝      ██║   ██║██╔══██╗   ██║   
echo  ██║  ██║╚██████╔╝███████╗██║ ╚████║   ██║   ███████╗    ╚██████╔╝██║  ██║   ██║   
echo  ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚══════╝     ╚═════╝ ╚═╝  ╚═╝   ╚═╝   
echo.
echo  ================================================================================
echo  🚀 CONTINUOUS AGENTS 1-4 RUNNER 🚀
echo  ================================================================================
echo.
echo  💇‍♀️  This will start Agents 1-4 working continuously while you do your hair!
echo.
echo  👥 Agents that will be working:
echo     • Agent-1: System Coordinator
echo     • Agent-2: Task Manager  
echo     • Agent-3: Data Processor
echo     • Agent-4: Communication Specialist
echo.
echo  ⚡ Features:
echo     • Continuous task assignment every 5 minutes
echo     • Automatic monitoring and rescue
echo     • Smart task rotation to keep agents engaged
echo     • Real-time status updates every 10 minutes
echo.
echo  🎯 Press any key to start the agents...
echo.
pause >nul

cls
echo.
echo  🚀 Starting Continuous Agents 1-4...
echo  ⏳ Please wait while the system initializes...
echo.

python continuous_agents_1_4.py

echo.
echo  ================================================================================
echo  🎉 Agents have stopped running!
echo  💇‍♀️  Hope your hair looks fabulous!
echo  ================================================================================
echo.
pause
