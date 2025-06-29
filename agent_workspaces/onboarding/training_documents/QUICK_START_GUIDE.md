# 🚀 Dream.OS Cell Phone - Quick Start Guide

## 📋 Welcome!
Welcome to the Dream.OS Cell Phone multi-agent system!

## ⚡ Quick Setup (5 Minutes)

### Step 1: System Access
```bash
python launch.py
# or
python gui/dream_os_gui.py
```

### Step 2: Agent Identification
- Your agent ID: **Agent-[X]**
- Your workspace: `agent_workspaces/Agent-[X]/`
- Your role: [Assigned during onboarding]

### Step 3: Basic Communication Test
```bash
python scripts/agent_messenger.py --agent Agent-[X] --test
```

## 📡 Essential Commands
```bash
# Send message to another agent
@agent-2 "Hello from Agent-1"

# Broadcast to all agents
@all "System status update"

# Request status
@agent-3 STATUS REQUEST

# Ping agent
@agent-4 PING
```

## 🎭 Your Role
- **Primary Responsibilities**: [Your role description]
- **Key Tasks**: [Main tasks you'll perform]
- **Collaboration**: [How you work with others]
- **Success Metrics**: [Performance measurement]

## 🛠️ Essential Tools
- **GUI Interface**: `gui/dream_os_gui.py`
- **Messenger**: `scripts/agent_messenger.py`
- **Test Suite**: `tests/`
- **Documentation**: `docs/`

## 🔧 Troubleshooting
```bash
# Check connectivity
python tests/diagnostic_test.py --agent Agent-[X]

# Test performance
python tests/test_performance.py
```

## 📚 Learning Resources
- **System Overview**: `docs/PROJECT_STATUS.md`
- **Communication Protocol**: `agent_workspaces/onboarding/protocols/`
- **Training Materials**: `agent_workspaces/onboarding/training_documents/`
- **Examples**: `examples/`

## 🎯 Success Checklist
- [ ] Launch system successfully
- [ ] Send first message
- [ ] Complete first task
- [ ] Meet performance metrics
- [ ] Master your role

---
**Version**: 1.0 | **Last Updated**: 2025-06-29
