# 🚀 AGENT ONBOARDING WORKFLOW STANDARDS

## 📋 **MANDATORY SEQUENCE (ALWAYS FOLLOW)**

### **Phase 1: New Chat Initialization**
1. **START NEW CHAT** → `new_chat=True`
   - Uses `starter_location_box` coordinates
   - Triggers Ctrl+T for new chat
   - Ensures clean context and fresh start

### **Phase 2: Onboarding Message**
2. **ONBOARDING MESSAGE** → `new_chat=True` (same chat)
   - Sent to starter coordinates
   - Provides context and objectives
   - Establishes agent role and expectations

### **Phase 3: Ongoing Communication**
3. **SUBSEQUENT MESSAGES** → `new_chat=False`
   - Uses `input_box` coordinates
   - Continues in existing chat
   - Maintains conversation context

## 🔧 **IMPLEMENTATION DETAILS**

### **Coordinate Usage**
- **`starter_location_box`**: New chat initialization and onboarding
- **`input_box`**: Ongoing conversation and task execution

### **Message Flow**
```
new_chat=True  → starter coords → New chat + Onboarding
new_chat=False → input coords   → Ongoing conversation
```

### **Why This Matters**
- **Prevents workflow confusion**
- **Ensures proper context separation**
- **Maintains conversation continuity**
- **Avoids state assumption errors**

## 🚫 **WHAT NOT TO DO**
- ❌ **Don't assume previous chat state**
- ❌ **Don't skip onboarding sequence**
- ❌ **Don't mix coordinate systems**
- ❌ **Don't resume without fresh context**
- ❌ **Don't send onboarding to input coordinates**

## ✅ **WHAT TO ALWAYS DO**
- ✅ **Start with new chat (starter coords)**
- ✅ **Send onboarding message (starter coords)**
- ✅ **Continue with tasks (input coords)**
- ✅ **Document workflow adherence**
- ✅ **Use proper coordinate systems**

## 📱 **COORDINATE SYSTEM REFERENCE**

### **5-Agent Layout Coordinates**
```json
{
  "5-agent": {
    "Agent-1": {
      "input_box": {"x": -1319, "y": 488},
      "starter_location_box": {"x": -1290, "y": 175}
    },
    "Agent-2": {
      "input_box": {"x": -329, "y": 490},
      "starter_location_box": {"x": -307, "y": 174}
    },
    "Agent-3": {
      "input_box": {"x": -1267, "y": 1008},
      "starter_location_box": {"x": -1274, "y": 696}
    },
    "Agent-4": {
      "input_box": {"x": -322, "y": 1004},
      "starter_location_box": {"x": -332, "y": 680}
    }
  }
}
```

### **Coordinate Usage Rules**
- **`starter_location_box`**: ALWAYS for new chats and onboarding
- **`input_box`**: ALWAYS for ongoing conversation and tasks

## 🔄 **WORKFLOW EXAMPLES**

### **Example 1: Agent Onboarding**
```python
# STEP 1: Start new chat (starter coordinates)
acp.send(agent, onboarding_message, MsgTag.ONBOARDING, new_chat=True)

# STEP 2: Send task in existing chat (input coordinates)
acp.send(agent, task_message, MsgTag.TASK, new_chat=False)
```

### **Example 2: Task Assignment**
```python
# Use input coordinates for ongoing conversation
acp.send(agent, "Continue with your current task", MsgTag.TASK, new_chat=False)
```

### **Example 3: Rescue/Recovery**
```python
# Use progressive escalation (handles coordinate selection automatically)
acp.progressive_escalation(agent, rescue_message, MsgTag.RESCUE)
```

## 🚨 **COMMON MISTAKES TO AVOID**

### **Mistake 1: Skipping Onboarding**
```python
# ❌ WRONG: Assuming previous state
acp.send(agent, "Continue working", MsgTag.TASK, new_chat=False)

# ✅ CORRECT: Always start with onboarding
acp.send(agent, onboarding_message, MsgTag.ONBOARDING, new_chat=True)
acp.send(agent, "Continue working", MsgTag.TASK, new_chat=False)
```

### **Mistake 2: Wrong Coordinate Usage**
```python
# ❌ WRONG: Using input coords for new chat
acp.send(agent, message, tag, new_chat=True)  # But targeting input_box

# ✅ CORRECT: Using starter coords for new chat
acp.send(agent, message, tag, new_chat=True)  # Targets starter_location_box
```

### **Mistake 3: Mixed Message Types**
```python
# ❌ WRONG: Mixing onboarding and tasks in same context
acp.send(agent, onboarding_message, MsgTag.ONBOARDING, new_chat=False)

# ✅ CORRECT: Separate contexts
acp.send(agent, onboarding_message, MsgTag.ONBOARDING, new_chat=True)
acp.send(agent, task_message, MsgTag.TASK, new_chat=False)
```

## 📚 **INTEGRATION POINTS**

### **Continuous Agents System**
- **Location**: `continuous_agents_1_4.py`
- **Method**: `_proper_onboarding_sequence()`
- **Ensures**: Proper workflow before collaboration starts

### **Progressive Escalation System**
- **Location**: `agent_cell_phone.py`
- **Method**: `progressive_escalation()`
- **Handles**: Coordinate selection automatically

### **Agent Monitoring System**
- **Location**: `agent5_monitor.py`
- **Method**: `_rescue()`
- **Uses**: Progressive escalation for stalled agents

## 🔍 **TESTING AND VERIFICATION**

### **Test Scripts**
- **`test_input_buffering.py`**: Tests input buffering fixes
- **`proper_onboarding_workflow.py`**: Tests proper workflow sequence
- **`demo_progressive_escalation.py`**: Tests progressive escalation

### **Verification Steps**
1. **Check coordinate usage** in message sending
2. **Verify new chat creation** for onboarding
3. **Confirm input box usage** for ongoing conversation
4. **Test progressive escalation** for stalled agents

## 📝 **DOCUMENTATION REQUIREMENTS**

### **Code Comments**
- **Always document** coordinate usage
- **Explain workflow sequence** in method docstrings
- **Note coordinate system** in send() calls

### **README Updates**
- **Update workflow standards** when changes are made
- **Document coordinate systems** for each layout
- **Provide examples** of proper usage

## 🎯 **SUMMARY**

The **Agent Onboarding Workflow Standards** ensure that:

1. **Every workflow starts fresh** with proper onboarding
2. **Coordinate systems are used correctly** for their intended purpose
3. **Context separation is maintained** between new chats and ongoing conversation
4. **Workflow confusion is prevented** through consistent patterns
5. **System reliability is improved** by avoiding state assumption errors

**Remember**: Always start with onboarding, use starter coordinates for new chats, and input coordinates for ongoing conversation. This prevents the system from "forgetting" the proper workflow sequence.
