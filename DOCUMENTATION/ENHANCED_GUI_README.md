# 🚀 Enhanced Overnight Runner GUI - Agent-5 Command Center

## 📋 Overview

The Enhanced Overnight Runner GUI provides a comprehensive interface for Agent-5 to command and coordinate other agents, manage overnight runs, and prevent PyAutoGUI conflicts through an intelligent queue system.

## 🎯 Key Features

### 1. **Agent-5 Command Center**
- **Individual Agent Commands**: Send specific commands to any agent
- **Broadcast Commands**: Send the same command to all agents simultaneously
- **Predefined Commands**: Quick access to common operations
- **Task Management**: Assign and track collaborative tasks
- **Command Logging**: Real-time log of all commands and responses

### 2. **PyAutoGUI Queue System**
- **Conflict Prevention**: Prevents multiple agents from controlling PyAutoGUI simultaneously
- **Priority-based Processing**: Messages are processed based on priority levels
- **Agent Locking**: Each agent has a dedicated lock to prevent interference
- **Queue Management**: Pause, resume, and monitor queue status

### 3. **Agent Coordination**
- **Team Coordination**: Coordinate multiple agents for collaborative tasks
- **Overnight Run Facilitation**: Automated coordination for extended development sessions
- **Status Monitoring**: Real-time monitoring of agent status and progress
- **Nudge System**: Wake up stalled agents with gentle nudges

### 4. **Enhanced Monitoring**
- **Real-time Status**: Live updates of agent and queue status
- **Activity Logging**: Comprehensive logging of all system activities
- **Performance Metrics**: Queue depth, processing times, and agent locks
- **Emergency Controls**: Emergency stop and recovery mechanisms

## 🏗️ Architecture

### Core Components

```
EnhancedRunnerGUI
├── Agent5CommandCenter
│   ├── PyAutoGUIQueue
│   ├── Agent Status Management
│   └── Task Coordination
├── PyAutoGUIQueue
│   ├── Message Queue
│   ├── Agent Locks
│   └── Processing Thread
└── Enhanced AgentCellPhone
    ├── Queue Integration
    ├── Priority-based Sending
    └── Fallback Mechanisms
```

### Queue System Flow

```
Message Request → Queue → Priority Sorting → Agent Lock → PyAutoGUI → Completion
     ↓              ↓         ↓            ↓         ↓         ↓
  Validation    FIFO Order  Priority    Lock Wait  Execute   Release Lock
```

## 🚀 Getting Started

### 1. Launch the Enhanced GUI

```bash
cd Agent_Cellphone
python overnight_runner/enhanced_gui.py
```

### 2. Basic Usage

#### **Agent-5 Command Center Tab**
- Select target agent from dropdown
- Type command in the command field
- Click "Send Command" to send to individual agent
- Use "Broadcast to All" for team-wide messages
- Use predefined buttons for common operations

#### **Overnight Runner Control Tab**
- Configure layout, captain, and agent settings
- Set timing parameters (interval, duration)
- Start/stop listener and runner processes
- Calibrate agent coordinates

#### **Queue Management Tab**
- Monitor queue status and depth
- View agent lock status
- Pause/resume queue processing
- Clear queue if needed

#### **Agent Monitoring Tab**
- Check individual agent status
- Send nudge commands
- Monitor activity logs
- Emergency stop capabilities

### 3. Environment Configuration

The system supports several environment variables for customization:

```bash
# Enable PyAutoGUI queue system
export ACP_QUEUE_ENABLED=1

# Set queue priority (lower = higher priority)
export ACP_QUEUE_PRIORITY=1

# Set queue timeout in seconds
export ACP_QUEUE_TIMEOUT=30.0

# Enable queue for specific operations
export ACP_QUEUE_ENABLED=1
```

## 📱 AgentCellPhone Integration

### Enhanced Send Method

The `AgentCellPhone.send()` method now supports queue integration:

```python
from src.services.agent_cell_phone import AgentCellPhone

# Create AgentCellPhone instance
acp = AgentCellPhone(agent_id="Agent-5", layout_mode="5-agent")

# Set PyAutoGUI queue
acp.set_pyautogui_queue(queue_instance)

# Send with queue (automatic if queue is enabled)
acp.send("Agent-1", "Hello from Agent-5", use_queue=True)

# Send directly (bypass queue)
acp.send("Agent-1", "Hello from Agent-5", use_queue=False)

# Send with specific priority
acp.send_queued("Agent-1", "Priority message", priority=1)
```

### Queue Status Monitoring

```python
# Get current queue status
status = acp.get_queue_status()
print(f"Queue size: {status['queue_size']}")
print(f"Processing: {status['processing']}")
print(f"Agent locks: {status['agent_locks']}")

# Wait for queue to clear
if acp.wait_for_queue_clear(timeout=60.0):
    print("Queue cleared successfully")
else:
    print("Queue clear timeout")
```

## 🔧 Advanced Features

### 1. **Priority-based Message Processing**

Messages are processed based on priority levels:

- **Priority 1**: High priority (status checks, emergency messages)
- **Priority 2**: Normal priority (task assignments, coordination)
- **Priority 3**: Low priority (nudges, background operations)

### 2. **Agent Lock Management**

Each agent has a dedicated lock to prevent interference:

```python
# Check if agent is locked
status = queue.get_queue_status()
if status['agent_locks']['Agent-1']:
    print("Agent-1 is currently processing a message")
else:
    print("Agent-1 is available for new messages")
```

### 3. **Coordinated Task Execution**

Coordinate multiple agents for collaborative tasks:

```python
# Coordinate team for a task
command_center.coordinate_agents("Implement new feature")

# This will send coordinated messages to all agents:
# Agent-1: "Coordinate: Implement new feature - Take lead on planning"
# Agent-2: "Coordinate: Implement new feature - Handle technical architecture"
# Agent-3: "Coordinate: Implement new feature - Manage data and analytics"
# Agent-4: "Coordinate: Implement new feature - Handle DevOps and infrastructure"
```

### 4. **Overnight Run Coordination**

Automated coordination for extended development sessions:

```python
# Start overnight run
command_center.start_overnight_run(duration_minutes=120)

# This will:
# 1. Send onboarding messages to all agents
# 2. Assign specific tasks based on agent roles
# 3. Monitor progress throughout the session
# 4. Provide status updates and coordination
```

## 📊 Monitoring and Debugging

### Queue Status Monitoring

```python
# Get comprehensive queue status
status = queue.get_queue_status()

print(f"Queue Size: {status['queue_size']}")
print(f"Processing: {status['processing']}")
print(f"Agent Locks: {status['agent_locks']}")

# Monitor specific agent
agent = "Agent-1"
if agent in status['agent_locks']:
    lock_status = "Locked" if status['agent_locks'][agent] else "Unlocked"
    print(f"{agent}: {lock_status}")
```

### Performance Metrics

The system provides several performance indicators:

- **Queue Depth**: Number of pending messages
- **Processing Rate**: Messages processed per second
- **Lock Contention**: How often agents wait for locks
- **Response Times**: Time from queue to completion

### Debugging Tools

```python
# Enable debug logging
import logging
logging.getLogger("agent_cell_phone").setLevel(logging.DEBUG)

# Check queue health
if queue.processing:
    print("Queue is processing messages")
else:
    print("Queue is stopped")

# Monitor agent locks
for agent, locked in queue.agent_locks.items():
    print(f"{agent}: {'🔒' if locked else '🔓'}")
```

## 🚨 Troubleshooting

### Common Issues

#### **Queue Not Processing**
```python
# Check if processing thread is running
if not queue.processing:
    queue.start_processing()
    print("Queue processing restarted")
```

#### **Agent Locked Indefinitely**
```python
# Force release agent lock (use with caution)
if agent in queue.agent_locks:
    # This would need to be implemented in the queue class
    print("Agent lock release requested")
```

#### **High Queue Depth**
```python
# Check queue status
status = queue.get_queue_status()
if status['queue_size'] > 10:
    print("High queue depth detected")
    print("Consider pausing new messages or clearing queue")
```

### Performance Optimization

1. **Adjust Priority Levels**: Use appropriate priorities for different message types
2. **Batch Operations**: Group related messages to reduce queue overhead
3. **Monitor Lock Times**: Identify agents that hold locks too long
4. **Queue Size Limits**: Set reasonable limits to prevent memory issues

## 🔮 Future Enhancements

### Planned Features

1. **Advanced Queue Management**
   - Queue size limits and overflow handling
   - Dead letter queue for failed messages
   - Message retry mechanisms

2. **Enhanced Monitoring**
   - Real-time performance dashboards
   - Alert system for queue issues
   - Historical performance analytics

3. **Intelligent Coordination**
   - AI-powered task assignment
   - Predictive queue management
   - Adaptive priority adjustment

4. **Integration Improvements**
   - WebSocket support for real-time updates
   - REST API for external control
   - Plugin system for custom extensions

## 📚 API Reference

### PyAutoGUIQueue Class

```python
class PyAutoGUIQueue:
    def __init__(self)
    def add_agent(self, agent_id: str) -> None
    def queue_message(self, agent_id: str, message: str, priority: int = 1) -> bool
    def start_processing(self) -> None
    def stop_processing(self) -> None
    def get_queue_status(self) -> Dict[str, any]
```

### Agent5CommandCenter Class

```python
class Agent5CommandCenter:
    def __init__(self, gui)
    def send_command(self, agent_id: str, command: str, priority: int = 1) -> bool
    def broadcast_command(self, command: str, priority: int = 1) -> None
    def coordinate_agents(self, task_description: str) -> None
    def start_overnight_run(self, duration_minutes: int = 60) -> None
    def monitor_agent_status(self) -> None
    def get_queue_status(self) -> Dict[str, any]
```

### Enhanced AgentCellPhone Methods

```python
class AgentCellPhone:
    def set_pyautogui_queue(self, queue_instance) -> None
    def send(self, agent: str, message: str, tag: MsgTag = MsgTag.NORMAL, 
             new_chat: bool = False, nudge_stalled: bool = False, 
             use_queue: bool = None) -> None
    def send_queued(self, agent: str, message: str, tag: MsgTag = MsgTag.NORMAL, 
                    priority: int = None, timeout: float = None) -> bool
    def get_queue_status(self) -> Dict[str, any]
    def wait_for_queue_clear(self, timeout: float = None) -> bool
    def clear_queue(self) -> bool
```

## 🤝 Contributing

### Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Agent_Cellphone
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run tests**
   ```bash
   python -m pytest tests/
   ```

4. **Run demonstration**
   ```bash
   python demo_enhanced_gui.py
   ```

### Code Style

- Follow PEP 8 guidelines
- Use type hints for all function parameters
- Include comprehensive docstrings
- Add unit tests for new features

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

### Getting Help

1. **Check the documentation**: This README and related docs
2. **Run the demonstration**: `python demo_enhanced_gui.py`
3. **Review the code**: Examine the implementation for examples
4. **Check issues**: Look for similar problems in the issue tracker

### Reporting Issues

When reporting issues, please include:

- **Environment**: OS, Python version, dependencies
- **Steps to reproduce**: Clear sequence of actions
- **Expected behavior**: What should happen
- **Actual behavior**: What actually happens
- **Logs**: Relevant error messages and logs
- **Screenshots**: If applicable

---

**🎉 Congratulations!** You now have a powerful, coordinated system for managing multiple agents with conflict-free PyAutoGUI operations. The Enhanced GUI provides Agent-5 with the tools needed to command, coordinate, and monitor the entire agent team effectively.
