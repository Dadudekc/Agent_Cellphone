# 🚀 v2.0.0 Bi-Directional Onboarding Guide

**Version**: 2.0.0  
**Release Date**: August 15, 2025  
**Status**: 🆕 **NEW - Complete Bi-Directional Communication Unlocked!**

---

## 🎯 What's New in v2.0.0

### **🚨 BREAKTHROUGH ACHIEVED!**
The Overnight Runner has evolved from a **one-way messaging system** into a **full bi-directional coordination platform**. Agents can now respond to system prompts, creating a closed feedback loop that enables sophisticated multi-agent workflows.

### **Before vs After**
```
v1.x: Overnight Runner → Send Messages → Agents (one-way)
v2.0: Overnight Runner → Send Messages → Agents → Capture Responses → Parse Structure → Route to FSM → Agent-5 Coordination
```

---

## 🚀 Quick Start with Bi-Directional Features

### **1. Basic Setup (5 minutes)**
```bash
# From D:\Agent_Cellphone
cd overnight_runner

# Test basic messaging
python runner.py --layout 5-agent --agents Agent-1 --msg "[VERIFY] Hello v2.0!" --test
```

### **2. Enable Response Capture (10 minutes)**
```bash
# Start runner with capture enabled
python runner.py \
  --layout 5-agent \
  --agents Agent-1,Agent-2,Agent-3,Agent-4 \
  --plan prd-creation \
  --capture-enabled \
  --capture-config runtime/config/agent_capture.yaml \
  --coords-json runtime/agent_comms/cursor_agent_coords.json
```

### **3. Test Bi-Directional Flow (15 minutes)**
```bash
# Terminal A: Start FSM bridge
python runtime/fsm_bridge/inbox_consumer.py

# Terminal B: Start capture-enabled runner
python runner.py --layout 5-agent --agents Agent-1 --plan contracts --capture-enabled

# Terminal C: Monitor inbox
watch -n 5 "ls -la runtime/agent_comms/inbox/"
```

---

## 🔄 How Bi-Directional Communication Works

### **Response Capture Strategies**
The system automatically captures agent responses using multiple strategies:

1. **File Strategy** (default): Monitors `agent_workspaces/Agent-X/response.txt`
2. **Clipboard Strategy**: System-wide clipboard monitoring
3. **OCR Strategy**: Screenshot-based text extraction (Tesseract)

### **Response Format**
Agents write structured responses to `agent_workspaces/Agent-X/response.txt`:
```
Task: [Current task description]
Actions:
- [Action taken 1]
- [Action taken 2]
- [Action taken 3]
Commit Message: [Git commit message]
Status: [Current status and next steps]
```

### **Automatic Processing**
1. **Capture**: System monitors response files
2. **Parse**: Intelligent parsing with fallback handling
3. **Route**: JSON envelopes sent to inbox
4. **FSM**: Automatic conversion to Agent-5 events

---

## 🛠️ Configuration

### **Capture Configuration**
Edit `runtime/config/agent_capture.yaml`:
```yaml
default_strategy: file   # file | clipboard | ocr
file:
  watch_root: "agent_workspaces"
  response_filename: "response.txt"
clipboard:
  poll_ms: 500
ocr:
  tesseract_cmd: "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
  lang: "eng"
  psm: 6
routing:
  inbox_root: "runtime/agent_comms/inbox"
  agent5_fsm_bridge_enabled: true
```

### **Agent Coordinates**
Update `runtime/agent_comms/cursor_agent_coords.json` for your layout:
```json
{
  "5-agent": {
    "Agent-1": {"x": 100, "y": 100, "width": 800, "height": 600},
    "Agent-2": {"x": 900, "y": 100, "width": 800, "height": 600},
    "Agent-3": {"x": 100, "y": 700, "width": 800, "height": 600},
    "Agent-4": {"x": 900, "y": 700, "width": 800, "height": 600},
    "Agent-5": {"x": 500, "y": 400, "width": 800, "height": 600}
  }
}
```

---

## 📋 New Workflow Plans

### **PRD Creation Plan**
```bash
python runner.py \
  --layout 5-agent \
  --agents Agent-1,Agent-2,Agent-3,Agent-4 \
  --plan prd-creation \
  --duration-min 120 --interval-sec 1800
```

**Workflow Steps:**
1. **RESUME**: Pick 2-3 repos for analysis
2. **TASK**: Create hand-crafted PRD.md based on manual inspection
3. **COORDINATE**: Declare repos being analyzed to avoid duplication
4. **SYNC**: 10-min progress check on PRD work
5. **VERIFY**: Commit PRD.md with evidence

### **Autonomous Development Plan**
```bash
python runner.py \
  --layout 5-agent \
  --agents Agent-1,Agent-2,Agent-3,Agent-4 \
  --plan autonomous-dev \
  --capture-enabled
```

**Workflow Steps:**
1. **RESUME**: Choose highest-leverage task from assigned repos
2. **TASK**: Implement concrete improvements (tests/build/lint/docs/refactor)
3. **COORDINATE**: Prompt peer agents for sanity checks
4. **SYNC**: 10-min status updates
5. **VERIFY**: Verify outcomes with tests/build evidence

---

## 🔍 Monitoring & Debugging

### **Response Capture Status**
```bash
# Check inbox for captured responses
ls -la runtime/agent_comms/inbox/

# Monitor FSM bridge output
tail -f runtime/fsm_bridge/inbox_consumer.log

# Check agent workspace responses
cat agent_workspaces/Agent-1/response.txt
```

### **Common Issues & Solutions**

#### **No Responses Captured**
- Verify `--capture-enabled` flag is set
- Check `agent_capture.yaml` configuration
- Ensure response files exist in agent workspaces

#### **FSM Bridge Not Processing**
- Verify `agent5_fsm_bridge_enabled: true` in config
- Check inbox directory permissions
- Monitor FSM bridge logs

#### **Coordinate Issues**
- Run coordinate calibration: `python tools/capture_coords.py`
- Verify `cursor_agent_coords.json` paths
- Check monitor resolution and layout

---

## 🧪 Testing & Validation

### **Basic Functionality Test**
```bash
# Test response capture
python test_capture.py

# Test FSM bridge
python runtime/fsm_bridge/inbox_consumer.py --test

# Test full integration
python runner.py --layout 5-agent --agents Agent-1 --plan contracts --capture-enabled --test
```

### **Validation Checklist**
- [ ] Response capture system working
- [ ] Structured parsing successful
- [ ] Inbox routing functional
- [ ] FSM bridge processing events
- [ ] Agent-5 coordination active

---

## 📚 Advanced Features

### **Custom Response Formats**
Extend parsing in `src/agent_cell_phone/response_capture.py`:
```python
# Add new format recognition
CUSTOM_RX = re.compile(r"Custom:\s*(?P<custom>.+)")

def parse_custom_format(text: str) -> Dict:
    m = CUSTOM_RX.search(text)
    if m:
        return {"type": "custom", "data": m.group("custom")}
    return {"type": "unknown", "raw": text}
```

### **Multiple Capture Strategies**
```bash
# Use clipboard strategy
python runner.py --capture-enabled --capture-config custom_capture.yaml

# Use OCR strategy (requires Tesseract)
python runner.py --capture-enabled --capture-config ocr_capture.yaml
```

### **FSM Workflow Customization**
Extend `runtime/fsm_bridge/inbox_consumer.py` for custom event processing:
```python
def process_custom_event(event_data: Dict) -> None:
    """Process custom event types."""
    event_type = event_data.get("type")
    if event_type == "custom":
        # Handle custom event
        pass
```

---

## 🚨 Migration from v1.x

### **For Existing Users**
1. **Install Dependencies**: `pip install -r requirements_capture.txt`
2. **Update Runner Calls**: Add `--capture-enabled` flag
3. **Configure Agents**: Set up response.txt files in agent workspaces
4. **Test Integration**: Verify capture system functionality

### **Breaking Changes**
- New `--capture-enabled` flag required for response capture
- Response files must follow structured format
- FSM bridge integration is now automatic

---

## 📞 Support & Resources

### **Documentation**
- `CAPTURE_IMPLEMENTATION_SUMMARY.md` - Technical details
- `BREAKTHROUGH_v1.0.0_CURSOR_BRIDGE.md` - Release notes
- `runtime/config/agent_capture.yaml` - Configuration reference

### **Testing & Validation**
- Run `python test_capture.py` for basic functionality
- Use `--capture-enabled` flag in runner for full integration
- Monitor `runtime/agent_comms/inbox/` for captured responses

### **Troubleshooting**
- Check coordinate configuration in `cursor_agent_coords.json`
- Verify capture strategy in `agent_capture.yaml`
- Monitor FSM bridge output in `runtime/fsm_bridge/`

---

## 🎯 Success Metrics

### **System Capabilities**
- **Before**: 1-way messaging (send only)
- **After**: 2-way coordination (send + receive + process)

### **Workflow Complexity**
- **Before**: Linear task assignment
- **After**: Dynamic task coordination with real-time feedback

### **Agent Autonomy**
- **Before**: Passive message recipients
- **After**: Active participants in coordinated workflows

---

## 🏆 What This Unlocks

**The Overnight Runner is now a true agent coordination platform, not just a messaging system.**

- **Autonomous Agent Workflows**: Self-coordinating multi-agent systems
- **Real-time Task Management**: Live status tracking and coordination
- **Intelligent Orchestration**: FSM-based workflow management
- **Scalable Architecture**: Support for complex agent networks

---

**Next Steps**: 
1. Complete the [Basic Setup](#1-basic-setup-5-minutes) above
2. Test [Response Capture](#2-enable-response-capture-10-minutes)
3. Explore [New Workflow Plans](#new-workflow-plans)
4. Customize [Configuration](#configuration) for your environment

[Back to Index](00_INDEX.md) | [Previous: Standard Onboarding](01_GETTING_STARTED.md)
