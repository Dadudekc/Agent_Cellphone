#!/usr/bin/env python3
"""
Vision System Demo for AI Agents
Demonstrates how AI agents can "see" and interact with screen content
"""

import time
import json
import logging
from vision_system import VisionSystem
from agent_vision_integration import VisionEnabledAgent

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def demo_basic_vision():
    """
    Demo basic vision capabilities
    """
    print("=== Basic Vision Demo ===")
    
    # Initialize vision system
    vision = VisionSystem()
    
    # Capture screen
    print("Capturing screen...")
    image = vision.capture_screen()
    
    if image is not None:
        print(f"Screen captured: {image.shape}")
        
        # Analyze content
        analysis = vision.analyze_screen_content(image)
        
        print(f"Text content length: {len(analysis['text_content'])}")
        print(f"UI elements detected: {len(analysis['ui_elements'])}")
        print(f"Text regions found: {len(analysis['text_regions'])}")
        
        # Show some text content
        if analysis['text_content']:
            print("\nSample text content:")
            print(analysis['text_content'][:200] + "...")
        
        # Save analysis
        vision.save_vision_data(analysis, "vision_demo_output.json")
        print("Analysis saved to vision_demo_output.json")

def demo_agent_vision():
    """
    Demo agent with vision capabilities
    """
    print("\n=== Agent Vision Demo ===")
    
    # Create vision-enabled agent
    agent_config = {
        'vision_config': {
            'capture_frequency': 1.0,  # Capture every second
            'capture_region': None  # Full screen
        }
    }
    
    agent = VisionEnabledAgent("demo_agent", agent_config)
    
    print("Starting vision monitoring...")
    agent.start_vision()
    
    try:
        # Run for 10 seconds
        for i in range(10):
            print(f"Vision monitoring... ({i+1}/10)")
            
            # Get current vision data
            vision_data = agent.get_vision_data()
            if vision_data:
                text_content = vision_data.get('text_content', '')
                if text_content:
                    print(f"Current text: {text_content[:100]}...")
            
            time.sleep(1)
            
    finally:
        agent.stop_vision()
        print("Vision monitoring stopped")

def demo_text_interaction():
    """
    Demo clicking on text
    """
    print("\n=== Text Interaction Demo ===")
    
    agent = VisionEnabledAgent("interaction_agent", {})
    agent.start_vision()
    
    try:
        # Wait a moment for vision to initialize
        time.sleep(2)
        
        # Try to find and click on common UI elements
        common_texts = ["File", "Edit", "View", "Help", "OK", "Cancel", "Save", "Close"]
        
        for text in common_texts:
            print(f"Looking for text: '{text}'")
            if agent.click_text(text):
                print(f"Successfully clicked on '{text}'")
                break
            else:
                print(f"Text '{text}' not found")
        
    finally:
        agent.stop_vision()

def demo_continuous_monitoring():
    """
    Demo continuous vision monitoring with callbacks
    """
    print("\n=== Continuous Monitoring Demo ===")
    
    def vision_callback(analysis):
        """Custom callback for vision events"""
        text_content = analysis.get('text_content', '')
        if text_content:
            # Look for specific keywords
            if any(keyword in text_content.lower() for keyword in ['error', 'warning', 'success']):
                print(f"Important event detected: {text_content[:100]}...")
    
    # Create agent with custom callback
    agent_config = {
        'vision_config': {
            'capture_frequency': 0.5,  # Capture every 0.5 seconds
        }
    }
    
    agent = VisionEnabledAgent("monitor_agent", agent_config)
    agent.vision_integration.add_vision_callback(vision_callback)
    
    print("Starting continuous monitoring (30 seconds)...")
    agent.start_vision()
    
    try:
        time.sleep(30)
    finally:
        agent.stop_vision()
        print("Continuous monitoring stopped")

def main():
    """
    Run all vision demos
    """
    print("AI Agent Vision System Demo")
    print("=" * 50)
    
    try:
        # Run demos
        demo_basic_vision()
        demo_agent_vision()
        demo_text_interaction()
        demo_continuous_monitoring()
        
        print("\n=== Demo Complete ===")
        print("Vision system successfully demonstrated!")
        
    except KeyboardInterrupt:
        print("\nDemo interrupted by user")
    except Exception as e:
        print(f"Demo error: {e}")

if __name__ == "__main__":
    main() 