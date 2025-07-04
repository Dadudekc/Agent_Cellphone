# Dream.OS Configuration Structure

## Overview

This document describes the canonical configuration structure for Dream.OS after the runtime folder cleanup and consolidation.

## Canonical Configuration Locations

### Runtime Configuration
All runtime configuration files are located in:
```
src/runtime/config/
```

**Files:**
- `cursor_agent_coords.json` - Agent coordinate mappings for different GUI layouts (2-agent, 4-agent, 8-agent)
- `templates/agent_modes.json` - Agent mode templates and configurations

### Templates
All template files are located in:
```
config/templates/
```

**Files:**
- `agent_modes.json` - Agent mode definitions
- `message_templates.json` - Message template definitions
- `workspace_template/` - Workspace template structure

## File Descriptions

### cursor_agent_coords.json
Contains coordinate mappings for agent input boxes in different GUI layouts:
- **2-agent mode**: Agent-1, Agent-2 coordinates
- **4-agent mode**: Agent-1 through Agent-4 coordinates  
- **8-agent mode**: Agent-1 through Agent-8 coordinates

Each agent has an `input_box` with `x` and `y` coordinates for GUI positioning.

### agent_modes.json
Defines different operational modes for agents with:
- Mode names and descriptions
- Prompt templates
- Configuration parameters

### message_templates.json
Contains templates for various message types used in agent communication.

## Code References

### Python Modules
- `src/agent_cell_phone.py` - Uses relative paths from its location
- `scripts/onboarding_utils.py` - References `src/runtime/config/cursor_agent_coords.json`

### Import Paths
```python
# For runtime config
CONFIG_DIR = Path(__file__).resolve().parent / "runtime" / "config"
COORD_FILE = CONFIG_DIR / "cursor_agent_coords.json"

# For templates
TEMPLATE_DIR = project_root / "config" / "templates"
```

## Migration History

### Before Cleanup
- Multiple `runtime/` folders existed:
  - `runtime/config/` (project root)
  - `src/runtime/config/`
  - `gui/runtime/config/`
- Duplicate files with inconsistent formats
- Confusing import paths

### After Cleanup
- **Canonical location**: `src/runtime/config/`
- **Templates**: `config/templates/` (project root)
- **Backup**: `backup/runtime_configs/` (contains old versions)
- **Single source of truth** for all configuration

## Best Practices

1. **Always use canonical paths** when referencing configuration files
2. **Update imports** when adding new modules that need config access
3. **Backup before changes** to configuration files
4. **Document changes** to configuration structure
5. **Test configuration** after any structural changes

## Adding New Configuration

When adding new configuration files:

1. **Runtime config**: Place in `src/runtime/config/`
2. **Templates**: Place in `config/templates/`
3. **Update this documentation** with new file descriptions
4. **Update code references** to use canonical paths
5. **Test the configuration** in all relevant modules

## Troubleshooting

### Common Issues
- **Import errors**: Check that paths reference canonical locations
- **Missing files**: Verify files exist in `src/runtime/config/` or `config/templates/`
- **Inconsistent data**: Ensure only one copy of each config file exists

### Recovery
- **Backup files**: Available in `backup/runtime_configs/`
- **Restore process**: Copy from backup and update paths as needed 