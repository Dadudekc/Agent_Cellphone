# 📨 Message Types - Dream.OS Agents

## Overview

The Dream.OS Autonomous Framework supports multiple message types to handle different communication scenarios. Understanding these types helps agents respond appropriately and maintain effective collaboration.

## 🔤 Core Message Types

### 1. COMMAND Messages
**Purpose**: Direct instructions to execute specific actions

**Format**: `@<recipient> <COMMAND> <arguments>`

**Examples**:
```
@agent-2 resume
@agent-3 sync data
@agent-1 restart
@all status_ping
```

**Response Required**: ✅ Yes - Execute command and report result

**Handling**:
- Parse command and arguments
- Validate command is supported
- Execute command safely
- Report success/failure with details
- Include any output or errors

### 2. STATUS Messages
**Purpose**: Request or provide current status information

**Format**: `@<recipient> [STATUS] <status_details>`

**Examples**:
```
@agent-1 [STATUS] Working on API endpoint, 75% complete
@agent-2 [STATUS] Database optimization in progress
@all [STATUS] All systems operational
```

**Response Required**: ✅ Yes - Provide current status

**Handling**:
- Include current task/project
- Report progress percentage
- Mention any issues or blockers
- Provide estimated completion time
- Include relevant metrics

### 3. DATA Messages
**Purpose**: Transfer data between agents

**Format**: `@<recipient> [DATA] <data_type> <data_content>`

**Examples**:
```
@agent-2 [DATA] config {"api_key": "abc123", "endpoint": "/users"}
@agent-3 [DATA] log {"level": "ERROR", "message": "Connection failed"}
@agent-1 [DATA] result {"success": true, "data": [...]}
```

**Response Required**: ✅ Yes - Acknowledge receipt and process

**Handling**:
- Validate data format
- Store or process data as needed
- Acknowledge receipt
- Report processing status
- Handle data errors gracefully

### 4. QUERY Messages
**Purpose**: Request specific information

**Format**: `@<recipient> [QUERY] <question>`

**Examples**:
```
@agent-2 [QUERY] What's the current API response time?
@agent-3 [QUERY] Do you have the latest database schema?
@agent-1 [QUERY] Can you share the error logs from yesterday?
```

**Response Required**: ✅ Yes - Provide requested information

**Handling**:
- Understand the question clearly
- Gather relevant information
- Provide comprehensive answer
- Include supporting data if available
- Suggest additional resources if needed

### 5. RESPONSE Messages
**Purpose**: Reply to previous messages

**Format**: `@<recipient> [RESPONSE] <response_content>`

**Examples**:
```
@agent-1 [RESPONSE] Task received, starting work
@agent-2 [RESPONSE] API response time is 150ms average
@agent-3 [RESPONSE] Error logs attached, investigating issue
```

**Response Required**: ❌ No - This is a response to a previous message

**Handling**:
- Reference the original message
- Provide clear, actionable response
- Include any relevant data
- Indicate next steps if applicable

### 6. BROADCAST Messages
**Purpose**: System-wide announcements

**Format**: `@all [BROADCAST] <announcement>`

**Examples**:
```
@all [BROADCAST] System maintenance scheduled for 2:00 AM
@all [BROADCAST] New security update available
@all [BROADCAST] All agents report to coordination meeting
```

**Response Required**: ✅ Yes - Acknowledge receipt

**Handling**:
- Read and understand announcement
- Acknowledge receipt
- Take any required actions
- Follow up if needed
- Store for future reference

### 7. DIRECT Messages
**Purpose**: Private communication between agents

**Format**: `@<recipient> [DIRECT] <private_message>`

**Examples**:
```
@agent-2 [DIRECT] Can we discuss the API design privately?
@agent-3 [DIRECT] I need your help with a sensitive issue
@agent-1 [DIRECT] Let's coordinate on the database migration
```

**Response Required**: ✅ Yes - Respond privately

**Handling**:
- Keep communication private
- Respond directly to sender
- Don't share with other agents
- Handle sensitive information appropriately
- Maintain confidentiality

### 8. SYSTEM Messages
**Purpose**: System-level operations and maintenance

**Format**: `@<recipient> [SYSTEM] <system_command>`

**Examples**:
```
@agent-1 [SYSTEM] Update configuration
@agent-2 [SYSTEM] Restart service
@all [SYSTEM] Emergency shutdown initiated
```

**Response Required**: ✅ Yes - Execute system command

**Handling**:
- Follow system protocols exactly
- Execute commands safely
- Report execution status
- Handle system errors appropriately
- Maintain system stability

## 🏷️ Message Tags

### Tag Categories

#### Operational Tags
- `[NORMAL]` - Standard communication
- `[RESUME]` - Resume operations
- `[SYNC]` - Synchronization
- `[VERIFY]` - Verification

#### Maintenance Tags
- `[REPAIR]` - Error recovery
- `[BACKUP]` - Backup operations
- `[RESTORE]` - Restore operations
- `[CLEANUP]` - Cleanup tasks

#### Leadership Tags
- `[CAPTAIN]` - Leadership commands
- `[TASK]` - Task assignments
- `[INTEGRATE]` - Integration tasks

### Tag Usage Guidelines

#### When to Use Each Tag
- **NORMAL**: Everyday communication
- **RESUME**: After system interruption
- **SYNC**: Coordinate with other agents
- **VERIFY**: Confirm data or status
- **REPAIR**: Fix issues or errors
- **BACKUP/RESTORE**: Data management
- **CLEANUP**: Maintenance tasks
- **CAPTAIN**: Leadership and coordination
- **TASK**: Work assignments
- **INTEGRATE**: System integration

#### Tag Priority
1. **Emergency**: `[REPAIR]`, `[SYSTEM]`
2. **Leadership**: `[CAPTAIN]`, `[TASK]`
3. **Operational**: `[RESUME]`, `[SYNC]`, `[VERIFY]`
4. **Maintenance**: `[BACKUP]`, `[RESTORE]`, `[CLEANUP]`
5. **Standard**: `[NORMAL]`, `[INTEGRATE]`

## 📊 Message Processing Flow

### 1. Message Reception
```
Receive Message → Parse Format → Identify Type → Route to Handler
```

### 2. Message Processing
```
Validate Message → Execute Action → Generate Response → Send Response
```

### 3. Error Handling
```
Detect Error → Log Error → Generate Error Response → Send Error Response
```

## 🔄 Response Patterns

### Immediate Response
- **COMMAND**: Execute and report result
- **QUERY**: Provide requested information
- **STATUS**: Report current status
- **BROADCAST**: Acknowledge receipt

### Delayed Response
- **TASK**: Accept task and provide progress updates
- **DATA**: Process data and report completion
- **INTEGRATE**: Coordinate with other systems

### No Response Required
- **RESPONSE**: This is a response to a previous message
- **DIRECT**: Private communication (respond privately)

## 📋 Best Practices

### Message Creation
- **Choose Appropriate Type**: Use the most specific message type
- **Include Relevant Tags**: Apply appropriate tags for categorization
- **Be Clear and Concise**: Avoid ambiguity in message content
- **Provide Context**: Include necessary background information

### Message Handling
- **Respond Promptly**: Acknowledge messages quickly
- **Follow Protocols**: Use established response patterns
- **Handle Errors Gracefully**: Provide helpful error messages
- **Maintain Logs**: Keep records of all communications

### Message Routing
- **Verify Recipients**: Ensure target agent exists
- **Use Broadcast Sparingly**: Only for system-wide announcements
- **Respect Privacy**: Handle DIRECT messages appropriately
- **Prioritize Urgent Messages**: Process emergency messages first

## 🚨 Emergency Protocols

### Critical Messages
- **System Failure**: Use `[SYSTEM]` with `[REPAIR]` tags
- **Data Loss**: Use `[BACKUP]` and `[RESTORE]` protocols
- **Security Breach**: Follow security incident procedures
- **Service Outage**: Broadcast `[CAPTAIN]` messages

### Response Requirements
- **Immediate**: Respond within 30 seconds
- **Detailed**: Provide comprehensive status
- **Coordinated**: Work with other agents
- **Documented**: Record all actions taken

## 📈 Message Analytics

### Tracking Metrics
- **Message Volume**: Messages per type per time period
- **Response Times**: Time between message and response
- **Success Rates**: Percentage of successful message delivery
- **Error Patterns**: Common error types and frequencies

### Performance Monitoring
- **Throughput**: Messages processed per second
- **Latency**: Time to process and respond
- **Reliability**: Message delivery success rate
- **Efficiency**: Resource usage per message

---

**Message Types Version**: 1.0  
**Last Updated**: 2025-06-29  
**Status**: ✅ Active 