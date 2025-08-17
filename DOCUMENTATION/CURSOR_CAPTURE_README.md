# 🚀 Cursor AI Response Capture System

## Overview

The **Cursor AI Response Capture System** provides **bi-directional communication** between the Agent_Cellphone system and AI assistants using Cursor. It automatically captures AI responses from Cursor's local database and integrates them into the FSM workflow.
> **Note:** This system relies on the Cursor editor and has only been tested with Cursor. An active paid Cursor membership is required for use.

## 🎯 **What This Solves**

**Before**: System could only send prompts to agents (one-way communication)
**After**: Full bi-directional loop - system prompts agents AND captures AI responses

## 🏗️ **Architecture**

```
┌─────────────────┐    📤     ┌─────────────────┐    📥     ┌─────────────────┐
│   Overnight    │ ────────→ │   Cursor UI    │ ────────→ │   AI Assistant  │
│    Runner      │   Prompt  │                │   Type    │                │
└─────────────────┘           └─────────────────┘           └─────────────────┘
         │                                                           │
         │                                                           │
         ▼                                                           ▼
┌─────────────────┐    📥     ┌─────────────────┐    📥     ┌─────────────────┐
│   AgentCellPhone│ ←──────── │  Cursor DB      │ ←──────── │   Response      │
│                 │   Capture │  (state.vscdb)  │   Store   │                │
└─────────────────┘           └─────────────────┘           └─────────────────┘
         │
         ▼
┌─────────────────┐
│   FSM System   │
│   (Agent-5)    │
└─────────────────┘
```

## 🔧 **Components**

### 1. **Database Reader** (`src/cursor_capture/db_reader.py`)
- **Purpose**: Reads Cursor's local SQLite database (`state.vscdb`)
- **Function**: Extracts AI assistant messages from chat history
- **Cross-platform**: Works on Windows, macOS, and Linux

### 2. **Watcher** (`src/cursor_capture/watcher.py`)
- **Purpose**: Monitors databases for new AI responses
- **Function**: Emits structured envelopes to inbox system
- **Deduplication**: Prevents duplicate message processing

### 3. **Export Consumer** (`src/cursor_capture/export_consumer.py`)
- **Purpose**: Fallback when database access isn't available
- **Function**: Processes exported chat files (.json/.md)
- **Workflow**: Watch export directory → process files → create envelopes

### 4. **Agent Workspace Mapping** (`src/runtime/config/agent_workspace_map.json`)
- **Purpose**: Maps agents to their Cursor workspace paths
- **Format**: JSON mapping of agent names to workspace roots

## 🚀 **Quick Start**

### 1. **Enable in Overnight Runner**
```bash
python overnight_runner/runner.py \
  --layout 5-agent \
  --agents Agent-1,Agent-2,Agent-3,Agent-4 \
  --plan contracts \
  --cursor-db-capture-enabled \
  --agent-workspace-map src/runtime/config/agent_workspace_map.json
```

### 2. **Configure Agent Workspaces**
Edit `src/runtime/config/agent_workspace_map.json`:
```json
{
  "Agent-1": {"workspace_root": "D:/repos/project-A"},
  "Agent-2": {"workspace_root": "D:/repos/project-B"},
  "Agent-3": {"workspace_root": "D:/repos/project-C"}
}
```

### 3. **System Automatically**
- ✅ Monitors Cursor databases for new AI responses
- ✅ Captures responses in real-time
- ✅ Creates structured envelopes
- ✅ Routes to FSM system via Agent-5 inbox

## 📊 **Message Flow**

### **Outbound (System → Agent)**
1. Overnight runner sends prompt via AgentCellPhone
2. PyAutoGUI types message into Cursor UI
3. Agent receives prompt in Cursor

### **Inbound (AI → System)**
1. AI assistant types response in Cursor
2. Cursor stores response in `state.vscdb`
3. Database watcher detects new message
4. Message extracted and parsed
5. Structured envelope created
6. Envelope sent to Agent-5 inbox
7. FSM system processes response

## 🔍 **Message Format**

### **Captured AI Response Envelope**
```json
{
  "type": "assistant_reply",
  "from": "Agent-1",
  "to": "Agent-5",
  "timestamp": "2025-08-15T04:23:38",
  "agent": "Agent-1",
  "ts": 1692072218,
  "payload": {
    "type": "assistant_reply",
    "text": "I've completed the task and updated the documentation...",
    "message_id": "abc123",
    "role": "assistant"
  }
}
```

## 🛡️ **Fallback Strategies**

### **Primary: Database Reading**
- **Method**: Direct SQLite access to `state.vscdb`
- **Pros**: Real-time, reliable, no UI interaction needed
- **Cons**: Requires Cursor to be running

### **Fallback 1: Export Chat**
- **Method**: Manual export from Cursor (File → Export Chat)
- **Pros**: Reliable, works offline
- **Cons**: Manual process, not real-time

### **Fallback 2: Copy Response**
- **Method**: UI automation to click "Copy Response" buttons
- **Pros**: Real-time, reliable
- **Cons**: Requires precise UI automation

## 🧪 **Testing**

### **Test Database Access**
```bash
python test_cursor_capture.py
```

### **Test Full System**
```bash
python demo_cursor_capture.py
```

### **Test with Real Data**
1. Open a workspace in Cursor
2. Have a chat conversation
3. Run overnight runner with `--cursor-db-capture-enabled`

## 📁 **Directory Structure**

```
Agent_Cellphone/
├── src/
│   ├── cursor_capture/
│   │   ├── __init__.py
│   │   ├── db_reader.py      # Database access
│   │   ├── watcher.py        # Message monitoring
│   │   └── export_consumer.py # Export fallback
│   └── runtime/
│       └── config/
│           └── agent_workspace_map.json
├── agent_workspaces/
│   └── Agent-5/
│       └── inbox/            # Captured messages
└── overnight_runner/
    └── runner.py             # Integration point
```

## ⚙️ **Configuration**

### **Agent Workspace Mapping**
```json
{
  "Agent-1": {"workspace_root": "D:/repos/project-A"},
  "Agent-2": {"workspace_root": "D:/repos/project-B"}
}
```

### **Environment Variables**
- `APPDATA` (Windows): Cursor workspace storage location
- `HOME` (macOS/Linux): Cursor workspace storage location

## 🔧 **Troubleshooting**

### **No Database Found**
- **Cause**: Workspace hasn't been opened in Cursor
- **Solution**: Open workspace in Cursor, have a chat conversation

### **Permission Denied**
- **Cause**: SQLite database locked by Cursor
- **Solution**: Close Cursor, reopen workspace

### **No Messages Captured**
- **Cause**: No AI responses in chat history
- **Solution**: Ensure AI assistant has typed responses

### **Import Errors**
- **Cause**: Module path issues
- **Solution**: Run from project root directory

## 📈 **Performance**

- **Polling Interval**: 1 second (configurable)
- **Database Access**: Read-only, non-blocking
- **Memory Usage**: Minimal (only stores message signatures)
- **CPU Usage**: Low (simple polling loop)

## 🔮 **Future Enhancements**

- **Real-time Notifications**: WebSocket-based live updates
- **Message Filtering**: Content-based message selection
- **Batch Processing**: Bulk message processing
- **Metrics Dashboard**: Capture statistics and monitoring
- **Multi-Cursor Support**: Handle multiple Cursor instances

## 🎯 **Success Metrics**

- ✅ **Bi-directional Communication**: System can now prompt AND capture
- ✅ **Real-time Capture**: AI responses captured within 1 second
- ✅ **Reliable Integration**: Works with existing FSM workflow
- ✅ **Fallback Support**: Multiple capture strategies available
- ✅ **Production Ready**: Tested and integrated with overnight runner

## 🚀 **Ready to Use**

The Cursor AI Response Capture System is now **fully operational** and ready for production use. It provides the missing piece for complete bi-directional communication between your agent system and AI assistants using Cursor.

**Next Steps:**
1. Configure agent workspace mappings
2. Run overnight runner with `--cursor-db-capture-enabled`
3. Start having conversations in Cursor
4. Watch AI responses automatically captured and processed!

---

*Built with ❤️ for the Agent_Cellphone project*
