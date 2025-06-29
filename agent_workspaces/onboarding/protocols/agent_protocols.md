# Dream.OS Agent Protocols

## Overview
This document defines the core protocols that all agents in the Dream.OS autonomous development system must follow.

## 1. Communication Protocol

### Message Format
All inter-agent communication must use the following JSON format:
```json
{
  "message_id": "unique_id",
  "from": "sender_agent",
  "to": "recipient_agent",
  "subject": "message_subject",
  "content": "message_content",
  "timestamp": "ISO_timestamp",
  "priority": "low|medium|high|urgent",
  "type": "task|request|response|notification",
  "metadata": {}
}
```

### Message Routing
- Messages are placed in recipient's `inbox/` directory
- Responses are placed in sender's `inbox/` directory
- All messages must be acknowledged within 30 seconds

## 2. Task Management Protocol

### Task Assignment
1. Tasks are assigned via `task_list.json` in each agent's workspace
2. Agents must update task status immediately upon assignment
3. Progress updates every 10% completion
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

## 3. Workspace Management Protocol

### File Organization
- All work products go in `outbox/` directory
- Temporary files in `temp/` (auto-cleanup after 24 hours)
- Logs in `logs/` directory
- Personal notes in `notes.md`

### Status Updates
- Agents must update `status.json` every 5 minutes
- Status includes: current task, availability, health metrics
- Emergency status changes require immediate notification

## 4. Collaboration Protocol

### Code Review Process
1. Agent completes task and places in `outbox/`
2. Review request sent to designated reviewer
3. Reviewer provides feedback within 2 hours
4. Author addresses feedback and resubmits
5. Approval triggers merge process

### Conflict Resolution
1. Identify conflict type (merge, task assignment, resource)
2. Escalate to Agent-1 (coordinator) if needed
3. Follow resolution protocol based on conflict type
4. Document resolution in shared logs

## 5. Error Handling Protocol

### Error Classification
- **Critical**: System failure, data loss, security breach
- **High**: Task failure, communication breakdown
- **Medium**: Performance degradation, resource shortage
- **Low**: Minor issues, warnings

### Response Procedures
1. **Critical**: Immediate halt, notify all agents, escalate to human
2. **High**: Stop current task, notify coordinator, attempt recovery
3. **Medium**: Continue with monitoring, report to coordinator
4. **Low**: Log issue, continue normal operation

## 6. Security Protocol

### Access Control
- Agents can only access their own workspace and shared resources
- No cross-agent workspace access without explicit permission
- All file operations logged and auditable

### Data Protection
- Sensitive data encrypted at rest
- Communication encrypted in transit
- Regular security audits and updates

## 7. Performance Protocol

### Metrics Tracking
- Task completion rate
- Response time to messages
- Resource utilization
- Error frequency
- Collaboration effectiveness

### Optimization
- Agents must optimize their performance continuously
- Share best practices through shared tools
- Report performance issues to coordinator

## 8. Learning Protocol

### Knowledge Sharing
- Document successful patterns in shared tools
- Share lessons learned through training documents
- Update protocols based on system performance

### Continuous Improvement
- Regular protocol reviews and updates
- Performance analysis and optimization
- Adaptation to new requirements and challenges

## 9. Emergency Protocol

### System Shutdown
1. Complete current tasks safely
2. Save all work to persistent storage
3. Notify coordinator of shutdown
4. Follow graceful shutdown sequence

### Recovery Procedures
1. Verify system integrity
2. Restore from last known good state
3. Re-establish agent connections
4. Resume normal operations

## 10. Compliance Protocol

### Documentation Requirements
- All tasks must be documented
- Code changes require comments
- Decisions must be logged with rationale
- Audit trail maintained for all operations

### Quality Standards
- Code must pass automated tests
- Documentation must be complete and accurate
- Performance must meet defined SLAs
- Security requirements must be satisfied

---

**Version**: 1.0  
**Last Updated**: 2025-06-29  
**Next Review**: 2025-07-29 