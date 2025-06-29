# 📁 Dream.OS Cell Phone Configuration

This directory contains all configuration files for the Dream.OS Cell Phone multi-agent system, organized by category for better maintainability and clarity.

## 📂 Directory Structure

```
config/
├── agents/           # Agent-specific configurations
│   ├── agent_coordinates.json    # Screen coordinates for each agent
│   └── agent_roles.json          # Role assignments and capabilities
├── system/           # System-wide configurations
│   └── system_config.json        # General system settings
├── templates/        # Template configurations
│   ├── agent_modes.json          # Agent operation modes
│   └── message_templates.json    # Communication message templates
└── README.md         # This file
```

## 🔧 Configuration Files

### Agents Configuration (`agents/`)

#### `agent_coordinates.json`
- **Purpose**: Defines screen coordinates for each agent's input box
- **Layouts**: Supports 2-agent, 4-agent, and 8-agent layouts
- **Usage**: Used by PyAutoGUI for automated agent communication

#### `agent_roles.json`
- **Purpose**: Defines role assignments and capabilities for each agent
- **Structure**: Primary, secondary, and backup roles for each agent
- **Capabilities**: Lists specific skills and abilities for each agent

### System Configuration (`system/`)

#### `system_config.json`
- **Purpose**: General system settings and parameters
- **Includes**: Communication settings, logging configuration, performance limits
- **Usage**: System-wide configuration that affects all agents

### Templates Configuration (`templates/`)

#### `agent_modes.json`
- **Purpose**: Defines different operation modes for agents
- **Modes**: Resume, cleanup, captain, task, integrate
- **Usage**: Standardized prompts for different agent operations

#### `message_templates.json`
- **Purpose**: Standardized message formats for communication
- **Templates**: Status requests, task assignments, pings, broadcasts, etc.
- **Priorities**: Defines message priority levels

## 🚀 Usage

### Loading Configurations
```python
import json

# Load agent coordinates
with open('config/agents/agent_coordinates.json', 'r') as f:
    coordinates = json.load(f)

# Load system configuration
with open('config/system/system_config.json', 'r') as f:
    system_config = json.load(f)

# Load message templates
with open('config/templates/message_templates.json', 'r') as f:
    templates = json.load(f)
```

### Updating Configurations
1. **Agent Coordinates**: Update when screen layout changes
2. **Agent Roles**: Modify when role assignments change
3. **System Config**: Update for system-wide changes
4. **Templates**: Modify for new communication patterns

## 🔄 Migration from Runtime Directory

The configuration files were previously located in `runtime/config/` and have been reorganized for better structure:

- `runtime/config/cursor_agent_coords.json` → `config/agents/agent_coordinates.json`
- `runtime/config/templates/agent_modes.json` → `config/templates/agent_modes.json`

## 📝 Best Practices

1. **Backup Configurations**: Always backup before making changes
2. **Version Control**: Keep configurations in version control
3. **Validation**: Validate JSON syntax before deployment
4. **Documentation**: Update this README when adding new configurations
5. **Testing**: Test configuration changes in development environment first

## 🔍 Troubleshooting

### Common Issues
- **Invalid JSON**: Use a JSON validator to check syntax
- **Missing Files**: Ensure all required configuration files exist
- **Permission Errors**: Check file permissions for read/write access
- **Path Issues**: Verify file paths in your code match the new structure

### Validation Commands
```bash
# Validate JSON syntax
python -m json.tool config/agents/agent_coordinates.json

# Check file permissions
ls -la config/

# Test configuration loading
python -c "import json; json.load(open('config/system/system_config.json'))"
```

---

**Last Updated**: 2025-06-29  
**Version**: 2.0.0  
**Maintainer**: Dream.OS Cell Phone Development Team 