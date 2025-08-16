#!/usr/bin/env python3
"""
Send PRD Instructions to Agents 1-4 (Simplified)
================================================
Directly uses AgentCellPhone to send PRD creation/modification instructions.
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from services.agent_cell_phone import AgentCellPhone, MsgTag

def send_prd_instructions():
    """Send PRD creation/modification instructions to all agents"""
    print("🎖️ CAPTAIN Agent-5 Sending PRD Instructions")
    print("=" * 50)
    
    # Initialize AgentCellPhone
    acp = AgentCellPhone(agent_id="Agent-5", layout_mode="5-agent", test=False)
    
    # Get agent repository assignments from D:\repos\Dadudekc
    agent_repos = {
        "Agent-1": ["AI_Debugger_Assistant", "DigitalDreamscape", "FreeRideInvestor", "Hive-Mind", "MeT"],
        "Agent-2": ["Auto_Blogger", "Dream.os", "FreeWork", "IT_help_desk", "NewSims4ModProject"],
        "Agent-3": ["DaDudeKC-Website", "DreamVault", "FreerideinvestorWebsite", "LSTMmodel_trainer"],
        "Agent-4": ["DaDudekC", "FocusForge", "HCshinobi", "MLRobotmaker", "SWARM"]
    }
    
    print("📋 Agent Repository Assignments:")
    print(f"📍 Working Directory: D:\\repos\\Dadudekc")
    for agent, repos in agent_repos.items():
        print(f"  {agent}: {', '.join(repos)}")
    
    print("\n🚀 Sending PRD Instructions...")
    print("-" * 40)
    
    # Send instructions to each agent
    for agent, repos in agent_repos.items():
        print(f"\n📤 Sending to {agent}:")
        
        # Create comprehensive PRD instruction
        instruction = f"""🎯 CAPTAIN INSTRUCTION: PRD Creation/Modification

📋 AGENT: {agent}
📅 TIMESTAMP: {Path(__file__).parent / "runtime/fsm"}
📍 WORKING DIRECTORY: D:\\repos\\Dadudekc

🎯 MISSION: Create or modify PRDs for your assigned repositories

📁 YOUR ASSIGNED REPOSITORIES:
{chr(10).join([f"  • {repo}" for repo in repos])}

🔍 STEP 1: INSPECT EACH REPOSITORY
- Navigate to D:\\repos\\Dadudekc\\[REPO_NAME]
- Review all source code files
- Analyze existing documentation
- Understand the project's purpose and scope
- Identify key features and functionality
- Note any existing PRDs that need updates

📝 STEP 2: CREATE/MODIFY PRDs
For each repository, create or update the PRD using this structure:

# Project Requirements Document (PRD)

## 📋 Project Overview
- **Project Name**: [ACTUAL_REPO_NAME]
- **Version**: [CURRENT_VERSION]
- **Last Updated**: [TODAY'S_DATE]
- **Status**: [ACTUAL_STATUS]

## 🎯 Objectives
- [Specific objective based on code analysis]
- [Another objective you discovered]
- [Third objective from repository review]

## 🚀 Features
### Core Features
- [Actual feature found in code]
- [Another feature you identified]

### Future Features
- [Feature you think should be added]
- [Enhancement opportunity]

## 📊 Requirements
### Functional Requirements
- [FR1] [Specific requirement from code analysis]
- [FR2] [Another requirement you found]

### Non-Functional Requirements
- [NFR1] [Performance, security, etc.]
- [NFR2] [Scalability, maintainability, etc.]

## 🔧 Technical Specifications
- **Language**: [Actual language used]
- **Framework**: [Framework if any]
- **Database**: [Database if any]

## 📅 Timeline
- **Phase 1**: [Realistic dates] - [Specific deliverables]
- **Phase 2**: [Realistic dates] - [Specific deliverables]
- **Phase 3**: [Realistic dates] - [Specific deliverables]

## ✅ Acceptance Criteria
- [AC1] [Specific, measurable criteria]
- [AC2] [Another specific criteria]

## 🚨 Risks & Mitigation
- **Risk 1**: [Actual risk you identified] → [Mitigation strategy]
- **Risk 2**: [Another risk] → [Mitigation strategy]

🎯 CRITICAL REQUIREMENTS:
1. DO NOT use placeholder text - fill in everything with real information
2. Base all content on actual repository analysis from D:\\repos\\Dadudekc
3. Make objectives specific and measurable
4. Ensure features match what's actually in the code
5. Set realistic timelines based on project complexity
6. Identify real risks and provide practical mitigation

📊 DELIVERABLES:
- Create/update PRD.md file in each repository at D:\\repos\\Dadudekc\\[REPO_NAME]
- Ensure all sections are properly filled
- Remove any placeholder text
- Make content specific to each project

⏰ TIMELINE: Complete within 24 hours
📝 REPORT BACK: Send completion status to Agent-5 (CAPTAIN)

🚀 START NOW: Begin with your highest priority repository!

---
🎖️ CAPTAIN Agent-5
🤖 Autonomous Development System
📍 Working from D:\\repos\\Dadudekc
"""
        
        # Send the instruction
        try:
            acp.send(agent, instruction, MsgTag.TASK, new_chat=True)
            print(f"  ✅ Instruction sent to {agent}")
            print(f"  📁 Repositories: {len(repos)}")
            print(f"  🎯 Mission: PRD Creation/Modification")
            print(f"  📍 Location: D:\\repos\\Dadudekc")
        except Exception as e:
            print(f"  ❌ Failed to send to {agent}: {e}")
    
    print("\n🎉 PRD Instructions Sent to All Agents!")
    print("\n📊 Summary:")
    print(f"  • Agent-1: {len(agent_repos['Agent-1'])} repositories")
    print(f"  • Agent-2: {len(agent_repos['Agent-2'])} repositories")
    print(f"  • Agent-3: {len(agent_repos['Agent-3'])} repositories")
    print(f"  • Agent-4: {len(agent_repos['Agent-4'])} repositories")
    print(f"  • Total: {sum(len(repos) for repos in agent_repos.values())} repositories")
    print(f"  📍 Working Directory: D:\\repos\\Dadudekc")
    
    print("\n🎯 Next Steps:")
    print("  1. Agents will begin PRD creation/modification")
    print("  2. Monitor progress through the system")
    print("  3. Review completed PRDs for quality")
    print("  4. Move to roadmap creation phase")

if __name__ == "__main__":
    send_prd_instructions()


