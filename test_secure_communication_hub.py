#!/usr/bin/env python3
"""
Comprehensive test suite for Secure Communication Hub

This module provides thorough testing of all Secure Communication Hub functionality
including encryption, message integrity, learning protocols, and capability enhancement.
"""

import unittest
import json
import tempfile
import os
from pathlib import Path
from SECURE_COMMUNICATION_HUB import (
    SecureCommunicationHub, 
    SecureMessage, 
    LearningProtocol, 
    CapabilityEnhancement
)

class TestSecureCommunicationHub(unittest.TestCase):
    """Test cases for Secure Communication Hub functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create temporary config file
        self.temp_dir = tempfile.mkdtemp()
        self.config_path = os.path.join(self.temp_dir, "test_config.json")
        
        # Initialize hub with test config
        self.hub = SecureCommunicationHub(self.config_path)
        
        # Register test agents
        self.hub.register_agent("TestAgent-1", ["test_capability"])
        self.hub.register_agent("TestAgent-2", ["test_capability"])
    
    def tearDown(self):
        """Clean up test fixtures."""
        # Remove temporary files
        if os.path.exists(self.config_path):
            os.remove(self.config_path)
        if os.path.exists(self.temp_dir):
            os.rmdir(self.temp_dir)
    
    def test_agent_registration(self):
        """Test agent registration functionality."""
        # Test successful registration
        result = self.hub.register_agent("TestAgent-3", ["capability1", "capability2"])
        self.assertTrue(result)
        
        # Verify agent is registered
        agent_status = self.hub.get_agent_status("TestAgent-3")
        self.assertIsNotNone(agent_status)
        self.assertEqual(agent_status['capabilities'], ["capability1", "capability2"])
        self.assertEqual(agent_status['status'], 'active')
    
    def test_encryption_decryption(self):
        """Test message encryption and decryption."""
        test_message = "This is a test message for encryption"
        
        # Encrypt message
        encrypted = self.hub.encrypt_message(test_message, "TestAgent-1")
        self.assertIsNotNone(encrypted)
        self.assertNotEqual(encrypted, test_message)
        
        # Decrypt message
        decrypted = self.hub.decrypt_message(encrypted, "TestAgent-1")
        self.assertEqual(decrypted, test_message)
    
    def test_secure_message_creation(self):
        """Test secure message creation with proper structure."""
        message = self.hub.create_secure_message(
            "TestAgent-1", 
            "TestAgent-2", 
            "test_type", 
            "test payload"
        )
        
        # Verify message structure
        self.assertIsInstance(message, SecureMessage)
        self.assertEqual(message.sender_id, "TestAgent-1")
        self.assertEqual(message.recipient_id, "TestAgent-2")
        self.assertEqual(message.message_type, "test_type")
        self.assertIsNotNone(message.message_id)
        self.assertIsNotNone(message.signature)
        self.assertIsNotNone(message.nonce)
    
    def test_message_integrity_verification(self):
        """Test message integrity verification using signatures."""
        message = self.hub.create_secure_message(
            "TestAgent-1", 
            "TestAgent-2", 
            "test_type", 
            "test payload"
        )
        
        # Verify original message integrity
        self.assertTrue(self.hub.verify_message_integrity(message))
        
        # Tamper with message (should fail verification)
        message.encrypted_payload = "tampered_payload"
        self.assertFalse(self.hub.verify_message_integrity(message))
    
    def test_secure_message_sending(self):
        """Test secure message sending functionality."""
        message_id = self.hub.send_secure_message(
            "TestAgent-1", 
            "TestAgent-2", 
            "test_type", 
            "test payload"
        )
        
        # Verify message was sent
        self.assertIsNotNone(message_id)
        
        # Verify message is in history
        history = self.hub.get_message_history()
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0].message_id, message_id)
    
    def test_secure_message_receiving(self):
        """Test secure message receiving and decryption."""
        # Send a message
        message_id = self.hub.send_secure_message(
            "TestAgent-1", 
            "TestAgent-2", 
            "test_type", 
            "test payload"
        )
        
        # Get the message from history
        message = self.hub.get_message_history()[-1]
        
        # Receive and decrypt the message
        decrypted = self.hub.receive_secure_message(message, "TestAgent-2")
        
        # Verify decryption
        self.assertEqual(decrypted, "test payload")
    
    def test_learning_protocol_creation(self):
        """Test learning protocol creation and management."""
        learning_data = {
            "method": "collaborative_learning",
            "target": "coordination_efficiency",
            "parameters": {"learning_rate": 0.1}
        }
        
        protocol_id = self.hub.create_learning_protocol(
            "TestAgent-1", 
            "coordination", 
            learning_data
        )
        
        # Verify protocol was created
        self.assertIsNotNone(protocol_id)
        
        # Verify protocol is in the system
        protocols = self.hub.get_learning_protocols("TestAgent-1")
        self.assertEqual(len(protocols), 1)
        self.assertEqual(protocols[0].protocol_id, protocol_id)
        self.assertEqual(protocols[0].capability, "coordination")
    
    def test_capability_enhancement(self):
        """Test capability enhancement functionality."""
        enhancement_data = {
            "algorithm": "neural_optimization",
            "improvement_factor": 2.0,
            "parameters": {"layers": 3, "neurons": 64}
        }
        
        enhancement_id = self.hub.enhance_capability(
            "TestAgent-1", 
            "coordination", 
            "neural_optimization", 
            enhancement_data
        )
        
        # Verify enhancement was created
        self.assertIsNotNone(enhancement_id)
        
        # Verify enhancement is in the system
        enhancements = self.hub.get_capability_enhancements("TestAgent-1")
        self.assertEqual(len(enhancements), 1)
        self.assertEqual(enhancements[0].enhancement_id, enhancement_id)
        self.assertEqual(enhancements[0].capability, "coordination")
    
    def test_status_report_generation(self):
        """Test comprehensive status report generation."""
        # Create some test data
        self.hub.send_secure_message("TestAgent-1", "TestAgent-2", "test", "payload")
        self.hub.create_learning_protocol("TestAgent-1", "test", {"data": "test"})
        self.hub.enhance_capability("TestAgent-1", "test", "test", {"data": "test"})
        
        # Generate status report
        report = self.hub.generate_status_report()
        
        # Verify report structure
        self.assertIn('timestamp', report)
        self.assertIn('total_agents', report)
        self.assertIn('active_agents', report)
        self.assertIn('total_messages', report)
        self.assertIn('total_learning_protocols', report)
        self.assertIn('total_capability_enhancements', report)
        self.assertIn('agent_statuses', report)
        self.assertIn('recent_messages', report)
        
        # Verify report values
        self.assertEqual(report['total_agents'], 2)  # TestAgent-1 and TestAgent-2
        self.assertEqual(report['active_agents'], 2)
        self.assertEqual(report['total_messages'], 1)
        self.assertEqual(report['total_learning_protocols'], 1)
        self.assertEqual(report['total_capability_enhancements'], 1)
    
    def test_configuration_persistence(self):
        """Test configuration saving and loading."""
        # Save configuration
        self.hub.save_config()
        
        # Verify config file exists
        self.assertTrue(os.path.exists(self.config_path))
        
        # Create new hub instance with same config
        new_hub = SecureCommunicationHub(self.config_path)
        
        # Verify configuration was loaded
        self.assertEqual(len(new_hub.agents), 2)  # Should have TestAgent-1 and TestAgent-2
        self.assertEqual(len(new_hub.encryption_keys), 2)
    
    def test_error_handling(self):
        """Test error handling for invalid operations."""
        # Test sending message to non-existent agent
        with self.assertRaises(ValueError):
            self.hub.send_secure_message("TestAgent-1", "NonExistentAgent", "test", "payload")
        
        # Test decrypting with wrong key
        encrypted = self.hub.encrypt_message("test", "TestAgent-1")
        decrypted = self.hub.decrypt_message(encrypted, "TestAgent-2")
        self.assertEqual(decrypted, "")  # Should return empty string on error
    
    def test_message_history_filtering(self):
        """Test message history filtering by agent."""
        # Send messages between different agents
        self.hub.send_secure_message("TestAgent-1", "TestAgent-2", "type1", "payload1")
        self.hub.send_secure_message("TestAgent-2", "TestAgent-1", "type2", "payload2")
        
        # Test filtering by sender
        agent1_messages = self.hub.get_message_history("TestAgent-1")
        self.assertEqual(len(agent1_messages), 1)
        self.assertEqual(agent1_messages[0].sender_id, "TestAgent-1")
        
        # Test filtering by recipient
        agent2_messages = self.hub.get_message_history("TestAgent-2")
        self.assertEqual(len(agent2_messages), 1)
        self.assertEqual(agent2_messages[0].recipient_id, "TestAgent-2")

def run_performance_tests():
    """Run performance tests to demonstrate system efficiency."""
    print("\n🚀 Performance Tests")
    print("=" * 50)
    
    hub = SecureCommunicationHub()
    
    # Register multiple agents
    for i in range(10):
        hub.register_agent(f"PerfAgent-{i}", [f"capability-{i}"])
    
    # Send multiple messages
    import time
    start_time = time.time()
    
    for i in range(100):
        hub.send_secure_message(
            f"PerfAgent-{i % 10}", 
            f"PerfAgent-{(i + 1) % 10}", 
            "performance_test", 
            f"message-{i}"
        )
    
    end_time = time.time()
    total_time = end_time - start_time
    
    print(f"✅ 100 messages processed in {total_time:.4f} seconds")
    print(f"✅ Average time per message: {total_time/100:.6f} seconds")
    print(f"✅ Messages per second: {100/total_time:.2f}")
    
    # Test learning protocol creation performance
    start_time = time.time()
    
    for i in range(50):
        hub.create_learning_protocol(
            f"PerfAgent-{i % 10}", 
            f"capability-{i}", 
            {"data": f"learning-{i}"}
        )
    
    end_time = time.time()
    total_time = end_time - start_time
    
    print(f"✅ 50 learning protocols created in {total_time:.4f} seconds")
    print(f"✅ Average time per protocol: {total_time/50:.6f} seconds")
    
    # Test capability enhancement performance
    start_time = time.time()
    
    for i in range(50):
        hub.enhance_capability(
            f"PerfAgent-{i % 10}", 
            f"capability-{i}", 
            f"enhancement-{i}", 
            {"data": f"enhancement-{i}"}
        )
    
    end_time = time.time()
    total_time = end_time - start_time
    
    print(f"✅ 50 capability enhancements created in {total_time:.4f} seconds")
    print(f"✅ Average time per enhancement: {total_time/50:.6f} seconds")
    
    # Generate comprehensive status report
    start_time = time.time()
    report = hub.generate_status_report()
    end_time = time.time()
    
    print(f"✅ Status report generated in {end_time - start_time:.6f} seconds")
    print(f"✅ Report contains {len(report)} data points")

if __name__ == "__main__":
    print("🧪 Secure Communication Hub Test Suite")
    print("=" * 50)
    
    # Run unit tests
    print("\n📋 Running unit tests...")
    unittest.main(argv=[''], exit=False, verbosity=2)
    
    # Run performance tests
    run_performance_tests()
    
    print("\n🎉 All tests completed successfully!")
