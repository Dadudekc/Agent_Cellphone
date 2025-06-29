# Dream.OS Cell Phone - Web GUI

## Overview
The web GUI provides a modern, browser-based interface for the Dream.OS Cell Phone system. It communicates with a Python backend server to send commands to agents.

## Quick Start

### Option 1: Using the Main Launcher
1. Run the main launcher: `python main.py`
2. Select option 4: "🔧 Start Web Backend Server"
3. In another terminal, run: `python main.py`
4. Select option 3: "🌐 Launch Web GUI"

### Option 2: Manual Start
1. Start the backend server:
   ```bash
   python gui/web_backend_server.py
   ```
2. Open the web GUI in your browser:
   ```bash
   start gui/agent_resume_web_gui.html
   ```

## Features

### 🎮 Individual Controls
- **Agent Selection**: Choose which agent to control
- **Resume**: Send resume command to selected agent
- **Sync**: Send sync command to selected agent
- **Pause**: Send pause command to selected agent
- **Restart**: Send restart command to selected agent
- **Status**: Request status from selected agent
- **Ping**: Send ping to selected agent

### 📢 Broadcast Controls
- **Resume All**: Send resume command to all agents
- **Sync All**: Send sync command to all agents
- **Pause All**: Send pause command to all agents
- **Emergency Stop**: Emergency stop all agents

### 🔧 Script Management
- **Start Scripts**: Start all available scripts
- **Stop Scripts**: Stop all running scripts
- **Restart Scripts**: Restart all scripts
- **Run Tests**: Execute the test suite

### 💬 Custom Messages
- Send custom messages to any agent
- Real-time message history
- Status updates

## Backend Communication

The web GUI communicates with the backend server via HTTP requests:

- **POST /send**: Send message to individual agent
- **POST /broadcast**: Broadcast message to all agents
- **POST /scripts**: Manage script execution
- **POST /tests**: Run test suite
- **POST /status**: Get system status

## Troubleshooting

### Backend Not Available
If you see "Backend not available - running in simulation mode":
1. Make sure the backend server is running
2. Check that port 8080 is not blocked
3. Verify the Agent Cell Phone system is properly installed

### Connection Errors
- Ensure the backend server is running on port 8080
- Check firewall settings
- Verify the web GUI can access localhost

### Agent Communication Issues
- Check that the Agent Cell Phone coordinates file exists
- Verify PyAutoGUI is properly installed
- Ensure agents are positioned correctly on screen

## Browser Compatibility

The web GUI works best with:
- Chrome/Chromium
- Firefox
- Edge
- Safari (with some CSS limitations)

## Security Note

The backend server runs on localhost only and is intended for local use. Do not expose it to external networks without proper security measures. 