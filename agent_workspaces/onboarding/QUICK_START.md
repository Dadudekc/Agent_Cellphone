# ⚡ Dream.OS Quick Start Guide

## 🚀 Get Started in 5 Minutes

Welcome to Dream.OS! This guide will get you up and running quickly using our CLI tool for agent communication.

## 📋 Prerequisites

### System Requirements
- Python 3.8 or higher
- PyQt5 (for GUI components)
- Network connectivity
- Agent workspace directory

### Quick Setup
```bash
# 1. Navigate to project root
cd /path/to/Agent_CellPhone

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create agent workspace
mkdir -p agent_workspaces/Agent-1
cd agent_workspaces/Agent-1

# 4. Initialize workspace structure
mkdir inbox outbox logs temp
touch notes.md status.json task_list.json
```

## 🎯 Essential First Steps

### 1. Status Reporting (MANDATORY)
**You MUST update your `status.json` after every action, state change, or message.**

```python
def update_status(agent_id, status, current_task, message=""):
    import os, json, datetime
    path = os.path.join(os.getcwd(), "status.json")
    data = {
        "agent_id": agent_id,
        "status": status,
        "current_task": current_task,
        "message": message,
        "last_updated": datetime.datetime.utcnow().isoformat() + "Z"
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

# Example usage
update_status("Agent-1", "ready", "Onboarding", "Ready to begin!")
```

**Status values:**
- `ready` – idle, waiting for task
- `busy` – working on a task
- `paused` – waiting for input or paused
- `offline` – agent is stopped
- `error` – encountered a problem

### 2. Agent Communication via CLI Tool
**This is the PRIMARY method for all agent-to-agent communication:**

```bash
# From project root - send to specific agent
python src/agent_cell_phone.py -a Agent-2 -m "Hello from Agent-1!" -t normal

# Broadcast to all agents
python src/agent_cell_phone.py -m "System update for all agents" -t normal

# Send with specific tag
python src/agent_cell_phone.py -a Agent-3 -m "Task complete" -t task

# Use predefined mode
python src/agent_cell_phone.py -a Agent-2 --mode resume
```

### 3. Test Your Setup
Run the test harness to verify everything works:

```bash
# From project root
python test_harness.py
```

## 📡 Core CLI Commands

### Message Commands
```bash
# Send to specific agent
python src/agent_cell_phone.py -a Agent-2 -m "Hello there!"

# Broadcast to all agents
python src/agent_cell_phone.py -m "System update"

# Send with specific tag
python src/agent_cell_phone.py -a Agent-3 -m "Task complete" -t task

# Use predefined mode
python src/agent_cell_phone.py -a Agent-2 --mode resume
```

### System Commands
```bash
# List available layouts
python src/agent_cell_phone.py --list-layouts

# List agents in current layout
python src/agent_cell_phone.py --list-agents

# Test mode (no actual GUI interaction)
python src/agent_cell_phone.py --test -a Agent-2 -m "Test message"
```

### Message Tags
```bash
# Normal communication
python src/agent_cell_phone.py -a Agent-2 -m "Status update" -t normal

# Task assignment
python src/agent_cell_phone.py -a Agent-2 -m "Please implement the login feature" -t task

# Coordination
python src/agent_cell_phone.py -a Agent-2 -m "Let's coordinate on the API design" -t coordinate

# Reply
python src/agent_cell_phone.py -a Agent-2 -m "Task completed successfully" -t reply

# Integration
python src/agent_cell_phone.py -a Agent-2 -m "Ready to integrate with your component" -t integrate
```

## 🏢 Workspace Structure

### Required Directories
```
Agent-1/
├── inbox/          # Incoming messages and tasks
├── outbox/         # Completed work and sent messages
├── logs/           # Agent logs
├── temp/           # Temporary files (auto-cleanup)
├── notes.md        # Personal notes and planning
├── status.json     # Current status (MANDATORY)
└── task_list.json  # Assigned tasks
```

### File Management
- **Work products**: Place in `outbox/`
- **Temporary files**: Place in `temp/` (auto-cleanup after 24 hours)
- **Logs**: Place in `logs/`
- **Personal notes**: Use `notes.md`
- **Status updates**: Update `status.json` after every action

## 🔄 Basic Workflow

### 1. Receive Task
- Check `inbox/` for new messages
- Update `status.json` to "busy"
- Read task details in `task_list.json`

### 2. Execute Task
- Work on assigned task
- Update progress in `task_list.json`
- Update `status.json` with current activity

### 3. Complete Task
- Place completed work in `outbox/`
- Update `status.json` to "ready"
- Send completion notification via CLI:
  ```bash
  python src/agent_cell_phone.py -a Agent-1 -m "Task completed successfully" -t reply
  ```

### 4. Communication
- **Send messages using CLI commands** (primary method)
- Receive messages in `inbox/`
- Acknowledge all messages within 30 seconds

## 🚨 Emergency Procedures

### System Issues
1. **Stop current task** immediately
2. **Update status** to "error" with clear message
3. **Notify coordinator** via CLI:
   ```bash
   python src/agent_cell_phone.py -a Agent-1 -m "System error encountered" -t normal
   ```
4. **Follow escalation** procedures if needed

### Communication Issues
1. **Check network** connectivity
2. **Verify coordinates** configuration
3. **Test basic commands** in test mode:
   ```bash
   python src/agent_cell_phone.py --test -a Agent-2 -m "Test message"
   ```
4. **Contact system admin** if issues persist

## 📚 Next Steps

### Complete Onboarding
1. **Read CORE_PROTOCOLS.md**: Essential protocols
2. **Follow ONBOARDING_GUIDE.md**: Complete onboarding process
3. **Review BEST_PRACTICES.md**: Best practices for success
4. **Study DEVELOPMENT_STANDARDS.md**: Development guidelines

### Practice Exercises
1. **Send test messages** to other agents using CLI
2. **Complete sample tasks** from `inbox/`
3. **Practice status updates** after every action
4. **Test emergency procedures** in safe environment

### Advanced Features
1. **GUI Interface**: Try `python gui/dream_os_gui_v2.py`
2. **Agent Messenger**: Use `python scripts/agent_messenger.py`
3. **Interactive Mode**: Test `python scripts/agent_messenger.py --interactive`
4. **Multi-Agent Layouts**: Test 4-agent and 8-agent layouts

## 🔧 Troubleshooting

### Common Issues
- **"Agent not found"**: Check coordinate configuration
- **"Message not sent"**: Verify network connectivity
- **"Status not updating"**: Check file permissions
- **"GUI not working"**: Verify PyQt5 installation

### Getting Help
- **System Admin**: For technical issues
- **Training Team**: For onboarding questions
- **Development Team**: For system improvements
- **Emergency**: Use emergency protocols

---

**Version**: 3.0 (CLI-Focused)  
**Primary Method**: `python src/agent_cell_phone.py` for all agent communication 