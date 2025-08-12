# 🎯 Dream.OS PyAutoGUI Onboarding System

## Overview

This directory contains scripts for automated agent onboarding using PyAutoGUI. These scripts will automatically identify agents by their screen positions and send them personalized onboarding messages with links to their specific training materials.

## 📁 Available Scripts

### 1. `agent_onboarding_sequence.py`
**Full-featured onboarding system with comprehensive messages**

- **Purpose**: Complete onboarding system with detailed personalized messages
- **Features**: 
  - Loads agent coordinates automatically
  - Sends comprehensive onboarding messages
  - Includes role-specific training materials
  - Handles errors gracefully

**Usage**:
```bash
# Onboard all agents
python agent_onboarding_sequence.py

# Onboard specific agent
python agent_onboarding_sequence.py Agent-1
```

### 2. `onboard_all_agents.py`
**Simplified script for onboarding all agents at once**

- **Purpose**: Quick onboarding of all agents with personalized messages
- **Features**:
  - Personalized messages for each agent role
  - Links to specific training materials
  - Progress tracking and reporting

**Usage**:
```bash
# Onboard all agents
python onboard_all_agents.py

# Show help
python onboard_all_agents.py --help
```

### 3. `send_onboarding_message.py`
**Simple script for sending individual onboarding messages**

- **Purpose**: Send onboarding messages to specific agents
- **Features**:
  - Quick message sending
  - Custom message support
  - Simple command-line interface

**Usage**:
```bash
# Send default onboarding message
python send_onboarding_message.py Agent-1

# Send custom message
python send_onboarding_message.py Agent-2 "Custom welcome message"
```

### 4. `run_onboarding.py`
**Wrapper script for easy onboarding execution**

- **Purpose**: Simple interface to run onboarding sequences
- **Features**:
  - Easy-to-use interface
  - Supports both full and individual onboarding
  - Error handling and reporting

**Usage**:
```bash
# Run full onboarding
python run_onboarding.py

# Onboard specific agent
python run_onboarding.py Agent-1
```

## 🚀 Quick Start

### Prerequisites
1. **Agent Coordinates**: Run `coordinate_finder.py` first to set up agent positions
2. **PyAutoGUI**: Ensure PyAutoGUI is installed (`pip install pyautogui`)
3. **Agent Windows**: Make sure all agent windows are visible and active

### Environment model (important)
- Agents are Cursor-based; onboarding messages are typed into Cursor windows using ACP.
- Agents share the same repositories/files on disk. Keep changes small and verifiable to reduce conflicts.
- Prefer comprehensive single-message onboarding; include repo-relative paths that are valid for all agents.

### Step 1: Set Up Agent Positions
```bash
# Run the coordinate finder to set up agent positions
python coordinate_finder.py
```

### Step 2: Run Onboarding
```bash
# Option 1: Use the comprehensive system
python agent_onboarding_sequence.py

# Option 2: Use the simplified system
python onboard_all_agents.py

# Option 3: Use the wrapper script
python run_onboarding.py
```

### Step 3: Verify Onboarding
- Check that each agent received their personalized message
- Verify links to training materials work
- Confirm agents can access their onboarding documents

## 🎯 Agent Roles and Messages

### Agent-1: System Coordinator & Project Manager 🎯
- **Role**: Project coordination, task assignment, progress monitoring
- **Key Documents**: README.md, agent_roles_and_responsibilities.md, agent_protocols.md

### Agent-2: Frontend Development Specialist 🎨
- **Role**: UI/UX development, responsive design, component development
- **Key Documents**: README.md, development_standards.md, tools_and_technologies.md

### Agent-3: Backend Development Specialist ⚙️
- **Role**: API development, database design, server architecture
- **Key Documents**: README.md, development_standards.md, workflow_protocols.md

### Agent-4: DevOps & Infrastructure Specialist 🛠️
- **Role**: Infrastructure management, CI/CD, monitoring, security
- **Key Documents**: README.md, tools_and_technologies.md, command_reference.md

### Agent-5: Testing & Quality Assurance Specialist 🔍
- **Role**: Test strategy, automation, quality assurance, performance testing
- **Key Documents**: README.md, development_standards.md, best_practices.md

### Agent-6: Data Science & Analytics Specialist 📊
- **Role**: Data analysis, machine learning, visualization, business intelligence
- **Key Documents**: README.md, tools_and_technologies.md, system_overview.md

### Agent-7: Security & Compliance Specialist 🔒
- **Role**: Security architecture, vulnerability assessment, compliance, incident response
- **Key Documents**: README.md, agent_protocols.md, troubleshooting.md

### Agent-8: Documentation & Knowledge Management Specialist 📚
- **Role**: Technical documentation, knowledge management, training materials
- **Key Documents**: README.md, development_standards.md, getting_started.md

## 📋 Onboarding Process

### 1. **Preparation**
- Ensure all agent windows are visible
- Run coordinate finder to set up positions
- Verify PyAutoGUI is working correctly

### 2. **Execution**
- Run the onboarding script of your choice
- Monitor the process for any errors
- Wait for completion confirmation

### 3. **Verification**
- Check that each agent received their message
- Verify links to training materials
- Confirm agents can access onboarding documents

### 4. **Follow-up**
- Agents should read their onboarding materials
- Complete the onboarding checklist
- Begin team collaboration exercises

## 🔧 Troubleshooting

### Common Issues

**Issue**: "No agent coordinates found"
- **Solution**: Run `coordinate_finder.py` first to set up agent positions

**Issue**: "PyAutoGUI failsafe triggered"
- **Solution**: Move mouse to corner to disable failsafe, or adjust screen resolution

**Issue**: "Agent window not found"
- **Solution**: Ensure agent windows are visible and active before running

**Issue**: "Message not sent properly"
- **Solution**: Check that agent windows are in focus and text input is ready

### Error Recovery
1. **Stop the script**: Press Ctrl+C to stop execution
2. **Check agent positions**: Verify coordinates are correct
3. **Restart the process**: Run the onboarding script again
4. **Manual verification**: Check that messages were sent correctly

## 📊 Success Metrics

### Onboarding Success Indicators
- ✅ All agents receive personalized messages
- ✅ Links to training materials are accessible
- ✅ Agents can navigate to their onboarding documents
- ✅ No PyAutoGUI errors during execution
- ✅ All agent roles are properly identified

### Quality Assurance
- **Message Accuracy**: Each agent receives role-specific information
- **Link Functionality**: All training material links work correctly
- **Process Reliability**: Onboarding completes without errors
- **User Experience**: Smooth and professional onboarding experience

## 🎉 Expected Results

After successful onboarding, each agent will:

1. **Know Their Role**: Understand their specific responsibilities
2. **Access Training Materials**: Have links to relevant documentation
3. **Follow Onboarding Process**: Complete the step-by-step checklist
4. **Join the Team**: Be ready for collaboration and task assignment
5. **Contribute Effectively**: Understand how to work within the system

## 🔮 Future Enhancements

### Planned Improvements
- **Interactive Onboarding**: Add hands-on exercises and tests
- **Progress Tracking**: Monitor agent onboarding completion
- **Customization Options**: Allow custom onboarding messages
- **Integration**: Connect with the main Dream.OS system
- **Analytics**: Track onboarding success rates and metrics

### Advanced Features
- **Video Tutorials**: Add visual onboarding materials
- **Certification**: Formal skill validation process
- **Mentorship**: Pair new agents with experienced team members
- **Continuous Learning**: Ongoing training and development

---

**Ready to onboard your Dream.OS agents? Start with `python onboard_all_agents.py`!** 🚀 