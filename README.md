# 📱 Agent Cell Phone (ACP)

**Project Codename:** `agent_cell_phone`  
**Version:** 2.0.0  
**Status:** Autonomous Orchestration Enabled  
**Purpose:** Enable fast, deterministic inter-agent messaging across Cursor instances via PyAutoGUI using pre-mapped input box coordinates, with a modern GUI interface for seamless agent management.

## 🎯 Overview

Agent Cell Phone enables agents to:
- Programmatically "text" each other via terminal input
- Parse, route, and act on messages using a custom protocol
- Operate in 2, 4, or 8-agent layouts with pre-defined screen coordinates
- Manage agents through an intuitive GUI interface
- Skip all human-like behavior; pure mechanical precision

## 🚀 Quick Start

### Installation

1. **Clone and setup:**
```bash
git clone <repository>
cd Agent_CellPhone
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Launch the system (autonomous 5‑agent mode):**
```powershell
$env:ACP_DEFAULT_NEW_CHAT=1; $env:ACP_AUTO_ONBOARD=1; $env:ACP_SINGLE_MESSAGE=1; `
  $env:ACP_MESSAGE_VERBOSITY=extensive; $env:ACP_NEW_CHAT_INTERVAL_SEC=1800

# Terminal A: start Agent-5 listener
python overnight_runner/listener.py --agent Agent-5 | cat

# Terminal B: start FSM cadence (contracts‑tailored)
python overnight_runner/runner.py `
  --layout 5-agent --captain Agent-5 --resume-agents Agent-1,Agent-2,Agent-3,Agent-4 `
  --duration-min 60 --interval-sec 1200 --sender Agent-3 --plan contracts `
  --fsm-enabled --fsm-agent Agent-5 --fsm-workflow default `
  --contracts-file D:/repositories/communications/overnight_YYYYMMDD_/Agent-5/contracts.json `
  --suppress-resume --skip-assignments --skip-captain-kickoff --skip-captain-fsm-feed `
  --resume-cooldown-sec 3600 --active-grace-sec 1200 `
  --initial-wait-sec 10 --phase-wait-sec 8 --stagger-ms 2500 --jitter-ms 800 `
  --comm-root D:/repositories/communications/overnight_YYYYMMDD_ --create-comm-folders | cat
```

### Basic Usage

#### Main Launcher (Recommended)
```bash
python main.py
```
This provides a menu-driven interface to access all components (GUIs, tests, docs).

#### Direct GUI Access
```bash
# Launch modern PyQt v2 GUI (8 agents panel with controls)
python gui/dream_os_gui_v2.py

# Two-Agent Horizontal GUI (focused beta flow)
python gui/two_agent_horizontal_gui.py

# Four-Agent Horizontal GUI
python gui/four_agent_horizontal_gui.py

# Legacy GUIs (archived)
# python archive/simple_gui.py
# python archive/cell_phone_gui.py
```

#### Command Line Interface
```python
from src.agent_cell_phone import AgentCellPhone

# Initialize agent
acp = AgentCellPhone("agent-1")
acp.load_layout("4")  # 4-agent mode

# Send message to specific agent
acp.send("agent-2", "Hello from agent-1!")

# Broadcast to all agents
acp.broadcast("Status update: All systems operational")
```

## 🧩 System Components

### 1. Layout Mapper
- Dictionary of agent input box coordinates
- Auto-loaded on init with hot-reload support
- Supports 2, 4, and 8-agent configurations

### 2. AgentCellPhone
- Core PyAutoGUI messenger module
- `.send(to_agent_id, message)` - Send to specific agent
- `.broadcast(message)` - Send to all agents
- Handles window focus → cursor click → keystroke → return

### 3. Message Protocol
- Format: `@agent-x <COMMAND> <ARGS>`
- Reserved prefixes: `@all`, `@self`, `@agent-x`
- Examples: `@agent-2 resume`, `@all status_ping`

### 4. GUI Interface
- Modern PyQt5-based desktop application with dark theme
- Three-tab interface: Controls, Messaging, Status
- Agent selection and individual controls
- Broadcast functionality for all agents
- Real-time status monitoring and message history
- Professional styling with color-coded buttons
- Alternative launcher script for easy access

### 5. File Inbox + Listener (Active)
- Silent channel under `agent_workspaces/Agent-X/inbox/*.json`.
- Listener updates `agent_workspaces/Agent-X/state.json` and mirrors evidence into communications.
- Recognized types: `task`, `sync`, `verify`, `fsm_request`, `fsm_update`.

### 6. FSM Cadence Runner
- Cycles RESUME/TASK/COORDINATE/SYNC/VERIFY with anti‑duplication and pacing.
- Drops `fsm_request_YYYYMMDD_HHMMSS.json` into Agent‑5 inbox each cycle when `--fsm-enabled`.
- Optional contracts tailoring via `--contracts-file`.

## 📁 Project Structure

```
Agent_CellPhone/
├── launch.py                    # 🚀 Main launcher script
├── README.md                    # 📖 This file
├── requirements.txt             # 📦 Dependencies
├── .gitignore                   # 🚫 Git ignore rules
├── src/                         # 🔧 Core system files
│   ├── agent_cell_phone.py      # Core messaging system
│   ├── inter_agent_framework.py # Inter-agent communication
│   └── main.py                  # Main system entry point
├── gui/                         # 🖥️ GUI interfaces
│   ├── dream_os_gui.py          # ✅ Modern PyQt GUI (main)
│   ├── run_gui.py               # ✅ GUI launcher script
│   └── agent_resume_web_gui.html # ✅ Web-based interface
├── tests/                       # 🧪 Test suite
│   ├── test_harness.py          # Main test harness
│   ├── test_8_agent_coordinates.py # 8-agent coordinate testing
│   ├── test_inter_agent_framework.py # Framework testing
│   ├── test_special_chars.py    # Special character testing
│   ├── diagnostic_test.py       # Diagnostic testing tools
│   └── coordinate_finder.py     # Coordinate mapping utility
├── scripts/                     # 🔧 Utility scripts
│   ├── agent_messenger.py       # Agent messaging utilities
│   ├── agent_onboarding_sequence.py # Onboarding system
│   ├── send_onboarding.py       # Onboarding sender
│   ├── send_single_onboarding.py # Single agent onboarding
│   ├── send_specific_onboarding.py # Specific onboarding
│   ├── send_to_agents.py        # Agent communication
│   └── onboarding_messages.py   # Onboarding message templates
├── examples/                    # 🎯 Example code
│   ├── agent_conversation_demo.py # Conversation examples
│   ├── coordination_demo.py     # Coordination examples
│   ├── real_agent_messages.py   # Real message examples
│   └── example_usage.py         # Basic usage examples
├── docs/                        # 📚 Documentation
│   ├── PROJECT_STATUS.md        # Project status and progress
│   ├── PROJECT_ROADMAP.md       # Development roadmap
│   ├── PRODUCT_REQUIREMENTS_DOCUMENT.md # PRD
│   ├── GUI_DEVELOPMENT_SUMMARY.md # GUI development documentation
│   ├── INTER_AGENT_FRAMEWORK_SUMMARY.md # Framework documentation
│   ├── GUI_CONSOLIDATION_SUMMARY.md # GUI consolidation summary
│   ├── DREAM_OS_BRANDING_UPDATE.md # Branding updates
│   └── PUSH_SUMMARY.md          # Push summaries
├── archive/                     # 📦 Archived versions
│   ├── simple_gui.py            # Legacy tkinter GUI
│   └── cell_phone_gui.py        # Legacy PyQt GUI
├── runtime/                     # ⚙️ Runtime configuration
│   └── config/                  # Configuration files
│       └── cursor_agent_coords.json # Cursor agent coordinates
└── agent-*/                     # 🤖 Agent-specific logs
    └── devlog.md                # Message logs
```

## 🛠️ Testing

### Run Demo
```bash
python tests/test_harness.py --mode demo
```

### Interactive Mode
```bash
python tests/test_harness.py --mode interactive --agent agent-1
```

### Test Specific Functions
```bash
# Test message sending
python tests/test_harness.py --mode send --agent agent-1 --target agent-2 --message "Test message"

# Test broadcasting
python tests/test_harness.py --mode broadcast --agent agent-1 --message "Broadcast test"

# Test message parsing
python tests/test_harness.py --mode parse

# Test layout loading
python tests/test_harness.py --mode layout --layout 8
```

### Diagnostic Testing
```bash
# Run comprehensive diagnostic tests
python tests/diagnostic_test.py

# Smoke tests (headless)
pytest -q tests/smoke/test_smoke.py -q
```

## 📊 Layout Configurations

### 2-Agent Mode
```json
{
  "agent-1": [120, 180],
  "agent-2": [720, 180]
}
```

### 4-Agent Mode
```json
{
  "agent-1": [120, 180],
  "agent-2": [720, 180],
  "agent-3": [120, 980],
  "agent-4": [720, 980]
}
```

### 8-Agent Mode
```json
{
  "agent-1": [120, 180],
  "agent-2": [720, 180],
  "agent-3": [1320, 180],
  "agent-4": [1920, 180],
  "agent-5": [120, 980],
  "agent-6": [720, 980],
  "agent-7": [1320, 980],
  "agent-8": [1920, 980]
}
```

## 📊 Coordinate Configuration

### Cursor Agent Coordinates
The system uses a unified coordinate file at `runtime/config/cursor_agent_coords.json`:

```json
{
  "Agent-1": {"input_box": {"x": 120, "y": 180}},
  "Agent-2": {"input_box": {"x": 720, "y": 180}},
  "Agent-3": {"input_box": {"x": 1320, "y": 180}},
  "Agent-4": {"input_box": {"x": 1920, "y": 180}},
  "Agent-5": {"input_box": {"x": 120, "y": 980}},
  "Agent-6": {"input_box": {"x": 720, "y": 980}},
  "Agent-7": {"input_box": {"x": 1320, "y": 980}},
  "Agent-8": {"input_box": {"x": 1920, "y": 980}}
}
```

### Setting Up Coordinates
Use the coordinate finder utility to set up your cursor agent coordinates:

```bash
# Interactive coordinate finder
python tests/coordinate_finder.py --mode find

# Show current coordinates
python tests/coordinate_finder.py --mode show

# Update specific agent coordinates
python tests/coordinate_finder.py --mode update

# Track mouse position
python tests/coordinate_finder.py --mode track
```

## 🎨 GUI Features

### Desktop GUI (`simple_gui.py`)
- **Agent Selection:** Dropdown to select specific agent
- **Individual Controls:** Resume, Sync, Pause, Resume buttons
- **Broadcast Controls:** Resume All, Sync All, Pause All
- **Custom Messaging:** Send custom messages to selected agent
- **Status Monitoring:** Real-time status display and logging
- **Color-coded Interface:** Green=Resume, Blue=Sync, Orange=Pause

### Web GUI (`agent_resume_web_gui.html`)
- **Responsive Design:** Works on desktop and mobile
- **Agent Status Cards:** Visual status indicators for all agents
- **Interactive Controls:** Click-to-select agent functionality
- **Real-time Logs:** Live log display with export capability
- **Modern UI:** Clean, professional interface

## 🛠️ Configuration

### Typing/Onboarding Behavior (Environment)
- `ACP_DEFAULT_NEW_CHAT`: 1 to enable Ctrl+T flow by default (first contact).
- `ACP_NEW_CHAT_INTERVAL_SEC`: throttle Ctrl+T per agent (e.g., 1800 = 30 minutes).
- `ACP_AUTO_ONBOARD`: 1 to prepend onboarding pointer to the first message in new chat.
- `ACP_SINGLE_MESSAGE`: 1 to compose a single message (Shift+Enter for line breaks; one Enter at end).
- `ACP_MESSAGE_VERBOSITY`: `extensive` or `simple` onboarding pointer content.

### Runner Pacing/Noise Flags
- `--suppress-resume`: never send RESUME prompts.
- `--resume-cooldown-sec`: minimum seconds between RESUME per agent.
- `--active-grace-sec`: skip messaging agents updated within the last N seconds.
- `--skip-assignments`, `--skip-captain-kickoff`, `--skip-captain-fsm-feed`: silence early chatter.
- `--contracts-file`: path to `contracts.json` for per‑agent tailored prompts.

### Coordinate Management
The system uses a unified coordinate file at `runtime/config/cursor_agent_coords.json`:

```json
{
  "Agent-1": {"input_box": {"x": x1, "y": y1}},
  "Agent-2": {"input_box": {"x": x2, "y": y2}},
  ...
}
```

### Coordinate Mapping
- Use screen coordinates (x, y) for input box locations
- Coordinates are relative to screen resolution
- Use the coordinate finder utility to set up coordinates

### GUI Configuration
- **Theme:** Modern with color coding
- **Layout:** Intuitive button arrangement
- **Logging:** Real-time status updates
- **Error Handling:** Graceful error recovery

## 📈 Performance Metrics

### Current Performance:
- **Message sending:** ~200ms per message
- **Layout loading:** ~50ms
- **Message parsing:** ~1ms
- **Logging overhead:** ~10ms
- **GUI initialization:** < 2 seconds
- **GUI response time:** < 1 second

### Scalability:
- Supports 2, 4, 8 agent configurations
- Extensible to custom layouts
- Memory efficient (minimal overhead)
- GUI supports unlimited agent scaling

## 🎯 Project Status

### ✅ Phase 1: MVP Comm Layer - COMPLETED
- Core messaging system operational
- 8-agent layout fully functional
- Modern GUI interface completed
- Web-based interface created
- Comprehensive testing framework
- Full documentation and examples
- Diagnostic and testing tools
- Production-ready foundation

### 🔄 Phase 2: Full Listener Loop - IN PROGRESS
- Bidirectional communication
- Message detection and processing
- Command routing system
- Real-time status monitoring

### 🔮 Phase 3: Robustness - PLANNED
- Reliability enhancements
- Advanced error handling
- Health monitoring
- Performance optimization

### 🔮 Phase 4: Logging & Debug Panel - PLANNED
- Advanced debug interface
- Comprehensive logging
- Performance monitoring
- Production deployment

## 📞 Support & Documentation

### Available Resources:
- **README.md** - This comprehensive guide
- **PROJECT_STATUS.md** - Current project status and progress
- **PROJECT_ROADMAP.md** - Development roadmap and milestones
- **PRODUCT_REQUIREMENTS_DOCUMENT.md** - Detailed PRD
- **GUI_DEVELOPMENT_SUMMARY.md** - GUI development documentation
- **Example usage scripts** - Practical examples
- **CLI test harness** - Testing and validation
- **Coordinate finder utility** - Setup assistance

### Getting Help:
- Check `GUI_DEVELOPMENT_SUMMARY.md` for GUI usage
- Review `test_harness.py` for CLI examples
- Examine devlog files for debugging
- Use `diagnostic_test.py` for system validation
- Consult `PROJECT_STATUS.md` for current status

## 🏆 Achievements

### Phase 1 Milestones:
- ✅ **Core System:** Fully operational messaging system
- ✅ **GUI Interface:** Modern, intuitive user interface
- ✅ **Testing:** Comprehensive testing framework
- ✅ **Documentation:** Complete documentation suite
- ✅ **Performance:** All performance targets met
- ✅ **Quality:** High code quality and reliability

### Recognition:
- **Innovation:** Novel approach to inter-agent communication
- **Usability:** Intuitive interface design
- **Reliability:** Robust error handling
- **Scalability:** Extensible architecture

## 🚀 Next Steps

### Immediate (Phase 2):
1. Implement OCR-based message detection
2. Add command router with basic handlers
3. Create message processing pipeline
4. Integrate GUI with listener loop

### Short-term (Phase 3):
1. Add reliability features
2. Implement error recovery
3. Add health monitoring
4. Enhance GUI with advanced features

### Long-term (Phase 4):
1. Create debug interface
2. Add performance monitoring
3. Implement advanced logging
4. Deploy production-ready system

---

**Project Version:** 2.0.0  
**Last Updated:** 2025-08-12  
**Status:** Autonomous Orchestration Enabled  
**Next Phase:** Robust pacing defaults + CI hooks for verify gates