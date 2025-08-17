# 🔧 Configurable Paths System

## Overview

The Agent Cellphone system now features a **fully configurable path system** that eliminates hardcoded directories. Users can easily customize where agents focus their work by simply setting environment variables or using the configuration script.

## 🎯 Why This Matters

**Before**: Hardcoded `D:\repos` paths throughout the system made it difficult for users to:
- Focus agents on different projects
- Use different drive letters
- Work with different organizational structures
- Scale the system across different environments

**After**: **Zero hardcoded paths** - everything is configurable through:
- Environment variables
- `.env` file configuration
- Simple command-line configuration script

## 🚀 Quick Start

### 1. Show Current Configuration
```bash
python configure_project_focus.py --show
```

### 2. Change Project Focus
```bash
# Focus on personal projects
python configure_project_focus.py --repos-root "C:/my-projects" --owner "MyName"

# Focus on company projects
python configure_project_focus.py --repos-root "D:/company-projects" --owner "CompanyName"

# Focus on a different drive
python configure_project_focus.py --repos-root "E:/development" --owner "DevTeam"
```

### 3. Make Changes Permanent
Add to your `.env` file:
```bash
REPOS_ROOT=C:/my-projects
DEFAULT_OWNER=MyName
```

## 🔧 Configuration Options

### Core Environment Variables

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `REPOS_ROOT` | Main repository root | `D:/repos` | `C:/projects` |
| `DEFAULT_OWNER` | Organization/owner name | `Dadudekc` | `MyCompany` |
| `COMMUNICATIONS_ROOT` | Communications directory | `{REPOS_ROOT}/communications` | `C:/my-comms` |
| `AGENT_WORKSPACES_ROOT` | Agent workspaces directory | `{REPOS_ROOT}/{OWNER}` | `C:/my-workspaces` |

### Legacy Compatibility

| Variable | Description | Purpose |
|----------|-------------|---------|
| `REPO_DEST` | Clone destination | Backward compatibility |
| `AGENT_FILE_ROOT` | Agent file root | Legacy scripts |

## 📁 Path Structure

The system automatically builds a logical directory structure:

```
{REPOS_ROOT}/
├── {DEFAULT_OWNER}/           # Agent workspaces
│   ├── Agent-1/
│   ├── Agent-2/
│   ├── Agent-3/
│   ├── Agent-4/
│   └── Agent-5/
├── communications/             # Communications
│   ├── overnight_YYYYMMDD_/
│   └── _signals/
└── github_config.json         # GitHub configuration
```

## 🎨 Usage Examples

### Personal Development
```bash
# Focus on your personal GitHub projects
python configure_project_focus.py --repos-root "C:/github" --owner "MyUsername"

# Result: Agents work in C:/github/MyUsername/
```

### Company Projects
```bash
# Focus on company development
python configure_project_focus.py --repos-root "D:/company" --owner "CompanyName"

# Result: Agents work in D:/company/CompanyName/
```

### Custom Communications
```bash
# Use a separate drive for communications
python configure_project_focus.py \
  --repos-root "C:/projects" \
  --owner "MyTeam" \
  --communications "E:/agent-comms"

# Result: 
# - Projects: C:/projects/MyTeam/
# - Communications: E:/agent-comms/
```

### Cross-Platform
```bash
# Linux/Mac paths work too
python configure_project_focus.py --repos-root "/home/user/projects" --owner "MyName"

# Windows with different drive
python configure_project_focus.py --repos-root "F:/dev" --owner "DevTeam"
```

## 🔄 Runtime Configuration

### Environment Variables (PowerShell)
```powershell
$env:REPOS_ROOT = "C:/my-projects"
$env:DEFAULT_OWNER = "MyName"
python your_script.py
```

### Environment Variables (Bash)
```bash
export REPOS_ROOT="/home/user/projects"
export DEFAULT_OWNER="MyName"
python your_script.py
```

### Python Script
```python
import os
os.environ['REPOS_ROOT'] = 'C:/my-projects'
os.environ['DEFAULT_OWNER'] = 'MyName'

# Import after setting environment
from src.core.config import get_repos_root, get_owner_path
```

## 🏗️ Integration Points

### 1. Core Configuration System
```python
from src.core.config import (
    get_repos_root,
    get_owner_path,
    get_agent_workspace_path,
    get_communications_path
)

# Get configurable paths
repos_root = get_repos_root()
agent_path = get_agent_workspace_path('Agent-1')
comms_path = get_communications_path('20241201')
```

### 2. Legacy Code Migration
```python
# OLD (hardcoded)
workspace = "D:/repos/Dadudekc/Agent-1"

# NEW (configurable)
from src.core.config import get_agent_workspace_path
workspace = get_agent_workspace_path('Agent-1')
```

### 3. Command Line Tools
```bash
# All existing tools now use configurable paths
python overnight_runner/runner.py --workspace-root $(python -c "from src.core.config import get_agent_workspaces_root; print(get_agent_workspaces_root())")
```

## 🧪 Testing Your Configuration

### 1. Verify Paths
```bash
python configure_project_focus.py --show
```

### 2. Test Agent Workspaces
```bash
python -c "
from src.core.config import get_agent_workspace_path
for agent in ['Agent-1', 'Agent-2', 'Agent-3', 'Agent-4', 'Agent-5']:
    print(f'{agent}: {get_agent_workspace_path(agent)}')
"
```

### 3. Test Communications
```bash
python -c "
from src.core.config import get_communications_path, get_agent_communications_path
print(f'Comms: {get_communications_path()}')
print(f'Agent-1 Comms: {get_agent_communications_path(\"Agent-1\", \"20241201\")}')
"
```

## 🔍 Troubleshooting

### Common Issues

#### 1. Paths Not Updating
```bash
# Check if environment variables are set
echo $env:REPOS_ROOT  # PowerShell
echo $REPOS_ROOT       # Bash

# Verify configuration loaded
python configure_project_focus.py --show
```

#### 2. Import Errors
```bash
# Make sure you're in the right directory
cd Agent_Cellphone

# Check Python path
python -c "import sys; print(sys.path)"
```

#### 3. Permission Issues
```bash
# Create directories if they don't exist
mkdir -p "C:/my-projects/MyName"
mkdir -p "C:/my-projects/communications"
```

### Debug Mode
```python
from src.core.config import config
config.print_configuration()  # Shows all paths and environment variables
```

## 📚 Migration Guide

### For Existing Users

1. **No Breaking Changes**: All existing functionality continues to work
2. **Gradual Migration**: Update paths one file at a time
3. **Backward Compatibility**: Legacy environment variables still supported

### For New Users

1. **Start Fresh**: Use `configure_project_focus.py` to set your paths
2. **Customize Early**: Set paths before running agents
3. **Document Your Setup**: Keep your `.env` file in version control

## 🎉 Benefits

### For Users
- ✅ **Easy Customization**: Change project focus with one command
- ✅ **No Hardcoded Paths**: Everything is configurable
- ✅ **Cross-Platform**: Works on Windows, Linux, and Mac
- ✅ **Scalable**: Easy to manage multiple project environments

### For Developers
- ✅ **Maintainable Code**: No more path hunting
- ✅ **Testable**: Easy to test with different configurations
- ✅ **Flexible**: Support multiple deployment scenarios
- ✅ **Professional**: Industry-standard configuration management

## 🔮 Future Enhancements

- [ ] Configuration validation and schema
- [ ] Multiple environment profiles (dev, staging, prod)
- [ ] Configuration inheritance and overrides
- [ ] Web-based configuration interface
- [ ] Configuration backup and restore

## 📞 Support

### Getting Help
1. Check current configuration: `python configure_project_focus.py --show`
2. Review environment variables
3. Check the `.env` file format
4. Verify directory permissions

### Contributing
- Report issues with configuration
- Suggest new configuration options
- Improve the configuration script
- Add configuration validation

---

**🎯 The goal**: Make Agent Cellphone work seamlessly in **any** project environment with **zero** hardcoded paths.

**💡 The solution**: A simple, powerful configuration system that puts users in control of where agents focus their work.
