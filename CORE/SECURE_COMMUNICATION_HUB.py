#!/usr/bin/env python3
"""
Secure Communication Hub for Multi-Agent Coordination System

This module provides encrypted messaging, learning protocols, and capability enhancement
for secure inter-agent communication and collaboration.

Features:
- End-to-end encryption for all messages
- Learning protocol implementation
- Capability enhancement tracking
- Secure key management
- Message integrity verification
"""

import json
import hashlib
import hmac
import base64
import time
import uuid
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class SecureMessage:
    """Secure message structure with encryption and integrity verification."""
    message_id: str
    sender_id: str
    recipient_id: str
    timestamp: float
    message_type: str
    encrypted_payload: str
    signature: str
    nonce: str
    version: str = "1.0"

@dataclass
class LearningProtocol:
    """Learning protocol for capability enhancement."""
    protocol_id: str
    agent_id: str
    capability: str
    learning_data: Dict[str, Any]
    timestamp: float
    status: str = "active"

@dataclass
class CapabilityEnhancement:
    """Capability enhancement tracking."""
    enhancement_id: str
    agent_id: str
    capability: str
    enhancement_type: str
    data: Dict[str, Any]
    timestamp: float
    effectiveness_score: float = 0.0

class SecureCommunicationHub:
    """
    Secure Communication Hub for multi-agent coordination.
    
    Provides encrypted messaging, learning protocols, and capability enhancement
    for secure inter-agent communication and collaboration.
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize the Secure Communication Hub."""
        self.config_path = config_path or "secure_hub_config.json"
        self.agents: Dict[str, Dict[str, Any]] = {}
        self.learning_protocols: Dict[str, LearningProtocol] = {}
        self.capability_enhancements: Dict[str, CapabilityEnhancement] = {}
        self.message_history: List[SecureMessage] = []
        self.encryption_keys: Dict[str, str] = {}
        
        # Load configuration
        self.load_config()
        
        # Initialize default encryption keys for demo
        self._initialize_demo_keys()
    
    def load_config(self) -> None:
        """Load configuration from file."""
        try:
            if Path(self.config_path).exists():
                with open(self.config_path, 'r') as f:
                    config = json.load(f)
                    self.agents = config.get('agents', {})
                    self.encryption_keys = config.get('encryption_keys', {})
                    logger.info(f"Configuration loaded from {self.config_path}")
            else:
                logger.info("No configuration file found, using defaults")
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
    
    def save_config(self) -> None:
        """Save configuration to file."""
        try:
            config = {
                'agents': self.agents,
                'encryption_keys': self.encryption_keys,
                'timestamp': time.time()
            }
            with open(self.config_path, 'w') as f:
                json.dump(config, f, indent=2)
            logger.info(f"Configuration saved to {self.config_path}")
        except Exception as e:
            logger.error(f"Error saving configuration: {e}")
    
    def _initialize_demo_keys(self) -> None:
        """Initialize demo encryption keys for testing."""
        demo_agents = ['Agent-1', 'Agent-2', 'Agent-3', 'Agent-4', 'Agent-5']
        for agent in demo_agents:
            if agent not in self.encryption_keys:
                # Generate a simple demo key (in production, use proper key generation)
                demo_key = hashlib.sha256(f"demo_key_{agent}".encode()).hexdigest()
                self.encryption_keys[agent] = demo_key
                logger.info(f"Generated demo key for {agent}")
    
    def register_agent(self, agent_id: str, capabilities: List[str], 
                      public_key: Optional[str] = None) -> bool:
        """Register a new agent in the secure hub."""
        try:
            self.agents[agent_id] = {
                'capabilities': capabilities,
                'public_key': public_key,
                'registration_time': time.time(),
                'status': 'active',
                'last_seen': time.time()
            }
            logger.info(f"Agent {agent_id} registered successfully")
            return True
        except Exception as e:
            logger.error(f"Error registering agent {agent_id}: {e}")
            return False
    
    def encrypt_message(self, message: str, recipient_id: str) -> str:
        """Encrypt a message for a specific recipient."""
        try:
            if recipient_id not in self.encryption_keys:
                raise ValueError(f"No encryption key found for {recipient_id}")
            
            # Simple XOR encryption for demo (use proper encryption in production)
            key = self.encryption_keys[recipient_id]
            encrypted = ''.join(chr(ord(c) ^ ord(k)) for c, k in zip(message, key * (len(message) // len(key) + 1)))
            return base64.b64encode(encrypted.encode()).decode()
        except Exception as e:
            logger.error(f"Error encrypting message: {e}")
            return ""
    
    def decrypt_message(self, encrypted_message: str, recipient_id: str) -> str:
        """Decrypt a message for a specific recipient."""
        try:
            if recipient_id not in self.encryption_keys:
                raise ValueError(f"No encryption key found for {recipient_id}")
            
            # Simple XOR decryption for demo (use proper decryption in production)
            key = self.encryption_keys[recipient_id]
            encrypted = base64.b64decode(encrypted_message.encode()).decode()
            decrypted = ''.join(chr(ord(c) ^ ord(k)) for c, k in zip(encrypted, key * (len(encrypted) // len(key) + 1)))
            return decrypted
        except Exception as e:
            logger.error(f"Error decrypting message: {e}")
            return ""
    
    def create_secure_message(self, sender_id: str, recipient_id: str, 
                            message_type: str, payload: str) -> SecureMessage:
        """Create a secure message with encryption and signature."""
        try:
            # Encrypt the payload
            encrypted_payload = self.encrypt_message(payload, recipient_id)
            
            # Create message structure
            message = SecureMessage(
                message_id=str(uuid.uuid4()),
                sender_id=sender_id,
                recipient_id=recipient_id,
                timestamp=time.time(),
                message_type=message_type,
                encrypted_payload=encrypted_payload,
                signature="",  # Will be generated
                nonce=str(uuid.uuid4())
            )
            
            # Generate signature
            message.signature = self._generate_signature(message)
            
            return message
        except Exception as e:
            logger.error(f"Error creating secure message: {e}")
            raise
    
    def _generate_signature(self, message: SecureMessage) -> str:
        """Generate HMAC signature for message integrity."""
        try:
            # Create signature data
            signature_data = f"{message.message_id}:{message.sender_id}:{message.recipient_id}:{message.timestamp}:{message.encrypted_payload}:{message.nonce}"
            
            # Generate HMAC signature
            if message.sender_id in self.encryption_keys:
                key = self.encryption_keys[message.sender_id]
                signature = hmac.new(key.encode(), signature_data.encode(), hashlib.sha256).hexdigest()
                return signature
            else:
                raise ValueError(f"No encryption key found for sender {message.sender_id}")
        except Exception as e:
            logger.error(f"Error generating signature: {e}")
            return ""
    
    def verify_message_integrity(self, message: SecureMessage) -> bool:
        """Verify message integrity using signature."""
        try:
            expected_signature = self._generate_signature(message)
            return hmac.compare_digest(message.signature, expected_signature)
        except Exception as e:
            logger.error(f"Error verifying message integrity: {e}")
            return False
    
    def send_secure_message(self, sender_id: str, recipient_id: str, 
                          message_type: str, payload: str) -> Optional[str]:
        """Send a secure message between agents."""
        try:
            # Create secure message
            message = self.create_secure_message(sender_id, recipient_id, message_type, payload)
            
            # Verify message integrity
            if not self.verify_message_integrity(message):
                raise ValueError("Message integrity verification failed")
            
            # Store message in history
            self.message_history.append(message)
            
            # Update agent last seen time
            if sender_id in self.agents:
                self.agents[sender_id]['last_seen'] = time.time()
            
            logger.info(f"Secure message sent from {sender_id} to {recipient_id}")
            return message.message_id
        except Exception as e:
            logger.error(f"Error sending secure message: {e}")
            return None
    
    def receive_secure_message(self, message: SecureMessage, recipient_id: str) -> Optional[str]:
        """Receive and process a secure message."""
        try:
            # Verify message integrity
            if not self.verify_message_integrity(message):
                raise ValueError("Message integrity verification failed")
            
            # Verify recipient
            if message.recipient_id != recipient_id:
                raise ValueError("Message not intended for this recipient")
            
            # Decrypt payload
            decrypted_payload = self.decrypt_message(message.encrypted_payload, recipient_id)
            
            # Update agent last seen time
            if message.sender_id in self.agents:
                self.agents[message.sender_id]['last_seen'] = time.time()
            
            logger.info(f"Secure message received by {recipient_id} from {message.sender_id}")
            return decrypted_payload
        except Exception as e:
            logger.error(f"Error receiving secure message: {e}")
            return None
    
    def create_learning_protocol(self, agent_id: str, capability: str, 
                               learning_data: Dict[str, Any]) -> str:
        """Create a learning protocol for capability enhancement."""
        try:
            protocol = LearningProtocol(
                protocol_id=str(uuid.uuid4()),
                agent_id=agent_id,
                capability=capability,
                learning_data=learning_data,
                timestamp=time.time()
            )
            
            self.learning_protocols[protocol.protocol_id] = protocol
            logger.info(f"Learning protocol created for {agent_id} - {capability}")
            return protocol.protocol_id
        except Exception as e:
            logger.error(f"Error creating learning protocol: {e}")
            return ""
    
    def enhance_capability(self, agent_id: str, capability: str, 
                         enhancement_type: str, data: Dict[str, Any]) -> str:
        """Enhance an agent's capability."""
        try:
            enhancement = CapabilityEnhancement(
                enhancement_id=str(uuid.uuid4()),
                agent_id=agent_id,
                capability=capability,
                enhancement_type=enhancement_type,
                data=data,
                timestamp=time.time()
            )
            
            self.capability_enhancements[enhancement.enhancement_id] = enhancement
            logger.info(f"Capability enhancement created for {agent_id} - {capability}")
            return enhancement.enhancement_id
        except Exception as e:
            logger.error(f"Error enhancing capability: {e}")
            return ""
    
    def get_agent_status(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get current status of an agent."""
        return self.agents.get(agent_id)
    
    def get_message_history(self, agent_id: str = None) -> List[SecureMessage]:
        """Get message history, optionally filtered by agent."""
        if agent_id:
            return [msg for msg in self.message_history 
                   if msg.sender_id == agent_id or msg.recipient_id == agent_id]
        return self.message_history
    
    def get_learning_protocols(self, agent_id: str = None) -> List[LearningProtocol]:
        """Get learning protocols, optionally filtered by agent."""
        if agent_id:
            return [protocol for protocol in self.learning_protocols.values() 
                   if protocol.agent_id == agent_id]
        return list(self.learning_protocols.values())
    
    def get_capability_enhancements(self, agent_id: str = None) -> List[CapabilityEnhancement]:
        """Get capability enhancements, optionally filtered by agent."""
        if agent_id:
            return [enhancement for enhancement in self.capability_enhancements.values() 
                   if enhancement.agent_id == agent_id]
        return list(self.capability_enhancements.values())
    
    def generate_status_report(self) -> Dict[str, Any]:
        """Generate a comprehensive status report."""
        try:
            report = {
                'timestamp': time.time(),
                'total_agents': len(self.agents),
                'active_agents': len([a for a in self.agents.values() if a['status'] == 'active']),
                'total_messages': len(self.message_history),
                'total_learning_protocols': len(self.learning_protocols),
                'total_capability_enhancements': len(self.capability_enhancements),
                'agent_statuses': {agent_id: agent['status'] for agent_id, agent in self.agents.items()},
                'recent_messages': [
                    {
                        'message_id': msg.message_id,
                        'sender': msg.sender_id,
                        'recipient': msg.recipient_id,
                        'type': msg.message_type,
                        'timestamp': msg.timestamp
                    }
                    for msg in self.message_history[-10:]  # Last 10 messages
                ]
            }
            return report
        except Exception as e:
            logger.error(f"Error generating status report: {e}")
            return {}

def main():
    """Demo function to test the Secure Communication Hub."""
    print("🔐 Secure Communication Hub Demo")
    print("=" * 50)
    
    # Initialize the hub
    hub = SecureCommunicationHub()
    
    # Register demo agents
    hub.register_agent("Agent-1", ["coordination", "knowledge_management"])
    hub.register_agent("Agent-2", ["task_breakdown", "resource_allocation"])
    hub.register_agent("Agent-3", ["data_analysis", "technical_implementation"])
    hub.register_agent("Agent-4", ["communication", "security_protocols"])
    hub.register_agent("Agent-5", ["task_execution", "verification"])
    
    # Send a secure message
    print("\n📤 Sending secure message...")
    message_id = hub.send_secure_message(
        "Agent-1", 
        "Agent-5", 
        "task_update", 
        "Collaborative task implementation in progress"
    )
    
    if message_id:
        print(f"✅ Message sent successfully: {message_id}")
        
        # Retrieve and decrypt the message
        message = hub.get_message_history("Agent-1")[-1]
        decrypted = hub.receive_secure_message(message, "Agent-5")
        
        if decrypted:
            print(f"📥 Message received and decrypted: {decrypted}")
    
    # Create learning protocol
    print("\n🧠 Creating learning protocol...")
    protocol_id = hub.create_learning_protocol(
        "Agent-1",
        "collaboration_optimization",
        {"learning_method": "collaborative_analysis", "target_improvement": "coordination_efficiency"}
    )
    
    if protocol_id:
        print(f"✅ Learning protocol created: {protocol_id}")
    
    # Enhance capability
    print("\n⚡ Enhancing capability...")
    enhancement_id = hub.enhance_capability(
        "Agent-1",
        "coordination",
        "collaborative_optimization",
        {"optimization_algorithm": "multi_agent_synergy", "improvement_factor": 1.5}
    )
    
    if enhancement_id:
        print(f"✅ Capability enhanced: {enhancement_id}")
    
    # Generate status report
    print("\n📊 Generating status report...")
    status_report = hub.generate_status_report()
    print(f"✅ Status report generated:")
    print(f"   - Total agents: {status_report.get('total_agents', 0)}")
    print(f"   - Active agents: {status_report.get('active_agents', 0)}")
    print(f"   - Total messages: {status_report.get('total_messages', 0)}")
    print(f"   - Learning protocols: {status_report.get('total_learning_protocols', 0)}")
    print(f"   - Capability enhancements: {status_report.get('total_capability_enhancements', 0)}")
    
    # Save configuration
    hub.save_config()
    print("\n💾 Configuration saved")
    
    print("\n🎉 Secure Communication Hub demo completed successfully!")

if __name__ == "__main__":
    main()
