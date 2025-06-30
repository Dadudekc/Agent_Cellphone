# Dream.OS Cell Phone GUI v2.0 - User Guide

## 🎯 Overview

The Dream.OS Cell Phone GUI v2.0 provides a modern, intuitive interface for managing autonomous agents. This guide explains how to use all features effectively.

## 🚀 Getting Started

### Launching the GUI
```bash
# From project root
python main.py
# Select option 1: Launch Dream.OS GUI v2.0

# Or directly
python gui/dream_os_gui_v2.py
```

### Initial Setup
1. **Splash Screen**: Wait for system initialization
2. **Mode Selection**: Choose 2, 4, or 8 agent mode
3. **Agent Selection**: Select agents you want to work with
4. **Coordinate Testing**: Use "🧪 Test Coordinates" to verify agent positions

## 📱 Interface Layout

### Left Panel - System Monitoring
- **System Status**: Real-time system health and agent count
- **Mode Indicator**: Shows current agent mode (2/4/8 agents)
- **System Logs**: Live activity feed with clear/save options
- **Coordinate Management**: Test and view agent coordinates

### Right Panel - Agent Management
- **Mode Selector**: Switch between 2, 4, or 8 agent modes
- **Agent Grid**: Visual agent status with detailed information
- **Individual Controls**: Target specific selected agents
- **Broadcast Controls**: Send commands to all active agents

## 🎮 Agent Controls Explained

### Individual Controls (for selected agents)

#### 🔍 Ping Agent
- **What it does**: Tests if agent is responsive
- **How it works**: Clicks agent coordinates and sends `[PING]` command
- **Expected response**: Agent should respond with status
- **Use case**: Quick health check of specific agents

#### 📊 Get Status
- **What it does**: Reads agent's `status.json` file
- **How it works**: Reads file from `agent_workspaces/agent-X/status.json`
- **Expected response**: Detailed status, task, and last update
- **Use case**: Get comprehensive agent information

#### ▶️ Resume Agent
- **What it does**: Tells agent to resume normal operations
- **How it works**: Sends `[RESUME]` command via PyAutoGUI
- **Expected response**: Agent should set status to "online"
- **Use case**: Wake up paused agents

#### ⏸️ Pause Agent
- **What it does**: Tells agent to pause current operations
- **How it works**: Sends `[PAUSE]` command via PyAutoGUI
- **Expected response**: Agent should set status to "offline"
- **Use case**: Stop agents temporarily

#### 🔄 Sync Agent
- **What it does**: Synchronizes agent with system state
- **How it works**: Sends `[SYNC]` command via PyAutoGUI
- **Expected response**: Agent should update status
- **Use case**: Ensure agent is in sync with system

#### 🎯 Assign Task
- **What it does**: Sends a specific task to selected agents
- **How it works**: Prompts for task description, sends `[TASK]` command
- **Expected response**: Agent should acknowledge and execute task
- **Use case**: Assign specific work to agents

### Broadcast Controls (for all active agents)

#### 📢 Broadcast Message
- **What it does**: Sends a message to all agents in current mode
- **How it works**: Prompts for message, sends `[BROADCAST]` command
- **Expected response**: All agents should acknowledge
- **Use case**: System-wide announcements

#### 🔍 Broadcast Ping
- **What it does**: Pings all agents to check responsiveness
- **How it works**: Sends `[BROADCAST_PING]` to all agents
- **Expected response**: All agents should respond with status
- **Use case**: System-wide health check

#### 📊 Broadcast Status
- **What it does**: Requests status reports from all agents
- **How it works**: Sends `[BROADCAST_STATUS]` command
- **Expected response**: All agents should provide status
- **Use case**: System-wide status check

#### ▶️ Broadcast Resume
- **What it does**: Tells all agents to resume operations
- **How it works**: Sends `[BROADCAST_RESUME]` command
- **Expected response**: All agents should set status to "online"
- **Use case**: Wake up entire system

#### 🎯 Broadcast Task
- **What it does**: Assigns the same task to all agents
- **How it works**: Prompts for task, sends `[BROADCAST_TASK]` command
- **Expected response**: All agents should acknowledge and execute
- **Use case**: Parallel task execution

## 🎯 Agent Selection

### Selecting Agents
1. **Individual Selection**: Click on agent widgets to select them
2. **Select All**: Use "Select All Agents" button
3. **Clear Selection**: Use "Clear Selection" button
4. **Mode-Aware**: Only active agents in current mode can be selected

### Agent Widget Information
Each agent widget shows:
- **Agent ID**: The agent identifier (e.g., "agent-1")
- **Status**: Color-coded status indicator
  - 🟢 Green: Online
  - 🟡 Yellow: Busy
  - 🔴 Red: Error
  - ⚫ Gray: Offline
- **Current Task**: What the agent is working on
- **Last Update**: When status was last updated
- **Quick Actions**: Ping, Status, Resume buttons

## 🔧 Coordinate Management

### Testing Coordinates
- **🧪 Test Coordinates**: Verifies all agent coordinates are loaded
- **👁️ View Coordinates**: Shows current coordinate values
- **Purpose**: Ensures PyAutoGUI can reach agent windows

### Coordinate Requirements
- Agents must be in visible windows
- Coordinates must be accurate for PyAutoGUI to work
- Use coordinate finder tool to set up coordinates

## 📊 Status Monitoring

### Real-time Updates
- **Automatic**: Status updates every 5 seconds
- **Manual**: Use "🔄 Refresh" button
- **Log Display**: All activity shown in system logs

### Status.json Structure
Agents maintain a `status.json` file with:
```json
{
    "status": "online|busy|offline|error",
    "last_update": "YYYY-MM-DD HH:MM:SS",
    "current_task": "description of current task",
    "agent_id": "agent-X",
    "performance_metrics": {...},
    "message_history": [...]
}
```

## 🎮 Common Workflows

### 1. System Health Check
1. Select "8 Agents" mode
2. Click "Select All Agents"
3. Click "📊 Get Status"
4. Review status in logs

### 2. Task Assignment
1. Select specific agents
2. Click "🎯 Assign Task"
3. Enter task description
4. Monitor agent responses

### 3. System-wide Command
1. Choose appropriate mode (2/4/8 agents)
2. Click broadcast button (e.g., "📢 Broadcast Message")
3. Enter message/task
4. Monitor all agent responses

### 4. Troubleshooting
1. Use "🧪 Test Coordinates" to verify setup
2. Check agent status.json files manually
3. Use "🔍 Ping Agent" for individual testing
4. Review system logs for errors

## 🚨 Troubleshooting

### Common Issues

#### "Could not find coordinates for agent-X"
- **Solution**: Use coordinate finder to set up coordinates
- **Check**: Ensure agent windows are visible

#### "No status.json found"
- **Solution**: Agent needs to create status.json file
- **Check**: Verify agent workspace exists

#### "PyAutoGUI failed"
- **Solution**: Check if agent windows are active
- **Check**: Verify coordinates are accurate

#### "Agent not responding"
- **Solution**: Check if agent is listening for commands
- **Check**: Verify agent has proper feedback loop

### Debug Steps
1. **Test Coordinates**: Use coordinate testing feature
2. **Check Logs**: Review system logs for errors
3. **Manual Testing**: Try clicking agent coordinates manually
4. **Agent Status**: Check agent's status.json file directly

## 📝 Best Practices

### Agent Management
- **Start Small**: Use 2-agent mode for testing
- **Monitor Logs**: Always check system logs for feedback
- **Test First**: Use ping before sending complex commands
- **Clear Communication**: Use descriptive task descriptions

### System Operations
- **Regular Health Checks**: Use broadcast ping periodically
- **Status Monitoring**: Check agent status regularly
- **Coordinate Maintenance**: Keep coordinates updated
- **Log Management**: Clear logs periodically to prevent bloat

### Performance
- **Mode Selection**: Use appropriate mode for task
- **Batch Operations**: Use broadcast for system-wide tasks
- **Efficient Selection**: Select only needed agents
- **Response Monitoring**: Watch for agent responses

## 🔄 Integration with Agents

### Agent Requirements
Agents must:
1. **Listen for Commands**: Monitor input for GUI commands
2. **Update Status.json**: Maintain current status file
3. **Respond Appropriately**: Acknowledge and process commands
4. **Log Interactions**: Keep message history

### Command Format
GUI sends commands in format:
```
[COMMAND_TYPE] agent-X - description
```

### Expected Responses
Agents should respond with:
```
[COMMAND_TYPE_RESPONSE] agent-X: response content
```

This user guide provides comprehensive information for using the Dream.OS Cell Phone GUI v2.0 effectively. The interface is designed to be intuitive while providing powerful agent management capabilities. 