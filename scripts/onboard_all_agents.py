#!/usr/bin/env python3
"""
Onboard all Dream.OS agents with personalized messages
Automated onboarding for all 8 agents using PyAutoGUI
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

def get_agent_onboarding_info():
    """Get personalized onboarding information for each agent"""
    return {
        "Agent-1": {
            "role": "System Coordinator & Project Manager",
            "emoji": "🎯",
            "key_responsibilities": [
                "Project coordination and task assignment",
                "Progress monitoring and bottleneck identification", 
                "Conflict resolution and team leadership",
                "Quality assurance and strategic planning"
            ],
            "onboarding_path": "agent_workspaces/onboarding/README.md",
            "priority_docs": [
                "agent_workspaces/onboarding/training_documents/agent_roles_and_responsibilities.md",
                "agent_workspaces/onboarding/protocols/agent_protocols.md",
                "agent_workspaces/onboarding/training_documents/onboarding_checklist.md"
            ]
        },
        "Agent-2": {
            "role": "Frontend Development Specialist",
            "emoji": "🎨",
            "key_responsibilities": [
                "UI/UX development and responsive design",
                "Frontend architecture and component development",
                "Performance optimization and accessibility",
                "Cross-browser compatibility and PWA development"
            ],
            "onboarding_path": "agent_workspaces/onboarding/README.md",
            "priority_docs": [
                "agent_workspaces/onboarding/training_documents/agent_roles_and_responsibilities.md",
                "agent_workspaces/onboarding/training_documents/development_standards.md",
                "agent_workspaces/onboarding/training_documents/tools_and_technologies.md"
            ]
        },
        "Agent-3": {
            "role": "Backend Development Specialist",
            "emoji": "⚙️",
            "key_responsibilities": [
                "API development and database design",
                "Server architecture and microservices",
                "Authentication, authorization, and security",
                "Data processing and external integrations"
            ],
            "onboarding_path": "agent_workspaces/onboarding/README.md",
            "priority_docs": [
                "agent_workspaces/onboarding/training_documents/agent_roles_and_responsibilities.md",
                "agent_workspaces/onboarding/training_documents/development_standards.md",
                "agent_workspaces/onboarding/protocols/workflow_protocols.md"
            ]
        },
        "Agent-4": {
            "role": "DevOps & Infrastructure Specialist",
            "emoji": "🛠️",
            "key_responsibilities": [
                "Infrastructure management and cloud platforms",
                "CI/CD pipelines and automation",
                "Monitoring, logging, and security",
                "Performance optimization and disaster recovery"
            ],
            "onboarding_path": "agent_workspaces/onboarding/README.md",
            "priority_docs": [
                "agent_workspaces/onboarding/training_documents/agent_roles_and_responsibilities.md",
                "agent_workspaces/onboarding/training_documents/tools_and_technologies.md",
                "agent_workspaces/onboarding/protocols/command_reference.md"
            ]
        },
        "Agent-5": {
            "role": "Testing & Quality Assurance Specialist",
            "emoji": "🔍",
            "key_responsibilities": [
                "Test strategy and automation frameworks",
                "Quality assurance and reliability testing",
                "Performance testing and security testing",
                "Test environment management"
            ],
            "onboarding_path": "agent_workspaces/onboarding/README.md",
            "priority_docs": [
                "agent_workspaces/onboarding/training_documents/agent_roles_and_responsibilities.md",
                "agent_workspaces/onboarding/training_documents/development_standards.md",
                "agent_workspaces/onboarding/training_documents/best_practices.md"
            ]
        },
        "Agent-6": {
            "role": "Data Science & Analytics Specialist",
            "emoji": "📊",
            "key_responsibilities": [
                "Data analysis and machine learning",
                "Data visualization and business intelligence",
                "Predictive analytics and forecasting",
                "Data pipeline development"
            ],
            "onboarding_path": "agent_workspaces/onboarding/README.md",
            "priority_docs": [
                "agent_workspaces/onboarding/training_documents/agent_roles_and_responsibilities.md",
                "agent_workspaces/onboarding/training_documents/tools_and_technologies.md",
                "agent_workspaces/onboarding/training_documents/system_overview.md"
            ]
        },
        "Agent-7": {
            "role": "Security & Compliance Specialist",
            "emoji": "🔒",
            "key_responsibilities": [
                "Security architecture and vulnerability assessment",
                "Compliance management and incident response",
                "Security monitoring and threat detection",
                "Security training and awareness"
            ],
            "onboarding_path": "agent_workspaces/onboarding/README.md",
            "priority_docs": [
                "agent_workspaces/onboarding/training_documents/agent_roles_and_responsibilities.md",
                "agent_workspaces/onboarding/protocols/agent_protocols.md",
                "agent_workspaces/onboarding/training_documents/troubleshooting.md"
            ]
        },
        "Agent-8": {
            "role": "Documentation & Knowledge Management Specialist",
            "emoji": "📚",
            "key_responsibilities": [
                "Technical documentation and user guides",
                "API documentation and knowledge management",
                "Training materials and process documentation",
                "Information architecture and content management"
            ],
            "onboarding_path": "agent_workspaces/onboarding/README.md",
            "priority_docs": [
                "agent_workspaces/onboarding/training_documents/agent_roles_and_responsibilities.md",
                "agent_workspaces/onboarding/training_documents/development_standards.md",
                "agent_workspaces/onboarding/training_documents/getting_started.md"
            ]
        }
    }

def create_onboarding_message(agent_name, agent_info):
    """Create personalized onboarding message for agent"""
    emoji = agent_info["emoji"]
    role = agent_info["role"]
    responsibilities = agent_info["key_responsibilities"]
    onboarding_path = agent_info["onboarding_path"]
    priority_docs = agent_info["priority_docs"]
    
    message = f"""{emoji} Welcome {agent_name}: {role}

Your role is essential to our Dream.OS system:

"""
    
    for resp in responsibilities:
        message += f"• {resp}\n"
    
    message += f"""
📚 Your Onboarding Journey:
• Start here: {onboarding_path}
• Your role details: {priority_docs[0]}
• Development standards: {priority_docs[1]}
• Additional resources: {priority_docs[2]}

🚀 Next Steps:
1. Read the main README.md
2. Complete the onboarding checklist
3. Review your specific role responsibilities
4. Practice with team communication protocols

You're now part of our Dream.OS team - let's build something amazing together! 🎉"""
    
    return message

def send_onboarding_to_agent(agent_name, message):
    """Send onboarding message to specific agent"""
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
        print(f"🎯 Onboarding {agent_name} at ({x}, {y})...")
        
        # Move to agent position
        pyautogui.moveTo(x, y, duration=1)
        
        # Click to activate the agent window
        pyautogui.click()
        time.sleep(2)
        
        # Type the message in parts to avoid issues
        lines = message.split('\n')
        for line in lines:
            if line.strip():  # Only type non-empty lines
                pyautogui.typewrite(line)
                pyautogui.press('enter')
                time.sleep(0.5)
        
        # Add timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        pyautogui.typewrite(f"📅 Onboarding completed: {timestamp}")
        pyautogui.press('enter')
        
        print(f"✅ Successfully onboarded {agent_name}")
        return True
        
    except Exception as e:
        print(f"❌ Error onboarding {agent_name}: {e}")
        return False

def onboard_all_agents():
    """Onboard all agents with personalized messages"""
    print("🚀 Dream.OS Agent Onboarding System")
    print("=" * 60)
    
    agents = load_agent_coordinates()
    if not agents:
        print("❌ No agents found. Please run coordinate_finder.py first.")
        return
    
    agent_info = get_agent_onboarding_info()
    
    print(f"📋 Found {len(agents)} agents to onboard:")
    for agent_name in agents.keys():
        if agent_name in agent_info:
            role = agent_info[agent_name]["role"]
            emoji = agent_info[agent_name]["emoji"]
            print(f"   {emoji} {agent_name}: {role}")
    
    print("\n⏳ Starting onboarding sequence in 5 seconds...")
    print("Please ensure all agent windows are visible and active.")
    time.sleep(5)
    
    success_count = 0
    total_agents = len(agents)
    
    for agent_name in agents.keys():
        if agent_name in agent_info:
            print(f"\n🎯 Onboarding {agent_name}...")
            
            # Create personalized message
            message = create_onboarding_message(agent_name, agent_info[agent_name])
            
            # Send onboarding message
            if send_onboarding_to_agent(agent_name, message):
                success_count += 1
            
            # Wait between agents
            time.sleep(3)
        else:
            print(f"⚠️  No onboarding info found for {agent_name}, skipping...")
    
    print("\n" + "=" * 60)
    print(f"🎉 Onboarding sequence completed!")
    print(f"✅ Successfully onboarded: {success_count}/{total_agents} agents")
    
    if success_count == total_agents:
        print("🏆 All agents successfully onboarded!")
        print("\n📚 Next Steps:")
        print("• Each agent should read their onboarding materials")
        print("• Complete the onboarding checklist")
        print("• Begin team collaboration exercises")
        print("• Start working on assigned tasks")
    else:
        print(f"⚠️  {total_agents - success_count} agents need manual onboarding")

def main():
    """Main function"""
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        print("Dream.OS Agent Onboarding System")
        print("=" * 40)
        print("Usage: python onboard_all_agents.py")
        print("This will onboard all agents with personalized messages.")
        print("\nRequirements:")
        print("• Run coordinate_finder.py first to set up agent positions")
        print("• Ensure all agent windows are visible and active")
        print("• Have PyAutoGUI installed")
        return
    
    onboard_all_agents()

if __name__ == "__main__":
    main() 