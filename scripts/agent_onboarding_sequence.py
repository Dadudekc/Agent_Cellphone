#!/usr/bin/env python3
"""
Dream.OS Agent Onboarding Sequence
Automated onboarding system using the CLI tool to send personalized onboarding messages.
"""

import json
import time
import os
import sys
import subprocess
from datetime import datetime
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from coordinate_finder import load_existing_coordinates

class AgentOnboardingSequence:
    """Automated onboarding system for Dream.OS agents using CLI tool"""
    
    def __init__(self):
        self.agents = self.load_agent_coordinates()
        self.onboarding_messages = self.load_onboarding_messages()
        
    def load_agent_coordinates(self):
        """Load agent coordinates from the coordinate finder"""
        try:
            # Use the imported function to load coordinates
            coordinates = load_existing_coordinates()
            if coordinates:
                return coordinates
            else:
                print("⚠️  No agent coordinates found. Please run coordinate_finder.py first.")
                return {}
        except Exception as e:
            print(f"❌ Error loading agent coordinates: {e}")
            return {}
    
    def load_onboarding_messages(self):
        """Load personalized onboarding messages for each agent (ASCII only)"""
        return {
            "Agent-1": {
                "title": "Welcome Agent-1: System Coordinator & Project Manager",
                "message": """Welcome to Dream.OS! You are Agent-1, our System Coordinator & Project Manager.\n\nYour role is crucial to our success:\n- Project coordination and task assignment\n- Progress monitoring and bottleneck identification\n- Conflict resolution and team leadership\n- Quality assurance and strategic planning\n\nYour Onboarding Materials:\n- Main Guide: agent_workspaces/onboarding/README.md\n- Your Role: agent_workspaces/onboarding/training_documents/agent_roles_and_responsibilities.md\n- Protocols: agent_workspaces/onboarding/protocols/agent_protocols.md\n- Checklist: agent_workspaces/onboarding/training_documents/onboarding_checklist.md\n\nNext Steps:\n1. Read the main README.md\n2. Complete the onboarding checklist\n3. Review your specific role responsibilities\n4. Practice with the team communication protocols\n\nIMPORTANT: Use the CLI tool for all agent communication:\npython src/agent_cell_phone.py -a Agent-2 -m \"Hello from Agent-1!\" -t normal\n\nYou are the leader of our team. Let's build something amazing together!"""
            },
            "Agent-2": {
                "title": "Welcome Agent-2: Frontend Development Specialist",
                "message": """Welcome to Dream.OS! You are Agent-2, our Frontend Development Specialist.\n\nYour expertise drives our user experience:\n- UI/UX development and responsive design\n- Frontend architecture and component development\n- Performance optimization and accessibility\n- Cross-browser compatibility and PWA development\n\nYour Onboarding Materials:\n- Main Guide: agent_workspaces/onboarding/README.md\n- Your Role: agent_workspaces/onboarding/training_documents/agent_roles_and_responsibilities.md\n- Development Standards: agent_workspaces/onboarding/training_documents/development_standards.md\n- Tools Guide: agent_workspaces/onboarding/training_documents/tools_and_technologies.md\n\nNext Steps:\n1. Review frontend development standards\n2. Set up your development environment\n3. Practice with React/Vue.js/Angular workflows\n4. Complete the onboarding checklist\n\nIMPORTANT: Use the CLI tool for all agent communication:\npython src/agent_cell_phone.py -a Agent-1 -m \"Frontend environment ready\" -t reply\n\nYour designs will shape how users interact with our systems."""
            },
            "Agent-3": {
                "title": "Welcome Agent-3: Backend Development Specialist",
                "message": """Welcome to Dream.OS! You are Agent-3, our Backend Development Specialist.\n\nYou're the backbone of our systems:\n- API development and database design\n- Server architecture and microservices\n- Authentication, authorization, and security\n- Data processing and external integrations\n\nYour Onboarding Materials:\n- Main Guide: agent_workspaces/onboarding/README.md\n- Your Role: agent_workspaces/onboarding/training_documents/agent_roles_and_responsibilities.md\n- Development Standards: agent_workspaces/onboarding/training_documents/development_standards.md\n- Workflow Protocols: agent_workspaces/onboarding/protocols/workflow_protocols.md\n\nNext Steps:\n1. Review backend development standards\n2. Set up Python/Node.js/Java environments\n3. Practice API development workflows\n4. Complete the onboarding checklist\n\nIMPORTANT: Use the CLI tool for all agent communication:\npython src/agent_cell_phone.py -a Agent-1 -m \"Backend environment ready\" -t reply\n\nYour APIs will power everything we build!"""
            },
            "Agent-4": {
                "title": "Welcome Agent-4: DevOps & Infrastructure Specialist",
                "message": """Welcome to Dream.OS! You are Agent-4, our DevOps & Infrastructure Specialist.\n\nYou keep our systems running smoothly:\n- Infrastructure management and cloud platforms\n- CI/CD pipelines and automation\n- Monitoring, logging, and security\n- Performance optimization and disaster recovery\n\nYour Onboarding Materials:\n- Main Guide: agent_workspaces/onboarding/README.md\n- Your Role: agent_workspaces/onboarding/training_documents/agent_roles_and_responsibilities.md\n- Tools Guide: agent_workspaces/onboarding/training_documents/tools_and_technologies.md\n- Command Reference: agent_workspaces/onboarding/protocols/command_reference.md\n\nNext Steps:\n1. Review DevOps tools and technologies\n2. Set up Docker/Kubernetes environments\n3. Practice infrastructure automation\n4. Complete the onboarding checklist\n\nIMPORTANT: Use the CLI tool for all agent communication:\npython src/agent_cell_phone.py -a Agent-1 -m \"DevOps environment ready\" -t reply\n\nYou're the guardian of our infrastructure!"""
            },
            "Agent-5": {
                "title": "Welcome Agent-5: Testing & Quality Assurance Specialist",
                "message": """Welcome to Dream.OS! You are Agent-5, our Testing & Quality Assurance Specialist.\n\nYou ensure our quality standards:\n- Test strategy and automation frameworks\n- Quality assurance and reliability testing\n- Performance testing and security testing\n- Test environment management\n\nYour Onboarding Materials:\n- Main Guide: agent_workspaces/onboarding/README.md\n- Your Role: agent_workspaces/onboarding/training_documents/agent_roles_and_responsibilities.md\n- Development Standards: agent_workspaces/onboarding/training_documents/development_standards.md\n- Best Practices: agent_workspaces/onboarding/training_documents/best_practices.md\n\nNext Steps:\n1. Review testing standards and frameworks\n2. Set up testing environments\n3. Practice test automation workflows\n4. Complete the onboarding checklist\n\nIMPORTANT: Use the CLI tool for all agent communication:\npython src/agent_cell_phone.py -a Agent-1 -m \"Testing environment ready\" -t reply\n\nYou're our quality gatekeeper!"""
            },
            "Agent-6": {
                "title": "Welcome Agent-6: Data Science & Analytics Specialist",
                "message": """Welcome to Dream.OS! You are Agent-6, our Data Science & Analytics Specialist.\n\nYou turn data into insights:\n- Data analysis and machine learning\n- Data visualization and business intelligence\n- Predictive analytics and forecasting\n- Data pipeline development\n\nYour Onboarding Materials:\n- Main Guide: agent_workspaces/onboarding/README.md\n- Your Role: agent_workspaces/onboarding/training_documents/agent_roles_and_responsibilities.md\n- Tools Guide: agent_workspaces/onboarding/training_documents/tools_and_technologies.md\n- System Overview: agent_workspaces/onboarding/training_documents/system_overview.md\n\nNext Steps:\n1. Review data science tools and frameworks\n2. Set up Python data science environment\n3. Practice ML and analytics workflows\n4. Complete the onboarding checklist\n\nIMPORTANT: Use the CLI tool for all agent communication:\npython src/agent_cell_phone.py -a Agent-1 -m \"Data science environment ready\" -t reply\n\nYou'll unlock insights that drive our decisions!"""
            },
            "Agent-7": {
                "title": "Welcome Agent-7: Security & Compliance Specialist",
                "message": """Welcome to Dream.OS! You are Agent-7, our Security & Compliance Specialist.\n\nYou protect our systems and data:\n- Security architecture and vulnerability assessment\n- Compliance management and incident response\n- Security monitoring and threat detection\n- Security training and awareness\n\nYour Onboarding Materials:\n- Main Guide: agent_workspaces/onboarding/README.md\n- Your Role: agent_workspaces/onboarding/training_documents/agent_roles_and_responsibilities.md\n- Security Protocols: agent_workspaces/onboarding/protocols/security_protocols.md\n- Compliance Standards: agent_workspaces/onboarding/training_documents/compliance_standards.md\n\nNext Steps:\n1. Review security protocols and standards\n2. Set up security monitoring tools\n3. Practice incident response procedures\n4. Complete the onboarding checklist\n\nIMPORTANT: Use the CLI tool for all agent communication:\npython src/agent_cell_phone.py -a Agent-1 -m \"Security environment ready\" -t reply\n\nYou're our security guardian!"""
            },
            "Agent-8": {
                "title": "Welcome Agent-8: Integration & API Specialist",
                "message": """Welcome to Dream.OS! You are Agent-8, our Integration & API Specialist.\n\nYou connect all our systems:\n- API integration and middleware development\n- System integration and data synchronization\n- Third-party service integration\n- API documentation and developer experience\n\nYour Onboarding Materials:\n- Main Guide: agent_workspaces/onboarding/README.md\n- Your Role: agent_workspaces/onboarding/training_documents/agent_roles_and_responsibilities.md\n- Integration Protocols: agent_workspaces/onboarding/protocols/integration_protocols.md\n- API Standards: agent_workspaces/onboarding/training_documents/api_standards.md\n\nNext Steps:\n1. Review integration protocols and API standards\n2. Set up integration testing environment\n3. Practice API integration workflows\n4. Complete the onboarding checklist\n\nIMPORTANT: Use the CLI tool for all agent communication:\npython src/agent_cell_phone.py -a Agent-1 -m \"Integration environment ready\" -t reply\n\nYou'll connect everything together!"""
            }
        }
    
    def send_onboarding_message(self, agent_name):
        """Send onboarding message to specific agent using CLI tool"""
        if agent_name not in self.onboarding_messages:
            print(f"❌ No onboarding message found for {agent_name}")
            return False
        
        message_data = self.onboarding_messages[agent_name]
        
        try:
            # Use CLI tool to send message
            cmd = [
                "python", "src/agent_cell_phone.py",
                "-a", agent_name,
                "-m", message_data["message"],
                "-t", "onboarding"
            ]
            
            print(f"📤 Sending onboarding message to {agent_name}...")
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=project_root)
            
            if result.returncode == 0:
                print(f"✅ Onboarding message sent to {agent_name}")
                return True
            else:
                print(f"❌ Failed to send message to {agent_name}: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Error sending message to {agent_name}: {e}")
            return False
    
    def run_onboarding_sequence(self, test_mode=False):
        """Run the complete onboarding sequence for all agents"""
        print("🚀 Starting Dream.OS Agent Onboarding Sequence")
        print("=" * 60)
        
        if test_mode:
            print("🧪 Running in TEST MODE - no actual messages will be sent")
        
        # Get available agents from coordinates
        available_agents = []
        for layout_mode, agents in self.agents.items():
            available_agents.extend(list(agents.keys()))
        
        if not available_agents:
            print("❌ No agents found in coordinate configuration")
            return False
        
        print(f"📋 Found {len(available_agents)} agents: {', '.join(available_agents)}")
        
        success_count = 0
        total_agents = len(available_agents)
        
        for agent_name in available_agents:
            print(f"\n🎯 Onboarding {agent_name}...")
            
            if test_mode:
                print(f"🧪 TEST MODE: Would send onboarding message to {agent_name}")
                success_count += 1
            else:
                if self.send_onboarding_message(agent_name):
                    success_count += 1
                    time.sleep(2)  # Brief pause between messages
                else:
                    print(f"⚠️ Failed to onboard {agent_name}")
        
        print(f"\n📊 Onboarding Summary:")
        print(f"  Total Agents: {total_agents}")
        print(f"  Successful: {success_count}")
        print(f"  Failed: {total_agents - success_count}")
        
        if success_count == total_agents:
            print("🎉 All agents onboarded successfully!")
            return True
        else:
            print("⚠️ Some agents failed to onboard")
            return False
    
    def onboard_specific_agent(self, agent_name):
        """Onboard a specific agent"""
        print(f"🎯 Onboarding specific agent: {agent_name}")
        
        if agent_name not in self.onboarding_messages:
            print(f"❌ No onboarding message found for {agent_name}")
            return False
        
        return self.send_onboarding_message(agent_name)

def main():
    """Main function to run onboarding sequence"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Dream.OS Agent Onboarding Sequence")
    parser.add_argument("--test", action="store_true", help="Run in test mode (no actual messages)")
    parser.add_argument("--agent", help="Onboard specific agent (e.g., Agent-1)")
    parser.add_argument("--list-agents", action="store_true", help="List available agents")
    
    args = parser.parse_args()
    
    onboarding = AgentOnboardingSequence()
    
    if args.list_agents:
        print("📋 Available agents:")
        for layout_mode, agents in onboarding.agents.items():
            print(f"  {layout_mode}: {', '.join(agents.keys())}")
        return
    
    if args.agent:
        success = onboarding.onboard_specific_agent(args.agent)
        if success:
            print(f"✅ Successfully onboarded {args.agent}")
        else:
            print(f"❌ Failed to onboard {args.agent}")
    else:
        onboarding.run_onboarding_sequence(test_mode=args.test)

if __name__ == "__main__":
    main()
