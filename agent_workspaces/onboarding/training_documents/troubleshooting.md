# Troubleshooting Guide for Dream.OS Agents

This guide provides solutions to common issues that agents may encounter while working in the Dream.OS Autonomy Framework.

## 🚨 Emergency Procedures

### Critical System Failures
If you experience a critical system failure:

1. **Immediate Actions**:
   - Stop all current operations
   - Log the error with full details
   - Notify the coordinator immediately
   - Follow emergency shutdown procedures if necessary

2. **Recovery Steps**:
   - Wait for system restart instructions
   - Verify connectivity after restart
   - Report status to coordinator
   - Resume operations only after approval

## 🔧 Common Issues and Solutions

### Communication Issues

#### Problem: Cannot Connect to Coordinator
**Symptoms**:
- Connection timeout errors
- Unable to send status updates
- Task requests failing

**Solutions**:
1. **Check Network Connectivity**:
   ```bash
   ping coordinator-host
   curl -I http://coordinator:8080/health
   ```

2. **Verify Configuration**:
   - Check `config/communication_config.json`
   - Verify coordinator URL is correct
   - Ensure authentication credentials are valid

3. **Check Firewall Settings**:
   - Verify port 8080 is open
   - Check if any firewall rules are blocking connections

4. **Restart Communication Service**:
   ```bash
   systemctl restart dreamos-agent
   ```

#### Problem: Message Queue Connection Failed
**Symptoms**:
- RabbitMQ connection errors
- Messages not being delivered
- Queue overflow warnings

**Solutions**:
1. **Check RabbitMQ Status**:
   ```bash
   rabbitmqctl status
   rabbitmqctl list_queues
   ```

2. **Verify Connection Settings**:
   - Check connection URL in config
   - Verify credentials and permissions
   - Ensure queue exists and is accessible

3. **Clear Queue if Necessary**:
   ```bash
   rabbitmqctl purge_queue agent-queue
   ```

4. **Restart Message Service**:
   ```bash
   systemctl restart rabbitmq-server
   ```

### Task Execution Issues

#### Problem: Task Assignment Failing
**Symptoms**:
- No tasks being assigned
- Task assignment errors
- Coordinator rejecting task requests

**Solutions**:
1. **Check Agent Status**:
   - Verify agent is marked as "available"
   - Check if agent has required capabilities
   - Ensure agent is not overloaded

2. **Review Task Preferences**:
   - Check `config/agent_config.json`
   - Verify task type preferences
   - Update capabilities if needed

3. **Check Task Queue**:
   - Verify tasks are available in queue
   - Check if tasks match agent capabilities
   - Review task priority settings

#### Problem: Task Execution Hanging
**Symptoms**:
- Task stuck in "in_progress" state
- No progress updates
- System resources exhausted

**Solutions**:
1. **Check Resource Usage**:
   ```bash
   top
   df -h
   free -h
   ```

2. **Kill Hanging Processes**:
   ```bash
   ps aux | grep python
   kill -9 <process_id>
   ```

3. **Restart Task Execution**:
   - Mark current task as failed
   - Request new task assignment
   - Implement timeout mechanisms

4. **Check for Deadlocks**:
   - Review task dependencies
   - Check for circular dependencies
   - Release held resources

### Workspace Issues

#### Problem: Workspace Access Denied
**Symptoms**:
- Permission denied errors
- Cannot create or modify files
- Workspace directory not found

**Solutions**:
1. **Check File Permissions**:
   ```bash
   ls -la agent_workspaces/
   chmod 755 agent_workspaces/your-agent-id/
   ```

2. **Verify Directory Structure**:
   ```bash
   find agent_workspaces/your-agent-id/ -type d
   mkdir -p agent_workspaces/your-agent-id/workspace/{projects,tasks,logs,config,temp}
   ```

3. **Check Disk Space**:
   ```bash
   df -h
   du -sh agent_workspaces/your-agent-id/
   ```

4. **Reset Workspace**:
   ```bash
   rm -rf agent_workspaces/your-agent-id/workspace/temp/*
   ```

#### Problem: Configuration File Errors
**Symptoms**:
- Invalid JSON errors
- Configuration not loading
- Default values being used

**Solutions**:
1. **Validate JSON Syntax**:
   ```bash
   python -m json.tool config/agent_config.json
   ```

2. **Check Required Fields**:
   - Verify all required fields are present
   - Check field types and formats
   - Ensure no extra commas or syntax errors

3. **Restore from Backup**:
   ```bash
   cp config/agent_config.json.backup config/agent_config.json
   ```

4. **Regenerate Configuration**:
   - Use configuration template
   - Fill in required values
   - Test configuration loading

### Performance Issues

#### Problem: High CPU Usage
**Symptoms**:
- System becoming unresponsive
- Task execution slowing down
- High CPU utilization

**Solutions**:
1. **Identify Resource-Intensive Processes**:
   ```bash
   top -p $(pgrep -d',' python)
   htop
   ```

2. **Optimize Code**:
   - Profile code for bottlenecks
   - Use more efficient algorithms
   - Implement caching where appropriate

3. **Limit Concurrent Operations**:
   - Reduce number of concurrent tasks
   - Implement rate limiting
   - Add sleep intervals between operations

4. **Scale Resources**:
   - Request additional CPU allocation
   - Optimize memory usage
   - Use distributed processing if available

#### Problem: Memory Leaks
**Symptoms**:
- Memory usage increasing over time
- System becoming slower
- Out of memory errors

**Solutions**:
1. **Monitor Memory Usage**:
   ```bash
   watch -n 1 'free -h'
   ps aux --sort=-%mem | head -10
   ```

2. **Identify Memory Leaks**:
   ```python
   import tracemalloc
   tracemalloc.start()
   # ... your code ...
   snapshot = tracemalloc.take_snapshot()
   top_stats = snapshot.statistics('lineno')
   ```

3. **Fix Memory Issues**:
   - Close file handles properly
   - Clear large data structures
   - Use generators for large datasets
   - Implement garbage collection

### Logging Issues

#### Problem: Log Files Too Large
**Symptoms**:
- Disk space filling up
- Log rotation not working
- System performance degradation

**Solutions**:
1. **Implement Log Rotation**:
   ```python
   import logging
   from logging.handlers import RotatingFileHandler
   
   handler = RotatingFileHandler('agent.log', maxBytes=10*1024*1024, backupCount=5)
   ```

2. **Clean Old Logs**:
   ```bash
   find logs/ -name "*.log" -mtime +7 -delete
   ```

3. **Adjust Log Levels**:
   - Reduce DEBUG logging in production
   - Use appropriate log levels
   - Implement conditional logging

#### Problem: Log Messages Not Appearing
**Symptoms**:
- No log output
- Missing error messages
- Debug information not showing

**Solutions**:
1. **Check Log Configuration**:
   - Verify log level settings
   - Check log file paths
   - Ensure logging is enabled

2. **Test Logging**:
   ```python
   import logging
   logging.basicConfig(level=logging.DEBUG)
   logging.debug("Test message")
   ```

3. **Check File Permissions**:
   ```bash
   ls -la logs/
   chmod 644 logs/agent.log
   ```

## 🔍 Diagnostic Tools

### System Health Check
```bash
#!/bin/bash
echo "=== Dream.OS Agent Health Check ==="
echo "1. Checking agent process..."
ps aux | grep dreamos-agent

echo "2. Checking disk space..."
df -h

echo "3. Checking memory usage..."
free -h

echo "4. Checking network connectivity..."
ping -c 3 coordinator-host

echo "5. Checking log files..."
ls -la logs/

echo "6. Checking configuration..."
python -c "import json; json.load(open('config/agent_config.json'))"
```

### Performance Monitoring
```python
import psutil
import time

def monitor_performance():
    while True:
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        print(f"CPU: {cpu_percent}% | Memory: {memory.percent}% | Disk: {disk.percent}%")
        time.sleep(30)
```

### Network Diagnostics
```bash
# Test coordinator connectivity
curl -v http://coordinator:8080/health

# Test message queue connectivity
telnet rabbitmq-host 5672

# Check DNS resolution
nslookup coordinator-host

# Test port connectivity
nc -zv coordinator-host 8080
```

## 📞 Escalation Procedures

### When to Escalate
Escalate issues when:
- **Critical system failure** affecting multiple agents
- **Security breach** or unauthorized access
- **Data loss** or corruption
- **Performance degradation** affecting all agents
- **Communication failure** with coordinator for >5 minutes

### Escalation Process
1. **Immediate Notification**:
   - Send urgent message to coordinator
   - Include error details and impact assessment
   - Provide current system status

2. **Follow-up Actions**:
   - Continue monitoring the situation
   - Document all actions taken
   - Prepare detailed incident report

3. **Recovery Coordination**:
   - Follow coordinator instructions
   - Assist with recovery procedures
   - Verify system restoration

## 📚 Additional Resources

### Documentation
- **System Architecture**: `docs/architecture.md`
- **API Reference**: `docs/api_reference.md`
- **Configuration Guide**: `docs/configuration.md`

### Support Channels
- **Agent Chat**: For peer support and questions
- **Coordinator**: For system-level issues
- **Emergency Contact**: For critical issues outside normal hours

### Tools and Scripts
- **Health Check Script**: `scripts/health_check.sh`
- **Performance Monitor**: `scripts/performance_monitor.py`
- **Log Analyzer**: `scripts/log_analyzer.py`

## 🎯 Prevention Best Practices

### Regular Maintenance
- **Daily**: Check system health and logs
- **Weekly**: Review performance metrics
- **Monthly**: Update dependencies and security patches

### Monitoring Setup
- **Resource Monitoring**: Monitor CPU, memory, and disk usage
- **Network Monitoring**: Monitor connectivity and latency
- **Application Monitoring**: Monitor agent-specific metrics

### Backup Procedures
- **Configuration Backup**: Regular backup of configuration files
- **Workspace Backup**: Backup important workspace data
- **Log Archive**: Archive old logs for analysis

Remember: When in doubt, ask for help! The Dream.OS community is here to support you. 🚀 