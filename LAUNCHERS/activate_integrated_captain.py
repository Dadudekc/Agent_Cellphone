#!/usr/bin/env python3
"""
INTEGRATED CAPTAIN SYSTEM
=========================
Connects Agent Contract System → FSM System → Agent Prompting System
to keep agents working continuously with automatic stall detection and rescue.
"""

import os
import sys
import time
import json
import threading
from pathlib import Path
from datetime import datetime

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

try:
    from src.services.agent_cell_phone import AgentCellPhone, MsgTag
    from src.agent_monitors.agent5_monitor import Agent5Monitor, MonitorConfig
    from src.fsm.enhanced_fsm import EnhancedFSM
except ImportError as e:
    print(f"Import error: {e}")
    sys.exit(1)

class IntegratedCaptain:
    """Integrated Captain system that connects all agent coordination systems"""
    
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
        
        # Initialize FSM system
        self.fsm = EnhancedFSM(str(self.repos_root))
        
        # Initialize Agent5Monitor for stall detection and rescue
        self.monitor = None
        self._setup_monitor()
        
        # Control flags
        self._stop = threading.Event()
        self._start_time = time.time()
        
    def _setup_monitor(self):
        """Setup Agent5Monitor for automatic stall detection and rescue"""
        try:
            # Configure monitor with aggressive settings for immediate response
            cfg = MonitorConfig(
                agents=self.agents,
                stall_threshold_sec=300,      # 5 minutes - detect stalls quickly
                warn_threshold_sec=180,       # 3 minutes - warn early
                normal_response_time=120,     # 2 minutes - normal response time
                check_every_sec=15,           # Check every 15 seconds
                rescue_cooldown_sec=60,       # 1 minute between rescues
                active_grace_sec=120,         # 2 minutes grace period
                fsm_enabled=True
            )
            
            self.monitor = Agent5Monitor(cfg, sender="Agent-5", layout="5-agent", test=False)
            print("✅ Agent5Monitor configured for automatic stall detection and rescue")
            
        except Exception as e:
            print(f"❌ Failed to setup Agent5Monitor: {e}")
            self.monitor = None
        
    def activate_captain_mode(self):
        """Activate integrated Captain mode with all systems connected"""
        print("🎖️ INTEGRATED CAPTAIN Agent-5 ACTIVATING...")
        print("=" * 70)
        print(f"📅 Activated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"👥 Coordinating agents: {', '.join(self.agents)}")
        print(f"📁 Repository root: {self.repos_root}")
        print(f"🤖 FSM System: {'✅ Connected' if self.fsm else '❌ Failed'}")
        print(f"🚨 Stall Monitor: {'✅ Active' if self.monitor else '❌ Failed'}")
        
        # Verify repositories exist
        self._verify_repositories()
        
        # Start the integrated systems
        self._start_integrated_systems()
        
        # Assign initial work to all agents
        self._assign_work_to_all_agents()
        
        # Start continuous coordination with FSM integration
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
                    
    def _start_integrated_systems(self):
        """Start all integrated systems"""
        print("\n🚀 Starting integrated systems...")
        
        # Start Agent5Monitor for stall detection
        if self.monitor:
            try:
                self.monitor.start()
                print("✅ Agent5Monitor started - will detect stalls and send rescue messages automatically")
            except Exception as e:
                print(f"❌ Failed to start Agent5Monitor: {e}")
        
        # Start FSM system
        try:
            # Initialize FSM with current agent states
            for agent in self.agents:
                self.fsm.update_agent_state(agent)
            print("✅ EnhancedFSM started - tracking agent states and work context")
        except Exception as e:
            print(f"❌ Failed to start EnhancedFSM: {e}")
            
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
Deadline: Continuous until completion

⚠️ IMPORTANT: The Captain system will automatically detect if you stall and send rescue messages.
Keep working continuously and post updates to Discord!"""

        try:
            self.acp.send(agent, assignment_msg, MsgTag.TASK, new_chat=True)
            print(f"✅ Assigned work to {agent}: {len(repos)} repositories")
            
            # Update FSM state
            if self.fsm:
                self.fsm.update_agent_state(agent)
                
        except Exception as e:
            print(f"❌ Failed to assign work to {agent}: {e}")
            
    def _start_continuous_coordination(self):
        """Start continuous coordination cycle with FSM integration"""
        print("\n🔄 Starting continuous coordination cycle...")
        print("💡 Captain will coordinate agents every 5 minutes")
        print("🚨 Agent5Monitor will detect stalls every 15 seconds")
        print("🤖 FSM will track agent states and work context")
        print("📊 Monitor progress in agent workspaces and Discord")
        
        coordination_interval = 300  # 5 minutes
        
        try:
            while not self._stop.is_set():
                time.sleep(coordination_interval)
                self._coordinate_agents()
        except KeyboardInterrupt:
            print("\n🛑 Captain coordination stopped by user")
            
    def _coordinate_agents(self):
        """Coordinate all agents for progress updates with FSM integration"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        print(f"\n📊 [COORDINATION CYCLE] {timestamp}")
        print("🤝 Checking in with all agents...")
        
        for agent in self.agents:
            self._check_agent_progress(agent)
            
            # Update FSM state
            if self.fsm:
                try:
                    state = self.fsm.update_agent_state(agent)
                    print(f"📊 {agent} FSM State: {state.status} | Repo: {state.current_repo or 'None'}")
                except Exception as e:
                    print(f"⚠️ FSM update failed for {agent}: {e}")
                    
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
⚠️ The Captain system is monitoring your activity - keep working!

Status: 🔄 Progress Check
Action: Provide comprehensive update"""

        try:
            self.acp.send(agent, progress_msg, MsgTag.TASK, new_chat=False)
            print(f"📊 Progress check sent to {agent}")
        except Exception as e:
            print(f"❌ Failed to send progress check to {agent}: {e}")
            
    def get_system_status(self):
        """Get status of all integrated systems"""
        status = {
            "timestamp": datetime.now().isoformat(),
            "uptime_sec": time.time() - self._start_time,
            "agents": len(self.agents),
            "fsm_status": "✅ Active" if self.fsm else "❌ Failed",
            "monitor_status": "✅ Active" if self.monitor else "❌ Failed"
        }
        
        if self.monitor:
            try:
                monitor_status = self.monitor.get_status()
                status.update(monitor_status)
            except Exception as e:
                status["monitor_error"] = str(e)
                
        return status
        
    def stop(self):
        """Stop all integrated systems"""
        print("\n🛑 Stopping integrated Captain systems...")
        self._stop.set()
        
        if self.monitor:
            try:
                self.monitor.stop()
                print("✅ Agent5Monitor stopped")
            except Exception as e:
                print(f"⚠️ Error stopping Agent5Monitor: {e}")

def main():
    """Main integrated Captain activation"""
    captain = IntegratedCaptain()
    
    try:
        captain.activate_captain_mode()
    except KeyboardInterrupt:
        print("\n🛑 Captain activation interrupted")
    except Exception as e:
        print(f"❌ Captain error: {e}")
    finally:
        captain.stop()

if __name__ == "__main__":
    main()


