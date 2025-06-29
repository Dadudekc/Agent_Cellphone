#!/usr/bin/env python3
"""
Send onboarding message to a specific agent
Simple script to send personalized onboarding messages using PyAutoGUI
"""

import pyautogui
import json
import time
import sys
from datetime import datetime
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

def load_agent_coordinates():
    """Load agent coordinates"""
    try:
        coordinates_file = project_root / "runtime" / "config" / "cursor_agent_coords.json"
        if coordinates_file.exists():
            with open(coordinates_file, 'r') as f:
                return json.load(f)
        else:
            print("❌ No agent coordinates found. Please run coordinate_finder.py first.")
            return {}
    except Exception as e:
        print(f"❌ Error loading agent coordinates: {e}")
        return {}

def get_onboarding_message(agent_name):
    """Get personalized onboarding message for agent"""
    messages = {
        "Agent-1": "🎯 Welcome Agent-1! You are our System Coordinator & Project Manager. Your role: project coordination, task assignment, progress monitoring, conflict resolution. 📚 Start with: agent_workspaces/onboarding/README.md",
        "Agent-2": "🎨 Welcome Agent-2! You are our Frontend Development Specialist. Your role: UI/UX development, responsive design, component development, performance optimization. 📚 Start with: agent_workspaces/onboarding/README.md",
        "Agent-3": "⚙️ Welcome Agent-3! You are our Backend Development Specialist. Your role: API development, database design, server architecture, authentication. 📚 Start with: agent_workspaces/onboarding/README.md",
        "Agent-4": "🛠️ Welcome Agent-4! You are our DevOps & Infrastructure Specialist. Your role: infrastructure management, CI/CD, monitoring, security. 📚 Start with: agent_workspaces/onboarding/README.md",
        "Agent-5": "🔍 Welcome Agent-5! You are our Testing & Quality Assurance Specialist. Your role: test strategy, automation, quality assurance, performance testing. 📚 Start with: agent_workspaces/onboarding/README.md",
        "Agent-6": "📊 Welcome Agent-6! You are our Data Science & Analytics Specialist. Your role: data analysis, machine learning, visualization, business intelligence. 📚 Start with: agent_workspaces/onboarding/README.md",
        "Agent-7": "🔒 Welcome Agent-7! You are our Security & Compliance Specialist. Your role: security architecture, vulnerability assessment, compliance, incident response. 📚 Start with: agent_workspaces/onboarding/README.md",
        "Agent-8": "📚 Welcome Agent-8! You are our Documentation & Knowledge Management Specialist. Your role: technical documentation, knowledge management, training materials. 📚 Start with: agent_workspaces/onboarding/README.md"
    }
    return messages.get(agent_name, f"Welcome {agent_name}! Please check agent_workspaces/onboarding/README.md for your onboarding materials.")

def send_message_to_agent(agent_name, message):
    """Send message to specific agent"""
    agents = load_agent_coordinates()
    
    if agent_name not in agents:
        print(f"❌ Agent {agent_name} not found in coordinates")
        return False
    
    coords = agents[agent_name]
    if 'coordinates' not in coords:
        print(f"❌ No coordinates found for {agent_name}")
        return False
    
    x = coords['coordinates']['x']
    y = coords['coordinates']['y']
    
    try:
        print(f"🎯 Sending message to {agent_name} at ({x}, {y})...")
        
        # Move to agent position
        pyautogui.moveTo(x, y, duration=1)
        
        # Click to activate the agent window
        pyautogui.click()
        time.sleep(2)
        
        # Type the message
        pyautogui.typewrite(message)
        pyautogui.press('enter')
        
        # Add timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        pyautogui.typewrite(f"📅 Onboarding sent: {timestamp}")
        pyautogui.press('enter')
        
        print(f"✅ Message sent to {agent_name}")
        return True
        
    except Exception as e:
        print(f"❌ Error sending message to {agent_name}: {e}")
        return False

def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("Usage: python send_onboarding_message.py <agent_name> [custom_message]")
        print("Example: python send_onboarding_message.py Agent-1")
        print("Example: python send_onboarding_message.py Agent-2 'Custom welcome message'")
        return
    
    agent_name = sys.argv[1]
    
    if len(sys.argv) > 2:
        # Use custom message
        message = " ".join(sys.argv[2:])
    else:
        # Use default onboarding message
        message = get_onboarding_message(agent_name)
    
    print(f"🎯 Sending onboarding message to {agent_name}...")
    print(f"📝 Message: {message}")
    
    success = send_message_to_agent(agent_name, message)
    
    if success:
        print(f"✅ Successfully sent onboarding message to {agent_name}")
    else:
        print(f"❌ Failed to send message to {agent_name}")

if __name__ == "__main__":
    main() 