@echo off
echo Starting PRD Analysis...
echo.

set count=0
set with_prd=0
set without_prd=0

for /d %%i in (*) do (
    set /a count+=1
    if exist "%%i\PRD.md" (
        echo [%count%] %%i - PRD: EXISTS
        set /a with_prd+=1
    ) else (
        echo [%count%] %%i - PRD: MISSING
        set /a without_prd+=1
    )
)

echo.
echo ========================================
echo ANALYSIS SUMMARY
echo ========================================
echo Total Repositories: %count%
echo With PRD: %with_prd%
echo Without PRD: %without_prd%
echo.
echo Repositories WITHOUT PRDs:
echo ----------------------------------------
for /d %%i in (*) do (
    if not exist "%%i\PRD.md" (
        echo ❌ %%i
    )
)
echo.
echo Analysis complete!
pause
