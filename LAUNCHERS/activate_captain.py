#!/usr/bin/env python3
"""
CAPTAIN Agent-5 Activation Script
=================================
Activates the Captain system to coordinate agents 1-4 on repository work.
"""

import os
import sys
import time
import json
from pathlib import Path
from datetime import datetime

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

try:
    from src.services.agent_cell_phone import AgentCellPhone, MsgTag
except ImportError as e:
    print(f"Import error: {e}")
    sys.exit(1)

class CaptainCoordinator:
    """Captain system to coordinate agents 1-4 on repository work"""
    
    def __init__(self):
        self.acp = AgentCellPhone(agent_id="Agent-5", layout_mode="5-agent", test=False)
        self.agents = ["Agent-1", "Agent-2", "Agent-3", "Agent-4"]
        self.repos_root = Path("D:/repos/Dadudekc")
        
        # Repository assignments for each agent
        self.agent_repos = {
            "Agent-1": [
                "AI_Debugger_Assistant", "DigitalDreamscape", "FreeRideInvestor", 
                "Hive-Mind", "MeTuber", "osrsAIagent", "osrsbot"
            ],
            "Agent-2": [
                "Auto_Blogger", "Dream.os", "FreeWork", "IT_help_desk", 
                "NewSims4ModProject", "practice", "projectscanner"
            ],
            "Agent-3": [
                "DaDudeKC-Website", "DreamVault", "FreerideinvestorWebsite", 
                "LSTMmodel_trainer", "machinelearningproject", "MLRobotmaker"
            ],
            "Agent-4": [
                "DaDudekC", "FocusForge", "HCshinobi", "SWARM", 
                "TradingRobotPlug", "ultimate_trading_intelligence"
            ]
        }
        
        # Task priorities for each agent
        self.agent_tasks = {
            "Agent-1": [
                "Create comprehensive PRDs for AI and gaming projects",
                "Develop task lists and project roadmaps",
                "Post progress updates to Discord",
                "Coordinate with other agents on shared projects"
            ],
            "Agent-2": [
                "Create PRDs for automation and utility projects",
                "Develop project management frameworks",
                "Track progress and update task lists",
                "Post completion updates to Discord"
            ],
            "Agent-3": [
                "Create PRDs for web and ML projects",
                "Develop technical specifications",
                "Create implementation roadmaps",
                "Post technical updates to Discord"
            ],
            "Agent-4": [
                "Create PRDs for trading and financial projects",
                "Develop security and monitoring protocols",
                "Create deployment strategies",
                "Post security and performance updates to Discord"
            ]
        }
        
    def activate_captain_mode(self):
        """Activate Captain mode and coordinate all agents"""
        print("🎖️ CAPTAIN Agent-5 ACTIVATING...")
        print("=" * 60)
        print(f"📅 Activated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"👥 Coordinating agents: {', '.join(self.agents)}")
        print(f"📁 Repository root: {self.repos_root}")
        
        # Verify repositories exist
        self._verify_repositories()
        
        # Assign work to all agents
        self._assign_work_to_all_agents()
        
        # Start continuous coordination
        self._start_continuous_coordination()
        
    def _verify_repositories(self):
        """Verify that assigned repositories exist"""
        print("\n🔍 Verifying repository assignments...")
        
        for agent, repos in self.agent_repos.items():
            print(f"\n📋 {agent} repositories:")
            for repo in repos:
                repo_path = self.repos_root / repo
                if repo_path.exists():
                    print(f"  ✅ {repo}")
                else:
                    print(f"  ❌ {repo} (missing)")
                    
    def _assign_work_to_all_agents(self):
        """Assign repository work to all agents"""
        print("\n🎯 Assigning work to all agents...")
        
        for agent in self.agents:
            self._assign_work_to_agent(agent)
            
    def _assign_work_to_agent(self, agent: str):
        """Assign specific work to an agent"""
        repos = self.agent_repos[agent]
        tasks = self.agent_tasks[agent]
        
        # Create comprehensive work assignment
        assignment_msg = f"""🎖️ [CAPTAIN ASSIGNMENT] {datetime.now().strftime('%H:%M:%S')}

📋 AGENT: {agent}
🎯 ROLE: Repository Development Specialist

📁 ASSIGNED REPOSITORIES:
{chr(10).join(f"• {repo}" for repo in repos)}

📋 PRIMARY TASKS:
{chr(10).join(f"• {task}" for task in tasks)}

🎯 IMMEDIATE ACTIONS REQUIRED:
1. Analyze each assigned repository
2. Create comprehensive PRDs (Product Requirements Documents)
3. Develop detailed task lists and project roadmaps
4. Post progress updates to Discord as you complete work
5. Coordinate with other agents on shared dependencies

💡 COLLABORATION NOTES:
- Work with other agents on overlapping projects
- Share insights and best practices
- Update TASK_LIST.md files in each repository
- Post completion milestones to Discord

🚀 STATUS: ASSIGNED - START WORKING NOW!

Status: 🟡 In Progress
Priority: HIGH
Deadline: Continuous until completion"""

        try:
            self.acp.send(agent, assignment_msg, MsgTag.TASK, new_chat=True)
            print(f"✅ Assigned work to {agent}: {len(repos)} repositories")
        except Exception as e:
            print(f"❌ Failed to assign work to {agent}: {e}")
            
    def _start_continuous_coordination(self):
        """Start continuous coordination cycle"""
        print("\n🔄 Starting continuous coordination cycle...")
        print("💡 Captain will coordinate agents every 10 minutes")
        print("📊 Monitor progress in agent workspaces and Discord")
        
        coordination_interval = 600  # 10 minutes
        
        try:
            while True:
                time.sleep(coordination_interval)
                self._coordinate_agents()
        except KeyboardInterrupt:
            print("\n🛑 Captain coordination stopped by user")
            
    def _coordinate_agents(self):
        """Coordinate all agents for progress updates"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        print(f"\n📊 [COORDINATION CYCLE] {timestamp}")
        print("🤝 Checking in with all agents...")
        
        for agent in self.agents:
            self._check_agent_progress(agent)
            
    def _check_agent_progress(self, agent: str):
        """Check progress for a specific agent"""
        repos = self.agent_repos[agent]
        
        progress_msg = f"""📊 [PROGRESS CHECK] {datetime.now().strftime('%H:%M:%S')}

👤 Agent: {agent}

📋 PROGRESS UPDATE REQUESTED:
Please provide status update on your assigned repositories:

{chr(10).join(f"• {repo}" for repo in repos)}

🎯 REPORT ON:
1. Which repositories have PRDs completed?
2. Which task lists are finished?
3. What Discord updates have been posted?
4. Any blockers or dependencies?
5. Next steps and priorities?

💡 Remember: Keep the momentum going and post updates to Discord!

Status: 🔄 Progress Check
Action: Provide comprehensive update"""

        try:
            self.acp.send(agent, progress_msg, MsgTag.TASK, new_chat=False)
            print(f"📊 Progress check sent to {agent}")
        except Exception as e:
            print(f"❌ Failed to send progress check to {agent}: {e}")

def main():
    """Main Captain activation"""
    captain = CaptainCoordinator()
    
    try:
        captain.activate_captain_mode()
    except KeyboardInterrupt:
        print("\n🛑 Captain activation interrupted")
    except Exception as e:
        print(f"❌ Captain error: {e}")

if __name__ == "__main__":
    main()


