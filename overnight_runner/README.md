# Overnight Runner – Autonomous Multi-Agent Coordination System

This directory contains the core orchestration system for coordinating autonomous AI agents using the Agent Cell Phone (ACP) framework. The system enables multiple agents to work simultaneously on development tasks while maintaining coordinated progress through structured workflows.

## 🏗️ System Architecture

### Core Components Integration

The overnight runner connects with Agent_Cellphone's core components to create a complete autonomous development system:

```
Core Components (Foundation)          Overnight Runner (Orchestration)
├── MultimodalAgent                    ├── Runner (sends scheduled prompts)
├── DevAutomationAgent                 ├── Listener (receives agent responses)  
├── InboxListener                      └── FSM Bridge (manages workflows)
└── CommandRouter
```

### How It All Works Together

1. **Runner** sends scheduled messages to agents through their Cursor input areas
2. **Agents** work autonomously and send structured responses via JSON files
3. **Listener** monitors agent inboxes and processes responses
4. **FSM Bridge** manages task states and workflow progression
5. **Core Components** handle message routing and command processing

## 🚀 Key Components

### `runner.py` - The Master Controller
- **Purpose**: Orchestrates the entire multi-agent system overnight
- **Function**: Sends scheduled prompts (RESUME, TASK, COORDINATE, SYNC, VERIFY) to agents
- **Plans**: Supports various work strategies (contracts, autonomous-dev, single-repo-beta, etc.)
- **Integration**: Uses AgentCellPhone to physically type messages into agent input areas

### `listener.py` - The Communication Hub
- **Purpose**: Monitors agent responses and coordinates communication
- **Function**: Watches agent inboxes for new JSON message files
- **Processing**: Routes messages, updates agent states, triggers next actions
- **Integration**: Connects with core InboxListener and MessagePipeline components

### `fsm_bridge.py` - The Workflow Engine
- **Purpose**: Manages Finite State Machine workflows and task assignments
- **Function**: Processes task updates, assigns work, tracks progress
- **Integration**: Bridges core FSM components with the overnight runner system

## 📡 How Communication Works

### Outbound: Runner → Agents
```
Runner → AgentCellPhone → PyAutoGUI → Cursor Input Box → Agent
```

1. **Runner** creates structured messages based on work plans
2. **AgentCellPhone** looks up agent screen coordinates
3. **PyAutoGUI** moves mouse to agent's input area and types the message
4. **Agent** receives prompt and begins working

### Inbound: Agents → System
```
Agent → JSON File → Inbox → Listener → FSM Bridge → System Update
```

1. **Agent** completes task and creates structured response
2. **Response** is written to target agent's inbox directory
3. **Listener** detects new file and processes content
4. **FSM Bridge** updates task state and triggers next actions

## 🔄 Response Collection Methods

### Primary: FSM Updates
Agents send structured task updates:
```json
{
  "type": "fsm_update",
  "task_id": "task_123",
  "state": "completed",
  "summary": "Implemented user authentication",
  "evidence": ["commit_hash", "test_results", "build_output"],
  "repo_path": "D:/repos/auth-service"
}
```

### Secondary: Direct Messages
Agents can send coordination messages:
```json
{
  "type": "note",
  "from": "Agent-1",
  "to": "Agent-2",
  "topic": "coordination",
  "summary": "API endpoints ready",
  "details": {"endpoints": ["/users", "/auth"]}
}
```

## 🛠️ Setup & Configuration

### Prerequisites
- Run commands from `D:\Agent_Cellphone` for proper path resolution
- Calibrate agent screen coordinates once per layout/window configuration
- Keep Cursor windows visible for automated interaction
- Python dependencies installed (`pip install -r requirements.txt`)

### Environment Configuration
Create `.env` in repo root:
```env
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/.../...
DEVLOG_USERNAME=Agent Devlog
```

### Coordinate Calibration
Calibrate agent input box positions:
```powershell
python -c "
import time,json,pyautogui
p='src/runtime/config/cursor_agent_coords.json'
print('Hover over Agent-1 input box (4-agent)...')
time.sleep(6)
x,y=pyautogui.position()
d=json.load(open(p,'r',encoding='utf-8'))
d.setdefault('4-agent',{})
d['4-agent'].setdefault('Agent-1',{})
d['4-agent']['Agent-1']['input_box']={'x':int(x),'y':int(y)}
d['4-agent']['Agent-1']['starter_location_box']={'x':int(x),'y':int(y)}
json.dump(d, open(p,'w',encoding='utf-8'), indent=2)
print('Updated',x,y)
"
```

## 🚀 Quick Start

### 1. Start the Listener (Terminal A)
```powershell
python overnight_runner/listener.py --agent Agent-5 --env-file .env --devlog-embed --devlog-username "Agent Devlog"
```

### 2. Start the Runner (Terminal B)
```powershell
# Set environment variables for optimal operation
$env:ACP_DEFAULT_NEW_CHAT='1'
$env:ACP_AUTO_ONBOARD='1'
$env:ACP_SINGLE_MESSAGE='1'
$env:ACP_MESSAGE_VERBOSITY='extensive'
$env:ACP_NEW_CHAT_INTERVAL_SEC='1800'

# Launch the runner
python overnight_runner/runner.py --layout 5-agent --agents Agent-1,Agent-2,Agent-3,Agent-4 \
  --duration-min 60 --interval-sec 1200 --sender Agent-3 --plan contracts \
  --fsm-enabled --fsm-agent Agent-5 --fsm-workflow default \
  --seed-from-tasklists --skip-assignments --skip-captain-kickoff --skip-captain-fsm-feed \
  --devlog-sends --devlog-embed --devlog-username "Agent Devlog"
```

## 🔧 Run-Forever Scripts

For production resilience, use the PowerShell wrapper scripts:

### Listener Forever
```powershell
pwsh -File scripts/run_listener_forever.ps1 -Agent Agent-5
```

### Runner Forever  
```powershell
pwsh -File scripts/run_runner_forever.ps1 -Agents 'Agent-1,Agent-2,Agent-3,Agent-4' -Layout '5-agent'
```

These scripts automatically restart their respective Python processes on failure and maintain continuous operation.

## 📋 Work Plans

### Contracts Mode
- **Purpose**: Focused work on specific assigned contracts
- **Flow**: Agents receive tasks, execute, report progress via fsm_update
- **Best for**: Structured project work with clear deliverables

### Autonomous-Dev Mode
- **Purpose**: Self-directed development with peer coordination
- **Flow**: Agents choose high-leverage tasks, coordinate with peers
- **Best for**: Exploratory development and system improvements

### Single-Repo-Beta Mode
- **Purpose**: Focused effort to bring a single repository to beta-ready state
- **Flow**: All agents work on same repo with specific checklist items
- **Best for**: Final push to production readiness

### PRD-Milestones Mode
- **Purpose**: Work aligned to Product Requirements Document milestones
- **Flow**: PRD milestones converted to FSM tasks, agents work sequentially
- **Best for**: Milestone-driven development with clear acceptance criteria

## 🔄 Message Flow Examples

### Complete Cycle Example
1. **Runner** sends: "Agent-1 resume: focus the target repo to reach beta-ready"
2. **Agent-1** receives prompt in Cursor input area
3. **Agent-1** works on assigned task
4. **Agent-1** sends fsm_update with progress and evidence
5. **Listener** processes response and updates system state
6. **FSM Bridge** assigns next task or triggers verification

### Response Processing
```
Agent Response → InboxListener → MessagePipeline → CommandRouter → FSM Bridge
     ↓
State Updates + Task Progression + Notifications + Next Actions
```

## 🚨 Troubleshooting

### Common Issues

**"File not found" errors**
- Ensure you're running from `D:\Agent_Cellphone`
- Check that all paths in configuration files are correct

**No typing/automation**
- Verify `src/runtime/config/cursor_agent_coords.json` exists and has correct coordinates
- Ensure Cursor windows are visible and not minimized
- Re-run coordinate calibration if windows were moved

**Too many messages**
- Increase `--interval-sec` for longer cycles
- Adjust `--stagger-ms` and `--jitter-ms` for better pacing
- Use `--suppress-resume` and `--resume-cooldown-sec` to reduce noise

**Discord notifications not working**
- Verify `.env` has correct `DISCORD_WEBHOOK_URL` (no quotes/trailing spaces)
- Test with: `python scripts/devlog_test.py`

### System Recovery
If the system appears broken:

1. **Sync code and dependencies**:
   ```powershell
   git fetch --all --prune
   git pull --rebase origin main
   pip install -r requirements.txt
   ```

2. **Re-verify configuration**:
   - Check coordinates and `.env` file
   - Test listener with: `python scripts/devlog_test.py`

3. **Restart components**:
   - Stop all processes
   - Start listener first, then runner
   - Use run-forever scripts for resilience

## 🎯 Best Practices

### Agent Coordination
- **Check TASK_LIST.md first**: Always review existing tasks before starting new work
- **Prefer reuse**: Look for existing solutions across repositories before creating new code
- **Small commits**: Make incremental, verifiable changes with clear evidence
- **Peer coordination**: Request sanity checks from other agents before large changes

### Response Quality
- **Structured updates**: Use fsm_update format for task progress
- **Evidence inclusion**: Attach commit hashes, test results, build outputs
- **Clear summaries**: Provide concise descriptions of what was accomplished
- **Next steps**: Always indicate what comes next or what's blocking progress

### System Maintenance
- **Monitor logs**: Check `logs/runner.log` and `logs/listener.log` for issues
- **Regular restarts**: Use run-forever scripts for long-running sessions
- **Coordinate updates**: Ensure all agents are using compatible versions
- **Backup states**: Archive important state files before major changes

## 🔗 Integration Points

### With Core Components
- **DevAutomationAgent**: Handles development task automation
- **DevAutomationAgent**: Handles development task automation
- **InboxListener**: Manages message routing and processing
- **CommandRouter**: Processes commands and routes to handlers

### With External Systems
- **Discord**: Devlog notifications and monitoring
- **Git**: Repository management and task tracking
- **File System**: Persistent message storage and state management
- **Cursor IDE**: Direct agent interaction through automated typing

## 📚 Additional Resources

- **Project Structure**: See `PROJECT_STRUCTURE.md` for system overview
- **Agent Communication**: See `INTER_AGENT_COMMUNICATION_GUIDE.md` for detailed protocols
- **FSM Workflows**: See `fsm_data/` directory for workflow definitions
- **Configuration**: See `config/` directory for system settings and templates

---

*This system creates a "digital assembly line" where multiple AI agents can work autonomously while maintaining coordinated progress toward project goals through structured communication and workflow management.*


