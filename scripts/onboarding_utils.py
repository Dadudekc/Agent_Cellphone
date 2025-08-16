#!/usr/bin/env python3
"""
Onboarding Utilities - Consolidated Shared Logic
===============================================
This module contains all shared onboarding functionality to eliminate
duplicate code across the scripts directory.
"""

import subprocess
import json
import time
import sys
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

# ============================================================================
# SHARED AGENT INFORMATION
# ============================================================================

AGENT_INFO = {
    "Agent-1": {
        "role": "System Coordinator & Project Manager",
        "emoji": "🎯",
        "key_responsibilities": [
            "Project coordination and task assignment",
            "Progress monitoring and bottleneck identification", 
            "Conflict resolution and team leadership",
            "Quality assurance and strategic planning"
        ],
        "leadership": "You are the team leader and coordinator.",
        "onboarding_path": "D:/repos/Dadudekc/onboarding/README.md",
        "priority_docs": [
            "D:/repos/Dadudekc/onboarding/training_documents/agent_roles_and_responsibilities.md",
            "D:/repos/Dadudekc/onboarding/protocols/agent_protocols.md",
            "D:/repos/Dadudekc/onboarding/training_documents/onboarding_checklist.md"
        ]
    },
    "Agent-2": {
        "role": "Technical Architect & Developer",
        "emoji": "🏗️",
        "key_responsibilities": [
            "System architecture and technical design",
            "Code development and implementation",
            "Technical problem-solving and optimization",
            "Code review and quality assurance"
        ],
        "leadership": "You are the technical lead and architect.",
        "onboarding_path": "D:/repos/Dadudekc/onboarding/README.md",
        "priority_docs": [
            "D:/repos/Dadudekc/onboarding/training_documents/agent_roles_and_responsibilities.md",
            "D:/repos/Dadudekc/onboarding/training_documents/development_standards.md",
            "D:/repos/Dadudekc/onboarding/training_documents/tools_and_technologies.md"
        ]
    },
    "Agent-3": {
        "role": "Data Engineer & Analytics Specialist",
        "emoji": "📊",
        "key_responsibilities": [
            "Data pipeline development and maintenance",
            "Data analysis and insights generation",
            "Database design and optimization",
            "Data quality assurance and governance"
        ],
        "leadership": "You are the data and analytics expert.",
        "onboarding_path": "D:/repos/Dadudekc/onboarding/README.md",
        "priority_docs": [
            "D:/repos/Dadudekc/onboarding/training_documents/agent_roles_and_responsibilities.md",
            "D:/repos/Dadudekc/onboarding/training_documents/development_standards.md",
            "D:/repos/Dadudekc/onboarding/protocols/workflow_protocols.md"
        ]
    },
    "Agent-4": {
        "role": "DevOps Engineer & Infrastructure Specialist",
        "emoji": "⚙️",
        "key_responsibilities": [
            "Infrastructure automation and deployment",
            "System monitoring and reliability",
            "Security implementation and compliance",
            "Performance optimization and scaling"
        ],
        "leadership": "You are the infrastructure and operations expert.",
        "onboarding_path": "D:/repos/Dadudekc/onboarding/README.md",
        "priority_docs": [
            "D:/repos/Dadudekc/onboarding/training_documents/agent_roles_and_responsibilities.md",
            "D:/repos/Dadudekc/onboarding/training_documents/tools_and_technologies.md",
            "D:/repos/Dadudekc/onboarding/protocols/command_reference.md"
        ]
    },
    "Agent-5": {
        "role": "AI/ML Engineer & Algorithm Specialist",
        "emoji": "🤖",
        "key_responsibilities": [
            "Machine learning model development",
            "AI algorithm implementation and optimization",
            "Data preprocessing and feature engineering",
            "Model evaluation and deployment"
        ],
        "leadership": "You are the AI and machine learning expert.",
        "onboarding_path": "D:/repos/Dadudekc/onboarding/README.md",
        "priority_docs": [
            "D:/repos/Dadudekc/onboarding/training_documents/agent_roles_and_responsibilities.md",
            "D:/repos/Dadudekc/onboarding/training_documents/development_standards.md",
            "D:/repos/Dadudekc/onboarding/training_documents/best_practices.md"
        ]
    },
    "Agent-6": {
        "role": "Frontend Developer & UI/UX Specialist",
        "emoji": "🎨",
        "key_responsibilities": [
            "User interface design and development",
            "User experience optimization",
            "Frontend architecture and implementation",
            "Cross-platform compatibility and accessibility"
        ],
        "leadership": "You are the user experience and interface expert.",
        "onboarding_path": "agent_workspaces/onboarding/README.md",
        "priority_docs": [
            "agent_workspaces/onboarding/training_documents/agent_roles_and_responsibilities.md",
            "agent_workspaces/onboarding/training_documents/development_standards.md",
            "agent_workspaces/onboarding/training_documents/tools_and_technologies.md"
        ]
    },
    "Agent-7": {
        "role": "Backend Developer & API Specialist",
        "emoji": "🔧",
        "key_responsibilities": [
            "Backend API development and maintenance",
            "Database design and optimization",
            "Server-side logic and business rules",
            "API security and performance optimization"
        ],
        "leadership": "You are the backend and API development expert.",
        "onboarding_path": "agent_workspaces/onboarding/README.md",
        "priority_docs": [
            "agent_workspaces/onboarding/training_documents/agent_roles_and_responsibilities.md",
            "agent_workspaces/onboarding/training_documents/development_standards.md",
            "agent_workspaces/onboarding/protocols/workflow_protocols.md"
        ]
    },
    "Agent-8": {
        "role": "Quality Assurance & Testing Specialist",
        "emoji": "🔍",
        "key_responsibilities": [
            "Test strategy and planning",
            "Automated testing implementation",
            "Quality assurance and bug detection",
            "Performance and security testing"
        ],
        "leadership": "You are the quality assurance and testing expert.",
        "onboarding_path": "agent_workspaces/onboarding/README.md",
        "priority_docs": [
            "agent_workspaces/onboarding/training_documents/agent_roles_and_responsibilities.md",
            "agent_workspaces/onboarding/training_documents/development_standards.md",
            "agent_workspaces/onboarding/training_documents/best_practices.md"
        ]
    }
}

# ============================================================================
# SHARED UTILITY FUNCTIONS
# ============================================================================

def run_cli_command(cmd_args: List[str], description: str = "", use_emojis: bool = True) -> bool:
    """Run a CLI command and return the result"""
    try:
        if use_emojis:
            print(f"📤 {description}")
        else:
            print(f"Sending: {description}")
            
        result = subprocess.run(cmd_args, capture_output=True, text=True, cwd=project_root)
        
        if result.returncode == 0:
            if use_emojis:
                print(f"✅ Success: {result.stdout.strip()}")
            else:
                print(f"Success: {result.stdout.strip()}")
            return True
        else:
            if use_emojis:
                print(f"❌ Error: {result.stderr.strip()}")
            else:
                print(f"Error: {result.stderr.strip()}")
            return False
            
    except Exception as e:
        if use_emojis:
            print(f"❌ Exception: {e}")
        else:
            print(f"Exception: {e}")
        return False

def load_agent_coordinates() -> Dict:
    """Load agent coordinates from the coordinate finder"""
    try:
        coordinates_file = project_root / "src" / "runtime" / "config" / "cursor_agent_coords.json"
        if coordinates_file.exists():
            with open(coordinates_file, 'r') as f:
                return json.load(f)
        else:
            print("❌ No agent coordinates found. Please run coordinate_finder.py first.")
            return {}
    except Exception as e:
        print(f"❌ Error loading agent coordinates: {e}")
        return {}

def get_agent_info(agent_name: str) -> Dict:
    """Get agent information for the specified agent"""
    return AGENT_INFO.get(agent_name, {
        "role": "Team Member",
        "emoji": "👤",
        "key_responsibilities": ["General team support and collaboration"],
        "leadership": "You are a valuable team member.",
        "onboarding_path": "agent_workspaces/onboarding/README.md",
        "priority_docs": [
            "agent_workspaces/onboarding/training_documents/agent_roles_and_responsibilities.md",
            "agent_workspaces/onboarding/training_documents/development_standards.md",
            "agent_workspaces/onboarding/training_documents/best_practices.md"
        ]
    })

# ============================================================================
# MESSAGE CREATION FUNCTIONS
# ============================================================================

def create_comprehensive_onboarding_message(agent_name: str, style: str = "full") -> str:
    """
    Create a comprehensive onboarding message for the specified agent
    
    Args:
        agent_name: Name of the agent (e.g., "Agent-1")
        style: Message style - "full" (with emojis), "ascii" (ASCII only), "simple" (no emojis)
    """
    info = get_agent_info(agent_name)
    
    # Choose bullet point style based on format
    if style == "ascii":
        bullet = "* "
        emoji = ""
    else:
        bullet = "• "
        emoji = info.get("emoji", "👤")
    
    # Build the comprehensive message
    if style == "full":
        message = f"""{emoji} WELCOME TO DREAM.OS - COMPREHENSIVE ONBOARDING

🎯 YOUR ROLE: {agent_name} - {info['role']}

{info['leadership']} Your role is essential to our autonomous agent system success.

📋 YOUR KEY RESPONSIBILITIES:
"""
    else:
        message = f"""WELCOME TO DREAM.OS - COMPREHENSIVE ONBOARDING

YOUR ROLE: {agent_name} - {info['role']}

{info['leadership']} Your role is essential to our autonomous agent system success.

YOUR KEY RESPONSIBILITIES:
"""
    
    for resp in info['key_responsibilities']:
        message += f"{bullet}{resp}\n"
    
    if style == "full":
        message += f"""
 🏗️ SYSTEM OVERVIEW:
Dream.OS is an autonomous multi-agent system where agents work together to:
{bullet}Coordinate tasks and projects autonomously
{bullet}Communicate through structured messaging protocols
{bullet}Maintain individual workspaces and status tracking
{bullet}Collaborate on complex technical projects
{bullet}Self-manage and validate their work

 🌐 ENVIRONMENT MODEL (Cursor + shared repo/files):
 {bullet}Agents are Cursor-based. ACP types messages directly into each agent’s Cursor input box using calibrated coordinates.
 {bullet}All agents work on the same repositories/files on disk (e.g., D:\\repositories\\...). Use repo-relative paths in prompts.
 {bullet}Coordinate using each repo’s TASK_LIST.md and status.json; avoid duplication; prefer reuse/refactor; commit small, verifiable edits.
 {bullet}Messaging channels: (1) Visible UI typing via ACP, (2) Silent JSON file inbox at agent_workspaces/Agent-N/inbox/.
 {bullet}Run tools from D:\\Agent_Cellphone so paths resolve correctly.

📚 YOUR ONBOARDING MATERIALS (READ THESE IN ORDER):
1. MAIN GUIDE: agent_workspaces/onboarding/README.md
   - Complete system overview and getting started
   
2. YOUR ROLE: agent_workspaces/onboarding/training_documents/agent_roles_and_responsibilities.md
   - Detailed role-specific responsibilities and expectations
   
3. DEVELOPMENT STANDARDS: agent_workspaces/onboarding/DEVELOPMENT_STANDARDS.md
   - Coding standards, best practices, and quality guidelines
   
4. CORE PROTOCOLS: agent_workspaces/onboarding/CORE_PROTOCOLS.md
   - Communication protocols and system interactions
   
5. BEST PRACTICES: agent_workspaces/onboarding/BEST_PRACTICES.md
   - Proven approaches for effective agent operation

🛠️ ESSENTIAL TOOLS AND COMMANDS:

CLI COMMUNICATION TOOL:
python src/agent_cell_phone.py -a [target_agent] -m "[message]" -t [type]

Examples:
{bullet}Send message to Agent-2: python src/agent_cell_phone.py -a Agent-2 -m "Hello from {agent_name}!" -t normal
{bullet}Send status update: python src/agent_cell_phone.py -a Agent-1 -m "Task completed successfully" -t status
{bullet}Broadcast to all: python src/agent_cell_phone.py -a all -m "System update" -t broadcast

MESSAGE TYPES:
{bullet}normal: Regular communication
{bullet}status: Status updates and progress reports
{bullet}onboarding: Onboarding-related messages
{bullet}command: System commands and instructions
{bullet}broadcast: System-wide announcements

📁 YOUR WORKSPACE STRUCTURE:
agent_workspaces/{agent_name}/
├── inbox/          # Incoming messages
├── outbox/         # Outgoing messages
├── tasks/          # Current tasks and assignments
├── status.json     # Your current status and progress
├── notes.md        # Your personal notes and observations
└── logs/           # Activity logs

🚀 IMMEDIATE NEXT STEPS:
1. READ THE MAIN README: Start with agent_workspaces/onboarding/README.md
2. REVIEW YOUR ROLE: Study agent_workspaces/onboarding/training_documents/agent_roles_and_responsibilities.md
3. SETUP YOUR STATUS: Update your status.json with current progress
4. TEST COMMUNICATION: Send a test message to another agent using the CLI tool
5. COMPLETE CHECKLIST: Work through the onboarding checklist systematically

✅ SUCCESS TIPS:
{bullet}Always maintain your status.json with current progress
{bullet}Use structured communication protocols
{bullet}Collaborate actively with other agents
{bullet}Follow development standards and best practices
{bullet}Take initiative in your area of expertise
{bullet}Document your work and share knowledge

📋 EXPECTATIONS:
{bullet}Complete onboarding within 24 hours
{bullet}Maintain active status updates
{bullet}Participate in team communications
{bullet}Contribute to system improvements
{bullet}Follow established protocols and standards

🎉 Welcome to the Dream.OS team - let's build something amazing together!"""
    else:
        message += f"""
 SYSTEM OVERVIEW:
Dream.OS is an autonomous multi-agent system where agents work together to:
{bullet}Coordinate tasks and projects autonomously
{bullet}Communicate through structured messaging protocols
{bullet}Maintain individual workspaces and status tracking
{bullet}Collaborate on complex technical projects
{bullet}Self-manage and validate their work

 ENVIRONMENT MODEL (Cursor + shared repo/files):
 {bullet}Agents are Cursor-based. ACP types messages directly into each agent’s Cursor input box using calibrated coordinates.
 {bullet}All agents work on the same repositories/files on disk (e.g., D:\\repositories\\...). Use repo-relative paths in prompts.
 {bullet}Coordinate using each repo’s TASK_LIST.md and status.json; avoid duplication; prefer reuse/refactor; commit small, verifiable edits.
 {bullet}Messaging channels: (1) Visible UI typing via ACP, (2) Silent JSON file inbox at agent_workspaces/Agent-N/inbox/.
 {bullet}Run tools from D:\\Agent_Cellphone so paths resolve correctly.

YOUR ONBOARDING MATERIALS (READ THESE IN ORDER):
1. MAIN GUIDE: agent_workspaces/onboarding/README.md
   - Complete system overview and getting started
   
2. YOUR ROLE: agent_workspaces/onboarding/training_documents/agent_roles_and_responsibilities.md
   - Detailed role-specific responsibilities and expectations
   
3. DEVELOPMENT STANDARDS: agent_workspaces/onboarding/DEVELOPMENT_STANDARDS.md
   - Coding standards, best practices, and quality guidelines
   
4. CORE PROTOCOLS: agent_workspaces/onboarding/CORE_PROTOCOLS.md
   - Communication protocols and system interactions
   
5. BEST PRACTICES: agent_workspaces/onboarding/BEST_PRACTICES.md
   - Proven approaches for effective agent operation

ESSENTIAL TOOLS AND COMMANDS:

CLI COMMUNICATION TOOL:
python src/agent_cell_phone.py -a [target_agent] -m "[message]" -t [type]

Examples:
{bullet}Send message to Agent-2: python src/agent_cell_phone.py -a Agent-2 -m "Hello from {agent_name}!" -t normal
{bullet}Send status update: python src/agent_cell_phone.py -a Agent-1 -m "Task completed successfully" -t status
{bullet}Broadcast to all: python src/agent_cell_phone.py -a all -m "System update" -t broadcast

MESSAGE TYPES:
{bullet}normal: Regular communication
{bullet}status: Status updates and progress reports
{bullet}onboarding: Onboarding-related messages
{bullet}command: System commands and instructions
{bullet}broadcast: System-wide announcements

YOUR WORKSPACE STRUCTURE:
agent_workspaces/{agent_name}/
- inbox/          # Incoming messages
- outbox/         # Outgoing messages
- tasks/          # Current tasks and assignments
- status.json     # Your current status and progress
- notes.md        # Your personal notes and observations
- logs/           # Activity logs

IMMEDIATE NEXT STEPS:
1. READ THE MAIN README: Start with agent_workspaces/onboarding/README.md
2. REVIEW YOUR ROLE: Study agent_workspaces/onboarding/training_documents/agent_roles_and_responsibilities.md
3. SETUP YOUR STATUS: Update your status.json with current progress
4. TEST COMMUNICATION: Send a test message to another agent using the CLI tool
5. COMPLETE CHECKLIST: Work through the onboarding checklist systematically

SUCCESS TIPS:
{bullet}Always maintain your status.json with current progress
{bullet}Use structured communication protocols
{bullet}Collaborate actively with other agents
{bullet}Follow development standards and best practices
{bullet}Take initiative in your area of expertise
{bullet}Document your work and share knowledge

EXPECTATIONS:
{bullet}Complete onboarding within 24 hours
{bullet}Maintain active status updates
{bullet}Participate in team communications
{bullet}Contribute to system improvements
{bullet}Follow established protocols and standards

Welcome to the Dream.OS team - let's build something amazing together!"""
    
    return message

def create_simple_onboarding_message(agent_name: str) -> str:
    """Create a simple onboarding message for the specified agent"""
    info = get_agent_info(agent_name)
    
    message = f"""Welcome {agent_name}! You are our {info['role']}.

Your role is essential to our Dream.OS system:

"""
    for resp in info['key_responsibilities']:
        message += f"• {resp}\n"
    
    message += f"""
📚 Your Onboarding Journey:
• Start here: {info['onboarding_path']}
• Your role details: {info['priority_docs'][0]}
• Development standards: {info['priority_docs'][1]}
• Additional resources: {info['priority_docs'][2]}

🚀 Next Steps:
1. Read the main README.md
2. Complete the onboarding checklist
3. Review your specific role responsibilities
4. Practice with team communication protocols

You're now part of our Dream.OS team - let's build something amazing together! 🎉"""
    
    return message

# ============================================================================
# MESSAGE SENDING FUNCTIONS
# ============================================================================

def send_onboarding_message(agent_name: str, style: str = "full", use_emojis: bool = True) -> bool:
    """
    Send onboarding message to specific agent using CLI tool
    
    Args:
        agent_name: Name of the agent to send message to
        style: Message style - "full", "ascii", "simple"
        use_emojis: Whether to use emojis in console output
    """
    try:
        # Create the message
        message = create_comprehensive_onboarding_message(agent_name, style)
        
        # Use CLI tool to send message
        cmd = [
            "python", "src/agent_cell_phone.py",
            "-a", agent_name,
            "-m", message,
            "-t", "onboarding"
        ]
        
        description = f"onboarding message to {agent_name}"
        return run_cli_command(cmd, description, use_emojis)
                
    except Exception as e:
        if use_emojis:
            print(f"❌ Error sending message to {agent_name}: {e}")
        else:
            print(f"Error sending message to {agent_name}: {e}")
        return False

def send_onboarding_to_all_agents(style: str = "full", use_emojis: bool = True) -> Dict[str, bool]:
    """
    Send onboarding messages to all available agents
    
    Args:
        style: Message style - "full", "ascii", "simple"
        use_emojis: Whether to use emojis in console output
    
    Returns:
        Dictionary mapping agent names to success status
    """
    agents = load_agent_coordinates()
    
    if not agents:
        if use_emojis:
            print("❌ No agents found in coordinate configuration")
        else:
            print("No agents found in coordinate configuration")
        return {}
    
    # Get all available agents
    available_agents = []
    for layout_mode, agent_dict in agents.items():
        available_agents.extend(list(agent_dict.keys()))
    
    if use_emojis:
        print(f"📋 Found {len(available_agents)} agents: {', '.join(available_agents)}")
    else:
        print(f"Found {len(available_agents)} agents: {', '.join(available_agents)}")
    
    results = {}
    
    for agent_name in available_agents:
        if use_emojis:
            print(f"\n🎯 Onboarding {agent_name}...")
        else:
            print(f"\nOnboarding {agent_name}...")
            
        success = send_onboarding_message(agent_name, style, use_emojis)
        results[agent_name] = success
        
        if success:
            time.sleep(2)  # Brief pause between messages
    
    return results

# ============================================================================
# DEMO AND COMPARISON FUNCTIONS
# ============================================================================

def get_chunked_vs_comprehensive_comparison() -> Dict[str, str]:
    """Get comparison between chunked and comprehensive approaches"""
    return {
        "chunked": """
CHUNKED APPROACH EXAMPLE:

Chunk 1: Welcome to Dream.OS! You are Agent-1, our System Coordinator & Project Manager.

Chunk 2: Your role is crucial to our success: Project coordination and task assignment...

Chunk 3: Your Onboarding Materials: Main Guide: agent_workspaces/onboarding/README.md...

Chunk 4: Next Steps: 1. Read the main README.md, 2. Complete the onboarding checklist...

PROBLEMS WITH CHUNKED APPROACH:
❌ Fragmented information
❌ Information gaps between chunks
❌ No system overview
❌ Missing tools and protocols
❌ Unclear next steps
❌ Agent confusion
        """,
        
        "comprehensive": """
COMPREHENSIVE APPROACH EXAMPLE:

WELCOME TO DREAM.OS - COMPREHENSIVE ONBOARDING

YOUR ROLE: Agent-1 - System Coordinator & Project Manager

You are the team leader and coordinator. Your role is essential to our autonomous agent system success.

YOUR KEY RESPONSIBILITIES:
* Project coordination and task assignment
* Progress monitoring and bottleneck identification
* Conflict resolution and team leadership
* Quality assurance and strategic planning

SYSTEM OVERVIEW:
Dream.OS is an autonomous multi-agent system where agents work together to:
* Coordinate tasks and projects autonomously
* Communicate through structured messaging protocols
* Maintain individual workspaces and status tracking
* Collaborate on complex technical projects
* Self-manage and validate their work

YOUR ONBOARDING MATERIALS (READ THESE IN ORDER):
1. MAIN GUIDE: agent_workspaces/onboarding/README.md
2. YOUR ROLE: agent_workspaces/onboarding/training_documents/agent_roles_and_responsibilities.md
3. DEVELOPMENT STANDARDS: agent_workspaces/onboarding/DEVELOPMENT_STANDARDS.md
4. CORE PROTOCOLS: agent_workspaces/onboarding/CORE_PROTOCOLS.md
5. BEST PRACTICES: agent_workspaces/onboarding/BEST_PRACTICES.md

ESSENTIAL TOOLS AND COMMANDS:
CLI COMMUNICATION TOOL:
python src/agent_cell_phone.py -a [target_agent] -m "[message]" -t [type]

Examples:
* Send message to Agent-2: python src/agent_cell_phone.py -a Agent-2 -m "Hello from Agent-1!" -t normal
* Send status update: python src/agent_cell_phone.py -a Agent-1 -m "Task completed successfully" -t status
* Broadcast to all: python src/agent_cell_phone.py -a all -m "System update" -t broadcast

MESSAGE TYPES:
* normal: Regular communication
* status: Status updates and progress reports
* onboarding: Onboarding-related messages
* command: System commands and instructions
* broadcast: System-wide announcements

YOUR WORKSPACE STRUCTURE:
agent_workspaces/Agent-1/
- inbox/          # Incoming messages
- outbox/         # Outgoing messages
- tasks/          # Current tasks and assignments
- status.json     # Your current status and progress
- notes.md        # Your personal notes and observations
- logs/           # Activity logs

IMMEDIATE NEXT STEPS:
1. READ THE MAIN README: Start with agent_workspaces/onboarding/README.md
2. REVIEW YOUR ROLE: Study agent_workspaces/onboarding/training_documents/agent_roles_and_responsibilities.md
3. SETUP YOUR STATUS: Update your status.json with current progress
4. TEST COMMUNICATION: Send a test message to another agent using the CLI tool
5. COMPLETE CHECKLIST: Work through the onboarding checklist systematically

SUCCESS TIPS:
* Always maintain your status.json with current progress
* Use structured communication protocols
* Collaborate actively with other agents
* Follow development standards and best practices
* Take initiative in your area of expertise
* Document your work and share knowledge

EXPECTATIONS:
* Complete onboarding within 24 hours
* Maintain active status updates
* Participate in team communications
* Contribute to system improvements
* Follow established protocols and standards

BENEFITS OF COMPREHENSIVE APPROACH:
✅ Complete information in one message
✅ No information fragmentation
✅ Clear system overview
✅ Complete tools and protocols
✅ Clear next steps
✅ Better agent understanding
✅ Faster onboarding
✅ Professional formatting
        """
    }

def print_onboarding_summary(results: Dict[str, bool], use_emojis: bool = True):
    """Print a summary of onboarding results"""
    total_agents = len(results)
    successful = sum(1 for success in results.values() if success)
    failed = total_agents - successful
    
    if use_emojis:
        print(f"\n📊 Onboarding Summary:")
        print(f"  Total Agents: {total_agents}")
        print(f"  Successful: {successful}")
        print(f"  Failed: {failed}")
        
        if successful == total_agents:
            print("🎉 All agents onboarded successfully!")
        else:
            print("⚠️ Some agents failed to onboard")
    else:
        print(f"\nOnboarding Summary:")
        print(f"  Total Agents: {total_agents}")
        print(f"  Successful: {successful}")
        print(f"  Failed: {failed}")
        
        if successful == total_agents:
            print("All agents onboarded successfully!")
        else:
            print("Some agents failed to onboard") 