# Agent-5 Production Monitor

## 🎯 **What This Is**

A **production-ready monitoring system** that replaces the demo script with real response capture, real rescue messages, and persistent state management. This is **NOT a simulation** - it actually monitors agent responses and sends real rescue messages.

## 🚀 **Key Features**

- ✅ **Real response capture** via file timestamps (`state.json`, `response.txt`)
- ✅ **Real rescue messages** sent via `AgentCellPhone.send()`
- ✅ **Persistent state** survives restarts
- ✅ **Health metrics** and monitoring
- ✅ **Configurable thresholds** via environment variables
- ✅ **Integration** with existing response capture pipeline
- ✅ **Optional DB lane** for cursor database monitoring

## 📊 **How It Works**

### 1. **Activity Monitoring**
- Monitors `agent_workspaces/<agent>/state.json` modification times
- Falls back to `agent_workspaces/<agent>/response.txt` if state.json missing
- Updates activity timestamps every 5 seconds (configurable)

### 2. **Stall Detection**
- **Active**: < 5 minutes since last activity
- **Idle**: 5-20 minutes since last activity  
- **Stalled**: > 20 minutes since last activity (triggers rescue)

### 3. **Rescue System**
- Automatically sends rescue messages to stalled agents
- **Cooldown**: 5 minutes between rescues (prevents spam)
- **Format**: Structured Dream.OS response template
- **Routing**: Uses existing AgentCellPhone infrastructure

### 4. **State Persistence**
- Saves state to `runtime/agent_monitors/agent5/activity.json`
- Restores state on restart (no false stalls)
- Maintains rescue cooldown timestamps

## 🔧 **Installation & Setup**

### 1. **Directory Structure**
```
src/agent_monitors/
├── __init__.py
├── agent5_monitor.py
└── README.md

scripts/
├── run_agent5_monitor.bat    # Windows
└── run_agent5_monitor.sh     # Linux/Mac

tests/agent_monitors/
├── __init__.py
└── test_agent5_monitor.py
```

### 2. **Dependencies**
- `src/services/agent_cell_phone` - For sending messages
- `src/agent_cell_phone/response_capture` - For response capture
- `src/cursor_capture_v2/watcher` - Optional DB monitoring

### 3. **Runtime Directories**
```
runtime/agent_monitors/agent5/
├── activity.json    # Current state
├── health.json      # Health status
├── metrics.json     # Performance metrics
└── monitor.log      # Activity log
```

## 🚀 **Usage**

### **Quick Start (Windows)**
```batch
scripts\run_agent5_monitor.bat
```

### **Quick Start (Linux/Mac)**
```bash
chmod +x scripts/run_agent5_monitor.sh
./scripts/run_agent5_monitor.sh
```

### **Direct Python Execution**
```bash
python -m src.agent_monitors.agent5_monitor
```

### **Environment Configuration**
```bash
# Core settings
export AGENT_STALL_SEC=1200              # 20 minutes
export AGENT_CHECK_SEC=5                 # Check every 5 seconds
export AGENT_FILE_ROOT=agent_workspaces  # Watch directory

# Rescue settings
export AGENT_RESCUE_COOLDOWN_SEC=300     # 5 minutes between rescues
export AGENT_ACTIVE_GRACE_SEC=300        # 5 minutes before idle

# Advanced settings
export AGENT_FSM_ENABLED=1               # Enable FSM integration
export AGENT_USE_DB_LANE=0               # Disable DB monitoring
```

## 📈 **Monitoring & Health**

### **Health Status** (`health.json`)
```json
{
  "ok": true,
  "note": "running",
  "ts": "2025-01-15T18:30:00.000000+00:00",
  "uptime_sec": 3600
}
```

### **Metrics** (`metrics.json`)
```json
{
  "ts": "2025-01-15T18:30:00.000000+00:00",
  "agents": {
    "Agent-1": {
      "age_sec": 120,
      "status": "active"
    },
    "Agent-2": {
      "age_sec": 1800,
      "status": "stalled"
    }
  }
}
```

### **Activity State** (`activity.json`)
```json
{
  "ts": "2025-01-15T18:30:00.000000+00:00",
  "last_activity": {
    "Agent-1": 1737037800.0,
    "Agent-2": 1737036000.0
  },
  "last_rescue": {
    "Agent-2": 1737036000.0
  },
  "config": {...},
  "uptime_sec": 3600
}
```

## 🧪 **Testing**

### **Run All Tests**
```bash
pytest tests/agent_monitors/ -v
```

### **Run Specific Test**
```bash
python tests/agent_monitors/test_agent5_monitor.py
```

### **Test Coverage**
- ✅ Stall detection triggers rescue
- ✅ Cooldown prevents spam
- ✅ File activity updates timestamps
- ✅ State restoration on restart
- ✅ Health and metrics writing
- ✅ Configuration defaults and overrides

## 🔍 **Troubleshooting**

### **Monitor Won't Start**
1. **Check dependencies**: Ensure `agent_cell_phone` module is available
2. **Check permissions**: Ensure write access to `runtime/agent_monitors/`
3. **Check agents**: Verify agents exist in layout mode

### **No Rescue Messages**
1. **Check cooldown**: Verify rescue cooldown isn't blocking
2. **Check thresholds**: Ensure stall threshold is reasonable
3. **Check file paths**: Verify agent workspace directories exist

### **False Stall Detection**
1. **Check file timestamps**: Verify `state.json` or `response.txt` are being updated
2. **Check timezone**: Ensure system time is correct
3. **Check file permissions**: Verify monitor can read agent files

## 🔄 **Integration with Overnight Runner**

The monitor works alongside the overnight runner:

- **Overnight Runner**: Sends scheduled messages
- **Agent-5 Monitor**: Detects stalls and sends rescues
- **Response Capture**: Captures agent responses
- **FSM Bridge**: Routes responses to workflow engine

### **Start Both Systems**
```bash
# Terminal 1: Start overnight runner
python overnight_runner/runner.py --capture-enabled --rescue-on-stall

# Terminal 2: Start Agent-5 monitor
python -m src.agent_monitors.agent5_monitor
```

## 📚 **API Reference**

### **MonitorConfig**
```python
@dataclass
class MonitorConfig:
    agents: List[str]                    # Agents to monitor
    stall_threshold_sec: int = 1200      # Stall threshold
    check_every_sec: int = 5            # Check interval
    rescue_cooldown_sec: int = 300      # Rescue cooldown
    active_grace_sec: int = 300         # Active grace period
    use_db_lane: bool = False           # Enable DB monitoring
```

### **Agent5Monitor**
```python
class Agent5Monitor:
    def start(self) -> bool              # Start monitoring
    def stop(self)                       # Stop monitoring
    def get_status(self) -> dict         # Get current status
    def _rescue(self, agent: str)        # Send rescue message
```

## 🎯 **Success Indicators**

✅ **Monitor is working when:**
- `runtime/agent_monitors/agent5/health.json` shows `"ok": true`
- `runtime/agent_monitors/agent5/metrics.json` updates every 5 seconds
- `runtime/agent_monitors/agent5/monitor.log` shows activity
- Stalled agents receive rescue messages
- No duplicate rescue messages (cooldown respected)

## 🔮 **Future Enhancements**

- **Web Dashboard**: Real-time monitoring interface
- **Alert System**: Discord/Slack notifications for stalls
- **Machine Learning**: Predict stalls before they happen
- **Performance Metrics**: Response time analysis
- **Agent Health Scoring**: Overall agent performance metrics

---

## 📝 **Commit Message**

```
feat(agent5-monitor): convert demo to production monitor

- Real response capture via file timestamps
- Real rescue messages via AgentCellPhone.send()
- Persistent state with health metrics
- Configurable via environment variables
- Integration with existing response capture pipeline
- Comprehensive test coverage
- Windows/Linux run scripts
```

**Status**: ✅ **Ready for Production** - Real signals in, real rescues out, with persistence and health monitoring.
