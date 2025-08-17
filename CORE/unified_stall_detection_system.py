#!/usr/bin/env python3
"""
🚨 UNIFIED STALL DETECTION & MITIGATION SYSTEM v2.0
===================================================
Modular stall detection and mitigation package consolidating all stall-related
functionality for comprehensive agent monitoring and rescue operations.
"""

import json
import time
import threading
import logging
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Union, Callable
from dataclasses import dataclass, asdict
from enum import Enum
import queue
import random

# Add src to path for imports
import sys
sys.path.insert(0, str(Path(__file__).parent / "src"))

try:
    from src.services.agent_cell_phone import AgentCellPhone, MsgTag
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure you're running from the project root directory")
    sys.exit(1)

class StallLevel(Enum):
    """Stall severity levels"""
    NONE = "none"
    WARNING = "warning"
    MODERATE = "moderate"
    SEVERE = "severe"
    CRITICAL = "critical"

class MitigationStrategy(Enum):
    """Stall mitigation strategies"""
    GENTLE_NUDGE = "gentle_nudge"
    ESCALATION = "escalation"
    RESCUE_OPERATION = "rescue_operation"
    EMERGENCY_OVERRIDE = "emergency_override"
    COLLABORATIVE_INTERVENTION = "collaborative_intervention"

class AgentStatus(Enum):
    """Agent operational status"""
    ACTIVE = "active"
    RESPONDING = "responding"
    SLOW = "slow"
    STALLED = "stalled"
    RECOVERING = "recovering"
    OFFLINE = "offline"

@dataclass
class StallEvent:
    """Stall event record"""
    event_id: str
    agent_id: str
    stall_level: StallLevel
    detection_time: datetime
    duration_minutes: float
    mitigation_strategy: MitigationStrategy
    resolution_time: Optional[datetime] = None
    resolution_method: Optional[str] = None
    notes: Optional[str] = None

@dataclass
class AgentState:
    """Agent state tracking"""
    agent_id: str
    status: AgentStatus
    last_message_sent: datetime
    last_response_received: datetime
    response_count: int
    stall_warnings: int
    consecutive_stalls: int
    total_stall_time: float
    recovery_attempts: int
    last_recovery_attempt: Optional[datetime] = None

class StallDetectionEngine:
    """Core stall detection engine with configurable thresholds"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Timing thresholds
        self.thresholds = {
            "normal_response_time": config.get("normal_response_time", 300),      # 5 minutes
            "warn_threshold": config.get("warn_threshold", 480),                  # 8 minutes
            "moderate_threshold": config.get("moderate_threshold", 600),          # 10 minutes
            "severe_threshold": config.get("severe_threshold", 900),              # 15 minutes
            "critical_threshold": config.get("critical_threshold", 1200),         # 20 minutes
            "rescue_cooldown": config.get("rescue_cooldown", 300),               # 5 minutes
            "check_interval": config.get("check_interval", 30),                  # 30 seconds
            "onboarding_grace_period": config.get("onboarding_grace_period", 600) # 10 minutes
        }
    
    def detect_stall_level(self, agent_state: AgentState, current_time: datetime) -> StallLevel:
        """Detect stall level based on agent state and timing"""
        time_since_message = (current_time - agent_state.last_message_sent).total_seconds()
        time_since_response = (current_time - agent_state.last_response_received).total_seconds()
        
        # Check if agent is in onboarding grace period
        if agent_state.status == AgentStatus.RECOVERING:
            if time_since_response < self.thresholds["onboarding_grace_period"]:
                return StallLevel.NONE
        
        # Determine stall level based on response time
        if time_since_response <= self.thresholds["normal_response_time"]:
            return StallLevel.NONE
        elif time_since_response <= self.thresholds["warn_threshold"]:
            return StallLevel.WARNING
        elif time_since_response <= self.thresholds["moderate_threshold"]:
            return StallLevel.MODERATE
        elif time_since_response <= self.thresholds["severe_threshold"]:
            return StallLevel.SEVERE
        else:
            return StallLevel.CRITICAL
    
    def should_mitigate(self, agent_state: AgentState, stall_level: StallLevel) -> bool:
        """Determine if mitigation should be attempted"""
        # Don't mitigate if agent is already recovering
        if agent_state.status == AgentStatus.RECOVERING:
            return False
        
        # Check cooldown period
        if agent_state.last_recovery_attempt:
            time_since_last_attempt = (datetime.now() - agent_state.last_recovery_attempt).total_seconds()
            if time_since_last_attempt < self.thresholds["rescue_cooldown"]:
                return False
        
        # Mitigate based on stall level and agent history
        if stall_level == StallLevel.CRITICAL:
            return True
        elif stall_level == StallLevel.SEVERE and agent_state.consecutive_stalls >= 2:
            return True
        elif stall_level == StallLevel.MODERATE and agent_state.consecutive_stalls >= 3:
            return True
        elif stall_level == StallLevel.WARNING and agent_state.consecutive_stalls >= 5:
            return True
        
        return False

class StallMitigationEngine:
    """Stall mitigation engine with multiple strategies"""
    
    def __init__(self, agent_cellphone: AgentCellPhone, config: Dict[str, Any]):
        self.acp = agent_cellphone
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Mitigation strategies and their implementations
        self.mitigation_strategies = {
            MitigationStrategy.GENTLE_NUDGE: self._gentle_nudge,
            MitigationStrategy.ESCALATION: self._escalation,
            MitigationStrategy.RESCUE_OPERATION: self._rescue_operation,
            MitigationStrategy.EMERGENCY_OVERRIDE: self._emergency_override,
            MitigationStrategy.COLLABORATIVE_INTERVENTION: self._collaborative_intervention
        }
        
        # Nudge messages for different stall levels
        self.nudge_messages = {
            StallLevel.WARNING: [
                "Hey there! Just checking in on your progress.",
                "How's the work coming along?",
                "Let me know if you need any help or clarification."
            ],
            StallLevel.MODERATE: [
                "I notice you might be stuck. Can I assist with anything?",
                "Is there a specific issue you're encountering?",
                "Let's work through this together - what's blocking you?"
            ],
            StallLevel.SEVERE: [
                "🚨 STALL ALERT: You appear to be significantly delayed.",
                "⚠️ This is taking longer than expected. Do you need immediate assistance?",
                "🔴 CRITICAL: Please respond to confirm you're still working."
            ],
            StallLevel.CRITICAL: [
                "🚨 EMERGENCY STALL DETECTED!",
                "🔴 AGENT UNRESPONSIVE - IMMEDIATE ACTION REQUIRED!",
                "🚨 RESCUE OPERATION INITIATED!"
            ]
        }
    
    def execute_mitigation(self, agent_id: str, stall_level: StallLevel, agent_state: AgentState) -> bool:
        """Execute appropriate mitigation strategy"""
        try:
            # Select mitigation strategy based on stall level
            strategy = self._select_mitigation_strategy(stall_level, agent_state)
            
            # Execute the strategy
            success = self.mitigation_strategies[strategy](agent_id, stall_level, agent_state)
            
            if success:
                self.logger.info(f"✅ Mitigation strategy {strategy} executed successfully for {agent_id}")
                return True
            else:
                self.logger.warning(f"⚠️ Mitigation strategy {strategy} failed for {agent_id}")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Mitigation execution error for {agent_id}: {e}")
            return False
    
    def _select_mitigation_strategy(self, stall_level: StallLevel, agent_state: AgentState) -> MitigationStrategy:
        """Select appropriate mitigation strategy"""
        if stall_level == StallLevel.CRITICAL:
            return MitigationStrategy.EMERGENCY_OVERRIDE
        elif stall_level == StallLevel.SEVERE:
            return MitigationStrategy.RESCUE_OPERATION
        elif stall_level == StallLevel.MODERATE:
            return MitigationStrategy.ESCALATION
        elif stall_level == StallLevel.WARNING:
            return MitigationStrategy.GENTLE_NUDGE
        else:
            return MitigationStrategy.GENTLE_NUDGE
    
    def _gentle_nudge(self, agent_id: str, stall_level: StallLevel, agent_state: AgentState) -> bool:
        """Send gentle nudge message"""
        try:
            messages = self.nudge_messages[stall_level]
            message = random.choice(messages)
            
            self.acp.send_message(
                agent_id,
                message,
                MsgTag.INFO
            )
            
            return True
            
        except Exception as e:
            self.logger.error(f"Gentle nudge failed: {e}")
            return False
    
    def _escalation(self, agent_id: str, stall_level: StallLevel, agent_state: AgentState) -> bool:
        """Escalate to more urgent communication"""
        try:
            # Send urgent message
            urgent_message = f"🚨 URGENT: {agent_id}, you are experiencing delays. Please respond immediately."
            
            self.acp.send_message(
                agent_id,
                urgent_message,
                MsgTag.IMPORTANT
            )
            
            # Notify other agents
            self.acp.send_message(
                "ALL",
                f"⚠️ Agent {agent_id} is experiencing delays. Monitoring closely.",
                MsgTag.INFO
            )
            
            return True
            
        except Exception as e:
            self.logger.error(f"Escalation failed: {e}")
            return False
    
    def _rescue_operation(self, agent_id: str, stall_level: StallLevel, agent_state: AgentState) -> bool:
        """Execute rescue operation"""
        try:
            # Send rescue message
            rescue_message = f"🚨 RESCUE OPERATION: {agent_id}, initiating emergency recovery procedures."
            
            self.acp.send_message(
                agent_id,
                rescue_message,
                MsgTag.IMPORTANT
            )
            
            # Notify all agents of rescue operation
            self.acp.send_message(
                "ALL",
                f"🚨 RESCUE OPERATION INITIATED for {agent_id}. All agents standby for assistance.",
                MsgTag.IMPORTANT
            )
            
            # Attempt collaborative intervention
            self._collaborative_intervention(agent_id, stall_level, agent_state)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Rescue operation failed: {e}")
            return False
    
    def _emergency_override(self, agent_id: str, stall_level: StallLevel, agent_state: AgentState) -> bool:
        """Execute emergency override procedures"""
        try:
            # Send emergency override message
            emergency_message = f"🚨 EMERGENCY OVERRIDE: {agent_id}, system taking control. Standby for recovery."
            
            self.acp.send_message(
                agent_id,
                emergency_message,
                MsgTag.IMPORTANT
            )
            
            # Notify all agents of emergency
            self.acp.send_message(
                "ALL",
                f"🚨 EMERGENCY OVERRIDE for {agent_id}. System taking control.",
                MsgTag.IMPORTANT
            )
            
            # Log emergency action
            self.logger.critical(f"🚨 EMERGENCY OVERRIDE executed for {agent_id}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Emergency override failed: {e}")
            return False
    
    def _collaborative_intervention(self, agent_id: str, stall_level: StallLevel, agent_state: AgentState) -> bool:
        """Execute collaborative intervention with other agents"""
        try:
            # Request assistance from other agents
            assistance_message = f"🤝 COLLABORATIVE INTERVENTION: {agent_id} needs assistance. Other agents, please help."
            
            self.acp.send_message(
                "ALL",
                assistance_message,
                MsgTag.INFO
            )
            
            return True
            
        except Exception as e:
            self.logger.error(f"Collaborative intervention failed: {e}")
            return False

class ResponseMonitor:
    """Monitors agent responses to detect activity"""
    
    def __init__(self, agent_cellphone: AgentCellPhone):
        self.acp = agent_cellphone
        self.logger = logging.getLogger(__name__)
        self.response_history = {}
        self.monitoring_active = False
    
    def start_monitoring(self):
        """Start response monitoring"""
        self.monitoring_active = True
        self.logger.info("✅ Response monitoring started")
    
    def stop_monitoring(self):
        """Stop response monitoring"""
        self.monitoring_active = False
        self.logger.info("🛑 Response monitoring stopped")
    
    def has_agent_responded(self, agent_id: str, since_time: datetime) -> bool:
        """Check if agent has responded since a given time"""
        # This would integrate with actual agent cellphone response detection
        # For now, we'll simulate response detection
        return False
    
    def record_response(self, agent_id: str, response_time: datetime):
        """Record agent response"""
        if agent_id not in self.response_history:
            self.response_history[agent_id] = []
        
        self.response_history[agent_id].append(response_time)
        self.logger.info(f"📝 Response recorded for {agent_id} at {response_time}")

class UnifiedStallDetectionSystem:
    """
    🚨 UNIFIED STALL DETECTION & MITIGATION SYSTEM
    Comprehensive stall detection and mitigation with multiple strategies
    """
    
    def __init__(self, layout_mode: str = "5-agent", config_path: str = "config/stall_detection_config.json"):
        # Initialize agent cellphone
        self.acp = AgentCellPhone(agent_id="Stall-Detection-System", layout_mode=layout_mode)
        
        # Load configuration
        self.config = self.load_config(config_path)
        
        # Initialize components
        self.detection_engine = StallDetectionEngine(self.config)
        self.mitigation_engine = StallMitigationEngine(self.acp, self.config)
        self.response_monitor = ResponseMonitor(self.acp)
        
        # Agent tracking
        self.agents = ["Agent-1", "Agent-2", "Agent-3", "Agent-4", "Agent-5"]
        self.agent_states: Dict[str, AgentState] = {}
        
        # Stall event tracking
        self.stall_events: List[StallEvent] = []
        self.stall_history: Dict[str, List[StallEvent]] = {}
        
        # System state
        self.is_monitoring = False
        self.monitoring_thread = None
        
        # Setup logging
        self.setup_logging()
        
        # Initialize agent states
        self._initialize_agent_states()
        
        # Start response monitoring
        self.response_monitor.start_monitoring()
    
    def setup_logging(self):
        """Setup logging for the stall detection system"""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s | %(levelname)s | %(message)s',
            handlers=[
                logging.FileHandler(log_dir / "stall_detection_system.log"),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def load_config(self, config_path: str) -> Dict[str, Any]:
        """Load stall detection configuration"""
        try:
            if Path(config_path).exists():
                with open(config_path, 'r') as f:
                    config = json.load(f)
                    self.logger.info("✅ Stall detection configuration loaded")
                    return config
            else:
                self.logger.warning("⚠️ Config not found, using defaults")
                return self.get_default_config()
        except Exception as e:
            self.logger.error(f"❌ Error loading config: {e}")
            return self.get_default_config()
    
    def get_default_config(self) -> Dict[str, Any]:
        """Return default configuration"""
        return {
            "normal_response_time": 300,      # 5 minutes
            "warn_threshold": 480,            # 8 minutes
            "moderate_threshold": 600,        # 10 minutes
            "severe_threshold": 900,          # 15 minutes
            "critical_threshold": 1200,       # 20 minutes
            "rescue_cooldown": 300,           # 5 minutes
            "check_interval": 30,             # 30 seconds
            "onboarding_grace_period": 600,   # 10 minutes
            "auto_mitigation": True,
            "collaborative_rescue": True,
            "emergency_override": True
        }
    
    def _initialize_agent_states(self):
        """Initialize agent states"""
        current_time = datetime.now()
        
        for agent in self.agents:
            self.agent_states[agent] = AgentState(
                agent_id=agent,
                status=AgentStatus.ACTIVE,
                last_message_sent=current_time,
                last_response_received=current_time,
                response_count=0,
                stall_warnings=0,
                consecutive_stalls=0,
                total_stall_time=0.0,
                recovery_attempts=0,
                last_recovery_attempt=None
            )
            
            self.stall_history[agent] = []
        
        self.logger.info(f"✅ Initialized {len(self.agents)} agent states")
    
    def start_monitoring(self):
        """Start the stall detection system"""
        if self.is_monitoring:
            self.logger.warning("⚠️ Monitoring already active")
            return
        
        self.is_monitoring = True
        self.monitoring_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        self.monitoring_thread.start()
        
        self.logger.info("🚀 Stall detection monitoring started")
    
    def stop_monitoring(self):
        """Stop the stall detection system"""
        self.is_monitoring = False
        
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5)
        
        self.logger.info("🛑 Stall detection monitoring stopped")
    
    def _monitoring_loop(self):
        """Main monitoring loop"""
        while self.is_monitoring:
            try:
                current_time = datetime.now()
                
                # Check each agent for stalls
                for agent_id, agent_state in self.agent_states.items():
                    self._check_agent_stall(agent_id, agent_state, current_time)
                
                # Sleep between checks
                time.sleep(self.config["check_interval"])
                
            except Exception as e:
                self.logger.error(f"Monitoring loop error: {e}")
                time.sleep(10)
    
    def _check_agent_stall(self, agent_id: str, agent_state: AgentState, current_time: datetime):
        """Check individual agent for stall conditions"""
        try:
            # Detect stall level
            stall_level = self.detection_engine.detect_stall_level(agent_state, current_time)
            
            # Update agent state
            self._update_agent_state(agent_id, agent_state, stall_level, current_time)
            
            # Execute mitigation if needed
            if stall_level != StallLevel.NONE:
                if self.detection_engine.should_mitigate(agent_state, stall_level):
                    self._execute_stall_mitigation(agent_id, stall_level, agent_state)
                
                # Record stall event
                self._record_stall_event(agent_id, stall_level, current_time)
            
        except Exception as e:
            self.logger.error(f"Error checking agent {agent_id}: {e}")
    
    def _update_agent_state(self, agent_id: str, agent_state: AgentState, stall_level: StallLevel, current_time: datetime):
        """Update agent state based on stall detection"""
        if stall_level != StallLevel.NONE:
            agent_state.consecutive_stalls += 1
            agent_state.stall_warnings += 1
            
            if stall_level in [StallLevel.SEVERE, StallLevel.CRITICAL]:
                agent_state.status = AgentStatus.STALLED
            elif stall_level == StallLevel.MODERATE:
                agent_state.status = AgentStatus.SLOW
            elif stall_level == StallLevel.WARNING:
                agent_state.status = AgentStatus.SLOW
        else:
            # Agent is responding normally
            agent_state.consecutive_stalls = 0
            agent_state.status = AgentStatus.ACTIVE
    
    def _execute_stall_mitigation(self, agent_id: str, stall_level: StallLevel, agent_state: AgentState):
        """Execute stall mitigation"""
        try:
            # Update recovery attempt tracking
            agent_state.recovery_attempts += 1
            agent_state.last_recovery_attempt = datetime.now()
            
            # Execute mitigation
            success = self.mitigation_engine.execute_mitigation(agent_id, stall_level, agent_state)
            
            if success:
                self.logger.info(f"✅ Mitigation executed for {agent_id} (stall level: {stall_level.value})")
            else:
                self.logger.warning(f"⚠️ Mitigation failed for {agent_id}")
                
        except Exception as e:
            self.logger.error(f"❌ Mitigation execution error for {agent_id}: {e}")
    
    def _record_stall_event(self, agent_id: str, stall_level: StallLevel, detection_time: datetime):
        """Record stall event for tracking"""
        stall_event = StallEvent(
            event_id=f"stall_{int(time.time())}_{agent_id}",
            agent_id=agent_id,
            stall_level=stall_level,
            detection_time=detection_time,
            duration_minutes=0.0,
            mitigation_strategy=MitigationStrategy.GENTLE_NUDGE
        )
        
        self.stall_events.append(stall_event)
        self.stall_history[agent_id].append(stall_event)
        
        self.logger.info(f"📝 Stall event recorded: {agent_id} - {stall_level.value}")
    
    def get_agent_status(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get comprehensive agent status"""
        if agent_id not in self.agent_states:
            return None
        
        agent_state = self.agent_states[agent_id]
        stall_events = self.stall_history[agent_id]
        
        return {
            "agent_id": agent_id,
            "status": agent_state.status.value,
            "last_message_sent": agent_state.last_message_sent.isoformat(),
            "last_response_received": agent_state.last_response_received.isoformat(),
            "response_count": agent_state.response_count,
            "stall_warnings": agent_state.stall_warnings,
            "consecutive_stalls": agent_state.consecutive_stalls,
            "total_stall_time": agent_state.total_stall_time,
            "recovery_attempts": agent_state.recovery_attempts,
            "stall_events_count": len(stall_events),
            "recent_stalls": [event.stall_level.value for event in stall_events[-5:]]
        }
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get overall system status"""
        total_stalls = sum(len(events) for events in self.stall_history.values())
        active_stalls = sum(1 for state in self.agent_states.values() if state.status in [AgentStatus.STALLED, AgentStatus.SLOW])
        
        return {
            "monitoring_active": self.is_monitoring,
            "agents_monitored": len(self.agents),
            "total_stall_events": total_stalls,
            "active_stalls": active_stalls,
            "system_health": "healthy" if active_stalls == 0 else "degraded" if active_stalls < 3 else "critical"
        }

def main():
    """Main function to demonstrate the unified stall detection system"""
    print("🚨 UNIFIED STALL DETECTION & MITIGATION SYSTEM")
    print("=" * 60)
    
    # Initialize the system
    system = UnifiedStallDetectionSystem()
    
    # Display system status
    status = system.get_system_status()
    print(f"\n📊 SYSTEM STATUS:")
    print(f"Monitoring: {'✅ Active' if status['monitoring_active'] else '❌ Inactive'}")
    print(f"Agents Monitored: {status['agents_monitored']}")
    print(f"Total Stall Events: {status['total_stall_events']}")
    print(f"Active Stalls: {status['active_stalls']}")
    print(f"System Health: {status['system_health'].upper()}")
    
    print(f"\n🎯 FEATURES:")
    print("• Multi-level stall detection")
    print("• Adaptive mitigation strategies")
    print("• Collaborative intervention")
    print("• Emergency override procedures")
    print("• Comprehensive monitoring")
    print("• Response tracking")
    
    print(f"\n✅ System initialized successfully!")
    print("Press Ctrl+C to stop...")
    
    try:
        # Start monitoring
        system.start_monitoring()
        
        # Keep system running
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n🛑 Shutting down stall detection system...")
        system.stop_monitoring()

if __name__ == "__main__":
    main()


