#!/usr/bin/env python3
"""
Agent Coordination Demo
=======================
Demonstration of agent-2 coordinating work with agent-1 in 2-agent mode.
Uses the new starter location system for reliable communication.
"""

import sys
import os
import time
import json
from datetime import datetime

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from utils.coordinate_finder import CoordinateFinder
except ImportError as e:
    print(f"Import error: {e}")
    print("Please run from the project root directory")
    sys.exit(1)

class AgentCoordinator:
    """Simulates agent-2 coordinating work with agent-1."""
    
    def __init__(self):
        self.coordinate_finder = CoordinateFinder()
        self.agent_2_id = "agent-2"
        self.agent_1_id = "agent-1"
        self.mode = "2-agent"
        
        # Load coordinates for 2-agent mode
        self.agent_1_starter = self.coordinate_finder.get_starter_location(self.agent_1_id)
        self.agent_1_input = self.coordinate_finder.get_input_box_location(self.agent_1_id)
        self.agent_2_starter = self.coordinate_finder.get_starter_location(self.agent_2_id)
        self.agent_2_input = self.coordinate_finder.get_input_box_location(self.agent_2_id)
        
        print(f"🎯 Agent Coordinator initialized for {self.mode} mode")
        print(f"Agent-1: Starter {self.agent_1_starter}, Input {self.agent_1_input}")
        print(f"Agent-2: Starter {self.agent_2_starter}, Input {self.agent_2_input}")
    
    def simulate_click(self, x: int, y: int, description: str):
        """Simulate clicking at coordinates (for demo purposes)."""
        print(f"🖱️  Click at ({x}, {y}) - {description}")
        time.sleep(0.5)  # Simulate click delay
    
    def simulate_type(self, message: str, description: str):
        """Simulate typing a message."""
        print(f"⌨️  Type: '{message}' - {description}")
        time.sleep(0.3)  # Simulate typing delay
    
    def simulate_enter(self, description: str):
        """Simulate pressing Enter."""
        print(f"↵ Press Enter - {description}")
        time.sleep(0.2)  # Simulate enter delay
    
    def send_message_to_agent(self, agent_id: str, message: str, message_type: str = "COORDINATE"):
        """Send a message to a specific agent using the starter location system."""
        print(f"\n📤 Sending message to {agent_id}:")
        print(f"   Message: [{message_type}] {message}")
        
        if agent_id == self.agent_1_id:
            starter_coords = self.agent_1_starter
            input_coords = self.agent_1_input
        elif agent_id == self.agent_2_id:
            starter_coords = self.agent_2_starter
            input_coords = self.agent_2_input
        else:
            print(f"❌ Unknown agent: {agent_id}")
            return False
        
        if not starter_coords or not input_coords:
            print(f"❌ Missing coordinates for {agent_id}")
            return False
        
        # Step 1: Click starter location to activate agent
        x, y = starter_coords
        self.simulate_click(x, y, f"Activate {agent_id} window")
        
        # Step 2: Click input box to position cursor
        x, y = input_coords
        self.simulate_click(x, y, f"Position cursor in {agent_id} input box")
        
        # Step 3: Type the message
        full_message = f"[{message_type}] {message}"
        self.simulate_type(full_message, f"Send coordination message to {agent_id}")
        
        # Step 4: Press Enter to send
        self.simulate_enter(f"Send message to {agent_id}")
        
        print(f"✅ Message sent to {agent_id} successfully!")
        return True
    
    def demonstrate_coordination_workflow(self):
        """Demonstrate a complete coordination workflow between agent-2 and agent-1."""
        print("\n" + "="*60)
        print("🤝 AGENT COORDINATION DEMONSTRATION")
        print("="*60)
        print("Scenario: Agent-2 is coordinating a data analysis project with Agent-1")
        print("Mode: 2-agent mode")
        print("="*60)
        
        # Step 1: Agent-2 initiates coordination
        print("\n📋 STEP 1: Agent-2 initiates project coordination")
        print("-" * 40)
        self.send_message_to_agent(
            self.agent_1_id,
            "Hello Agent-1! I'm coordinating our data analysis project. Are you ready to begin?",
            "COORDINATE"
        )
        
        # Simulate Agent-1 response
        print(f"\n📥 Simulating Agent-1 response...")
        time.sleep(1)
        print(f"   Agent-1: [REPLY] Yes, I'm ready! What's the first task?")
        
        # Step 2: Agent-2 assigns specific tasks
        print("\n📋 STEP 2: Agent-2 assigns specific tasks")
        print("-" * 40)
        self.send_message_to_agent(
            self.agent_1_id,
            "Great! Here's your task: Analyze the customer feedback dataset and identify top 3 improvement areas. Report back in 30 minutes.",
            "TASK"
        )
        
        # Simulate Agent-1 acknowledgment
        print(f"\n📥 Simulating Agent-1 acknowledgment...")
        time.sleep(1)
        print(f"   Agent-1: [ACKNOWLEDGE] Task received. Starting analysis now.")
        
        # Step 3: Agent-2 provides additional context
        print("\n📋 STEP 3: Agent-2 provides additional context")
        print("-" * 40)
        self.send_message_to_agent(
            self.agent_1_id,
            "Focus on sentiment analysis and feature requests. Use the new ML model we discussed.",
            "CONTEXT"
        )
        
        # Simulate Agent-1 confirmation
        print(f"\n📥 Simulating Agent-1 confirmation...")
        time.sleep(1)
        print(f"   Agent-1: [CONFIRM] Understood. Using ML model for sentiment analysis.")
        
        # Step 4: Agent-2 checks progress
        print("\n📋 STEP 4: Agent-2 checks progress (15 minutes later)")
        print("-" * 40)
        self.send_message_to_agent(
            self.agent_1_id,
            "How's the analysis going? Any preliminary findings to share?",
            "STATUS"
        )
        
        # Simulate Agent-1 progress update
        print(f"\n📥 Simulating Agent-1 progress update...")
        time.sleep(1)
        print(f"   Agent-1: [PROGRESS] 60% complete. Found 2 major improvement areas so far.")
        
        # Step 5: Agent-2 provides encouragement
        print("\n📋 STEP 5: Agent-2 provides encouragement")
        print("-" * 40)
        self.send_message_to_agent(
            self.agent_1_id,
            "Excellent progress! Keep up the good work. Looking forward to your final report.",
            "ENCOURAGE"
        )
        
        # Simulate Agent-1 completion
        print(f"\n📥 Simulating Agent-1 completion...")
        time.sleep(1)
        print(f"   Agent-1: [COMPLETE] Analysis finished! Top 3 areas: UI/UX, Performance, Security.")
        
        # Step 6: Agent-2 acknowledges completion
        print("\n📋 STEP 6: Agent-2 acknowledges completion")
        print("-" * 40)
        self.send_message_to_agent(
            self.agent_1_id,
            "Perfect! Thank you for the excellent work. I'll compile this into our final report.",
            "ACKNOWLEDGE"
        )
        
        print("\n" + "="*60)
        print("✅ COORDINATION DEMONSTRATION COMPLETED")
        print("="*60)
        print("Key Features Demonstrated:")
        print("• Reliable communication using starter location system")
        print("• Task assignment and tracking")
        print("• Progress monitoring")
        print("• Context sharing")
        print("• Encouragement and acknowledgment")
        print("• Complete workflow from initiation to completion")
        print("="*60)

def main():
    """Main function to run the coordination demonstration."""
    print("🚀 Starting Agent Coordination Demonstration")
    print("=" * 50)
    
    # Initialize the coordinator
    coordinator = AgentCoordinator()
    
    # Run the demonstration
    coordinator.demonstrate_coordination_workflow()
    
    print("\n🎉 Demonstration completed successfully!")
    print("This shows how agent-2 can effectively coordinate work with agent-1")
    print("using the new starter location system for reliable communication.")

if __name__ == "__main__":
    main() 