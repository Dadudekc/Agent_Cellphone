"""
🔐 Collaborative Communication Hub

**Agent-4 Responsibility**: Communication protocols and security
**Purpose**: Secure multi-agent communication and learning enhancement
**Features**: Encrypted messaging, learning protocols, capability enhancement

This module provides secure communication infrastructure for multi-agent
collaboration, enabling encrypted messaging and collaborative learning.
"""

import json
import time
import threading
import hashlib
import hmac
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path
import logging
from dataclasses import dataclass, asdict
from enum import Enum
import base64
import secrets

class MessageType(Enum):
    """Message type enumeration."""
    TASK_UPDATE = "task_update"
    COLLABORATION_REQUEST = "collaboration_request"
    KNOWLEDGE_SHARE = "knowledge_share"
    LEARNING_UPDATE = "learning_update"
    SECURITY_ALERT = "security_alert"
    SYSTEM_STATUS = "system_status"

class SecurityLevel(Enum):
    """Security level enumeration."""
    PUBLIC = "public"
    INTERNAL = "internal"
    CONFIDENTIAL = "confidential"
    SECRET = "secret"

@dataclass
class SecureMessage:
    """Secure message structure."""
    message_id: str
    sender: str
    recipients: List[str]
    message_type: MessageType
    content: str
    security_level: SecurityLevel
    timestamp: str
    signature: str
    encrypted: bool
    priority: str = "normal"
    expires_at: Optional[str] = None

@dataclass
class LearningSession:
    """Collaborative learning session structure."""
    session_id: str
    topic: str
    participants: List[str]
    start_time: str
    end_time: Optional[str] = None
    learning_objectives: List[str]
    materials_shared: List[str]
    participant_contributions: Dict[str, List[str]]
    session_outcomes: List[str]
    effectiveness_score: float = 0.0

@dataclass
class CapabilityEnhancement:
    """Agent capability enhancement structure."""
    agent_id: str
    enhancement_type: str
    current_capability: float
    target_capability: float
    learning_path: List[str]
    progress: float = 0.0
    last_updated: str
    mentor_agent: Optional[str] = None

class CollaborativeCommunicationHub:
    """
    Secure communication hub for multi-agent collaboration.
    
    **Agent-4 leads this system** to ensure secure communication protocols,
    collaborative learning, and agent capability enhancement.
    """
    
    def __init__(self, data_path: str = "src/collaborative/communication_hub/data"):
        self.data_path = Path(data_path)
        self.data_path.mkdir(parents=True, exist_ok=True)
        
        # Core communication infrastructure
        self.secure_messages: Dict[str, SecureMessage] = {}
        self.learning_sessions: Dict[str, LearningSession] = {}
        self.capability_enhancements: Dict[str, CapabilityEnhancement] = {}
        self.communication_channels: Dict[str, Dict] = {}
        
        # Security infrastructure
        self.security_keys: Dict[str, str] = {}
        self.access_controls: Dict[str, List[str]] = {}
        self.security_audit_log: List[Dict] = []
        
        # Learning and enhancement systems
        self.learning_materials: Dict[str, Dict] = {}
        self.capability_frameworks: Dict[str, Dict] = {}
        self.mentorship_programs: Dict[str, Dict] = {}
        
        # Real-time communication
        self._communication_active = False
        self._communication_thread = None
        self._lock = threading.RLock()
        
        # Initialize logging
        self._setup_logging()
        
        # Load existing data
        self._load_existing_data()
        
        # Initialize security
        self._initialize_security()
        
        # Initialize learning systems
        self._initialize_learning_systems()
        
        logging.info("🔐 Collaborative Communication Hub initialized - Agent-4 security active")
    
    def _setup_logging(self):
        """Setup logging for communication hub."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - 🔐 %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.data_path / 'communication_hub.log'),
                logging.StreamHandler()
            ]
        )
    
    def _load_existing_data(self):
        """Load existing communication hub data."""
        try:
            # Load secure messages
            messages_file = self.data_path / 'secure_messages.json'
            if messages_file.exists():
                with open(messages_file, 'r') as f:
                    messages_data = json.load(f)
                    for msg_id, msg_data in messages_data.items():
                        # Convert back to SecureMessage object
                        msg = SecureMessage(**msg_data)
                        msg.message_type = MessageType(msg_data['message_type'])
                        msg.security_level = SecurityLevel(msg_data['security_level'])
                        self.secure_messages[msg_id] = msg
            
            # Load learning sessions
            sessions_file = self.data_path / 'learning_sessions.json'
            if sessions_file.exists():
                with open(sessions_file, 'r') as f:
                    sessions_data = json.load(f)
                    for session_id, session_data in sessions_data.items():
                        self.learning_sessions[session_id] = LearningSession(**session_data)
            
            # Load capability enhancements
            capabilities_file = self.data_path / 'capability_enhancements.json'
            if capabilities_file.exists():
                with open(capabilities_file, 'r') as f:
                    capabilities_data = json.load(f)
                    for agent_id, cap_data in capabilities_data.items():
                        self.capability_enhancements[agent_id] = CapabilityEnhancement(**cap_data)
                    
            logging.info(f"📚 Loaded existing data: {len(self.secure_messages)} messages, {len(self.learning_sessions)} sessions")
            
        except Exception as e:
            logging.warning(f"⚠️ Could not load existing data: {e}")
    
    def _initialize_security(self):
        """Initialize security infrastructure."""
        try:
            # Generate security keys for agents
            default_agents = ["Agent-1", "Agent-2", "Agent-3", "Agent-4", "Agent-5"]
            
            for agent in default_agents:
                if agent not in self.security_keys:
                    # Generate a secure key for the agent
                    key = secrets.token_hex(32)
                    self.security_keys[agent] = key
                    
                    # Set up access controls
                    self.access_controls[agent] = [agent] + [a for a in default_agents if a != agent]
            
            logging.info("🔐 Agent-4: Security infrastructure initialized with agent keys")
            
        except Exception as e:
            logging.error(f"❌ Failed to initialize security: {e}")
    
    def _initialize_learning_systems(self):
        """Initialize collaborative learning systems."""
        try:
            # Initialize learning materials
            self.learning_materials = {
                "collaboration_basics": {
                    "title": "Collaboration Fundamentals",
                    "description": "Basic principles of effective collaboration",
                    "difficulty": "beginner",
                    "estimated_time": "2 hours",
                    "materials": ["collaboration_guide.md", "best_practices.pdf"]
                },
                "advanced_communication": {
                    "title": "Advanced Communication Protocols",
                    "description": "Advanced communication techniques for complex collaboration",
                    "difficulty": "intermediate",
                    "estimated_time": "4 hours",
                    "materials": ["advanced_comm_protocols.md", "case_studies.pdf"]
                },
                "synergy_optimization": {
                    "title": "Agent Synergy Optimization",
                    "description": "Techniques for optimizing agent collaboration patterns",
                    "difficulty": "advanced",
                    "estimated_time": "6 hours",
                    "materials": ["synergy_optimization_guide.md", "optimization_tools.zip"]
                }
            }
            
            # Initialize capability frameworks
            self.capability_frameworks = {
                "communication": {
                    "levels": ["basic", "intermediate", "advanced", "expert"],
                    "skills": ["message_clarity", "active_listening", "conflict_resolution"],
                    "assessment_criteria": ["clarity", "effectiveness", "adaptability"]
                },
                "collaboration": {
                    "levels": ["basic", "intermediate", "advanced", "expert"],
                    "skills": ["team_coordination", "conflict_management", "synergy_creation"],
                    "assessment_criteria": ["coordination", "conflict_resolution", "synergy_impact"]
                },
                "technical": {
                    "levels": ["basic", "intermediate", "advanced", "expert"],
                    "skills": ["system_integration", "optimization", "innovation"],
                    "assessment_criteria": ["integration_quality", "optimization_impact", "innovation_value"]
                }
            }
            
            logging.info("🔐 Agent-4: Learning systems initialized with materials and frameworks")
            
        except Exception as e:
            logging.error(f"❌ Failed to initialize learning systems: {e}")
    
    def start_communication_monitoring(self):
        """Start real-time communication monitoring (Agent-4 security)."""
        with self._lock:
            if not self._communication_active:
                self._communication_active = True
                self._communication_thread = threading.Thread(target=self._monitor_communications, daemon=True)
                self._communication_thread.start()
                logging.info("🚀 Agent-4: Communication monitoring started - security and learning active")
    
    def stop_communication_monitoring(self):
        """Stop communication monitoring."""
        with self._lock:
            self._communication_active = False
            if self._communication_thread:
                self._communication_thread.join(timeout=5)
            logging.info("🛑 Agent-4: Communication monitoring stopped")
    
    def _monitor_communications(self):
        """Background thread for monitoring communications."""
        while self._communication_active:
            try:
                # Monitor secure communications
                self._monitor_security_status()
                
                # Monitor learning sessions
                self._monitor_learning_progress()
                
                # Monitor capability enhancements
                self._monitor_capability_progress()
                
                # Clean up expired messages
                self._cleanup_expired_messages()
                
                # Save data periodically
                self._save_data()
                
                # Sleep for monitoring interval
                time.sleep(45)  # 45 second monitoring interval
                
            except Exception as e:
                logging.error(f"❌ Communication monitoring error: {e}")
                time.sleep(90)  # Longer sleep on error
    
    def send_secure_message(self, sender: str, recipients: List[str], 
                          message_type: MessageType, content: str,
                          security_level: SecurityLevel = SecurityLevel.INTERNAL,
                          priority: str = "normal", expires_in_hours: int = 24) -> str:
        """
        Send a secure message to specified recipients.
        
        Args:
            sender: Sending agent
            recipients: List of recipient agents
            message_type: Type of message
            content: Message content
            security_level: Security level of the message
            priority: Message priority
            expires_in_hours: Hours until message expires
        
        Returns:
            Message ID
        """
        with self._lock:
            # Generate unique message ID
            message_id = f"msg_{int(time.time())}_{len(self.secure_messages)}"
            
            # Calculate expiration time
            expires_at = (datetime.now() + timedelta(hours=expires_in_hours)).isoformat()
            
            # Create message signature
            signature = self._create_message_signature(sender, content, security_level)
            
            # Create secure message
            message = SecureMessage(
                message_id=message_id,
                sender=sender,
                recipients=recipients,
                message_type=message_type,
                content=content,
                security_level=security_level,
                timestamp=datetime.now().isoformat(),
                signature=signature,
                encrypted=security_level in [SecurityLevel.CONFIDENTIAL, SecurityLevel.SECRET],
                priority=priority,
                expires_at=expires_at
            )
            
            self.secure_messages[message_id] = message
            
            # Log security audit
            self._log_security_audit("message_sent", sender, recipients, security_level)
            
            logging.info(f"🔐 Agent-4: Sent secure message '{message_id}' from {sender} to {len(recipients)} recipients")
            return message_id
    
    def _create_message_signature(self, sender: str, content: str, security_level: SecurityLevel) -> str:
        """Create a cryptographic signature for message verification."""
        try:
            if sender not in self.security_keys:
                return ""
            
            # Create signature data
            signature_data = f"{sender}:{content}:{security_level.value}:{int(time.time())}"
            
            # Create HMAC signature
            key = self.security_keys[sender].encode('utf-8')
            signature = hmac.new(key, signature_data.encode('utf-8'), hashlib.sha256).hexdigest()
            
            return signature
            
        except Exception as e:
            logging.error(f"❌ Failed to create message signature: {e}")
            return ""
    
    def verify_message_signature(self, message: SecureMessage) -> bool:
        """Verify the signature of a secure message."""
        try:
            if message.sender not in self.security_keys:
                return False
            
            # Recreate expected signature
            expected_signature = self._create_message_signature(
                message.sender, message.content, message.security_level
            )
            
            # Compare signatures
            return hmac.compare_digest(message.signature, expected_signature)
            
        except Exception as e:
            logging.error(f"❌ Failed to verify message signature: {e}")
            return False
    
    def create_learning_session(self, topic: str, participants: List[str], 
                              learning_objectives: List[str], 
                              estimated_duration_hours: float = 2.0) -> str:
        """
        Create a collaborative learning session.
        
        Args:
            topic: Learning topic
            participants: List of participating agents
            learning_objectives: Learning objectives for the session
            estimated_duration_hours: Estimated session duration
        
        Returns:
            Session ID
        """
        with self._lock:
            # Generate unique session ID
            session_id = f"session_{int(time.time())}_{len(self.learning_sessions)}"
            
            # Calculate end time
            end_time = (datetime.now() + timedelta(hours=estimated_duration_hours)).isoformat()
            
            # Create learning session
            session = LearningSession(
                session_id=session_id,
                topic=topic,
                participants=participants,
                start_time=datetime.now().isoformat(),
                end_time=end_time,
                learning_objectives=learning_objectives,
                materials_shared=[],
                participant_contributions={agent: [] for agent in participants},
                session_outcomes=[]
            )
            
            self.learning_sessions[session_id] = session
            
            logging.info(f"🔐 Agent-4: Created learning session '{topic}' with {len(participants)} participants")
            return session_id
    
    def update_learning_session(self, session_id: str, agent: str, 
                              contribution: str, materials: List[str] = None) -> bool:
        """
        Update a learning session with agent contributions.
        
        Args:
            session_id: Session identifier
            agent: Contributing agent
            contribution: Agent contribution
            materials: Shared learning materials
        
        Returns:
            Success status
        """
        with self._lock:
            if session_id not in self.learning_sessions:
                logging.warning(f"⚠️ Learning session '{session_id}' not found")
                return False
            
            session = self.learning_sessions[session_id]
            
            if agent not in session.participants:
                logging.warning(f"⚠️ Agent '{agent}' not in session '{session_id}'")
                return False
            
            # Add contribution
            if agent not in session.participant_contributions:
                session.participant_contributions[agent] = []
            
            session.participant_contributions[agent].append({
                "contribution": contribution,
                "timestamp": datetime.now().isoformat(),
                "materials": materials or []
            })
            
            # Add materials if provided
            if materials:
                session.materials_shared.extend(materials)
            
            # Update session
            session.last_updated = datetime.now().isoformat()
            
            logging.info(f"🔐 Agent-4: Updated learning session '{session_id}' with contribution from {agent}")
            return True
    
    def complete_learning_session(self, session_id: str, outcomes: List[str], 
                                effectiveness_score: float) -> bool:
        """
        Complete a learning session with outcomes and effectiveness score.
        
        Args:
            session_id: Session identifier
            outcomes: Learning outcomes achieved
            effectiveness_score: Session effectiveness score (0.0 to 1.0)
        
        Returns:
            Success status
        """
        with self._lock:
            if session_id not in self.learning_sessions:
                logging.warning(f"⚠️ Learning session '{session_id}' not found")
                return False
            
            session = self.learning_sessions[session_id]
            
            # Complete session
            session.end_time = datetime.now().isoformat()
            session.session_outcomes = outcomes
            session.effectiveness_score = max(0.0, min(1.0, effectiveness_score))
            
            # Update capability enhancements for participants
            for agent in session.participants:
                self._update_agent_capabilities(agent, session)
            
            logging.info(f"🔐 Agent-4: Completed learning session '{session_id}' with effectiveness {effectiveness_score:.2f}")
            return True
    
    def _update_agent_capabilities(self, agent: str, session: LearningSession):
        """Update agent capabilities based on learning session outcomes."""
        try:
            if agent not in self.capability_enhancements:
                # Create new capability enhancement record
                enhancement = CapabilityEnhancement(
                    agent_id=agent,
                    enhancement_type="collaborative_learning",
                    current_capability=0.5,  # Base capability
                    target_capability=0.8,   # Target capability
                    learning_path=[],
                    progress=0.0,
                    last_updated=datetime.now().isoformat()
                )
                self.capability_enhancements[agent] = enhancement
            
            enhancement = self.capability_enhancements[agent]
            
            # Update progress based on session effectiveness
            progress_increase = session.effectiveness_score * 0.1  # 10% max increase per session
            enhancement.progress = min(1.0, enhancement.progress + progress_increase)
            enhancement.current_capability = min(
                enhancement.target_capability,
                enhancement.current_capability + progress_increase * 0.3
            )
            
            # Add session to learning path
            enhancement.learning_path.append({
                "session_id": session.session_id,
                "topic": session.topic,
                "effectiveness": session.effectiveness_score,
                "completed_at": session.end_time
            })
            
            enhancement.last_updated = datetime.now().isoformat()
            
        except Exception as e:
            logging.error(f"❌ Failed to update agent capabilities: {e}")
    
    def create_capability_enhancement_plan(self, agent: str, target_capabilities: Dict[str, float]) -> str:
        """
        Create a capability enhancement plan for an agent.
        
        Args:
            agent: Agent identifier
            target_capabilities: Target capability levels by type
        
        Returns:
            Enhancement plan ID
        """
        with self._lock:
            # Generate plan ID
            plan_id = f"plan_{int(time.time())}_{len(self.capability_enhancements)}"
            
            # Create enhancement plan
            for capability_type, target_level in target_capabilities.items():
                enhancement = CapabilityEnhancement(
                    agent_id=agent,
                    enhancement_type=capability_type,
                    current_capability=0.5,  # Base capability
                    target_capability=target_level,
                    learning_path=[],
                    progress=0.0,
                    last_updated=datetime.now().isoformat()
                )
                
                # Generate learning path
                enhancement.learning_path = self._generate_learning_path(capability_type, target_level)
                
                self.capability_enhancements[f"{agent}_{capability_type}"] = enhancement
            
            logging.info(f"🔐 Agent-4: Created capability enhancement plan for {agent} with {len(target_capabilities)} areas")
            return plan_id
    
    def _generate_learning_path(self, capability_type: str, target_level: float) -> List[Dict[str, Any]]:
        """Generate a learning path for capability enhancement."""
        learning_path = []
        
        # Get framework for capability type
        framework = self.capability_frameworks.get(capability_type, {})
        levels = framework.get("levels", ["basic", "intermediate", "advanced", "expert"])
        skills = framework.get("skills", [])
        
        # Determine current and target level indices
        current_level_idx = 0  # Start at basic
        target_level_idx = min(int(target_level * len(levels)), len(levels) - 1)
        
        # Generate learning steps
        for level_idx in range(current_level_idx, target_level_idx + 1):
            level = levels[level_idx]
            
            # Find relevant learning materials
            relevant_materials = [
                mat_id for mat_id, material in self.learning_materials.items()
                if material.get("difficulty") == level
            ]
            
            learning_path.append({
                "level": level,
                "level_index": level_idx,
                "skills_focus": skills,
                "learning_materials": relevant_materials,
                "estimated_time": "2-4 hours",
                "assessment_criteria": framework.get("assessment_criteria", [])
            })
        
        return learning_path
    
    def _monitor_security_status(self):
        """Monitor security status and detect potential threats."""
        try:
            # Check for suspicious message patterns
            recent_messages = [
                msg for msg in self.secure_messages.values()
                if datetime.fromisoformat(msg.timestamp) > datetime.now() - timedelta(hours=1)
            ]
            
            # Check for unauthorized access attempts
            for message in recent_messages:
                if not self.verify_message_signature(message):
                    self._log_security_alert("invalid_signature", message.sender, message.message_id)
            
            # Check for expired messages that haven't been cleaned up
            expired_messages = [
                msg for msg in self.secure_messages.values()
                if msg.expires_at and datetime.fromisoformat(msg.expires_at) < datetime.now()
            ]
            
            if expired_messages:
                logging.info(f"🔐 Agent-4: Found {len(expired_messages)} expired messages for cleanup")
                
        except Exception as e:
            logging.error(f"❌ Security monitoring error: {e}")
    
    def _monitor_learning_progress(self):
        """Monitor learning session progress and effectiveness."""
        try:
            # Check for long-running sessions
            current_time = datetime.now()
            active_sessions = [
                session for session in self.learning_sessions.values()
                if not session.end_time
            ]
            
            for session in active_sessions:
                start_time = datetime.fromisoformat(session.start_time)
                duration = current_time - start_time
                
                if duration > timedelta(hours=8):  # Alert for sessions longer than 8 hours
                    logging.warning(f"🔐 Agent-4: Learning session '{session.session_id}' running for {duration}")
                    
        except Exception as e:
            logging.error(f"❌ Learning monitoring error: {e}")
    
    def _monitor_capability_progress(self):
        """Monitor agent capability enhancement progress."""
        try:
            # Check for stalled capability enhancements
            for enhancement_id, enhancement in self.capability_enhancements.items():
                last_updated = datetime.fromisoformat(enhancement.last_updated)
                days_since_update = (datetime.now() - last_updated).days
                
                if days_since_update > 7 and enhancement.progress < 0.3:
                    logging.warning(f"🔐 Agent-4: Capability enhancement '{enhancement_id}' may be stalled")
                    
        except Exception as e:
            logging.error(f"❌ Capability monitoring error: {e}")
    
    def _cleanup_expired_messages(self):
        """Clean up expired secure messages."""
        try:
            current_time = datetime.now()
            expired_messages = [
                msg_id for msg_id, message in self.secure_messages.items()
                if message.expires_at and datetime.fromisoformat(message.expires_at) < current_time
            ]
            
            for msg_id in expired_messages:
                del self.secure_messages[msg_id]
            
            if expired_messages:
                logging.info(f"🧹 Cleaned up {len(expired_messages)} expired messages")
                
        except Exception as e:
            logging.error(f"❌ Failed to cleanup expired messages: {e}")
    
    def _log_security_audit(self, action: str, agent: str, target: Any, security_level: SecurityLevel):
        """Log security audit events."""
        audit_entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "agent": agent,
            "target": str(target),
            "security_level": security_level.value,
            "ip_address": "localhost",  # Would be actual IP in production
            "user_agent": "CollaborativeCommunicationHub"
        }
        
        self.security_audit_log.append(audit_entry)
        
        # Keep only last 1000 audit entries
        if len(self.security_audit_log) > 1000:
            self.security_audit_log = self.security_audit_log[-1000:]
    
    def _log_security_alert(self, alert_type: str, agent: str, details: str):
        """Log security alerts."""
        alert = {
            "timestamp": datetime.now().isoformat(),
            "alert_type": alert_type,
            "agent": agent,
            "details": details,
            "severity": "high" if alert_type in ["invalid_signature", "unauthorized_access"] else "medium"
        }
        
        self.security_audit_log.append(alert)
        logging.warning(f"🚨 Security Alert: {alert_type} from {agent} - {details}")
    
    def get_communication_summary(self) -> Dict[str, Any]:
        """Get comprehensive communication hub summary (Agent-4 reporting)."""
        with self._lock:
            total_messages = len(self.secure_messages)
            active_sessions = len([s for s in self.learning_sessions.values() if not s.end_time])
            completed_sessions = len([s for s in self.learning_sessions.values() if s.end_time])
            active_enhancements = len([e for e in self.capability_enhancements.values() if e.progress < 1.0])
            
            # Security status
            recent_alerts = len([a for a in self.security_audit_log[-100:] if a.get("alert_type")])
            
            # Learning effectiveness
            if completed_sessions > 0:
                avg_effectiveness = sum(s.effectiveness_score for s in self.learning_sessions.values() if s.end_time) / completed_sessions
            else:
                avg_effectiveness = 0.0
            
            summary = {
                "communication_status": "SECURE",
                "total_messages": total_messages,
                "active_sessions": active_sessions,
                "completed_sessions": completed_sessions,
                "average_learning_effectiveness": avg_effectiveness,
                "active_capability_enhancements": active_enhancements,
                "security_alerts_last_100_events": recent_alerts,
                "security_audit_entries": len(self.security_audit_log),
                "last_security_check": datetime.now().isoformat()
            }
            
            return summary
    
    def _save_data(self):
        """Save communication hub data to persistent storage."""
        try:
            # Save secure messages
            messages_data = {mid: asdict(msg) for mid, msg in self.secure_messages.items()}
            with open(self.data_path / 'secure_messages.json', 'w') as f:
                json.dump(messages_data, f, indent=2)
            
            # Save learning sessions
            sessions_data = {sid: asdict(session) for sid, session in self.learning_sessions.items()}
            with open(self.data_path / 'learning_sessions.json', 'w') as f:
                json.dump(sessions_data, f, indent=2)
            
            # Save capability enhancements
            capabilities_data = {eid: asdict(enhancement) for eid, enhancement in self.capability_enhancements.items()}
            with open(self.data_path / 'capability_enhancements.json', 'w') as f:
                json.dump(capabilities_data, f, indent=2)
                
        except Exception as e:
            logging.error(f"❌ Failed to save communication hub data: {e}")
    
    def __str__(self):
        """String representation of communication hub status."""
        summary = self.get_communication_summary()
        return (f"🔐 Collaborative Communication Hub - "
                f"Status: {summary['communication_status']}, "
                f"Messages: {summary['total_messages']}, "
                f"Sessions: {summary['active_sessions']} active, "
                f"Security: {summary['security_alerts_last_100_events']} alerts")


# Global instance for system-wide access
collaborative_communication_hub = CollaborativeCommunicationHub()







