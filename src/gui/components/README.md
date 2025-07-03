# Modular GUI Components for Dream.OS

This directory contains modular, reusable GUI components for the Dream.OS autonomous agent system. The components are designed to work with both tkinter and PyQt5 frameworks, providing a consistent interface across different GUI implementations.

## Component Architecture

### Core Components

#### Onboarding Components (`onboarding_components.py`)
- **OnboardingProgressWidget**: Progress bar and percentage display for onboarding status
- **OnboardingStatusWidget**: Status display for agent onboarding information
- **OnboardingLogWidget**: Logging widget with timestamp and error handling
- **OnboardingControlsWidget**: Control panel for onboarding operations
- **OnboardingChecklistWidget**: Treeview-based checklist for tracking onboarding progress
- **OnboardingManager**: Enhanced manager that integrates with GUI components

#### Custom Message Widget (`custom_message_widget.py`)
- **CustomMessageWidget**: Reusable widget for sending custom onboarding messages

#### PyQt5 Components (`onboarding_components_qt.py`)
- **OnboardingProgressWidget**: PyQt5 version with modern styling
- **OnboardingStatusWidget**: PyQt5 version with QTextEdit
- **OnboardingLogWidget**: PyQt5 version with signal-based communication
- **OnboardingControlsWidget**: PyQt5 version with QComboBox and QPushButton
- **OnboardingChecklistWidget**: PyQt5 version with QTreeWidget

#### PyQt5 Custom Message Widget (`custom_message_widget_qt.py`)
- **CustomMessageWidget**: PyQt5 version with QTextEdit and signal emission

## Usage Examples

### Tkinter Implementation

```python
from src.gui.components.onboarding_components import (
    OnboardingProgressWidget, OnboardingStatusWidget, OnboardingLogWidget,
    OnboardingControlsWidget, OnboardingChecklistWidget
)
from src.gui.components.custom_message_widget import CustomMessageWidget

# Create components
progress_widget = OnboardingProgressWidget(parent_frame)
status_widget = OnboardingStatusWidget(parent_frame)
log_widget = OnboardingLogWidget(parent_frame)
controls_widget = OnboardingControlsWidget(parent_frame, send_callback=handle_send)
custom_widget = CustomMessageWidget(parent_frame, send_callback=handle_send)
checklist_widget = OnboardingChecklistWidget(parent_frame)

# Update components
progress_widget.update_progress(75.5)
status_widget.update_status("Agent-1: Online\nAgent-2: Offline")
log_widget.log_message("Onboarding completed successfully")
checklist_widget.update_checklist(checklist_data)
```

### PyQt5 Implementation

```python
from src.gui.components.onboarding_components_qt import (
    OnboardingProgressWidget, OnboardingStatusWidget, OnboardingLogWidget,
    OnboardingControlsWidget, OnboardingChecklistWidget
)
from src.gui.components.custom_message_widget_qt import CustomMessageWidget

# Create components
progress_widget = OnboardingProgressWidget()
status_widget = OnboardingStatusWidget()
log_widget = OnboardingLogWidget()
controls_widget = OnboardingControlsWidget()
custom_widget = CustomMessageWidget()
checklist_widget = OnboardingChecklistWidget()

# Connect signals
controls_widget.send_request.connect(handle_send_request)
custom_widget.send_custom_message.connect(handle_custom_message)
log_widget.log_cleared.connect(handle_log_clear)

# Update components
progress_widget.update_progress(75.5)
status_widget.update_status("Agent-1: Online\nAgent-2: Offline")
log_widget.log_message("Onboarding completed successfully")
checklist_widget.update_checklist(checklist_data)
```

## Component Features

### OnboardingProgressWidget
- **Tkinter**: Uses ttk.Progressbar with percentage label
- **PyQt5**: Uses QProgressBar with modern styling and percentage display
- **Features**: Real-time progress updates, percentage formatting

### OnboardingStatusWidget
- **Tkinter**: Uses scrolledtext.ScrolledText for status display
- **PyQt5**: Uses QTextEdit with monospace font and read-only mode
- **Features**: Scrollable text area, status formatting

### OnboardingLogWidget
- **Tkinter**: Uses scrolledtext.ScrolledText with timestamp logging
- **PyQt5**: Uses QTextEdit with signal-based communication
- **Features**: Timestamped entries, error highlighting, auto-scroll

### OnboardingControlsWidget
- **Tkinter**: Uses ttk.Combobox and ttk.Button with callback system
- **PyQt5**: Uses QComboBox and QPushButton with signal emission
- **Features**: Agent selection, message type selection, quick action buttons

### OnboardingChecklistWidget
- **Tkinter**: Uses ttk.Treeview with status/document/description columns
- **PyQt5**: Uses QTreeWidget with modern styling
- **Features**: Dynamic checklist updates, completion status display

### CustomMessageWidget
- **Tkinter**: Uses scrolledtext.ScrolledText with send button
- **PyQt5**: Uses QTextEdit with signal-based message sending
- **Features**: Message content management, validation

## Integration with Onboarding Manager

All components are designed to work seamlessly with the enhanced OnboardingManager:

```python
from agent_workspaces.onboarding.onboarding_manager import OnboardingManager

# Initialize manager
manager = OnboardingManager(layout_mode="8-agent", test_mode=True)

# Get data for components
agents = manager.get_available_agents()
documents = manager.get_onboarding_documents()
checklist = manager.get_checklist()
progress = manager.get_onboarding_progress()

# Update components with manager data
controls_widget.set_agents(agents)
checklist_widget.update_checklist(checklist)
progress_widget.update_progress(progress.get("completion_percentage", 0))
```

## Styling and Theming

### Tkinter Styling
- Uses ttk widgets for consistent appearance
- Custom styling through ttk.Style configuration
- Responsive layout with proper padding and spacing

### PyQt5 Styling
- Modern dark theme with consistent color scheme
- Custom CSS-like styling for all components
- Hover effects and visual feedback
- Responsive design with proper margins and spacing

## Error Handling

All components include comprehensive error handling:

- **Import Errors**: Graceful fallback when dependencies are missing
- **Data Validation**: Input validation for user interactions
- **Thread Safety**: Proper thread handling for background operations
- **Signal/Slot Safety**: Safe signal emission and slot connection

## Performance Considerations

- **Lazy Loading**: Components initialize only when needed
- **Efficient Updates**: Minimal UI updates for better performance
- **Memory Management**: Proper cleanup and resource management
- **Threading**: Background operations to prevent UI blocking

## Future Enhancements

- **Theme Support**: Dynamic theme switching
- **Accessibility**: Screen reader support and keyboard navigation
- **Internationalization**: Multi-language support
- **Plugin System**: Extensible component architecture
- **Testing Framework**: Unit tests for all components

## Contributing

When adding new components:

1. **Follow Naming Convention**: Use descriptive class names with Widget suffix
2. **Implement Both Frameworks**: Create both tkinter and PyQt5 versions
3. **Add Documentation**: Include docstrings and usage examples
4. **Include Error Handling**: Graceful error handling and fallbacks
5. **Test Integration**: Ensure compatibility with existing components 