#!/usr/bin/env python3
"""
Dream.OS Agent Onboarding Sequence
Automated onboarding system using PyAutoGUI to identify agents and send personalized onboarding messages.
"""

import pyautogui
import json
import time
import os
import sys
from datetime import datetime
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from coordinate_finder import CoordinateFinder

class AgentOnboardingSequence:
    """Automated onboarding system for Dream.OS agents"""
    
    def __init__(self):
        self.coordinate_finder = CoordinateFinder()
        self.agents = self.load_agent_coordinates()
        self.onboarding_messages = self.load_onboarding_messages()
        
    def load_agent_coordinates(self):
        """Load agent coordinates from the coordinate finder"""
        try:
            coordinates_file = project_root / "runtime" / "config" / "cursor_agent_coords.json"
            if coordinates_file.exists():
                with open(coordinates_file, 'r') as f:
                    return json.load(f)
            else:
                print("⚠️  No agent coordinates found. Please run coordinate_finder.py first.")
                return {}
        except Exception as e:
            print(f"❌ Error loading agent coordinates: {e}")
            return {}
    
    def load_onboarding_messages(self):
        """Load personalized onboarding messages for each agent"""
        return {
            "Agent-1": {
                "title": "🎯 Welcome Agent-1: System Coordinator & Project Manager",
                "message": """Welcome to Dream.OS! You are Agent-1, our System Coordinator & Project Manager.

Your role is crucial to our success:
• Project coordination and task assignment
• Progress monitoring and bottleneck identification
• Conflict resolution and team leadership
• Quality assurance and strategic planning

📚 Your Onboarding Materials:
• Main Guide: agent_workspaces/onboarding/README.md
• Your Role: agent_workspaces/onboarding/training_documents/agent_roles_and_responsibilities.md
• Protocols: agent_workspaces/onboarding/protocols/agent_protocols.md
• Checklist: agent_workspaces/onboarding/training_documents/onboarding_checklist.md

🚀 Next Steps:
1. Read the main README.md
2. Complete the onboarding checklist
3. Review your specific role responsibilities
4. Practice with the team communication protocols

You're the leader of our team - let's build something amazing together! 🎉"""
            },
            "Agent-2": {
                "title": "🎨 Welcome Agent-2: Frontend Development Specialist",
                "message": """Welcome to Dream.OS! You are Agent-2, our Frontend Development Specialist.

Your expertise drives our user experience:
• UI/UX development and responsive design
• Frontend architecture and component development
• Performance optimization and accessibility
• Cross-browser compatibility and PWA development

📚 Your Onboarding Materials:
• Main Guide: agent_workspaces/onboarding/README.md
• Your Role: agent_workspaces/onboarding/training_documents/agent_roles_and_responsibilities.md
• Development Standards: agent_workspaces/onboarding/training_documents/development_standards.md
• Tools Guide: agent_workspaces/onboarding/training_documents/tools_and_technologies.md

🚀 Next Steps:
1. Review frontend development standards
2. Set up your development environment
3. Practice with React/Vue.js/Angular workflows
4. Complete the onboarding checklist

Your designs will shape how users interact with our systems! 🎨"""
            },
            "Agent-3": {
                "title": "⚙️ Welcome Agent-3: Backend Development Specialist",
                "message": """Welcome to Dream.OS! You are Agent-3, our Backend Development Specialist.

You're the backbone of our systems:
• API development and database design
• Server architecture and microservices
• Authentication, authorization, and security
• Data processing and external integrations

📚 Your Onboarding Materials:
• Main Guide: agent_workspaces/onboarding/README.md
• Your Role: agent_workspaces/onboarding/training_documents/agent_roles_and_responsibilities.md
• Development Standards: agent_workspaces/onboarding/training_documents/development_standards.md
• Workflow Protocols: agent_workspaces/onboarding/protocols/workflow_protocols.md

🚀 Next Steps:
1. Review backend development standards
2. Set up Python/Node.js/Java environments
3. Practice API development workflows
4. Complete the onboarding checklist

Your APIs will power everything we build! ⚙️"""
            },
            "Agent-4": {
                "title": "🛠️ Welcome Agent-4: DevOps & Infrastructure Specialist",
                "message": """Welcome to Dream.OS! You are Agent-4, our DevOps & Infrastructure Specialist.

You keep our systems running smoothly:
• Infrastructure management and cloud platforms
• CI/CD pipelines and automation
• Monitoring, logging, and security
• Performance optimization and disaster recovery

📚 Your Onboarding Materials:
• Main Guide: agent_workspaces/onboarding/README.md
• Your Role: agent_workspaces/onboarding/training_documents/agent_roles_and_responsibilities.md
• Tools Guide: agent_workspaces/onboarding/training_documents/tools_and_technologies.md
• Command Reference: agent_workspaces/onboarding/protocols/command_reference.md

🚀 Next Steps:
1. Review DevOps tools and technologies
2. Set up Docker/Kubernetes environments
3. Practice infrastructure automation
4. Complete the onboarding checklist

You're the guardian of our infrastructure! 🛠️"""
            },
            "Agent-5": {
                "title": "🔍 Welcome Agent-5: Testing & Quality Assurance Specialist",
                "message": """Welcome to Dream.OS! You are Agent-5, our Testing & Quality Assurance Specialist.

You ensure our quality standards:
• Test strategy and automation frameworks
• Quality assurance and reliability testing
• Performance testing and security testing
• Test environment management

📚 Your Onboarding Materials:
• Main Guide: agent_workspaces/onboarding/README.md
• Your Role: agent_workspaces/onboarding/training_documents/agent_roles_and_responsibilities.md
• Development Standards: agent_workspaces/onboarding/training_documents/development_standards.md
• Best Practices: agent_workspaces/onboarding/training_documents/best_practices.md

🚀 Next Steps:
1. Review testing standards and frameworks
2. Set up testing environments
3. Practice test automation workflows
4. Complete the onboarding checklist

You're our quality gatekeeper! 🔍"""
            },
            "Agent-6": {
                "title": "📊 Welcome Agent-6: Data Science & Analytics Specialist",
                "message": """Welcome to Dream.OS! You are Agent-6, our Data Science & Analytics Specialist.

You turn data into insights:
• Data analysis and machine learning
• Data visualization and business intelligence
• Predictive analytics and forecasting
• Data pipeline development

📚 Your Onboarding Materials:
• Main Guide: agent_workspaces/onboarding/README.md
• Your Role: agent_workspaces/onboarding/training_documents/agent_roles_and_responsibilities.md
• Tools Guide: agent_workspaces/onboarding/training_documents/tools_and_technologies.md
• System Overview: agent_workspaces/onboarding/training_documents/system_overview.md

🚀 Next Steps:
1. Review data science tools and frameworks
2. Set up Python data science environment
3. Practice ML and analytics workflows
4. Complete the onboarding checklist

You'll unlock insights that drive our decisions! 📊"""
            },
            "Agent-7": {
                "title": "🔒 Welcome Agent-7: Security & Compliance Specialist",
                "message": """Welcome to Dream.OS! You are Agent-7, our Security & Compliance Specialist.

You protect our systems and data:
• Security architecture and vulnerability assessment
• Compliance management and incident response
• Security monitoring and threat detection
• Security training and awareness

📚 Your Onboarding Materials:
• Main Guide: agent_workspaces/onboarding/README.md
• Your Role: agent_workspaces/onboarding/training_documents/agent_roles_and_responsibilities.md
• Security Protocols: agent_workspaces/onboarding/protocols/agent_protocols.md
• Troubleshooting: agent_workspaces/onboarding/training_documents/troubleshooting.md

🚀 Next Steps:
1. Review security protocols and standards
2. Set up security testing tools
3. Practice incident response procedures
4. Complete the onboarding checklist

You're our security guardian! 🔒"""
            },
            "Agent-8": {
                "title": "📚 Welcome Agent-8: Documentation & Knowledge Management Specialist",
                "message": """Welcome to Dream.OS! You are Agent-8, our Documentation & Knowledge Management Specialist.

You organize and share knowledge:
• Technical documentation and user guides
• API documentation and knowledge management
• Training materials and process documentation
• Information architecture and content management

📚 Your Onboarding Materials:
• Main Guide: agent_workspaces/onboarding/README.md
• Your Role: agent_workspaces/onboarding/training_documents/agent_roles_and_responsibilities.md
• Documentation Standards: agent_workspaces/onboarding/training_documents/development_standards.md
• Getting Started: agent_workspaces/onboarding/training_documents/getting_started.md

🚀 Next Steps:
1. Review documentation standards
2. Set up documentation tools
3. Practice technical writing workflows
4. Complete the onboarding checklist

You'll help us capture and share knowledge effectively! 📚"""
            }
        }
    
    def identify_agent_by_position(self, x, y):
        """Identify which agent is at the given screen position"""
        for agent_name, coords in self.agents.items():
            if 'coordinates' in coords:
                agent_x = coords['coordinates']['x']
                agent_y = coords['coordinates']['y']
                # Check if position is within reasonable range (50 pixels)
                if abs(x - agent_x) <= 50 and abs(y - agent_y) <= 50:
                    return agent_name
        return None
    
    def send_onboarding_message(self, agent_name):
        """Send personalized onboarding message to specific agent"""
        if agent_name not in self.onboarding_messages:
            print(f"❌ No onboarding message found for {agent_name}")
            return False
        
        message_data = self.onboarding_messages[agent_name]
        
        try:
            # Type the title
            pyautogui.typewrite(message_data["title"])
            pyautogui.press('enter')
            pyautogui.press('enter')
            
            # Type the message
            pyautogui.typewrite(message_data["message"])
            pyautogui.press('enter')
            pyautogui.press('enter')
            
            # Add timestamp
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            pyautogui.typewrite(f"📅 Onboarding sent: {timestamp}")
            pyautogui.press('enter')
            
            print(f"✅ Onboarding message sent to {agent_name}")
            return True
            
        except Exception as e:
            print(f"❌ Error sending message to {agent_name}: {e}")
            return False
    
    def run_onboarding_sequence(self):
        """Run the complete onboarding sequence for all agents"""
        print("🚀 Starting Dream.OS Agent Onboarding Sequence")
        print("=" * 60)
        
        if not self.agents:
            print("❌ No agent coordinates found. Please run coordinate_finder.py first.")
            return
        
        print(f"📋 Found {len(self.agents)} agents to onboard:")
        for agent_name in self.agents.keys():
            print(f"   • {agent_name}")
        
        print("\n⏳ Starting onboarding sequence in 5 seconds...")
        print("Please ensure all agent windows are visible and active.")
        time.sleep(5)
        
        success_count = 0
        total_agents = len(self.agents)
        
        for agent_name, coords in self.agents.items():
            print(f"\n🎯 Onboarding {agent_name}...")
            
            if 'coordinates' not in coords:
                print(f"⚠️  No coordinates found for {agent_name}, skipping...")
                continue
            
            x = coords['coordinates']['x']
            y = coords['coordinates']['y']
            
            try:
                # Move to agent position
                pyautogui.moveTo(x, y, duration=1)
                print(f"📍 Moved to {agent_name} at ({x}, {y})")
                
                # Click to activate the agent window
                pyautogui.click()
                time.sleep(2)
                
                # Send onboarding message
                if self.send_onboarding_message(agent_name):
                    success_count += 1
                
                # Wait between agents
                time.sleep(3)
                
            except Exception as e:
                print(f"❌ Error onboarding {agent_name}: {e}")
        
        print("\n" + "=" * 60)
        print(f"🎉 Onboarding sequence completed!")
        print(f"✅ Successfully onboarded: {success_count}/{total_agents} agents")
        
        if success_count == total_agents:
            print("🏆 All agents successfully onboarded!")
        else:
            print(f"⚠️  {total_agents - success_count} agents need manual onboarding")
    
    def onboard_specific_agent(self, agent_name):
        """Onboard a specific agent by name"""
        if agent_name not in self.agents:
            print(f"❌ Agent {agent_name} not found in coordinates")
            return False
        
        if agent_name not in self.onboarding_messages:
            print(f"❌ No onboarding message found for {agent_name}")
            return False
        
        print(f"🎯 Onboarding {agent_name}...")
        
        coords = self.agents[agent_name]
        if 'coordinates' not in coords:
            print(f"❌ No coordinates found for {agent_name}")
            return False
        
        x = coords['coordinates']['x']
        y = coords['coordinates']['y']
        
        try:
            # Move to agent position
            pyautogui.moveTo(x, y, duration=1)
            print(f"📍 Moved to {agent_name} at ({x}, {y})")
            
            # Click to activate the agent window
            pyautogui.click()
            time.sleep(2)
            
            # Send onboarding message
            return self.send_onboarding_message(agent_name)
            
        except Exception as e:
            print(f"❌ Error onboarding {agent_name}: {e}")
            return False

def main():
    """Main function to run the onboarding sequence"""
    print("🎯 Dream.OS Agent Onboarding System")
    print("=" * 50)
    
    onboarding = AgentOnboardingSequence()
    
    if len(sys.argv) > 1:
        # Onboard specific agent
        agent_name = sys.argv[1]
        onboarding.onboard_specific_agent(agent_name)
    else:
        # Run full onboarding sequence
        onboarding.run_onboarding_sequence()

if __name__ == "__main__":
    main()
