# Coordinate Capture Tools - Merged & Enhanced

This directory contains enhanced coordinate capture tools that combine the best features from multiple approaches:

## 🎯 **Enhanced Capture Tool** (`enhanced_capture_coords.py`)

**Best for:** Interactive use, batch operations, and comprehensive coordinate management

### Features:
- ✅ **Enter key timing** (no countdown stress!)
- ✅ **Batch capture** for all agents in a layout
- ✅ **Smart backup** creation
- ✅ **Auto-detection** of project structure
- ✅ **Better error handling** and validation
- ✅ **Agent descriptions** for each layout

### Usage Examples:

```bash
# Interactive capture for single agent
python overnight_runner/tools/enhanced_capture_coords.py --layout 5-agent --agent Agent-1

# Batch capture all agents in a layout
python overnight_runner/tools/enhanced_capture_coords.py --layout 5-agent --all-agents

# Quick capture of just input box
python overnight_runner/tools/enhanced_capture_coords.py --layout 4-agent --agent Agent-2 --field input

# Custom output path
python overnight_runner/tools/enhanced_capture_coords.py --layout 8-agent --all-agents --output custom_coords.json
```

---

## ⚡ **Updated Original Tool** (`capture_coords.py`)

**Best for:** Quick single-agent capture, automation, and backward compatibility

### New Features Added:
- ✅ **Enter key timing** option (`--enter-timing`)
- ✅ **Batch capture** support (`--all-agents`)
- ✅ **Better validation** and error handling
- ✅ **Agent descriptions** for guidance

### Usage Examples:

```bash
# Original countdown mode
python overnight_runner/tools/capture_coords.py --layout 5-agent --agent Agent-5 --delay 6

# New Enter key timing mode (recommended)
python overnight_runner/tools/capture_coords.py --layout 5-agent --agent Agent-5 --enter-timing

# Batch capture with Enter timing
python overnight_runner/tools/capture_coords.py --layout 5-agent --all-agents --enter-timing

# Quick input box only
python overnight_runner/tools/capture_coords.py --layout 4-agent --agent Agent-2 --field input
```

---

## 🔧 **Legacy Tool** (`calibrate_coords.py`)

**Best for:** Full interactive calibration sessions

### Features:
- ✅ **Full interactive mode** with menu system
- ✅ **Multiple layout support** in one session
- ✅ **Comprehensive guidance** and descriptions

### Usage:
```bash
python calibrate_coords.py
# Follow the interactive prompts
```

---

## 📋 **Which Tool to Use?**

| Use Case | Recommended Tool | Why |
|----------|------------------|-----|
| **Quick single agent** | `capture_coords.py --enter-timing` | Fast, simple, familiar |
| **Batch capture** | `enhanced_capture_coords.py --all-agents` | Efficient, comprehensive |
| **Full calibration** | `calibrate_coords.py` | Interactive, guided experience |
| **Automation** | `capture_coords.py --delay` | Scriptable, countdown-based |
| **Custom workflows** | `enhanced_capture_coords.py` | Flexible, feature-rich |

---

## 🚀 **Quick Start (Recommended)**

1. **Open Cursor** with your desired agent layout
2. **Run batch capture** for your layout:
   ```bash
   python overnight_runner/tools/enhanced_capture_coords.py --layout 5-agent --all-agents
   ```
3. **Follow prompts** to position mouse and press Enter
4. **Coordinates saved** automatically with backup

---

## 📁 **Output Files**

All tools save to: `runtime/agent_comms/cursor_agent_coords.json`

**File Structure:**
```json
{
  "5-agent": {
    "Agent-1": {
      "input_box": {"x": 1829, "y": 364},
      "starter_location_box": {"x": 1829, "y": 364}
    },
    "Agent-2": {
      "input_box": {"x": 1828, "y": 394},
      "starter_location_box": {"x": 1828, "y": 394}
    }
  }
}
```

---

## 🎯 **What Each Coordinate Does**

- **`input_box`**: Where messages are typed and sent
- **`starter_location_box`**: Where Ctrl+T opens new chats

---

## 🔍 **Troubleshooting**

### "Coordinates not working"
1. **Check screen resolution** - coordinates are absolute screen positions
2. **Verify Cursor layout** - ensure you're using the correct layout mode
3. **Re-capture coordinates** - use `--all-agents` to refresh everything

### "Tool not found"
1. **Check working directory** - run from `D:\Agent_Cellphone`
2. **Verify Python path** - ensure `pyautogui` is installed
3. **Check file permissions** - ensure write access to output directory

### "Negative coordinates"
1. **Re-capture coordinates** - negative values indicate wrong positions
2. **Check screen setup** - multi-monitor setups may need adjustment
3. **Use Enter timing** - more precise than countdown mode

---

## 📚 **Advanced Usage**

### Custom Output Paths
```bash
python enhanced_capture_coords.py --layout 5-agent --all-agents --output custom_coords.json
```

### Force Overwrite
```bash
python enhanced_capture_coords.py --layout 5-agent --all-agents --force
```

### No Backup
```bash
python enhanced_capture_coords.py --layout 5-agent --all-agents --backup=False
```

---

## 🎉 **Success Indicators**

✅ **Coordinates are working when:**
- Messages appear in Cursor agent windows
- No "ghost sending" (messages sent but not received)
- Overnight runner logs show successful sends
- Agent responses are captured correctly

---

## 🔄 **Maintenance**

**When to re-capture coordinates:**
- Screen resolution changes
- Cursor layout modifications
- Multi-monitor setup changes
- Agent window repositioning
- After system updates

**Recommended frequency:** Monthly or when issues arise
