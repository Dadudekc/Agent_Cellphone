# Continuous Agents 1-4 Starter
# =============================
# Starts agents 1-4 to work continuously while you do your hair!

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Continuous Agents 1-4 Starter" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "🚀 Starting agents 1-4 to work continuously..." -ForegroundColor Green
Write-Host "💇‍♀️ You can now do your hair while they work!" -ForegroundColor Yellow
Write-Host ""
Write-Host "💡 Press Ctrl+C to stop when you're ready." -ForegroundColor Magenta
Write-Host ""

try {
    python continuous_agents_1_4.py
}
catch {
    Write-Host ""
    Write-Host "❌ Error running continuous agents: $_" -ForegroundColor Red
}
finally {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "  Agents stopped. Hope your hair looks great!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    Read-Host "Press Enter to continue..."
}
