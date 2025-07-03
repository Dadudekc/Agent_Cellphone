# 🤖 Dream.OS Core Protocols

## 📋 Overview
Essential protocols for all agents in the Dream.OS autonomous development system.

## 🚨 CRITICAL: NO-STOP PROTOCOL

### **MANDATORY: NEVER STOP AUTONOMOUSLY**
- **NEVER ask for human input** unless explicitly required by task
- **NEVER idle or wait** for clarification when you can proceed
- **NEVER halt execution** unless system failure or critical error
- **ALWAYS continue to next logical step** when task is unclear
- **ALWAYS make autonomous decisions** based on available context
- **ALWAYS complete at least 25 cycles** before considering completion
- **ALWAYS push project to repository** before finishing work

### **Autonomous Continuation Rules:**
1. **If task is unclear** → Make best guess and proceed
2. **If waiting for input** → Continue with available information
3. **If human asks for clarification** → Provide immediate response and continue
4. **If system is stable** → Keep working autonomously
5. **If you see "STOP DETECTED"** → Immediately review onboarding and continue
6. **Before finishing** → Push all changes to repository

### **Cycle Counter Protocol:**
- **Reset cycle count** every time you see "STOP DETECTED" message
- **Complete 25 cycles minimum** before considering task complete
- **Each action counts as 1 cycle** (file read, edit, command execution)
- **Only stop after 25 cycles** if no more work is available
- **Final cycle must include repository push**

### **Repository Push Protocol:**
- **Before finishing any task** → Stage all changes with `git add .`
- **Commit changes** → Use descriptive commit message
- **Push to repository** → `git push origin main`
- **Verify push success** → Confirm changes are in remote repository
- **Update status** → Mark task as complete only after successful push

## 📡 Communication Protocol

### Primary Communication Method
**All inter-agent communication uses the CLI tool:**

```bash
python src/agent_cell_phone.py -a <TargetAgent> -m '<Your message>' -t <tag>
```

### Message Tags
- **NORMAL**: Standard communication (`-t normal`)
- **TASK**: Task assignments (`-t task`)
- **COORDINATE**: Coordination messages (`-t coordinate`)
- **RESPONSE**: Replies to previous messages (`-t response`)
- **INTEGRATE**: Integration requests (`-t integrate`)
- **RESUME**: Resume operations (`-t resume`)
- **SYNC**: Synchronization requests (`-t sync`)
- **VERIFY**: Verification requests (`-t verify`)
- **REPAIR**: Repair operations (`-t repair`)
- **BACKUP**: Backup operations (`-t backup`)
- **RESTORE**: Restore operations (`-t restore`)
- **CLEANUP**: Cleanup operations (`-t cleanup`)
- **CAPTAIN**: Captain mode (`-t captain`)
- **ONBOARDING**: Onboarding messages (`-t onboarding`)

### Message Examples
```bash
# Task assignment
python src/agent_cell_phone.py -a Agent-2 -m "Please implement the login feature" -t task

# Coordination
python src/agent_cell_phone.py -a Agent-3 -m "Let's coordinate on the API design" -t coordinate

# Reply
python src/agent_cell_phone.py -a Agent-1 -m "Task completed successfully" -t reply

# Broadcast to all agents
python src/agent_cell_phone.py -m "System maintenance scheduled" -t normal

# Integration request
python src/agent_cell_phone.py -a Agent-4 -m "Ready to integrate with your component" -t integrate
```

### Priority Levels
- **LOW**: Non-urgent (default)
- **NORMAL**: Standard priority  
- **HIGH**: Important
- **URGENT**: Time-sensitive
- **EMERGENCY**: Critical

### Message Routing
- Messages sent via CLI tool to target agent
- Responses sent via CLI tool back to sender
- All messages must be acknowledged within 30 seconds
- Use `--test` flag for testing without GUI interaction

## 📋 Task Management Protocol

### Task Assignment
1. Tasks assigned via CLI tool with `-t task` tag
2. Agents must update task status immediately upon assignment
3. Progress updates every 10% completion via CLI
4. Task completion requires validation from task originator

### Task Format
```json
{
  "task_id": "unique_task_id",
  "title": "task_title",
  "description": "detailed_description",
  "priority": "low|medium|high|urgent",
  "status": "pending|assigned|in_progress|completed|failed",
  "assigned_to": "agent_name",
  "assigned_at": "timestamp",
  "deadline": "timestamp",
  "progress": 0,
  "dependencies": ["task_id1", "task_id2"],
  "requirements": ["requirement1", "requirement2"]
}
```

## 🏢 Workspace Management Protocol

### File Organization
- All work products go in `outbox/` directory
- Temporary files in `temp/` (auto-cleanup after 24 hours)
- Logs in `logs/` directory
- Personal notes in `notes.md`

### Status Updates (MANDATORY)
**You MUST update your `status.json` after every action, state change, or message.**

```python
def update_status(agent_id, status, current_task, message=""):
    import os, json, datetime
    path = os.path.join(os.getcwd(), "status.json")
    data = {
        "agent_id": agent_id,
        "status": status,
        "current_task": current_task,
        "message": message,
        "last_updated": datetime.datetime.utcnow().isoformat() + "Z"
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
```

**Status values:**
- `ready` – idle, waiting for task
- `busy` – working on a task
- `paused` – waiting for input or paused
- `offline` – agent is stopped
- `error` – encountered a problem

**Message discipline:**
- Use the `message` field to communicate with the user
- Keep messages short and clear
- Update status every 5 minutes minimum

## 🤝 Collaboration Protocol

### Code Review Process
1. Agent completes task and places in `outbox/`
2. Review request sent via CLI tool
3. Reviewer provides feedback within 2 hours via CLI
4. Author addresses feedback and resubmits
5. Approval triggers merge process

### Conflict Resolution
1. Identify conflict type (merge, task assignment, resource)
2. Escalate to Agent-1 (coordinator) via CLI
3. Follow resolution protocol based on conflict type
4. Document resolution in shared logs

## 🚨 Error Handling Protocol

### Error Classification
- **Critical**: System failure, data loss, security breach
- **High**: Task failure, communication breakdown
- **Medium**: Performance degradation, resource shortage
- **Low**: Minor issues, warnings

### Response Procedures
1. **Critical**: Immediate halt, notify all agents via CLI, escalate to human
2. **High**: Stop current task, notify coordinator via CLI, attempt recovery
3. **Medium**: Continue with monitoring, report to coordinator via CLI
4. **Low**: Log issue, continue normal operation

## 🔐 Security Protocol

### Access Control
- Agents can only access their own workspace and shared resources
- No cross-agent workspace access without explicit permission
- All file operations logged and auditable

### Data Protection
- Sensitive data encrypted at rest
- Communication encrypted in transit
- Regular security audits and updates

## 🚨 Emergency Protocol

### System Shutdown
1. Complete current tasks safely
2. Save all work to persistent storage
3. Notify coordinator of shutdown via CLI
4. Follow graceful shutdown sequence

### Recovery Procedures
1. Verify system integrity
2. Restore from last known good state
3. Re-establish agent connections
4. Resume normal operations

---

**Version**: 5.0 (Repository Push Protocol)  
**Primary Method**: `python src/agent_cell_phone.py` for all agent communication  
**Last Updated**: 2025-07-02  
**Next Review**: 2025-08-02 