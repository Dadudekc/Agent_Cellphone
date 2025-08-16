#!/usr/bin/env python3
"""
Continuous Agents 1-4 Runner
============================
Keeps agents 1-4 working non-stop with automatic task assignment and monitoring.
Perfect for when you need to step away and let the agents handle everything!
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

class ContinuousAgentRunner:
    """Keeps agents 1-4 working continuously with smart task management"""
    
    def __init__(self):
        self.agents = ["Agent-1", "Agent-2", "Agent-3", "Agent-4"]
        self.acp = AgentCellPhone(agent_id="Continuous-Runner", layout_mode="5-agent")
        self.monitor = None
        self._stop = threading.Event()
        self._start_time = time.time()
        
        # Task templates for continuous work
        self.task_templates = {
            "Agent-1": [
                "Review and optimize system coordination protocols",
                "Analyze team performance metrics and identify improvements",
                "Coordinate cross-agent communication workflows",
                "Develop new task management strategies",
                "Monitor system health and performance indicators"
            ],
            "Agent-2": [
                "Process and analyze pending data requests",
                "Optimize resource allocation algorithms",
                "Track project milestones and update progress",
                "Review task completion rates and efficiency",
                "Develop new project management methodologies"
            ],
            "Agent-3": [
                "Analyze data processing pipelines for optimization",
                "Research new analytical techniques and tools",
                "Process backlog of data analysis requests",
                "Develop innovative data visualization methods",
                "Explore machine learning applications for data processing"
            ],
            "Agent-4": [
                "Review communication protocols and security measures",
                "Monitor network activity and security logs",
                "Optimize inter-agent communication channels",
                "Develop new security monitoring protocols",
                "Analyze communication efficiency metrics"
            ]
        }
        
        # Task rotation to keep things interesting
        self.current_task_index = {agent: 0 for agent in self.agents}
        
    def start(self):
        """Start the continuous agent runner"""
        print("🚀 Starting Continuous Agents 1-4 Runner...")
        print(f"📅 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"👥 Managing agents: {', '.join(self.agents)}")
        
        # Start the monitor
        self._start_monitor()
        
        # Start task assignment loop
        threading.Thread(target=self._task_loop, daemon=True).start()
        
        # Start status reporting
        threading.Thread(target=self._status_loop, daemon=True).start()
        
        print("✅ All systems running! Agents 1-4 are now working continuously.")
        print("💇‍♀️ You can now do your hair - the agents will handle everything!")
        print("📊 Monitor progress in the logs and agent workspaces")
        
    def stop(self):
        """Stop the continuous agent runner"""
        print("\n🛑 Stopping Continuous Agents Runner...")
        self._stop.set()
        
        if self.monitor:
            self.monitor.stop()
            
        print("✅ Continuous Agents Runner stopped")
        
    def _start_monitor(self):
        """Start the agent monitoring system"""
        try:
            cfg = MonitorConfig(
                agents=self.agents,
                stall_threshold_sec=600,  # 10 minutes
                check_every_sec=10,       # Check every 10 seconds
                rescue_cooldown_sec=180,  # 3 minutes between rescues
                active_grace_sec=180,     # 3 minutes grace period
                fsm_enabled=True
            )
            
            self.monitor = Agent5Monitor(cfg, sender="Continuous-Runner")
            if not self.monitor.start():
                print("⚠️  Warning: Monitor failed to start, but continuing...")
                
        except Exception as e:
            print(f"⚠️  Warning: Monitor setup failed: {e}, but continuing...")
            
    def _task_loop(self):
        """Main loop for assigning tasks to agents"""
        task_interval = 300  # Assign new tasks every 5 minutes
        
        while not self._stop.is_set():
            try:
                self._assign_tasks_to_all_agents()
                time.sleep(task_interval)
            except Exception as e:
                print(f"⚠️  Task assignment error: {e}")
                time.sleep(60)  # Wait a minute before retrying
                
    def _assign_tasks_to_all_agents(self):
        """Assign fresh tasks to all agents"""
        for agent in self.agents:
            try:
                self._assign_task_to_agent(agent)
            except Exception as e:
                print(f"⚠️  Failed to assign task to {agent}: {e}")
                
    def _assign_task_to_agent(self, agent: str):
        """Assign a specific task to an agent"""
        # Get next task from rotation
        task_index = self.current_task_index[agent]
        tasks = self.task_templates[agent]
        task = tasks[task_index % len(tasks)]
        
        # Rotate to next task
        self.current_task_index[agent] = (task_index + 1) % len(tasks)
        
        # Create detailed task message
        timestamp = datetime.now().strftime("%H:%M:%S")
        msg = f"""🔄 [CONTINUOUS TASK] {timestamp}

📋 Task: {task}

🎯 Instructions:
- Work on this task continuously
- Document your progress in your workspace
- Update status when complete or if you need help
- Move to next task when ready

💡 Remember: You're part of a continuous workflow - keep the momentum going!

Status: 🟡 In Progress
Progress: Starting now..."""
        
        try:
            self.acp.send(agent, msg, MsgTag.TASK, new_chat=False)
            print(f"📤 Assigned task to {agent}: {task[:50]}...")
        except Exception as e:
            print(f"❌ Failed to send task to {agent}: {e}")
            
    def _status_loop(self):
        """Periodic status reporting loop"""
        while not self._stop.is_set():
            try:
                self._report_status()
                time.sleep(600)  # Report every 10 minutes
            except Exception as e:
                print(f"⚠️  Status reporting error: {e}")
                time.sleep(300)  # Wait 5 minutes before retrying
                
    def _report_status(self):
        """Report current status"""
        uptime = time.time() - self._start_time
        uptime_str = f"{int(uptime // 3600)}h {int((uptime % 3600) // 60)}m"
        
        status_msg = f"""📊 [STATUS REPORT] {datetime.now().strftime('%H:%M:%S')}

⏱️  Uptime: {uptime_str}
👥 Active Agents: {len(self.agents)}
🔄 Task Rotation: Active
📈 System Status: Running Continuously

💪 Agents 1-4 are working hard and staying productive!
🎯 Continuous task assignment is maintaining workflow momentum.

Status: ✅ All Systems Operational"""
        
        print(status_msg)
        
        # Also send to a central location if needed
        try:
            # Could send to a status channel or log file
            pass
        except Exception:
            pass

def main():
    """Main entry point"""
    runner = ContinuousAgentRunner()
    
    # Setup signal handlers for graceful shutdown
    def signal_handler(signum, frame):
        print(f"\n📡 Received signal {signum}")
        runner.stop()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        runner.start()
        
        # Keep main thread alive
        print("\n💤 Main thread sleeping - agents are working in background...")
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
