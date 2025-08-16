# 🚀 v2.0.0 Quick Reference Card

**For agents during operations - keep this handy!**

---

## ⚡ **Essential Commands**

### **Start Runner with Capture**
```bash
python runner.py \
  --layout 5-agent \
  --agents Agent-1,Agent-2,Agent-3,Agent-4 \
  --plan prd-creation \
  --capture-enabled \
  --capture-config runtime/config/agent_capture.yaml
```

### **Test Response Capture**
```bash
# Test basic messaging
python runner.py --layout 5-agent --agents Agent-1 --msg "[VERIFY] Test" --test

# Test with capture enabled
python runner.py --layout 5-agent --agents Agent-1 --plan contracts --capture-enabled --test
```

---

## 📝 **Response Format (Write to `agent_workspaces/Agent-X/response.txt`)**

```
Task: [Current task description]
Actions:
- [Action taken 1]
- [Action taken 2]
- [Action taken 3]
Commit Message: [Git commit message]
Status: [Current status and next steps]
```

**Example:**
```
Task: Consolidating logging utilities in Auto_Blogger
Actions:
- Created unified_logging.py with consolidated functionality
- Updated main.py to use new utility
- Added comprehensive tests for logging functions
Commit Message: feat: consolidate logging utilities, reduce duplication
Status: Ready for testing, need to verify all imports updated
```

---

## 🔍 **Monitoring Commands**

### **Check Response Capture Status**
```bash
# View inbox contents
ls -la runtime/agent_comms/inbox/

# Monitor FSM bridge
tail -f runtime/fsm_bridge/inbox_consumer.log

# Check agent responses
cat agent_workspaces/Agent-1/response.txt
```

### **Verify System Health**
```bash
# Test capture system
python test_capture.py

# Check configuration
cat runtime/config/agent_capture.yaml

# Validate coordinates
python tools/capture_coords.py --layout 5-agent --agent Agent-1 --test
```

---

## 🛠️ **Common Workflow Plans**

### **PRD Creation**
```bash
python runner.py \
  --layout 5-agent \
  --agents Agent-1,Agent-2,Agent-3,Agent-4 \
  --plan prd-creation \
  --duration-min 120 --interval-sec 1800
```

### **Autonomous Development**
```bash
python runner.py \
  --layout 5-agent \
  --agents Agent-1,Agent-2,Agent-3,Agent-4 \
  --plan autonomous-dev \
  --capture-enabled
```

### **Contract Management**
```bash
python runner.py \
  --layout 5-agent \
  --agents Agent-1,Agent-2,Agent-3,Agent-4 \
  --plan contracts \
  --capture-enabled
```

---

## 🚨 **Troubleshooting Quick Fixes**

### **No Responses Captured**
- ✅ Verify `--capture-enabled` flag is set
- ✅ Check `agent_workspaces/Agent-X/response.txt` exists
- ✅ Confirm `agent_capture.yaml` configuration

### **FSM Bridge Issues**
- ✅ Verify `agent5_fsm_bridge_enabled: true` in config
- ✅ Check inbox directory permissions
- ✅ Monitor FSM bridge logs

### **Coordinate Problems**
- ✅ Run: `python tools/capture_coords.py --layout 5-agent --agent Agent-X`
- ✅ Verify `cursor_agent_coords.json` paths
- ✅ Check monitor resolution

---

## 📊 **Response Types & Parsing**

The system automatically recognizes these response formats:

1. **Structured Response** (preferred):
   ```
   Task: [description]
   Actions: [list]
   Commit Message: [message]
   Status: [status]
   ```

2. **Freeform Response** (fallback):
   - Any text format
   - System generates summary automatically

3. **Custom Formats** (extensible):
   - Add new patterns in `response_capture.py`
   - Support for specialized workflows

---

## 🔄 **Workflow Steps (RESUME → TASK → COORDINATE → SYNC → VERIFY)**

1. **RESUME**: Pick work and declare focus area
2. **TASK**: Implement concrete improvements
3. **COORDINATE**: Avoid duplication with peers
4. **SYNC**: 10-min status updates
5. **VERIFY**: Provide evidence and commit

---

## 📁 **Key Files & Directories**

- `runtime/config/agent_capture.yaml` - Capture configuration
- `runtime/agent_comms/cursor_agent_coords.json` - Agent coordinates
- `runtime/agent_comms/inbox/` - Response inbox
- `runtime/fsm_bridge/inbox_consumer.py` - FSM bridge
- `agent_workspaces/Agent-X/response.txt` - Your response file

---

## 🎯 **Success Indicators**

- ✅ Responses appear in inbox within seconds
- ✅ FSM bridge processes events automatically
- ✅ Agent-5 receives coordination updates
- ✅ Workflow progresses through all phases
- ✅ No duplicate work across agents

---

**Need Help?** Check `20_V2_BI_DIRECTIONAL_ONBOARDING.md` for complete documentation.

[Back to Index](00_INDEX.md) | [Full v2.0.0 Guide](20_V2_BI_DIRECTIONAL_ONBOARDING.md)
