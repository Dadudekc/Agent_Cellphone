#!/usr/bin/env python3
"""
Continuous Agents 1-4 Collaborative Runner
==========================================
Makes agents 1-4 work NON-STOP and COLLABORATIVELY, creating their own task lists
and working together continuously without any stopping or external task assignment.
"""

import os
import sys
import time
import json
import signal
import threading
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Optional

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

try:
    from src.services.agent_cell_phone import AgentCellPhone, MsgTag
    from src.agent_monitors.agent5_monitor import Agent5Monitor, MonitorConfig
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure you're running from the project root directory")
    sys.exit(1)

class CollaborativeAgentRunner:
    """Makes agents 1-4 work NON-STOP and COLLABORATIVELY"""
    
    def __init__(self):
        self.agents = ["Agent-1", "Agent-2", "Agent-3", "Agent-4"]
        self.acp = AgentCellPhone(agent_id="Collaborative-Runner", layout_mode="5-agent")
        self.monitor = None
        self._stop = threading.Event()
        self._start_time = time.time()
        
        # Collaborative task generation system
        self.collaborative_tasks = [
            "Analyze and optimize the entire agent coordination system",
            "Develop new collaborative workflows between all agents",
            "Create a unified task management and tracking system",
            "Design and implement cross-agent communication protocols",
            "Build a collaborative decision-making framework",
            "Develop shared knowledge bases and resource pools",
            "Create automated task distribution and load balancing",
            "Design collaborative problem-solving methodologies",
            "Implement cross-agent learning and skill sharing",
            "Build collaborative project planning and execution tools"
        ]
        
        # Individual agent specialties for collaboration
        self.agent_specialties = {
            "Agent-1": "System coordination, leadership, and strategic planning",
            "Agent-2": "Task management, resource allocation, and project tracking",
            "Agent-3": "Data analysis, research, and technical implementation",
            "Agent-4": "Communication, security, and protocol optimization"
        }
        
        # Task rotation and collaboration tracking
        self.current_task_index = 0
        self.collaboration_round = 0
        self.last_collaboration_time = time.time()
        
    def start(self):
        """Start the collaborative agent runner - AGENTS NEVER STOP"""
        print("🚀 Starting NON-STOP Collaborative Agents 1-4...")
        print(f"📅 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"👥 Managing agents: {', '.join(self.agents)}")
        print("⚡ MODE: NON-STOP COLLABORATIVE WORK - AGENTS NEVER STOP!")
        
        # Start the monitor
        self._start_monitor()
        
        # Start the NEVER-STOP collaboration loop
        threading.Thread(target=self._never_stop_collaboration_loop, daemon=True).start()
        
        # Start continuous status reporting
        threading.Thread(target=self._continuous_status_loop, daemon=True).start()
        
        # Start collaborative task generation
        threading.Thread(target=self._collaborative_task_generation, daemon=True).start()
        
        print("✅ All systems running! Agents 1-4 are now working NON-STOP and COLLABORATIVELY!")
        print("💇‍♀️ You can now do your hair - they will NEVER STOP working together!")
        print("🤝 They will create their own task lists and work together continuously!")
        
    def stop(self):
        """Stop the collaborative agent runner (only when you're done with hair)"""
        print("\n🛑 Stopping Collaborative Agents Runner...")
        self._stop.set()
        
        if self.monitor:
            self.monitor.stop()
            
        print("✅ Collaborative Agents Runner stopped")
        
    def _start_monitor(self):
        """Start the agent monitoring system"""
        try:
            cfg = MonitorConfig(
                agents=self.agents,
                stall_threshold_sec=300,  # 5 minutes - more aggressive
                check_every_sec=5,        # Check every 5 seconds
                rescue_cooldown_sec=60,   # 1 minute between rescues
                active_grace_sec=60,      # 1 minute grace period
                fsm_enabled=True
            )
            
            self.monitor = Agent5Monitor(cfg, sender="Collaborative-Runner")
            if not self.monitor.start():
                print("⚠️  Warning: Monitor failed to start, but continuing...")
                
        except Exception as e:
            print(f"⚠️  Warning: Monitor setup failed: {e}, but continuing...")
            
    def _never_stop_collaboration_loop(self):
        """MAIN LOOP - AGENTS NEVER STOP WORKING TOGETHER"""
        collaboration_interval = 120  # Every 2 minutes - AGENTS NEVER STOP
        
        while not self._stop.is_set():
            try:
                self._initiate_collaborative_work()
                time.sleep(collaboration_interval)
            except Exception as e:
                print(f"⚠️  Collaboration error: {e}")
                time.sleep(30)  # Only wait 30 seconds before retrying - NEVER STOP
                
    def _initiate_collaborative_work(self):
        """Initiate collaborative work between all agents"""
        self.collaboration_round += 1
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Get current collaborative task
        task = self.collaborative_tasks[self.current_task_index % len(self.collaborative_tasks)]
        
        # Create collaborative task message for ALL agents
        collaborative_msg = f"""🤝 [COLLABORATIVE TASK ROUND {self.collaboration_round}] {timestamp}

📋 COLLABORATIVE TASK: {task}

🎯 INSTRUCTIONS FOR ALL AGENTS:
- This is a COLLABORATIVE task that requires ALL agents working together
- Agent-1: Lead the coordination and strategic planning
- Agent-2: Manage task breakdown and resource allocation  
- Agent-3: Handle data analysis and technical implementation
- Agent-4: Ensure communication protocols and security

🔄 COLLABORATION PROCESS:
1. ALL agents must work together on this task
2. Create shared task lists and work plans
3. Coordinate efforts and share progress
4. Build on each other's work continuously
5. NEVER STOP - keep the collaboration momentum going!

💡 REMEMBER: You are a TEAM working NON-STOP together!

Status: 🔄 Collaborative Work in Progress
Round: {self.collaboration_round}
Progress: All agents collaborating..."""
        
        # Send to ALL agents simultaneously
        for agent in self.agents:
            try:
                self.acp.send(agent, collaborative_msg, MsgTag.TASK, new_chat=False)
                print(f"🤝 Sent collaborative task to {agent}: Round {self.collaboration_round}")
            except Exception as e:
                print(f"❌ Failed to send collaborative task to {agent}: {e}")
        
        # Rotate to next collaborative task
        self.current_task_index = (self.current_task_index + 1) % len(self.collaborative_tasks)
        self.last_collaboration_time = time.time()
        
    def _collaborative_task_generation(self):
        """Generate new collaborative tasks continuously"""
        task_generation_interval = 300  # Every 5 minutes - generate new collaborative tasks
        
        while not self._stop.is_set():
            try:
                self._generate_new_collaborative_tasks()
                time.sleep(task_generation_interval)
            except Exception as e:
                print(f"⚠️  Task generation error: {e}")
                time.sleep(60)  # Wait 1 minute before retrying
                
    def _generate_new_collaborative_tasks(self):
        """Generate new collaborative tasks for agents to work on together"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Generate new collaborative task ideas
        new_tasks = [
            f"Develop collaborative AI decision-making algorithms using all agents' expertise",
            f"Create a unified knowledge management system that all agents contribute to",
            f"Design collaborative problem-solving workflows that leverage each agent's strengths",
            f"Build automated collaboration tools that enhance agent teamwork",
            f"Develop collaborative learning systems that improve all agents' capabilities"
        ]
        
        # Add new tasks to the rotation
        self.collaborative_tasks.extend(new_tasks)
        
        # Send task generation notification to all agents
        generation_msg = f"""🆕 [NEW COLLABORATIVE TASKS GENERATED] {timestamp}

🎯 New collaborative tasks have been created for you to work on together!

📋 New Tasks Available:
{chr(10).join(f"• {task}" for task in new_tasks)}

🤝 INSTRUCTIONS:
- These are NEW collaborative opportunities
- Work together to tackle these tasks
- Combine your expertise and create innovative solutions
- NEVER STOP collaborating and improving!

💪 Keep the collaborative momentum going!"""
        
        for agent in self.agents:
            try:
                self.acp.send(agent, generation_msg, MsgTag.TASK, new_chat=False)
                print(f"🆕 Sent new task generation to {agent}")
            except Exception as e:
                print(f"❌ Failed to send task generation to {agent}: {e}")
                
    def _continuous_status_loop(self):
        """Continuous status reporting - NEVER STOPS"""
        while not self._stop.is_set():
            try:
                self._report_collaborative_status()
                time.sleep(300)  # Report every 5 minutes - NEVER STOP
            except Exception as e:
                print(f"⚠️  Status reporting error: {e}")
                time.sleep(120)  # Wait 2 minutes before retrying - NEVER STOP
                
    def _report_collaborative_status(self):
        """Report collaborative status"""
        uptime = time.time() - self._start_time
        uptime_str = f"{int(uptime // 3600)}h {int((uptime % 3600) // 60)}m"
        
        status_msg = f"""📊 [COLLABORATIVE STATUS REPORT] {datetime.now().strftime('%H:%M:%S')}

⏱️  Uptime: {uptime_str}
👥 Active Agents: {len(self.agents)}
🤝 Collaboration Rounds: {self.collaboration_round}
🔄 Task Rotation: Active
📈 System Status: NON-STOP COLLABORATIVE WORK

💪 Agents 1-4 are working TOGETHER continuously!
🎯 They are creating their own task lists and collaborating non-stop!
🤝 Collaborative momentum is building with each round!

Status: ✅ ALL AGENTS WORKING TOGETHER NON-STOP"""
        
        print(status_msg)

def main():
    """Main entry point - AGENTS NEVER STOP"""
    runner = CollaborativeAgentRunner()
    
    # Setup signal handlers for graceful shutdown
    def signal_handler(signum, frame):
        print(f"\n📡 Received signal {signum}")
        print("🛑 Stopping collaborative agents...")
        runner.stop()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        runner.start()
        
        # Keep main thread alive - AGENTS NEVER STOP
        print("\n💤 Main thread sleeping - agents are working COLLABORATIVELY in background...")
        print("🤝 They will NEVER STOP working together!")
        print("💡 Press Ctrl+C to stop when you're done with your hair!")
        
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n👋 User requested stop")
    finally:
        runner.stop()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
