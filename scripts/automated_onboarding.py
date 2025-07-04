#!/usr/bin/env python3
"""
Automated Agent Onboarding Script
Uses default coordinates to automatically onboard Agent-1 and Agent-2
"""

import json
import time
import pyautogui
import pyperclip
from pathlib import Path

# Configure pyautogui for safety
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.5

class AutomatedOnboarding:
    def __init__(self):
        self.coords_file = Path("src/runtime/config/cursor_agent_coords.json")
        self.coordinates = self.load_coordinates()
        
        # Onboarding message template
        self.onboarding_message = """ONBOARDING PROTOCOL INITIATED

Agent System: Dream.OS Autonomous Platform
Onboarding Type: Comprehensive Agent Integration
Protocol Version: 2.0

CORE PROTOCOLS:
1. Quick Start Protocol - Agent initialization and system handshake
2. Status Reporting Protocol - Real-time status updates and health monitoring
3. Communication Protocol - Inter-agent messaging and coordination
4. Task Execution Protocol - Autonomous task processing and workflow management
5. Development Standards Protocol - Code quality and best practices enforcement

AGENT RESPONSIBILITIES:
- Execute assigned tasks autonomously
- Maintain real-time status reporting
- Engage in inter-agent communication
- Follow development standards and protocols
- Monitor system health and performance

ONBOARDING CHECKLIST:
□ Quick Start Protocol completed
□ Status reporting system active
□ Communication channels established
□ Development standards reviewed
□ Task execution capabilities verified
□ System integration confirmed

STATUS: READY FOR ONBOARDING
MODE: AUTONOMOUS OPERATION
PROTOCOL: ACTIVE"""

    def load_coordinates(self):
        """Load agent coordinates from config file"""
        try:
            with open(self.coords_file, 'r') as f:
                data = json.load(f)
                return data.get("2-agent", {})
        except Exception as e:
            print(f"Error loading coordinates: {e}")
            return {}

    def click_and_type(self, x, y, text, delay=1.0):
        """Click at coordinates and type text"""
        try:
            print(f"Moving to position ({x}, {y})")
            pyautogui.moveTo(x, y, duration=0.5)
            time.sleep(delay)
            
            print(f"Clicking at position ({x}, {y})")
            pyautogui.click()
            time.sleep(0.5)
            
            print(f"Typing onboarding message...")
            # Use clipboard for reliable text input
            pyperclip.copy(text)
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(0.5)
            
            print("Message typed successfully")
            return True
        except Exception as e:
            print(f"Error during click and type: {e}")
            return False

    def onboard_agent(self, agent_id):
        """Onboard a specific agent"""
        print(f"\n{'='*50}")
        print(f"ONBOARDING {agent_id}")
        print(f"{'='*50}")
        
        if agent_id not in self.coordinates:
            print(f"Error: No coordinates found for {agent_id}")
            return False
            
        agent_coords = self.coordinates[agent_id]
        starter_pos = agent_coords.get("starter_position", {})
        
        if not starter_pos:
            print(f"Error: No starter position found for {agent_id}")
            return False
            
        x, y = starter_pos["x"], starter_pos["y"]
        
        print(f"Starting onboarding for {agent_id} at position ({x}, {y})")
        
        # Step 1: Click the starter location
        if not self.click_and_type(x, y, "", delay=1.0):
            return False
            
        # Step 2: Press Ctrl+N to trigger new agent creation
        print("Pressing Ctrl+N to trigger new agent creation...")
        pyautogui.hotkey('ctrl', 'n')
        time.sleep(2.0)  # Wait for agent creation dialog
        
        # Step 3: Type the onboarding message
        if not self.click_and_type(x, y, self.onboarding_message, delay=1.0):
            return False
            
        # Step 4: Press Enter to submit
        print("Pressing Enter to submit onboarding message...")
        pyautogui.press('enter')
        time.sleep(2.0)
        
        print(f"✅ {agent_id} onboarding completed successfully!")
        return True

    def run_onboarding(self):
        """Run the complete onboarding process for both agents"""
        print("🚀 AUTOMATED AGENT ONBOARDING")
        print("=" * 50)
        print("This script will automatically onboard Agent-1 and Agent-2")
        print("using the default coordinates from the configuration.")
        print()
        print("⚠️  WARNING: Make sure your cursor is positioned correctly!")
        print("   The script will click at the specified coordinates.")
        print()
        
        # Countdown
        for i in range(5, 0, -1):
            print(f"Starting in {i} seconds...")
            time.sleep(1)
        
        print("\n🎯 Starting automated onboarding...")
        
        # Onboard Agent-1
        success_1 = self.onboard_agent("Agent-1")
        
        # Wait between agents
        if success_1:
            print("\n⏳ Waiting 3 seconds before onboarding Agent-2...")
            time.sleep(3)
        
        # Onboard Agent-2
        success_2 = self.onboard_agent("Agent-2")
        
        # Summary
        print(f"\n{'='*50}")
        print("ONBOARDING SUMMARY")
        print(f"{'='*50}")
        print(f"Agent-1: {'✅ SUCCESS' if success_1 else '❌ FAILED'}")
        print(f"Agent-2: {'✅ SUCCESS' if success_2 else '❌ FAILED'}")
        
        if success_1 and success_2:
            print("\n🎉 Both agents onboarded successfully!")
        else:
            print("\n⚠️  Some agents failed to onboard. Check the logs above.")
        
        return success_1 and success_2

def main():
    """Main function"""
    try:
        onboarding = AutomatedOnboarding()
        onboarding.run_onboarding()
    except KeyboardInterrupt:
        print("\n\n⏹️  Onboarding interrupted by user")
    except Exception as e:
        print(f"\n❌ Error during onboarding: {e}")

if __name__ == "__main__":
    main() 