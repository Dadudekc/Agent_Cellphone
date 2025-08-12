@echo off
echo Starting Personal Jarvis...
echo.
echo This will launch your personal AI assistant that can control Cursor
echo and your entire development environment.
echo.
echo Make sure your microphone and speakers are working.
echo.
pause

cd /d "%~dp0"
python personal_jarvis.py

pause 