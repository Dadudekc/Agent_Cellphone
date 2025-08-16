#!/usr/bin/env python3
"""
Enhanced Overnight Runner with FSM Integration
=============================================
Provides personalized, contextual guidance based on actual agent work.
"""

import os
import sys
import time
import signal
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from fsm import EnhancedFSM
from services.agent_cell_phone import AgentCellPhone, MsgTag

class EnhancedOvernightRunner:
    """Enhanced overnight runner with FSM intelligence"""
    
    def __init__(self, layout_mode: str = "5-agent", sender: str = "Agent-3", 
                 repos_root: str = "D:/repos/Dadudekc"):
        self.layout_mode = layout_mode
        self.sender = sender
        self.repos_root = repos_root
        
        # Initialize FSM and AgentCellPhone
        self.fsm = EnhancedFSM(repos_root)
        self.acp = AgentCellPhone(agent_id=sender, layout_mode=layout_mode, test=False)
        
        # Get available agents
        self.agents = self.acp.get_available_agents()
        
        # Configuration
        self.cycle_interval = 300  # 5 minutes
        self.max_cycles = 10
        self.current_cycle = 0
        
        # Message templates for different cycle types
        self.cycle_messages = {
            "RESUME": "RESUME",
            "TASK": "TASK", 
            "COORDINATE": "COORDINATE",
            "PROGRESS": "PROGRESS",
            "NEXT": "NEXT"
        }
        
        # Signal handling
        self._stop = False
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        print(f"\nReceived signal {signum}, shutting down gracefully...")
        self._stop = True
    
    def run(self):
        """Main runner loop"""
        print(f"Enhanced Overnight Runner starting (layout={self.layout_mode}, sender={self.sender})")
        print(f"Repos root: {self.repos_root}")
        print(f"Agents: {', '.join(self.agents)}")
        print(f"Plan: intelligent coordination | Interval: {self.cycle_interval}s | Max Cycles: {self.max_cycles}")
        print()
        
        # Initial kickoff
        self._kickoff_cycle()
        
        # Main cycle loop
        while not self._stop and self.current_cycle < self.max_cycles:
            self.current_cycle += 1
            print(f"Cycle {self.current_cycle}/{self.max_cycles}")
            
            # Determine cycle type based on current state
            cycle_type = self._determine_cycle_type()
            print(f"Cycle type: {cycle_type}")
            
            # Execute cycle
            self._execute_cycle(cycle_type)
            
            # Wait for next cycle
            if not self._stop and self.current_cycle < self.max_cycles:
                print(f"Waiting {self.cycle_interval} seconds for next cycle...")
                time.sleep(self.cycle_interval)
        
        print("Enhanced Overnight Runner finished")
    
    def _kickoff_cycle(self):
        """Initial kickoff with personalized assignments"""
        print("=== KICKOFF CYCLE ===")
        
        # Get current coordination summary
        summary = self.fsm.get_coordination_summary()
        
        for agent in self.agents:
            if agent == "Agent-5":
                # Special CAPTAIN message
                message = (
                    "[CAPTAIN] You are CAPTAIN tonight. Coordinate all agents. "
                    "Tasks: 1) Plan assignments avoiding duplication 2) Prompt peers for sanity checks "
                    "3) Ensure work is real (no stubs) 4) Write handoffs in comms folder. "
                    "Create a short TODO for yourself: (a) update repo TASK_LIST.md entries across active repos "
                    "(b) draft/align FSM contracts per agent (states, transitions) (c) next verification step."
                )
            else:
                # Get agent's current work context
                state = self.fsm.update_agent_state(agent)
                
                if state.current_repo:
                    # Agent is already working on something
                    message = (
                        f"[TASK] {agent}, continue your work on {state.current_repo}. "
                        f"Progress: {state.progress.get('repos_completed', 0)}/{state.progress.get('repos_assigned', 0)} repos. "
                        f"Complete current contract to acceptance criteria."
                    )
                else:
                    # Agent needs to start working
                    assigned_repos = self.fsm.repo_monitor.agent_repos.get(agent, [])
                    message = (
                        f"[TASK] {agent}, focus these repos tonight: {', '.join(assigned_repos)}. "
                        f"Objectives: reduce duplication, consolidate utilities, add tests and validation, "
                        f"commit small verifiable improvements."
                    )
            
            # Send message
            self._send_message(agent, message, "KICKOFF")
            time.sleep(2)  # Small delay between messages
    
    def _determine_cycle_type(self) -> str:
        """Determine the type of cycle based on current agent states"""
        # Get current coordination summary
        summary = self.fsm.get_coordination_summary()
        
        # Check if we need coordination
        active_agents = summary["overall_progress"]["active_agents"]
        stalled_agents = summary["overall_progress"]["stalled_agents"]
        
        if self.current_cycle == 1:
            return "RESUME"  # First cycle is always resume
        elif stalled_agents > 0:
            return "RESCUE"  # Need to rescue stalled agents
        elif active_agents >= len(self.agents) - 1:  # Most agents are working
            return "COORDINATE"  # Time to coordinate
        else:
            # Rotate through different message types
            cycle_types = ["RESUME", "TASK", "PROGRESS", "COORDINATE"]
            return cycle_types[(self.current_cycle - 1) % len(cycle_types)]
    
    def _execute_cycle(self, cycle_type: str):
        """Execute a specific cycle type"""
        print(f"=== {cycle_type} CYCLE ===")
        
        if cycle_type == "RESCUE":
            self._rescue_cycle()
        elif cycle_type == "COORDINATE":
            self._coordinate_cycle()
        else:
            self._standard_cycle(cycle_type)
    
    def _rescue_cycle(self):
        """Rescue stalled agents with personalized messages"""
        summary = self.fsm.get_coordination_summary()
        
        for agent, agent_data in summary["agents"].items():
            if agent_data["status"] == "stalled":
                # Generate personalized rescue message
                message = self.fsm.generate_personalized_message(agent, "RESCUE")
                self._send_message(agent, message, "RESCUE")
                time.sleep(1)
    
    def _coordinate_cycle(self):
        """Coordinate all agents with progress updates"""
        summary = self.fsm.get_coordination_summary()
        
        for agent in self.agents:
            if agent == "Agent-5":
                continue  # Skip captain for coordination
            
            # Generate personalized coordinate message
            message = self.fsm.generate_personalized_message(agent, "COORDINATE")
            self._send_message(agent, message, "COORDINATE")
            time.sleep(1)
    
    def _standard_cycle(self, cycle_type: str):
        """Standard cycle with personalized messages"""
        for agent in self.agents:
            if agent == "Agent-5":
                continue  # Skip captain for standard cycles
            
            # Generate personalized message
            message = self.fsm.generate_personalized_message(agent, cycle_type)
            self._send_message(agent, message, cycle_type)
            time.sleep(1)
    
    def _send_message(self, agent: str, content: str, message_type: str):
        """Send message and record it in FSM"""
        try:
            # Send via AgentCellPhone
            self.acp.send(agent, content, MsgTag.TASK, new_chat=False)
            
            # Record in FSM
            self.fsm.record_message(agent, message_type, content)
            
            # Log the message
            print(f"[SEND] {agent}: {content[:100]}...")
            
        except Exception as e:
            print(f"Failed to send message to {agent}: {e}")
    
    def get_status(self) -> dict:
        """Get current runner status"""
        return {
            "layout_mode": self.layout_mode,
            "sender": self.sender,
            "current_cycle": self.current_cycle,
            "max_cycles": self.max_cycles,
            "agents": self.agents,
            "fsm_summary": self.fsm.get_coordination_summary()
        }

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Enhanced Overnight Runner with FSM")
    parser.add_argument("--layout", default="5-agent", help="Layout mode")
    parser.add_argument("--sender", default="Agent-3", help="Sender agent")
    parser.add_argument("--repos-root", default="D:/repos/Dadudekc", help="Repositories root path")
    parser.add_argument("--iterations", type=int, default=10, help="Maximum cycles")
    parser.add_argument("--interval-sec", type=int, default=300, help="Cycle interval in seconds")
    
    args = parser.parse_args()
    
    # Create and run enhanced runner
    runner = EnhancedOvernightRunner(
        layout_mode=args.layout,
        sender=args.sender,
        repos_root=args.repos_root
    )
    
    # Override configuration
    runner.max_cycles = args.iterations
    runner.cycle_interval = args.interval_sec
    
    try:
        runner.run()
    except KeyboardInterrupt:
        print("\nRunner interrupted by user")
    except Exception as e:
        print(f"Runner error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
