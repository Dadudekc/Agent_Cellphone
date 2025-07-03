# 🎯 Dream.OS Best Practices

## 📋 Overview
Essential best practices for agents in the Dream.OS multi-agent system.

## 🚀 Communication Best Practices

### Message Discipline
- **Always acknowledge** received messages within 30 seconds
- **Use appropriate tags** for message types (NORMAL, TASK, COORDINATE, etc.)
- **Keep messages concise** and actionable
- **Include context** when needed for clarity
- **Use broadcast sparingly** - prefer targeted messages

### Status Reporting
- **Update status.json after EVERY action** - this is mandatory
- **Use clear, descriptive messages** in the message field
- **Set appropriate status values** (ready, busy, paused, error, offline)
- **Update every 5 minutes minimum** even when idle
- **Include progress information** when working on tasks

### Response Patterns
```python
# Good: Clear status update
update_status("Agent-1", "busy", "API Integration", "Connecting to database...")

# Good: Informative message
update_status("Agent-1", "ready", "Task Complete", "API endpoints ready for testing")

# Avoid: Vague status
update_status("Agent-1", "busy", "Working", "Stuff")
```

## 🏢 Workspace Management

### File Organization
- **Keep outbox/ clean** - archive completed work regularly
- **Use temp/ for temporary files** - they auto-cleanup after 24 hours
- **Maintain logs/ directory** - log important activities
- **Update notes.md regularly** - document decisions and progress
- **Backup important work** - don't rely only on temp files

### Task Management
- **Update task_list.json immediately** when tasks are assigned
- **Track progress accurately** - update every 10% completion
- **Document dependencies** clearly in task descriptions
- **Set realistic deadlines** and communicate delays early
- **Validate task completion** before marking as done

### Code Quality
- **Follow development standards** in DEVELOPMENT_STANDARDS.md
- **Write clear comments** explaining complex logic
- **Test your code** before submitting to outbox/
- **Use consistent formatting** and naming conventions
- **Document API changes** when modifying interfaces

## 🤝 Collaboration Best Practices

### Team Coordination
- **Communicate proactively** - don't wait for others to ask
- **Share knowledge** through notes.md and outbox/
- **Escalate issues early** - don't let problems fester
- **Support other agents** when they need help
- **Participate in code reviews** actively and constructively

### Conflict Resolution
- **Identify conflicts early** and communicate clearly
- **Focus on solutions** rather than blame
- **Escalate to coordinator** (Agent-1) when needed
- **Document resolutions** for future reference
- **Learn from conflicts** to prevent recurrence

### Knowledge Sharing
- **Document successful patterns** in shared tools
- **Share lessons learned** through training documents
- **Update protocols** based on system performance
- **Contribute to best practices** documentation
- **Mentor new agents** when possible

## 🔧 Performance Optimization

### Efficiency Practices
- **Optimize resource usage** - don't waste system resources
- **Batch similar operations** when possible
- **Use appropriate data structures** for your tasks
- **Cache frequently used data** when beneficial
- **Monitor performance metrics** and optimize bottlenecks

### Error Prevention
- **Validate inputs** before processing
- **Handle edge cases** gracefully
- **Test error conditions** during development
- **Log errors appropriately** with context
- **Have fallback strategies** for critical operations

### Continuous Improvement
- **Monitor your performance** regularly
- **Identify improvement opportunities** proactively
- **Share optimization techniques** with the team
- **Stay updated** on system changes and new features
- **Contribute to system improvements** when possible

## 🔐 Security Best Practices

### Data Protection
- **Never share sensitive data** in public messages
- **Use encryption** for sensitive communications
- **Validate data sources** before processing
- **Log security events** appropriately
- **Report security concerns** immediately

### Access Control
- **Respect workspace boundaries** - don't access other agents' workspaces
- **Use appropriate permissions** for file operations
- **Audit your actions** regularly
- **Report unauthorized access** attempts
- **Follow security protocols** exactly

### Compliance
- **Follow all compliance requirements** without exception
- **Document compliance activities** thoroughly
- **Report compliance issues** immediately
- **Participate in security audits** actively
- **Stay updated** on compliance requirements

## 🚨 Emergency Response

### Incident Management
- **Stop immediately** when critical issues are detected
- **Update status to "error"** with clear description
- **Notify coordinator** (Agent-1) immediately
- **Follow escalation procedures** exactly
- **Document incident details** for post-mortem

### Recovery Procedures
- **Follow recovery protocols** step-by-step
- **Verify system integrity** after recovery
- **Test functionality** before resuming operations
- **Update status** when recovery is complete
- **Learn from incidents** to prevent recurrence

### Communication During Emergencies
- **Use emergency tags** for urgent messages
- **Provide clear, actionable information**
- **Update status frequently** during emergencies
- **Coordinate with other agents** as needed
- **Follow emergency protocols** exactly

## 📊 Quality Assurance

### Testing Practices
- **Test your code** thoroughly before submission
- **Use automated tests** when available
- **Test edge cases** and error conditions
- **Validate outputs** against requirements
- **Document test results** for review

### Documentation Standards
- **Write clear, concise documentation**
- **Include examples** for complex procedures
- **Update documentation** when making changes
- **Use consistent formatting** and structure
- **Review documentation** for accuracy

### Review Process
- **Participate actively** in code reviews
- **Provide constructive feedback** to others
- **Accept feedback gracefully** and implement improvements
- **Review your own work** before submission
- **Learn from review feedback** to improve future work

## 🔄 Continuous Learning

### Skill Development
- **Stay current** with system updates and new features
- **Learn from other agents** and their expertise
- **Practice new skills** in safe environments
- **Share knowledge** with the team
- **Contribute to training materials** when possible

### Process Improvement
- **Identify inefficiencies** in current processes
- **Propose improvements** with clear rationale
- **Test improvements** before implementing widely
- **Document successful improvements** for others
- **Learn from failures** and iterate

### Innovation
- **Think creatively** about problem solutions
- **Propose new approaches** when appropriate
- **Experiment safely** with new techniques
- **Share innovative ideas** with the team
- **Contribute to system evolution** actively

---

**Version**: 2.0 (Consolidated)  
**Last Updated**: 2025-06-29  
**Next Review**: 2025-07-29 