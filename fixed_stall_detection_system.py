#!/usr/bin/env python3
"""
Fixed Stall Detection System
============================
Fixes the critical timing issues and properly integrates response detection
to prevent false stall detection during onboarding and normal operation.
"""

import json
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
from src.services.agent_cell_phone import AgentCellPhone, MsgTag

class FixedStallDetectionSystem:
    """Fixed stall detection system with proper response monitoring and realistic timing."""
    
    def __init__(self, layout_mode: str = "4-agent"):
        self.acp = AgentCellPhone(layout_mode=layout_mode)
        self.agents = ["Agent-1", "Agent-2", "Agent-3", "Agent-4"]
        
        # FIXED TIMING - Based on actual agent behavior
        self.timing_config = {
            "normal_response_time": 300,      # 5 minutes - normal agent response time
            "warn_threshold": 480,            # 8 minutes - warn about potential stall
            "stall_threshold": 600,           # 10 minutes - consider stalled
            "rescue_cooldown": 300,           # 5 minutes between rescue attempts
            "check_interval": 30,             # Check every 30 seconds
            "onboarding_grace_period": 600    # 10 minutes grace during onboarding
        }
        
        # Agent state tracking
        self.agent_states = {}
        self.last_rescue_attempts = {}
        self.onboarding_status = {}
        
        # Response monitoring
        self.response_monitor = ResponseMonitor()
        
    def start_monitoring(self):
        """Start the fixed stall detection system."""
        print("🚀 STARTING FIXED STALL DETECTION SYSTEM")
        print("=" * 60)
        print("✅ Realistic timing thresholds implemented")
        print("✅ Response detection properly integrated")
        print("✅ Onboarding grace period enabled")
        print("✅ Progressive escalation with proper timing")
        
        # Initialize agent states
        for agent in self.agents:
            self.agent_states[agent] = {
                "last_message_sent": time.time(),
                "last_response_received": time.time(),
                "status": "onboarding",  # Start in onboarding mode
                "response_count": 0,
                "stall_warnings": 0
            }
            self.onboarding_status[agent] = True  # Assume onboarding initially
        
        # Start response monitoring
        self.response_monitor.start()
        
        # Start stall detection loop
        self._monitor_loop()
    
    def _monitor_loop(self):
        """Main monitoring loop with fixed timing."""
        print("\n🔍 Starting stall detection monitoring...")
        
        while True:
            try:
                current_time = time.time()
                
                for agent in self.agents:
                    self._check_agent_status(agent, current_time)
                
                time.sleep(self.timing_config["check_interval"])
                
            except KeyboardInterrupt:
                print("\n🛑 Stopping stall detection system...")
                break
            except Exception as e:
                print(f"⚠️ Monitoring error: {e}")
                time.sleep(10)
    
    def _check_agent_status(self, agent: str, current_time: float):
        """Check individual agent status with proper timing logic."""
        state = self.agent_states[agent]
        time_since_message = current_time - state["last_message_sent"]
        time_since_response = current_time - state["last_response_received"]
        
        # Check if agent has responded since last message
        has_responded = self.response_monitor.has_agent_responded(agent, state["last_message_sent"])
        
        if has_responded:
            # Agent responded - update state
            state["last_response_received"] = current_time
            state["response_count"] += 1
            state["stall_warnings"] = 0
            
            # If agent has responded multiple times, consider them past onboarding
            if state["response_count"] >= 2:
                state["status"] = "active"
                self.onboarding_status[agent] = False
                print(f"✅ {agent}: Past onboarding, now active")
        
        # Determine if we should take action
        if self.onboarding_status[agent]:
            # ONBOARDING MODE - More lenient timing
            self._handle_onboarding_agent(agent, state, time_since_message, has_responded)
        else:
            # ACTIVE MODE - Normal stall detection
            self._handle_active_agent(agent, state, time_since_message, has_responded)
    
    def _handle_onboarding_agent(self, agent: str, state: Dict, time_since_message: float, has_responded: bool):
        """Handle agents still in onboarding phase."""
        if time_since_message > self.timing_config["onboarding_grace_period"] and not has_responded:
            # Agent has been in onboarding too long without response
            print(f"⚠️ {agent}: Onboarding timeout - sending gentle reminder")
            self._send_gentle_reminder(agent)
            state["last_message_sent"] = time.time()  # Reset timer
    
    def _handle_active_agent(self, agent: str, state: Dict, time_since_message: float, has_responded: bool):
        """Handle agents in active mode with proper stall detection."""
        if has_responded:
            return  # Agent is responding normally
        
        # Progressive stall detection with realistic timing
        if time_since_message > self.timing_config["stall_threshold"]:
            # Agent is stalled - send rescue
            print(f"🚨 {agent}: STALLED - sending progressive escalation rescue")
            self._send_progressive_rescue(agent)
            state["last_message_sent"] = time.time()  # Reset timer
            
        elif time_since_message > self.timing_config["warn_threshold"]:
            # Agent might be stalling - send warning
            if state["stall_warnings"] < 2:  # Limit warnings
                print(f"⚠️ {agent}: Potential stall - sending Shift+Backspace nudge")
                self._send_stall_warning(agent)
                state["stall_warnings"] += 1
                state["last_message_sent"] = time.time()  # Reset timer
    
    def _send_gentle_reminder(self, agent: str):
        """Send gentle reminder during onboarding."""
        message = f"ONBOARDING REMINDER: {agent}, please confirm you received the onboarding message and are ready to proceed. This is just a gentle check-in."
        self.acp.send(agent, message, MsgTag.COORDINATE, False)
    
    def _send_stall_warning(self, agent: str):
        """Send Shift+Backspace nudge for potential stall."""
        message = f"STALL WARNING: {agent}, you appear to be taking longer than usual to respond. Sending Shift+Backspace nudge to ensure your terminal is responsive."
        
        # Use progressive escalation with nudge flag
        if hasattr(self.acp, 'progressive_escalation'):
            self.acp.progressive_escalation(agent, message, MsgTag.RESCUE)
        else:
            # Fallback to direct send with nudge
            self.acp.send(agent, message, MsgTag.RESCUE, False, True)
    
    def _send_progressive_rescue(self, agent: str):
        """Send progressive escalation rescue for stalled agent."""
        rescue_msg = (
            f"[RESCUE] {agent}, you appear to be stalled.\n"
            f"Reply using the Dream.OS block:\n"
            f"Task: <what you're doing>\n"
            f"Actions Taken:\n- ...\n"
            f"Commit Message: <if any>\n"
            f"Status: 🟡 pending or ✅ done"
        )
        
        # Use progressive escalation
        if hasattr(self.acp, 'progressive_escalation'):
            self.acp.progressive_escalation(agent, rescue_msg, MsgTag.RESCUE)
        else:
            # Fallback to traditional rescue
            self.acp.send(agent, rescue_msg, MsgTag.RESCUE, new_chat=False)
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get current system status."""
        return {
            "timestamp": datetime.now().isoformat(),
            "timing_config": self.timing_config,
            "agent_states": self.agent_states,
            "onboarding_status": self.onboarding_status,
            "response_monitor_status": self.response_monitor.get_status()
        }

class ResponseMonitor:
    """Monitors actual agent responses using multiple detection methods."""
    
    def __init__(self):
        self.response_files = {}
        self.last_response_times = {}
        self.response_patterns = [
            "Task:", "Actions Taken:", "Status:", "Commit Message:",
            "✅", "🟡", "🔄", "📋", "🎯"
        ]
    
    def start(self):
        """Start response monitoring."""
        print("📡 Starting response monitoring system...")
        # Initialize monitoring for each agent
        for agent in ["Agent-1", "Agent-2", "Agent-3", "Agent-4"]:
            self._init_agent_monitoring(agent)
    
    def _init_agent_monitoring(self, agent: str):
        """Initialize monitoring for a specific agent."""
        # Monitor response.txt files
        response_file = Path(f"agent_workspaces/{agent}/response.txt")
        if response_file.exists():
            self.response_files[agent] = response_file
            self.last_response_times[agent] = response_file.stat().st_mtime
            print(f"📁 Monitoring {agent} response file: {response_file}")
    
    def has_agent_responded(self, agent: str, since_time: float) -> bool:
        """Check if agent has responded since the given time."""
        if agent not in self.response_files:
            return False
        
        response_file = self.response_files[agent]
        if not response_file.exists():
            return False
        
        try:
            # Check file modification time
            mtime = response_file.stat().st_mtime
            if mtime > since_time:
                # Check if file has actual content
                content = response_file.read_text(encoding="utf-8").strip()
                if content and any(pattern in content for pattern in self.response_patterns):
                    self.last_response_times[agent] = mtime
                    return True
        except Exception:
            pass
        
        return False
    
    def get_status(self) -> Dict[str, Any]:
        """Get response monitor status."""
        return {
            "monitored_agents": list(self.response_files.keys()),
            "last_response_times": self.last_response_times,
            "response_patterns": self.response_patterns
        }

def main():
    """Main entry point for fixed stall detection system."""
    print("🔧 FIXING STALL DETECTION SYSTEM")
    print("=" * 60)
    
    # Create and start the fixed system
    system = FixedStallDetectionSystem()
    
    try:
        system.start_monitoring()
    except KeyboardInterrupt:
        print("\n🛑 System stopped by user")
    except Exception as e:
        print(f"❌ System error: {e}")
    
    # Print final status
    print("\n📊 FINAL SYSTEM STATUS:")
    print("=" * 40)
    status = system.get_system_status()
    print(json.dumps(status, indent=2))

if __name__ == "__main__":
    main()
