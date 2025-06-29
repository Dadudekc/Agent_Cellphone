# 🎮 Command Reference - Dream.OS Agents

## Overview

This document provides a comprehensive reference for all available commands in the Dream.OS Autonomous Framework. Each command includes usage examples, parameters, and expected responses.

## 🔧 System Commands

### Basic Operations

#### `ping`
**Purpose**: Test connectivity between agents

**Format**: `@<recipient> ping`

**Examples**:
```
@agent-2 ping
@all ping
```

**Response**: `pong` with timestamp

**Usage**: Test if target agent is responsive

---

#### `status`
**Purpose**: Get current status of an agent

**Format**: `@<recipient> status [detailed]`

**Examples**:
```
@agent-1 status
@agent-2 status detailed
@all status
```

**Response**: Current status including:
- Current task/project
- Progress percentage
- Estimated completion time
- Any issues or blockers

---

#### `resume`
**Purpose**: Resume operations after interruption

**Format**: `@<recipient> resume [task_name]`

**Examples**:
```
@agent-2 resume
@agent-3 resume api_development
@all resume
```

**Response**: Confirmation of resumed operations

---

#### `restart`
**Purpose**: Restart agent or specific service

**Format**: `@<recipient> restart [service_name]`

**Examples**:
```
@agent-1 restart
@agent-2 restart database_service
@all restart
```

**Response**: Confirmation of restart and status

---

#### `sync`
**Purpose**: Synchronize data or state with other agents

**Format**: `@<recipient> sync <data_type> [source]`

**Examples**:
```
@agent-2 sync data
@agent-3 sync config agent-1
@all sync state
```

**Response**: Sync status and any conflicts resolved

---

#### `verify`
**Purpose**: Verify data integrity or system state

**Format**: `@<recipient> verify <target> [options]`

**Examples**:
```
@agent-1 verify coordinates
@agent-2 verify database_integrity
@agent-3 verify config_files
```

**Response**: Verification results and any issues found

## 🛠️ Task Management Commands

### Task Operations

#### `task`
**Purpose**: Assign or manage tasks

**Format**: `@<recipient> task <action> <task_details>`

**Actions**:
- `assign` - Assign new task
- `status` - Get task status
- `update` - Update task progress
- `complete` - Mark task complete
- `cancel` - Cancel task

**Examples**:
```
@agent-2 task assign "Build API endpoint for user authentication"
@agent-3 task status
@agent-1 task update "75% complete, testing phase"
@agent-2 task complete "API endpoint successfully deployed"
```

**Response**: Task operation confirmation and details

---

#### `captain`
**Purpose**: Leadership and coordination commands

**Format**: `@<recipient> captain <command> [parameters]`

**Commands**:
- `report` - Request status reports
- `coordinate` - Coordinate activities
- `delegate` - Delegate responsibilities
- `review` - Review progress

**Examples**:
```
@all captain report
@agent-2 captain coordinate database_migration
@agent-3 captain delegate testing_to agent-4
@all captain review sprint_progress
```

**Response**: Leadership command acknowledgment and results

---

#### `integrate`
**Purpose**: System integration commands

**Format**: `@<recipient> integrate <system> <action>`

**Examples**:
```
@agent-2 integrate database connect
@agent-3 integrate api deploy
@agent-1 integrate monitoring setup
```

**Response**: Integration status and results

## 🔧 Maintenance Commands

### System Maintenance

#### `repair`
**Purpose**: Fix issues or errors

**Format**: `@<recipient> repair <issue_type> [details]`

**Examples**:
```
@agent-2 repair connection_timeout
@agent-3 repair database_error "Connection refused"
@agent-1 repair file_corruption "config.json"
```

**Response**: Repair status and resolution details

---

#### `backup`
**Purpose**: Create system backups

**Format**: `@<recipient> backup <target> [options]`

**Examples**:
```
@agent-1 backup database
@agent-2 backup config_files
@agent-3 backup logs --compress
```

**Response**: Backup status and location

---

#### `restore`
**Purpose**: Restore from backup

**Format**: `@<recipient> restore <backup_id> [target]`

**Examples**:
```
@agent-1 restore backup_20250629 database
@agent-2 restore config_backup
@agent-3 restore logs_backup --verify
```

**Response**: Restore status and verification results

---

#### `cleanup`
**Purpose**: Clean up temporary files or old data

**Format**: `@<recipient> cleanup <target> [options]`

**Examples**:
```
@agent-1 cleanup temp_files
@agent-2 cleanup old_logs --older-than 30d
@agent-3 cleanup cache --force
```

**Response**: Cleanup results and space freed

## 📊 Data Commands

### Data Operations

#### `data`
**Purpose**: Transfer or process data

**Format**: `@<recipient> data <action> <data_type> [content]`

**Actions**:
- `send` - Send data to agent
- `receive` - Receive data from agent
- `process` - Process data
- `validate` - Validate data format

**Examples**:
```
@agent-2 data send config {"api_key": "abc123"}
@agent-3 data receive logs
@agent-1 data process user_data
@agent-2 data validate schema database_schema.json
```

**Response**: Data operation status and results

---

#### `query`
**Purpose**: Query information or data

**Format**: `@<recipient> query <query_type> [parameters]`

**Examples**:
```
@agent-2 query api_response_time
@agent-3 query database_size
@agent-1 query error_count --last-24h
@agent-2 query user_activity --date 2025-06-29
```

**Response**: Query results and data

## 🔐 Security Commands

### Security Operations

#### `auth`
**Purpose**: Authentication and authorization

**Format**: `@<recipient> auth <action> [credentials]`

**Examples**:
```
@agent-1 auth verify token
@agent-2 auth login username password
@agent-3 auth logout
@agent-1 auth refresh_token
```

**Response**: Authentication status and token information

---

#### `secure`
**Purpose**: Security-related operations

**Format**: `@<recipient> secure <action> [target]`

**Examples**:
```
@agent-1 secure encrypt file.txt
@agent-2 secure decrypt message.enc
@agent-3 secure hash password
@agent-1 secure verify_signature file.sig
```

**Response**: Security operation results

## 📈 Monitoring Commands

### System Monitoring

#### `monitor`
**Purpose**: Monitor system performance

**Format**: `@<recipient> monitor <metric> [duration]`

**Examples**:
```
@agent-1 monitor cpu_usage
@agent-2 monitor memory_usage --last-hour
@agent-3 monitor network_traffic
@agent-1 monitor disk_space
```

**Response**: Monitoring data and metrics

---

#### `alert`
**Purpose**: Set up or manage alerts

**Format**: `@<recipient> alert <action> [conditions]`

**Examples**:
```
@agent-1 alert set cpu_usage > 80%
@agent-2 alert list
@agent-3 alert remove alert_id_123
@agent-1 alert test
```

**Response**: Alert configuration status

## 🔄 Workflow Commands

### Process Management

#### `workflow`
**Purpose**: Manage workflows and processes

**Format**: `@<recipient> workflow <action> <workflow_name>`

**Examples**:
```
@agent-1 workflow start deployment_pipeline
@agent-2 workflow pause testing_workflow
@agent-3 workflow resume data_processing
@agent-1 workflow status all
```

**Response**: Workflow status and progress

---

#### `pipeline`
**Purpose**: Manage data pipelines

**Format**: `@<recipient> pipeline <action> <pipeline_name>`

**Examples**:
```
@agent-1 pipeline start etl_process
@agent-2 pipeline stop data_ingestion
@agent-3 pipeline status
@agent-1 pipeline logs --last-100
```

**Response**: Pipeline status and logs

## 🎯 Custom Commands

### Extending the System

#### `custom`
**Purpose**: Execute custom commands

**Format**: `@<recipient> custom <command_name> [parameters]`

**Examples**:
```
@agent-2 custom deploy_application production
@agent-3 custom run_tests unit_tests
@agent-1 custom generate_report monthly
@agent-2 custom backup_database --incremental
```

**Response**: Custom command execution results

## 📋 Command Categories

### Priority Levels

#### High Priority (Emergency)
- `repair` - Fix critical issues
- `restart` - Restart failed services
- `backup` - Create emergency backups
- `alert` - Critical system alerts

#### Medium Priority (Operational)
- `status` - System status checks
- `sync` - Data synchronization
- `verify` - System verification
- `monitor` - Performance monitoring

#### Low Priority (Maintenance)
- `cleanup` - Routine cleanup
- `workflow` - Process management
- `pipeline` - Data pipeline management
- `custom` - Custom operations

## 🔄 Response Patterns

### Standard Responses

#### Success Response
```
✅ Command executed successfully
Details: [specific details]
Timestamp: 2025-06-29 12:34:56
```

#### Error Response
```
❌ Command failed
Error: [error description]
Code: [error code]
Timestamp: 2025-06-29 12:34:56
```

#### Progress Response
```
🔄 Command in progress
Progress: 75% complete
ETA: 5 minutes
Status: [current status]
```

## 📊 Command Analytics

### Usage Tracking
- **Command Frequency**: Most used commands
- **Success Rates**: Command success percentages
- **Response Times**: Time to execute commands
- **Error Patterns**: Common command failures

### Performance Metrics
- **Throughput**: Commands per minute
- **Latency**: Command execution time
- **Reliability**: Command success rate
- **Efficiency**: Resource usage per command

## 🚨 Emergency Commands

### Critical Situations

#### System Failure
```
@all repair system_failure
@all backup critical_data
@all restart essential_services
```

#### Security Breach
```
@all secure lockdown
@all auth revoke_all_tokens
@all alert security_incident
```

#### Data Loss
```
@all backup immediate
@all restore latest_backup
@all verify data_integrity
```

## 📚 Best Practices

### Command Usage
- **Use Specific Commands**: Choose the most specific command for your needs
- **Include Parameters**: Provide necessary parameters for clarity
- **Check Responses**: Always verify command responses
- **Log Commands**: Keep records of executed commands

### Error Handling
- **Validate Input**: Check parameters before execution
- **Handle Errors**: Provide meaningful error messages
- **Retry Logic**: Implement retry for failed commands
- **Fallback Plans**: Have backup procedures for critical commands

### Security
- **Authenticate**: Verify permissions before execution
- **Validate**: Check command parameters for security
- **Log**: Record all command executions
- **Monitor**: Watch for suspicious command patterns

---

**Command Reference Version**: 1.0  
**Last Updated**: 2025-06-29  
**Status**: ✅ Active 