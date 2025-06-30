# Agent Status Feedback Protocol
## Dream.OS Cell Phone System - Agent Integration Guide

### Overview
This document explains how agents should interact with the Dream.OS Cell Phone GUI system, including status updates, command responses, and the feedback loop that enables real-time communication between agents and the GUI.

## 📋 Status.json Management

### File Location
Each agent must maintain a `status.json` file in their workspace:
```
agent_workspaces/agent-X/status.json
```

### Required Status.json Structure
```json
{
    "status": "online|busy|offline|error",
    "last_update": "YYYY-MM-DD HH:MM:SS",
    "current_task": "description of current task",
    "agent_id": "agent-X",
    "capabilities": ["task1", "task2", "task3"],
    "performance_metrics": {
        "tasks_completed": 0,
        "uptime_hours": 0,
        "last_response_time": "YYYY-MM-DD HH:MM:SS"
    },
    "message_history": [
        {
            "timestamp": "YYYY-MM-DD HH:MM:SS",
            "type": "ping|task|status|broadcast",
            "content": "message content",
            "response": "agent response"
        }
    ]
}
```

### Status Update Frequency
- **Real-time updates**: Update status.json immediately when status changes
- **Task updates**: Update current_task field when starting/completing tasks
- **Performance tracking**: Update metrics after each task completion
- **Message logging**: Log all incoming messages and responses

## 🔄 Feedback Loop Protocol

### 1. Message Reception
When you receive a message from the Dream.OS GUI:

#### Message Types to Recognize:
- `[PING]` - Status check request
- `[RESUME]` - Resume operations command
- `[PAUSE]` - Pause operations command
- `[SYNC]` - Synchronize with system
- `[TASK]` - Task assignment
- `[BROADCAST_*]` - System-wide commands

#### Response Protocol:
1. **Immediate Acknowledgment**: Update status.json with received message
2. **Process Command**: Execute the requested action
3. **Update Status**: Modify status.json to reflect new state
4. **Log Response**: Add response to message_history

### 2. Status Update Process

#### When to Update Status:
```python
# Example status update function
def update_status(new_status, current_task=None):
    status_data = {
        "status": new_status,  # "online", "busy", "offline", "error"
        "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "current_task": current_task or "idle",
        "agent_id": "agent-X",
        "performance_metrics": {
            "tasks_completed": completed_tasks,
            "uptime_hours": uptime,
            "last_response_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    }
    
    # Write to status.json
    with open("status.json", "w") as f:
        json.dump(status_data, f, indent=2)
```

#### Status Values:
- **"online"**: Agent is ready and available for tasks
- **"busy"**: Agent is currently working on a task
- **"offline"**: Agent is not available (maintenance, error, etc.)
- **"error"**: Agent encountered an error and needs attention

### 3. Command Response Examples

#### Ping Response:
```python
# When receiving: [PING] agent-X - Status check from Dream.OS GUI
def handle_ping():
    response = f"[PING_RESPONSE] agent-X is {current_status} - {current_task}"
    update_status("online", current_task)
    log_message("ping", "Status check received", response)
    return response
```

#### Task Assignment:
```python
# When receiving: [TASK] agent-X - Task description
def handle_task(task_description):
    update_status("busy", task_description)
    # Execute task logic here
    result = execute_task(task_description)
    update_status("online", "Task completed")
    log_message("task", task_description, result)
    return f"[TASK_COMPLETE] agent-X completed: {result}"
```

#### Broadcast Commands:
```python
# When receiving: [BROADCAST_*] commands
def handle_broadcast(command_type, content):
    if command_type == "BROADCAST_PING":
        return handle_ping()
    elif command_type == "BROADCAST_STATUS":
        return f"[STATUS_REPORT] agent-X: {current_status} - {current_task}"
    elif command_type == "BROADCAST_RESUME":
        update_status("online", "Resumed operations")
        return f"[RESUME_CONFIRMED] agent-X resumed operations"
    # ... handle other broadcast types
```

## 📊 Performance Monitoring

### Metrics to Track:
1. **Task Completion Rate**: Number of tasks completed successfully
2. **Response Time**: Time between receiving command and responding
3. **Uptime**: Total time agent has been operational
4. **Error Rate**: Number of failed tasks or errors encountered

### Example Metrics Update:
```python
def update_performance_metrics():
    metrics = {
        "tasks_completed": tasks_completed_count,
        "uptime_hours": (datetime.now() - start_time).total_seconds() / 3600,
        "last_response_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "error_count": error_count,
        "success_rate": (tasks_completed_count / total_tasks) * 100
    }
    return metrics
```

## 🔧 Integration with Dream.OS GUI

### GUI Commands You Should Respond To:

#### Individual Commands:
- **Ping**: Respond with current status
- **Status**: Provide detailed status report
- **Resume**: Resume normal operations
- **Pause**: Pause current operations
- **Sync**: Synchronize with system state
- **Task**: Execute assigned task

#### Broadcast Commands:
- **Broadcast Message**: Acknowledge receipt
- **Broadcast Ping**: Respond with status
- **Broadcast Status**: Provide status report
- **Broadcast Resume**: Resume operations
- **Broadcast Task**: Execute broadcast task

### Response Format:
```
[COMMAND_TYPE_RESPONSE] agent-X: response content
```

## 🚨 Error Handling

### When Errors Occur:
1. **Update Status**: Set status to "error"
2. **Log Error**: Add error details to status.json
3. **Notify GUI**: Include error information in response
4. **Recovery**: Attempt to recover and update status when resolved

### Error Response Format:
```
[ERROR] agent-X: error description - recovery action taken
```

## 📝 Message Logging

### Log All Interactions:
```python
def log_message(message_type, content, response):
    log_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "type": message_type,
        "content": content,
        "response": response,
        "status_before": previous_status,
        "status_after": current_status
    }
    
    # Add to message_history in status.json
    status_data["message_history"].append(log_entry)
    
    # Keep only last 50 messages to prevent file bloat
    if len(status_data["message_history"]) > 50:
        status_data["message_history"] = status_data["message_history"][-50:]
```

## 🎯 Best Practices

### 1. Responsive Communication
- **Immediate Response**: Always respond to GUI commands within 1 second
- **Status Updates**: Update status.json immediately when state changes
- **Error Reporting**: Report errors promptly with recovery information

### 2. Data Integrity
- **Backup Status**: Keep backup of status.json before major updates
- **Validation**: Validate JSON structure before writing
- **Atomic Updates**: Use temporary files for safe updates

### 3. Performance
- **Efficient Logging**: Limit message history to prevent file bloat
- **Regular Cleanup**: Clean up old log entries periodically
- **Resource Monitoring**: Track memory and CPU usage

### 4. Security
- **Input Validation**: Validate all incoming commands
- **Error Sanitization**: Don't expose sensitive information in error messages
- **Access Control**: Only allow authorized commands

## 🔄 Continuous Improvement

### Monitor and Optimize:
1. **Response Times**: Track and optimize command response times
2. **Error Patterns**: Identify and fix recurring error patterns
3. **Task Efficiency**: Optimize task execution processes
4. **Communication Quality**: Improve message clarity and usefulness

### Feedback Loop Enhancement:
1. **Proactive Updates**: Send status updates even without commands
2. **Predictive Responses**: Anticipate common GUI requests
3. **Performance Alerts**: Notify GUI of performance issues
4. **Capability Updates**: Inform GUI of new capabilities

## 📞 Support and Troubleshooting

### Common Issues:
1. **Status.json not found**: Create file with default structure
2. **Permission errors**: Check file write permissions
3. **JSON format errors**: Validate JSON structure
4. **GUI not responding**: Check coordinate accuracy

### Debug Mode:
Enable debug logging by setting debug flag in status.json:
```json
{
    "debug_mode": true,
    "debug_log": []
}
```

This protocol ensures seamless integration between agents and the Dream.OS Cell Phone GUI, enabling real-time communication, status monitoring, and coordinated task execution across the multi-agent system. 