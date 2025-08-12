# Agent Cellphone Project Organization Plan

## Current Issues Identified:
1. **Scattered Files**: Multiple files in root directory that should be organized
2. **Duplicate Functionality**: Multiple audio/voice systems
3. **Inconsistent Naming**: Mixed naming conventions
4. **Missing Structure**: Some directories lack proper organization

## Organization Strategy:

### Audio/Voice System Consolidation
- `audio_system.py` → `src/audio/audio_system.py`
- `simple_audio_system.py` → `src/audio/simple_audio_system.py`
- `voice_recognition.py` → `src/audio/voice_recognition.py`
- `voice_selector.py` → `src/audio/voice_selector.py`
- `voice_profile_victor.json` → `config/voice_profiles/`
- Audio test files → `tests/audio/`

### Vision System Organization
- `vision_system.py` → `src/vision/vision_system.py`
- `agent_vision_integration.py` → `src/vision/agent_vision_integration.py`
- `vision_demo.py` → `examples/vision/`
- `vision_demo_output.json` → `data/vision/`
- `vision_requirements.txt` → `requirements/vision_requirements.txt`

### Core System Files
- `personal_jarvis.py` → `src/core/personal_jarvis.py`
- `conversation_engine.py` → `src/core/conversation_engine.py`
- `memory_system.py` → `src/core/memory_system.py`
- `multimodal_agent.py` → `src/core/multimodal_agent.py`

### Development & Testing
- Test files → `tests/`
- Debug files → `debug/` (temporary)
- Demo files → `examples/`

### Configuration & Data
- JSON configs → `config/`
- Database files → `data/`
- Memory files → `data/memory/`

### Documentation
- All .md files → `docs/`
- Requirements files → `requirements/`

## Execution Order:
1. Create missing directories
2. Move files systematically
3. Update import paths
4. Clean up duplicates
5. Update documentation
6. Test functionality 