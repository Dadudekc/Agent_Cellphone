# Autonomous Development Workflow Launcher
# This script launches the systematic repo-to-beta transformation workflow

Write-Host "🚀 Autonomous Development Workflow Launcher" -ForegroundColor Green
Write-Host "===============================================" -ForegroundColor Green
Write-Host ""

Write-Host "🎯 Mission: Transform all repos in D:\repos\Dadudekc to beta-ready state" -ForegroundColor Yellow
Write-Host "⏱️  Duration: 8 hours (16 x 30-minute cycles)" -ForegroundColor Yellow
Write-Host "👥 Agents: 5-agent layout with specialized roles" -ForegroundColor Yellow
Write-Host "📊 Phases: 8 systematic phases with smart Ctrl+T strategy" -ForegroundColor Yellow
Write-Host ""

# Check prerequisites
Write-Host "🔍 Checking prerequisites..." -ForegroundColor Cyan

# Check if coordinates are calibrated
if (-not (Test-Path "runtime\agent_comms\cursor_agent_coords.json")) {
    Write-Host "❌ Error: Coordinates not calibrated. Run calibrate_coords.py first." -ForegroundColor Red
    exit 1
}

# Check if agent workspaces exist
if (-not (Test-Path "agent_workspaces\Agent-1")) {
    Write-Host "❌ Error: Agent workspaces not set up. Run agent setup first." -ForegroundColor Red
    exit 1
}

# Check if response capture is configured
if (-not (Test-Path "runtime\config\agent_capture.yaml")) {
    Write-Host "❌ Error: Response capture not configured." -ForegroundColor Red
    exit 1
}

Write-Host "✅ All prerequisites met!" -ForegroundColor Green
Write-Host ""

# Display workflow overview
Write-Host "📋 Workflow Overview:" -ForegroundColor Cyan
Write-Host "  Phase 1: Assessment & Planning (Ctrl+T: Yes)" -ForegroundColor White
Write-Host "  Phase 2: Implementation Start (Ctrl+T: No)" -ForegroundColor White
Write-Host "  Phase 3: Progress Check (Ctrl+T: No)" -ForegroundColor White
Write-Host "  Phase 4: Implementation Continue (Ctrl+T: No)" -ForegroundColor White
Write-Host "  Phase 5: Mid-Course Correction (Ctrl+T: Yes)" -ForegroundColor White
Write-Host "  Phase 6: Implementation Final (Ctrl+T: No)" -ForegroundColor White
Write-Host "  Phase 7: Testing & Validation (Ctrl+T: Yes)" -ForegroundColor White
Write-Host "  Phase 8: Documentation & Deployment (Ctrl+T: No)" -ForegroundColor White
Write-Host ""

Write-Host "👥 Agent Roles:" -ForegroundColor Cyan
Write-Host "  Agent-1: Repository Assessment Specialist" -ForegroundColor White
Write-Host "  Agent-2: Implementation Architect" -ForegroundColor White
Write-Host "  Agent-3: Quality Assurance Engineer" -ForegroundColor White
Write-Host "  Agent-4: Documentation & DevOps Specialist" -ForegroundColor White
Write-Host "  Agent-5: Workflow Coordinator & Captain" -ForegroundColor White
Write-Host ""

Write-Host "🎯 Target Repositories:" -ForegroundColor Cyan
Write-Host "  SWARM, MLRobotmaker, DaDudekC, FocusForge, HCshinobi" -ForegroundColor White
Write-Host "  Focus: Reduce duplication, consolidate utilities, add tests" -ForegroundColor White
Write-Host "  Strategy: Small, verifiable improvements with TASK_LIST.md focus" -ForegroundColor White
Write-Host ""

# Confirm launch
$confirm = Read-Host "🚀 Ready to launch Autonomous Development Workflow? (y/n)"
if ($confirm -ne "y" -and $confirm -ne "Y") {
    Write-Host "❌ Workflow launch cancelled." -ForegroundColor Red
    exit 0
}

Write-Host ""
Write-Host "🚀 Launching Autonomous Development Workflow..." -ForegroundColor Green
Write-Host ""

# Launch the overnight runner with autonomous workflow configuration
$command = @"
python overnight_runner/runner.py `
  --layout 5-agent `
  --agents Agent-1,Agent-2,Agent-3,Agent-4 `
  --plan autonomous-development-workflow `
  --focus-repo "SWARM,MLRobotmaker,DaDudekC,FocusForge,HCshinobi" `
  --beta-ready-checklist "tests,build,deploy,docs,ui,monitoring,security,performance" `
  --duration-min 480 `
  --interval-sec 1800 `
  --capture-enabled `
  --capture-config runtime/config/agent_capture.yaml `
  --coords-json runtime/agent_comms/cursor_agent_coords.json `
  --fsm-enabled `
  --fsm-agent Agent-5 `
  --fsm-workflow autonomous-development `
  --new-chat `
  --max-new-chats-per-agent 8 `
  --new-chat-interval-sec 1800
"@

Write-Host "📝 Command:" -ForegroundColor Cyan
Write-Host $command -ForegroundColor White
Write-Host ""

# Execute the command
Write-Host "🔄 Executing workflow..." -ForegroundColor Green
Write-Host ""

try {
    Invoke-Expression $command
} catch {
    Write-Host "❌ Error launching workflow: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "✅ Autonomous Development Workflow launched successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "📊 Monitor Progress:" -ForegroundColor Cyan
Write-Host "  - Check agent_workspaces/Agent-X/response.txt for progress reports" -ForegroundColor White
Write-Host "  - Monitor runtime/agent_comms/inbox/ for captured responses" -ForegroundColor White
Write-Host "  - Watch logs/runner.log for system activity" -ForegroundColor White
Write-Host ""
Write-Host "🎯 Expected Results:" -ForegroundColor Cyan
Write-Host "  - 2-3 repos making progress per cycle" -ForegroundColor White
Write-Host "  - 1-2 repos reaching beta-readiness per day" -ForegroundColor White
Write-Host "  - Systematic transformation of all repositories" -ForegroundColor White
Write-Host ""
Write-Host "🚀 Good luck, agents! Let's bring these repos to beta! 🎯" -ForegroundColor Green
