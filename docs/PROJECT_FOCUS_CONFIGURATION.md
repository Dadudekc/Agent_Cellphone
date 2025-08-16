# Dynamic Project Focus Configuration

## Overview

The **Dynamic Project Focus Configuration** system eliminates hardcoded project assignments in your agent system, making it easy for users to customize which projects their agents work on without modifying code or restarting the system.

## 🚀 Key Benefits

- **No More Hardcoding**: Eliminate hardcoded project names scattered throughout the codebase
- **User-Friendly**: Simple JSON configuration and command-line tools
- **Real-time Changes**: Modify project focus without restarting agents
- **Scalable**: Easily add/remove projects and reassign agents
- **Fallback Support**: Gracefully falls back to hardcoded config if needed

## 📁 File Structure

```
config/agents/
├── project_focus.json          # Main configuration file
├── agent_roles.json           # Agent role definitions
└── agent_coordinates.json     # Agent positioning data

src/core/
└── project_focus_manager.py   # Core management class

scripts/
└── manage_project_focus.py    # User-friendly CLI tool
```

## 🔧 Configuration File

The main configuration is stored in `config/agents/project_focus.json`:

```json
{
  "project_focus_config": {
    "description": "Configure which projects your agents should focus on",
    "version": "1.0",
    "available_projects": [
      {
        "name": "FreeRideInvestor",
        "category": "trading",
        "priority": 1,
        "description": "Trading platform and investment tools",
        "repository_path": "Dadudekc/FreeRideInvestor",
        "active": true
      }
    ],
    "agent_project_assignments": {
      "Agent-1": {
        "primary_projects": ["FreeRideInvestor"],
        "secondary_projects": [],
        "max_projects": 3,
        "focus_area": "system_coordination"
      }
    }
  }
}
```

## 🛠️ Command-Line Interface

Use the `manage_project_focus.py` script for easy configuration management:

### List Current Configuration
```bash
python scripts/manage_project_focus.py list
```

### Add New Project
```bash
python scripts/manage_project_focus.py add-project "MyNewProject" "web_development" 2 "A new web project" "repos/myproject"
```

### Assign Project to Agent
```bash
python scripts/manage_project_focus.py assign "MyNewProject" "Agent-1" --primary
```

### Show Agent Workload
```bash
python scripts/manage_project_focus.py agent-workload --agent "Agent-1"
```

### System Overview
```bash
python scripts/manage_project_focus.py system-overview
```

## 🔄 Migration from Hardcoded System

### Before (Hardcoded)
```python
# OLD: Hardcoded in repository_activity_monitor.py
self.agent_repos = {
    "Agent-1": ["AI_Debugger_Assistant", "DigitalDreamscape", "FreeRideInvestor"],
    "Agent-2": ["Auto_Blogger", "Dream.os", "FreeWork"],
    # ... more hardcoded assignments
}
```

### After (Dynamic)
```python
# NEW: Dynamic configuration via ProjectFocusManager
from src.core.project_focus_manager import ProjectFocusManager

manager = ProjectFocusManager()
agent_projects = manager.get_agent_projects("Agent-1")
# Returns: ["FreeRideInvestor", "autonomous_platform"]
```

## 📊 Project Categories

Organize projects by category for better management:

- **trading**: Trading and investment projects
- **web_development**: Website and web applications
- **ai_automation**: AI and automation tools
- **platform_development**: Core platform infrastructure
- **general**: Miscellaneous projects

## 🎯 Priority System

Projects have priority levels (1 = highest, 5 = lowest):

1. **Priority 1**: Critical projects requiring immediate attention
2. **Priority 2**: High-priority projects
3. **Priority 3**: Medium-priority projects
4. **Priority 4**: Lower-priority projects
5. **Priority 5**: Background/experimental projects

## 👥 Agent Assignment Types

### Primary Projects
- Agents focus most of their time on these
- Limited by `max_projects` setting
- Higher priority for resource allocation

### Secondary Projects
- Agents work on these when primary projects are stable
- Can be reassigned dynamically
- Good for skill development and backup

## 🔍 Monitoring and Analytics

### Agent Workload
```python
workload = manager.get_agent_workload("Agent-1")
print(f"Utilization: {workload['utilization_percent']:.1f}%")
print(f"Current Load: {workload['current_load']}/{workload['max_capacity']}")
```

### System Overview
```python
overview = manager.get_system_overview()
print(f"Total Projects: {overview['total_projects']}")
print(f"Active Projects: {overview['active_projects']}")
```

## 🚨 Error Handling and Fallbacks

The system gracefully handles errors:

1. **Configuration File Missing**: Creates default configuration
2. **Import Errors**: Falls back to hardcoded assignments
3. **Invalid Data**: Logs errors and uses safe defaults
4. **File Corruption**: Restores from backup or creates new config

## 📝 Best Practices

### 1. Project Naming
- Use descriptive, unique names
- Avoid special characters and spaces
- Follow consistent naming conventions

### 2. Priority Management
- Don't assign too many Priority 1 projects
- Balance workload across agents
- Review priorities regularly

### 3. Agent Capacity
- Monitor `max_projects` settings
- Avoid overloading agents
- Consider skill matches when assigning

### 4. Regular Maintenance
- Review project assignments monthly
- Archive completed projects
- Update project descriptions and categories

## 🔧 Advanced Configuration

### Dynamic Reassignment Rules
```json
"dynamic_assignment_rules": {
  "enable_auto_reassignment": true,
  "reassignment_triggers": [
    "project_completion",
    "agent_overload",
    "priority_change",
    "skill_match"
  ]
}
```

### Skill Requirements
```json
"skill_requirements": {
  "FreeRideInvestor": ["trading", "php", "financial_analysis"],
  "osrsAIagent": ["ai_automation", "python", "game_automation"]
}
```

## 🧪 Testing Your Configuration

### 1. Validate Configuration
```bash
python scripts/manage_project_focus.py list
```

### 2. Test Agent Assignment
```bash
python scripts/manage_project_focus.py assign "TestProject" "Agent-1" --primary
```

### 3. Verify Changes
```bash
python scripts/manage_project_focus.py agent-workload --agent "Agent-1"
```

### 4. Export for Backup
```bash
python scripts/manage_project_focus.py export "backup_config_$(date +%Y%m%d).json"
```

## 🆘 Troubleshooting

### Common Issues

1. **Configuration Not Loading**
   - Check file permissions
   - Verify JSON syntax
   - Check file path in ProjectFocusManager

2. **Agent Not Getting Projects**
   - Verify agent ID spelling
   - Check project assignment
   - Ensure project is active

3. **Import Errors**
   - Check Python path
   - Verify module structure
   - Check for circular imports

### Debug Mode
```python
import logging
logging.basicConfig(level=logging.DEBUG)

manager = ProjectFocusManager()
# Will show detailed loading and parsing information
```

## 🔮 Future Enhancements

- **Web Interface**: GUI for configuration management
- **Auto-discovery**: Automatically detect new repositories
- **Performance Metrics**: Track project completion rates
- **Integration**: Connect with project management tools
- **Notifications**: Alert when agents are overloaded

## 📚 Related Documentation

- [Agent Roles Configuration](agent_roles.md)
- [FSM Configuration](fsm_configuration.md)
- [Repository Management](repository_management.md)
- [Agent Coordination](agent_coordination.md)

## 🤝 Contributing

To improve this system:

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Update documentation
5. Submit a pull request

## 📞 Support

For questions or issues:

1. Check the troubleshooting section
2. Review the logs for error details
3. Create an issue with configuration details
4. Include error messages and stack traces

---

**Remember**: This system is designed to make your agent configuration flexible and user-friendly. Start with a few projects and gradually expand as you become comfortable with the system!
