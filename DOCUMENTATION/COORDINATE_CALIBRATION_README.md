# 🎯 **5-AGENT MODE COORDINATE CALIBRATION SYSTEM**

## **🚀 Overview**

This system recalibrates coordinates for 5-agent mode in your Agent Cellphone system, ensuring agents can properly communicate with Cursor instances. The calibration integrates seamlessly with your existing architecture.

## **🔧 What This Fixes**

- **❌ Off coordinates** - Agents typing in wrong locations
- **❌ Communication failures** - Messages not reaching intended agents
- **❌ Layout changes** - Cursor window moved or resized
- **❌ Screen resolution changes** - Coordinates no longer accurate

## **📱 5-Agent Layout**

```
┌─────────────────┬─────────────────┐
│   Agent-1       │   Agent-2       │
│  (Top Left)     │  (Top Right)    │
├─────────────────┼─────────────────┤
│   Agent-3       │   Agent-4       │
│ (Bottom Left)   │ (Bottom Right)  │
├─────────────────┼─────────────────┤
│              Agent-5               │
│            (Center/Right)          │
└─────────────────────────────────────┘
```

## **🎯 Calibration Process**

### **Step 1: Run Calibration**
```bash
python calibrate_5_agent_coordinates.py
```

### **Step 2: Follow Prompts**
For each agent, you'll be prompted to:
1. **📍 Click starter location** - Where to click to start new chat
2. **⌨️ Click input box** - Where to type messages

### **Step 3: Automatic Backup**
- Current coordinates are automatically backed up
- New coordinates are saved to the system
- Integration with existing AgentCellPhone architecture

## **🧪 Testing Calibrated Coordinates**

### **Test All Coordinates**
```bash
python test_calibrated_coordinates.py
```

### **Test Single Agent**
```bash
python test_calibrated_coordinates.py Agent-1
```

### **What Testing Does**
- Moves mouse to each coordinate location
- Verifies coordinates are accessible
- Shows success/failure for each agent

## **🔄 Backup & Restoration**

### **Automatic Backup**
- Created during calibration: `cursor_agent_coords_backup.json`
- Preserves your original coordinates

### **Restore from Backup**
```bash
python restore_coordinate_backup.py
```

### **Manual Backup Locations**
- **Current**: `runtime/agent_comms/cursor_agent_coords.json`
- **Backup**: `runtime/agent_comms/cursor_agent_coords_backup.json`
- **Current Backup**: `runtime/agent_comms/cursor_agent_coords_current_backup.json`

## **🔗 Integration with Existing System**

### **Seamless Integration**
- Uses existing coordinate file structure
- Maintains compatibility with all layout modes
- Integrates with AgentCellPhone service
- Works with PyAutoGUI queue system

### **Files Updated**
- `runtime/agent_comms/cursor_agent_coords.json` - Main coordinate file
- All existing 2-agent, 4-agent, 8-agent configurations preserved

## **📋 Prerequisites**

### **System Requirements**
- Python 3.8+
- PyAutoGUI installed
- Cursor in 5-agent mode
- Windows visible and accessible

### **Install Dependencies**
```bash
pip install pyautogui
```

## **⚠️ Important Notes**

### **Before Calibration**
1. **Ensure Cursor is in 5-agent mode**
2. **Make sure all agent windows are visible**
3. **Don't minimize or hide Cursor**
4. **Close other applications that might interfere**

### **During Calibration**
1. **Position mouse carefully** over each location
2. **Don't move mouse** during countdown
3. **Use Ctrl+C** to cancel if needed
4. **Take your time** - accuracy is important

### **After Calibration**
1. **Test coordinates** before using system
2. **Verify each agent** can receive messages
3. **Check backup** was created successfully

## **🚨 Troubleshooting**

### **Common Issues**

#### **Coordinates Still Wrong**
- Run calibration again
- Check if Cursor layout changed
- Verify screen resolution
- Ensure Cursor is in correct mode

#### **Calibration Fails**
- Check PyAutoGUI installation
- Verify Cursor is visible
- Ensure mouse is accessible
- Check for permission issues

#### **System Not Working**
- Test coordinates first
- Check coordinate file permissions
- Verify file paths are correct
- Restore from backup if needed

### **Error Messages**

#### **"Coordinate file not found"**
- Check if `runtime/agent_comms/` directory exists
- Verify `cursor_agent_coords.json` is present
- Run from correct directory

#### **"Agent not found in coordinates"**
- Check if 5-agent mode is configured
- Verify coordinate file structure
- Run calibration to create configuration

## **📊 Coordinate File Structure**

### **Example 5-Agent Configuration**
```json
{
  "5-agent": {
    "Agent-1": {
      "starter_location_box": {"x": -1319, "y": 175},
      "input_box": {"x": -1319, "y": 488}
    },
    "Agent-2": {
      "starter_location_box": {"x": -329, "y": 174},
      "input_box": {"x": -329, "y": 490}
    },
    "Agent-3": {
      "starter_location_box": {"x": -1274, "y": 696},
      "input_box": {"x": -1267, "y": 1008}
    },
    "Agent-4": {
      "starter_location_box": {"x": -305, "y": 695},
      "input_box": {"x": -322, "y": 1004}
    },
    "Agent-5": {
      "starter_location_box": {"x": 1576, "y": 116},
      "input_box": {"x": 1579, "y": 945}
    }
  }
}
```

## **🎯 Best Practices**

### **Calibration Tips**
1. **Use consistent lighting** - avoid glare on screen
2. **Calibrate in same conditions** you'll use the system
3. **Test immediately** after calibration
4. **Keep backups** of working configurations

### **Maintenance**
1. **Re-calibrate** after major system changes
2. **Test coordinates** regularly
3. **Update coordinates** if Cursor layout changes
4. **Document changes** for team members

## **🔮 Future Enhancements**

### **Planned Features**
- **Auto-calibration** using screen recognition
- **Layout detection** for automatic mode switching
- **Coordinate validation** with visual feedback
- **Multi-monitor support** for complex setups

### **Integration Plans**
- **Discord notifications** for calibration events
- **Agent coordination** during calibration
- **Performance metrics** for coordinate accuracy
- **Machine learning** for coordinate optimization

## **📞 Support**

### **Getting Help**
1. **Check troubleshooting** section above
2. **Review coordinate file** structure
3. **Test with single agent** first
4. **Restore from backup** if needed

### **Reporting Issues**
- Document exact error messages
- Note Cursor version and mode
- Include coordinate file contents
- Describe system environment

---

## **🎉 Quick Start Guide**

1. **Prepare**: Ensure Cursor is in 5-agent mode and visible
2. **Calibrate**: `python calibrate_5_agent_coordinates.py`
3. **Test**: `python test_calibrated_coordinates.py`
4. **Verify**: Test agent communication
5. **Use**: Your system is ready!

**Your 5-agent mode coordinates will be perfectly calibrated and ready for seamless agent communication! 🚀**
