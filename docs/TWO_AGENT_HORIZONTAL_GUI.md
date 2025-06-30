# Two-Agent Horizontal GUI

## Overview

The **Two-Agent Horizontal GUI** is a modern, clean interface designed specifically for managing two agents in a horizontal layout. It's inspired by the v2 GUI design but focused on simplicity and efficiency for 2-agent scenarios.

## Features

### 🎨 **Modern Design**
- **Horizontal Layout**: Agent 1 on the left, Agent 2 on the right
- **V2-Inspired Styling**: Uses the same color palette and design language as the main v2 GUI
- **Clean Interface**: Minimal, focused design without clutter
- **Responsive**: Optimized for 1080p displays and scales well

### 🤖 **Agent Management**
- **Individual Agent Panels**: Each agent has its own dedicated panel
- **Real-time Status**: Live status updates from agent status.json files
- **Task Monitoring**: Shows current task and last update time
- **Visual Status Indicators**: Color-coded status (Online, Busy, Error, Offline)

### 🎯 **Agent Controls**
Each agent panel includes:
- **🔍 Ping**: Test agent responsiveness
- **📊 Get Status**: Read agent's status.json file
- **▶️ Resume**: Tell agent to resume operations
- **⏸️ Pause**: Tell agent to pause operations
- **🎯 Assign Task**: Send specific task to agent

### 🌐 **Shared System Controls**
- **🚀 Onboard Agents**: Run onboarding sequence for both agents
- **🔄 Restart System**: Restart the entire system
- **🗺️ Coordinate Mapping**: Test and manage agent coordinates
- **📤 Send Message**: Send message to both agents
- **📢 Broadcast**: Send broadcast command to both agents
- **📊 System Status**: Get status from both agents

### 📝 **Activity Logging**
- **Real-time Logs**: System activity displayed in real-time
- **Auto-scroll**: Automatically scrolls to show latest entries
- **Log Management**: Clear and save log functionality
- **Timestamped Entries**: All log entries include timestamps

## Usage

### Launching the GUI
```bash
# From project root
python gui/two_agent_horizontal_gui.py

# Or via main launcher
python main.py
# Select option 2: "Launch Two Agent Horizontal GUI"
```

### Basic Workflow
1. **Launch the GUI** - The interface loads with both agent panels
2. **Check Status** - Use "📊 System Status" to get current agent states
3. **Send Commands** - Use individual agent controls or shared controls
4. **Monitor Activity** - Watch the log area for real-time updates
5. **Manage Tasks** - Assign specific tasks to agents as needed

### Agent Status Monitoring
The GUI automatically updates agent status every 5 seconds by reading:
- `agent_workspaces/agent-1/status.json`
- `agent_workspaces/agent-2/status.json`

Status information includes:
- **Status**: online, busy, error, offline
- **Current Task**: What the agent is currently working on
- **Last Update**: When the status was last updated

## Technical Details

### Architecture
- **Framework**: PyQt5 for modern UI
- **Backend**: Integrates with existing coordinate_finder and agent framework
- **Communication**: Uses PyAutoGUI for agent communication
- **Status Updates**: Periodic polling of agent status files

### File Structure
```
gui/
├── two_agent_horizontal_gui.py    # Main GUI file
├── logo.png                       # Logo for header
└── ...

agent_workspaces/
├── agent-1/
│   └── status.json               # Agent 1 status file
└── agent-2/
    └── status.json               # Agent 2 status file
```

### Dependencies
- **PyQt5**: Modern GUI framework
- **pyautogui**: Agent communication
- **coordinate_finder**: Agent coordinate management
- **agent_autonomy_framework**: Agent framework integration

## Design Philosophy

### Simplicity First
- **Focused Layout**: Only what's needed for 2-agent management
- **Clear Visual Hierarchy**: Important information stands out
- **Intuitive Controls**: Self-explanatory button labels and tooltips

### Modern Aesthetics
- **Dark Theme**: Professional dark color scheme
- **Gradient Backgrounds**: Subtle gradients for visual depth
- **Rounded Corners**: Modern, friendly appearance
- **Consistent Spacing**: Proper visual rhythm

### Responsive Design
- **Flexible Layout**: Adapts to different window sizes
- **Readable Text**: Appropriate font sizes and contrast
- **Touch-Friendly**: Adequate button sizes for interaction

## Integration

### With Main System
- **Coordinate Integration**: Uses existing coordinate_finder system
- **Status Integration**: Reads from existing agent status files
- **Framework Integration**: Connects to agent autonomy framework
- **Launcher Integration**: Available through main.py launcher

### With Other GUIs
- **Consistent Styling**: Matches v2 GUI design language
- **Shared Backend**: Uses same coordinate and framework systems
- **Complementary Functionality**: Focused on 2-agent scenarios

## Troubleshooting

### Common Issues
1. **Import Errors**: Ensure running from project root with proper PYTHONPATH
2. **Coordinate Issues**: Check coordinate_finder configuration
3. **Status File Errors**: Verify agent_workspaces structure
4. **PyAutoGUI Issues**: Ensure proper screen coordinates

### Debug Mode
The GUI includes comprehensive logging:
- All actions are logged to the activity log
- Error messages provide detailed information
- Status updates show success/failure

## Future Enhancements

### Planned Features
- **Custom Agent Names**: Allow renaming agents
- **Task Templates**: Predefined task templates
- **Performance Metrics**: Agent performance monitoring
- **Advanced Logging**: Export logs in different formats

### Potential Improvements
- **Real-time Chat**: Direct agent-to-agent communication
- **Task Scheduling**: Schedule tasks for future execution
- **Agent Profiles**: Customizable agent configurations
- **Integration APIs**: Connect to external systems

## Conclusion

The Two-Agent Horizontal GUI provides a clean, efficient interface for managing two agents in a horizontal layout. It combines modern design with practical functionality, making it ideal for focused 2-agent scenarios while maintaining consistency with the broader Dream.OS system architecture. 