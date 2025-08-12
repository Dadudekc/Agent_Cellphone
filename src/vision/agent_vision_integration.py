import threading
import time
import json
import logging
from typing import Dict, List, Callable, Optional
from vision_system import VisionSystem
import pyautogui
import cv2

class AgentVisionIntegration:
    """
    Integrates vision capabilities with AI agents
    Allows agents to "see" and understand screen content
    """
    
    def __init__(self, agent_id: str, config: Dict = None):
        self.agent_id = agent_id
        self.config = config or {}
        self.vision_system = VisionSystem(config.get('vision_config', {}))
        self.logger = logging.getLogger(f"AgentVision_{agent_id}")
        
        # Vision state
        self.current_vision_data = {}
        self.vision_history = []
        self.is_monitoring = False
        self.monitor_thread = None
        
        # Callbacks for vision events
        self.vision_callbacks = []
        
        # Agent communication
        self.agent_message_queue = []
        
    def start_vision_monitoring(self, callback: Callable = None):
        """
        Start continuous vision monitoring
        """
        if self.is_monitoring:
            self.logger.warning("Vision monitoring already active")
            return
            
        if callback:
            self.vision_callbacks.append(callback)
            
        self.is_monitoring = True
        self.monitor_thread = threading.Thread(
            target=self._vision_monitor_loop,
            daemon=True
        )
        self.monitor_thread.start()
        self.logger.info("Vision monitoring started")
    
    def stop_vision_monitoring(self):
        """
        Stop vision monitoring
        """
        self.is_monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=2)
        self.logger.info("Vision monitoring stopped")
    
    def _vision_monitor_loop(self):
        """
        Main vision monitoring loop
        """
        while self.is_monitoring:
            try:
                # Capture and analyze screen
                image = self.vision_system.capture_screen()
                if image is not None:
                    analysis = self.vision_system.analyze_screen_content(image)
                    
                    # Update current vision data
                    self.current_vision_data = analysis
                    self.vision_history.append(analysis)
                    
                    # Keep only recent history
                    if len(self.vision_history) > 100:
                        self.vision_history = self.vision_history[-50:]
                    
                    # Trigger callbacks
                    for callback in self.vision_callbacks:
                        try:
                            callback(analysis)
                        except Exception as e:
                            self.logger.error(f"Vision callback error: {e}")
                    
                    # Check for important visual events
                    self._check_visual_events(analysis)
                
                time.sleep(self.config.get('vision_frequency', 1.0))
                
            except Exception as e:
                self.logger.error(f"Vision monitoring error: {e}")
                time.sleep(2)
    
    def _check_visual_events(self, analysis: Dict):
        """
        Check for important visual events that agents should know about
        """
        # Check for new text content
        if 'text_content' in analysis and analysis['text_content']:
            # Compare with previous text to detect changes
            if hasattr(self, '_previous_text'):
                if analysis['text_content'] != self._previous_text:
                    self._handle_text_change(analysis['text_content'])
            self._previous_text = analysis['text_content']
        
        # Check for UI element changes
        if 'ui_elements' in analysis:
            current_elements = len(analysis['ui_elements'])
            if hasattr(self, '_previous_ui_count'):
                if current_elements != self._previous_ui_count:
                    self._handle_ui_change(analysis['ui_elements'])
            self._previous_ui_count = current_elements
    
    def _handle_text_change(self, new_text: str):
        """
        Handle text content changes
        """
        event = {
            'type': 'text_change',
            'content': new_text,
            'timestamp': time.time(),
            'agent_id': self.agent_id
        }
        self.agent_message_queue.append(event)
        self.logger.info(f"Text change detected: {len(new_text)} characters")
    
    def _handle_ui_change(self, ui_elements: List[Dict]):
        """
        Handle UI element changes
        """
        event = {
            'type': 'ui_change',
            'elements': ui_elements,
            'timestamp': time.time(),
            'agent_id': self.agent_id
        }
        self.agent_message_queue.append(event)
        self.logger.info(f"UI change detected: {len(ui_elements)} elements")
    
    def get_current_vision(self) -> Dict:
        """
        Get current vision data
        """
        return self.current_vision_data.copy()
    
    def get_vision_history(self, limit: int = 10) -> List[Dict]:
        """
        Get recent vision history
        """
        return self.vision_history[-limit:] if self.vision_history else []
    
    def search_vision_history(self, query: str) -> List[Dict]:
        """
        Search vision history for specific content
        """
        results = []
        for entry in self.vision_history:
            if query.lower() in entry.get('text_content', '').lower():
                results.append(entry)
        return results
    
    def capture_specific_region(self, region: tuple) -> Dict:
        """
        Capture and analyze specific screen region
        """
        image = self.vision_system.capture_screen(region)
        if image is not None:
            return self.vision_system.analyze_screen_content(image)
        return {}
    
    def find_text_on_screen(self, search_text: str) -> List[Dict]:
        """
        Find specific text on screen
        """
        current_vision = self.get_current_vision()
        text_regions = current_vision.get('text_regions', [])
        
        matches = []
        for region in text_regions:
            if search_text.lower() in region['text'].lower():
                matches.append(region)
        
        return matches
    
    def click_on_text(self, text: str, confidence_threshold: float = 50.0):
        """
        Click on specific text on screen
        """
        matches = self.find_text_on_screen(text)
        
        if matches:
            # Use the best match (highest confidence)
            best_match = max(matches, key=lambda x: x['confidence'])
            
            if best_match['confidence'] >= confidence_threshold:
                x, y = best_match['position']
                w, h = best_match['size']
                
                # Click at center of text region
                click_x = x + w // 2
                click_y = y + h // 2
                
                pyautogui.click(click_x, click_y)
                self.logger.info(f"Clicked on text '{text}' at ({click_x}, {click_y})")
                return True
        
        self.logger.warning(f"Text '{text}' not found or confidence too low")
        return False
    
    def get_agent_messages(self) -> List[Dict]:
        """
        Get pending messages for agent
        """
        messages = self.agent_message_queue.copy()
        self.agent_message_queue.clear()
        return messages
    
    def add_vision_callback(self, callback: Callable):
        """
        Add callback for vision events
        """
        self.vision_callbacks.append(callback)
    
    def save_vision_session(self, filename: str):
        """
        Save current vision session data
        """
        session_data = {
            'agent_id': self.agent_id,
            'timestamp': time.time(),
            'current_vision': self.current_vision_data,
            'vision_history': self.vision_history[-20:],  # Last 20 entries
            'config': self.config
        }
        
        try:
            with open(filename, 'w') as f:
                json.dump(session_data, f, indent=2)
            self.logger.info(f"Vision session saved to {filename}")
        except Exception as e:
            self.logger.error(f"Failed to save vision session: {e}")

# Example integration with agent system
class VisionEnabledAgent:
    """
    Example agent class with vision capabilities
    """
    
    def __init__(self, agent_id: str, config: Dict = None):
        self.agent_id = agent_id
        self.vision_integration = AgentVisionIntegration(agent_id, config)
        self.logger = logging.getLogger(f"VisionAgent_{agent_id}")
        
        # Set up vision callback
        self.vision_integration.add_vision_callback(self._on_vision_update)
    
    def _on_vision_update(self, vision_data: Dict):
        """
        Handle vision updates
        """
        self.logger.info(f"Vision update received: {vision_data.get('text_content', '')[:50]}...")
        
        # Process vision data based on agent's needs
        if 'text_content' in vision_data:
            self._process_text_content(vision_data['text_content'])
    
    def _process_text_content(self, text: str):
        """
        Process text content from vision
        """
        # Example: Look for specific patterns or keywords
        if "error" in text.lower():
            self.logger.warning("Error detected in screen content")
        elif "success" in text.lower():
            self.logger.info("Success message detected")
    
    def start_vision(self):
        """
        Start vision monitoring for this agent
        """
        self.vision_integration.start_vision_monitoring()
    
    def stop_vision(self):
        """
        Stop vision monitoring
        """
        self.vision_integration.stop_vision_monitoring()
    
    def get_vision_data(self) -> Dict:
        """
        Get current vision data
        """
        return self.vision_integration.get_current_vision()
    
    def click_text(self, text: str) -> bool:
        """
        Click on specific text
        """
        return self.vision_integration.click_on_text(text)

# Example usage
if __name__ == "__main__":
    # Create vision-enabled agent
    agent_config = {
        'vision_config': {
            'capture_frequency': 0.5,  # Capture every 0.5 seconds
            'capture_region': None  # Full screen
        }
    }
    
    agent = VisionEnabledAgent("test_agent", agent_config)
    
    # Start vision monitoring
    agent.start_vision()
    
    try:
        # Run for 30 seconds
        time.sleep(30)
    finally:
        agent.stop_vision()
        print("Vision monitoring stopped") 