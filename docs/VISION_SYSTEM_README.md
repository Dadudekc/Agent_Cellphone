# AI Agent Vision System

## Overview

This vision system gives AI agents the ability to "see" and understand what's happening on your computer screen. It's like giving AI agents "eyes" to complement their existing "hands" (keyboard/mouse control).

## Features

### 🎯 **Core Capabilities**
- **Screen Capture**: Real-time screenshot capture
- **OCR (Optical Character Recognition)**: Extract text from images
- **UI Element Detection**: Identify buttons, text fields, and other interface elements
- **Text Region Analysis**: Find and locate specific text on screen
- **Continuous Monitoring**: Real-time vision monitoring with event detection

### 🤖 **Agent Integration**
- **Vision-Enabled Agents**: Agents can now "see" screen content
- **Event Detection**: Automatic detection of text changes and UI updates
- **Smart Interaction**: Click on specific text or UI elements
- **Vision History**: Track and search through visual changes over time

## Installation

### 1. Install Dependencies

```bash
pip install -r vision_requirements.txt
```

### 2. Install Tesseract OCR

**Windows:**
```bash
# Download and install from: https://github.com/UB-Mannheim/tesseract/wiki
# Add to PATH: C:\Program Files\Tesseract-OCR
```

**macOS:**
```bash
brew install tesseract
```

**Linux:**
```bash
sudo apt-get install tesseract-ocr
```

## Quick Start

### Basic Vision Demo

```python
from vision_system import VisionSystem

# Initialize vision system
vision = VisionSystem()

# Capture and analyze screen
image = vision.capture_screen()
analysis = vision.analyze_screen_content(image)

print(f"Text found: {analysis['text_content']}")
print(f"UI elements: {len(analysis['ui_elements'])}")
```

### Agent with Vision

```python
from agent_vision_integration import VisionEnabledAgent

# Create vision-enabled agent
agent = VisionEnabledAgent("my_agent")

# Start vision monitoring
agent.start_vision()

# Get current vision data
vision_data = agent.get_vision_data()
print(f"Current screen text: {vision_data.get('text_content', '')}")

# Click on specific text
agent.click_text("Save")

# Stop vision
agent.stop_vision()
```

## Advanced Usage

### 1. Continuous Monitoring

```python
def vision_callback(analysis):
    """Handle vision updates"""
    if "error" in analysis['text_content'].lower():
        print("Error detected on screen!")
    
    if len(analysis['ui_elements']) > 10:
        print("Many UI elements detected")

# Create agent with callback
agent = VisionEnabledAgent("monitor_agent")
agent.vision_integration.add_vision_callback(vision_callback)
agent.start_vision()
```

### 2. Region-Specific Capture

```python
# Capture specific screen region (x, y, width, height)
region = (100, 100, 800, 600)
analysis = agent.vision_integration.capture_specific_region(region)
```

### 3. Text Search and Interaction

```python
# Find specific text on screen
matches = agent.vision_integration.find_text_on_screen("Submit")

# Click on text with confidence threshold
success = agent.vision_integration.click_on_text("Submit", confidence_threshold=70.0)
```

### 4. Vision History

```python
# Get recent vision history
history = agent.vision_integration.get_vision_history(limit=20)

# Search vision history
results = agent.vision_integration.search_vision_history("error")
```

## Configuration

### Vision System Configuration

```python
config = {
    'vision_config': {
        'capture_frequency': 0.5,  # Capture every 0.5 seconds
        'capture_region': None,     # Full screen (or specify region)
    }
}

agent = VisionEnabledAgent("configured_agent", config)
```

### Advanced Configuration

```python
advanced_config = {
    'vision_config': {
        'capture_frequency': 0.2,           # High frequency capture
        'capture_region': (0, 0, 1920, 1080),  # Specific region
    },
    'ocr_config': {
        'language': 'eng',                   # OCR language
        'confidence_threshold': 60.0,        # Minimum confidence
    }
}
```

## Integration with Existing Agent System

### 1. Add Vision to Existing Agents

```python
from your_existing_agent import YourAgent
from agent_vision_integration import AgentVisionIntegration

class VisionEnabledYourAgent(YourAgent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.vision = AgentVisionIntegration(self.agent_id)
        self.vision.add_vision_callback(self._on_vision_update)
    
    def _on_vision_update(self, vision_data):
        # Handle vision updates
        text_content = vision_data.get('text_content', '')
        if "task completed" in text_content.lower():
            self.handle_task_completion()
    
    def start_vision_monitoring(self):
        self.vision.start_vision_monitoring()
```

### 2. Multi-Agent Vision Coordination

```python
class VisionCoordinator:
    def __init__(self):
        self.agents = {}
        self.shared_vision_data = {}
    
    def add_agent(self, agent_id, agent):
        self.agents[agent_id] = agent
        agent.vision_integration.add_vision_callback(
            lambda data: self._handle_shared_vision(agent_id, data)
        )
    
    def _handle_shared_vision(self, agent_id, vision_data):
        self.shared_vision_data[agent_id] = vision_data
        # Coordinate between agents based on shared vision
```

## Use Cases

### 1. **Automated Testing**
- Monitor application behavior
- Detect UI changes
- Verify expected text appears

### 2. **Content Monitoring**
- Watch for specific keywords
- Monitor social media feeds
- Track news updates

### 3. **Automation Enhancement**
- Smart form filling
- Context-aware clicking
- Error detection and recovery

### 4. **Multi-Agent Coordination**
- Shared visual context
- Coordinated actions
- Visual task verification

## Performance Considerations

### 1. **Capture Frequency**
- Higher frequency = more responsive but more CPU usage
- Lower frequency = less responsive but more efficient
- Recommended: 0.5-2.0 seconds for most use cases

### 2. **Region Limiting**
- Capture specific regions instead of full screen
- Reduces processing time and memory usage
- Useful for monitoring specific applications

### 3. **OCR Optimization**
- Use confidence thresholds to filter results
- Pre-process images for better OCR accuracy
- Consider language-specific OCR settings

## Troubleshooting

### Common Issues

1. **Tesseract not found**
   ```
   Error: Tesseract not found
   Solution: Install Tesseract and add to PATH
   ```

2. **Screen capture fails**
   ```
   Error: Screen capture failed
   Solution: Check permissions and display settings
   ```

3. **OCR accuracy issues**
   ```
   Problem: Poor text recognition
   Solution: Adjust image preprocessing or confidence thresholds
   ```

### Debug Mode

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Enable debug logging for vision system
vision = VisionSystem()
vision.logger.setLevel(logging.DEBUG)
```

## Security Considerations

### 1. **Screen Content Privacy**
- Vision system captures screen content
- Ensure sensitive information is not logged
- Consider region limiting for privacy

### 2. **Access Control**
- Limit vision capabilities to trusted agents
- Implement vision permission system
- Audit vision access logs

### 3. **Data Storage**
- Vision data may contain sensitive information
- Implement secure storage practices
- Consider data retention policies

## Future Enhancements

### 1. **Advanced Computer Vision**
- Object detection
- Facial recognition
- Gesture recognition

### 2. **Machine Learning Integration**
- Custom vision models
- Predictive analysis
- Pattern recognition

### 3. **Multi-Modal Integration**
- Audio-visual coordination
- Haptic feedback
- Environmental sensors

## Contributing

To contribute to the vision system:

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## License

This vision system is part of the Agent_Cellphone project and follows the same licensing terms.

---

**Note**: This vision system gives AI agents unprecedented access to visual information. Use responsibly and ensure proper security measures are in place. 