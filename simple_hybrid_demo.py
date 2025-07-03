#!/usr/bin/env python3
"""
Simple Hybrid Communication Demo
================================
A simplified version that demonstrates the hybrid communication concept
without the complex pipe reading that can cause freezing on Windows.
"""

import os
import json
import time
import threading
import queue
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

class SimpleHybridMessage:
    """Simplified message structure for hybrid communication."""
    
    def __init__(self, from_agent: str, to_agent: str, message: str, tag: str = "normal"):
        self.id = f"{datetime.now().strftime('%Y-%m-%dT%H-%M-%S-%f')}_{from_agent}_to_{to_agent}"
        self.timestamp = datetime.now().isoformat()
        self.from_agent = from_agent
        self.to_agent = to_agent
        self.message = message
        self.tag = tag
        self.status = "pending"
        self.persisted = False
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "timestamp": self.timestamp,
            "from": self.from_agent,
            "to": self.to_agent,
            "message": self.message,
            "tag": self.tag,
            "status": self.status,
            "persisted": self.persisted
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SimpleHybridMessage':
        """Create SimpleHybridMessage from dictionary."""
        msg = cls(data["from"], data["to"], data["message"], data.get("tag", "normal"))
        msg.id = data["id"]
        msg.timestamp = data["timestamp"]
        msg.status = data.get("status", "pending")
        msg.persisted = data.get("persisted", False)
        return msg

class SimpleHybridManager:
    """Simplified hybrid manager using in-memory queues and file persistence."""
    
    def __init__(self, layout_mode: str = "2-agent"):
        self.layout_mode = layout_mode
        
        # In-memory message queues (simulating pipes)
        self.message_queues: Dict[str, queue.Queue] = {}
        self.message_counts: Dict[str, int] = {}
        
        # File-based persistence
        self.base_dir = Path("agent_workspaces")
        self.persistent_dir = self.base_dir / "queue" / "persistent"
        self.persistent_dir.mkdir(parents=True, exist_ok=True)
        self.persistent_counts: Dict[str, int] = {}
        
        # Setup for layout
        self._setup_agents()
        
        print(f"🔗 SimpleHybridManager initialized for {layout_mode} mode")
    
    def _setup_agents(self):
        """Setup message queues for all agents in the layout."""
        if self.layout_mode == "2-agent":
            agents = ["agent-1", "agent-2"]
        elif self.layout_mode == "4-agent":
            agents = ["agent-1", "agent-2", "agent-3", "agent-4"]
        else:
            agents = ["agent-1", "agent-2"]
        
        for agent in agents:
            self.message_queues[agent] = queue.Queue()
            self.message_counts[agent] = 0
            self.persistent_counts[agent] = 0
        
        print(f"📡 Created message queues for {len(agents)} agents")
    
    def send_message(self, from_agent: str, to_agent: str, message: str, 
                    tag: str = "normal", use_persistence: bool = True) -> str:
        """Send a message via both in-memory queue and file persistence."""
        if to_agent not in self.message_queues:
            raise ValueError(f"Unknown agent: {to_agent}")
        
        hybrid_msg = SimpleHybridMessage(from_agent, to_agent, message, tag)
        
        # 1. Send via in-memory queue (real-time simulation)
        self.message_queues[to_agent].put(hybrid_msg)
        self.message_counts[from_agent] += 1
        
        # 2. Persist to file (reliability)
        if use_persistence:
            self._persist_message(hybrid_msg)
        
        print(f"📤 {from_agent} → {to_agent}: {message[:50]}... (Hybrid)")
        return hybrid_msg.id
    
    def _persist_message(self, message: SimpleHybridMessage):
        """Persist message to file for reliability."""
        persistent_file = self.persistent_dir / f"{message.id}.json"
        with open(persistent_file, 'w') as f:
            json.dump(message.to_dict(), f, indent=2)
        
        message.persisted = True
        self.persistent_counts[message.from_agent] += 1
    
    def get_message(self, agent_id: str, timeout: float = 1.0) -> Optional[SimpleHybridMessage]:
        """Get a message from an agent's queue."""
        if agent_id not in self.message_queues:
            raise ValueError(f"Unknown agent: {agent_id}")
        
        try:
            return self.message_queues[agent_id].get(timeout=timeout)
        except queue.Empty:
            return None
    
    def get_persistent_messages(self, agent_id: str) -> List[SimpleHybridMessage]:
        """Get all persistent messages for an agent."""
        messages = []
        persistent_files = list(self.persistent_dir.glob(f"*_to_{agent_id}.json"))
        
        for file in persistent_files:
            try:
                with open(file, 'r') as f:
                    msg_dict = json.load(f)
                    messages.append(SimpleHybridMessage.from_dict(msg_dict))
            except Exception as e:
                print(f"Error reading persistent message {file}: {e}")
        
        return sorted(messages, key=lambda x: x.timestamp)
    
    def broadcast_message(self, from_agent: str, message: str, tag: str = "normal") -> List[str]:
        """Broadcast a message to all agents except sender."""
        msg_ids = []
        
        for agent_id in self.message_queues.keys():
            if agent_id != from_agent:
                msg_id = self.send_message(from_agent, agent_id, message, tag)
                msg_ids.append(msg_id)
        
        return msg_ids
    
    def get_status(self) -> Dict[str, Any]:
        """Get comprehensive status of hybrid system."""
        status = {
            "layout_mode": self.layout_mode,
            "message_counts": self.message_counts.copy(),
            "persistent_counts": self.persistent_counts.copy(),
            "queue_sizes": {},
            "persistent_files": {}
        }
        
        for agent_id in self.message_queues.keys():
            status["queue_sizes"][agent_id] = self.message_queues[agent_id].qsize()
            
            # Count persistent files for this agent
            persistent_files = list(self.persistent_dir.glob(f"*_to_{agent_id}.json"))
            status["persistent_files"][agent_id] = len(persistent_files)
        
        return status

class SimpleHybridAgent:
    """Simplified agent client for hybrid communication."""
    
    def __init__(self, agent_id: str, hybrid_manager: SimpleHybridManager):
        self.agent_id = agent_id
        self.hybrid_manager = hybrid_manager
        self.message_handlers = {}
        
        # Register default handlers
        self.register_handler("coordinate", self._handle_coordination)
        self.register_handler("task", self._handle_task)
        self.register_handler("reply", self._handle_reply)
        self.register_handler("normal", self._handle_normal)
        
        print(f"🤖 {agent_id} simple hybrid client initialized")
    
    def register_handler(self, tag: str, handler_func):
        """Register a message handler for a specific tag."""
        self.message_handlers[tag] = handler_func
    
    def send_message(self, to_agent: str, message: str, tag: str = "normal", 
                    use_persistence: bool = True) -> str:
        """Send a message using hybrid system."""
        return self.hybrid_manager.send_message(
            self.agent_id, to_agent, message, tag, use_persistence
        )
    
    def broadcast(self, message: str, tag: str = "normal") -> List[str]:
        """Broadcast a message to all other agents."""
        return self.hybrid_manager.broadcast_message(self.agent_id, message, tag)
    
    def get_message(self, timeout: float = 1.0) -> Optional[SimpleHybridMessage]:
        """Get a message from queue."""
        return self.hybrid_manager.get_message(self.agent_id, timeout)
    
    def get_persistent_messages(self) -> List[SimpleHybridMessage]:
        """Get all persistent messages for this agent."""
        return self.hybrid_manager.get_persistent_messages(self.agent_id)
    
    def process_messages(self, timeout: float = 1.0):
        """Process incoming messages from queue."""
        msg = self.get_message(timeout)
        if msg:
            handler = self.message_handlers.get(msg.tag, self._handle_normal)
            return handler(msg)
        return None
    
    def process_persistent_messages(self):
        """Process all persistent messages (for recovery)."""
        messages = self.get_persistent_messages()
        processed_count = 0
        
        for msg in messages:
            if msg.status == "pending":
                handler = self.message_handlers.get(msg.tag, self._handle_normal)
                handler(msg)
                processed_count += 1
        
        if processed_count > 0:
            print(f"📋 {self.agent_id} processed {processed_count} persistent messages")
        
        return processed_count
    
    def _handle_coordination(self, message: SimpleHybridMessage):
        """Handle coordination messages."""
        print(f"🤝 {self.agent_id} handling coordination: {message.message[:50]}...")
        return self.send_message(message.from_agent, "Ready to coordinate!", "reply")
    
    def _handle_task(self, message: SimpleHybridMessage):
        """Handle task assignments."""
        print(f"📋 {self.agent_id} handling task: {message.message[:50]}...")
        return self.send_message(message.from_agent, f"Task received: {message.message[:30]}...", "reply")
    
    def _handle_reply(self, message: SimpleHybridMessage):
        """Handle reply messages."""
        print(f"💬 {self.agent_id} handling reply: {message.message[:50]}...")
        return None
    
    def _handle_normal(self, message: SimpleHybridMessage):
        """Handle normal messages."""
        print(f"📝 {self.agent_id} handling normal message: {message.message[:50]}...")
        return None

def demonstrate_simple_hybrid():
    """Demonstrate simple hybrid communication system."""
    print("🎯 Simple Hybrid Communication System Demo")
    print("=" * 60)
    
    try:
        # Initialize hybrid manager
        hybrid_manager = SimpleHybridManager("2-agent")
        
        # Create agent clients
        agent_1 = SimpleHybridAgent("agent-1", hybrid_manager)
        agent_2 = SimpleHybridAgent("agent-2", hybrid_manager)
        
        print("\n📤 Step 1: Agent-2 sends coordination message (with persistence)")
        agent_2.send_message("agent-1", "Hello Agent-1! Ready to coordinate via hybrid system?", "coordinate")
        
        # Let agents process messages
        time.sleep(0.5)
        agent_1.process_messages()
        
        print("\n📤 Step 2: Agent-2 assigns a task (with persistence)")
        agent_2.send_message("agent-1", "Please analyze the dataset using hybrid communication", "task")
        
        time.sleep(0.5)
        agent_1.process_messages()
        
        print("\n📤 Step 3: Agent-1 sends rapid message (queue-only, no persistence)")
        agent_1.send_message("agent-2", "Quick status update - working on it!", "normal", use_persistence=False)
        
        time.sleep(0.5)
        agent_2.process_messages()
        
        print("\n📤 Step 4: Agent-1 reports progress (with persistence)")
        agent_1.send_message("agent-2", "Hybrid communication working great! Analysis 75% complete.", "reply")
        
        time.sleep(0.5)
        agent_2.process_messages()
        
        print("\n📤 Step 5: Agent-2 broadcasts to all agents")
        agent_2.broadcast("Hybrid system combines speed of queues with reliability of files!", "normal")
        
        time.sleep(0.5)
        agent_1.process_messages()
        
        print("\n📤 Step 6: Agent-1 reports completion")
        agent_1.send_message("agent-2", "Analysis complete! Hybrid system is the best of both worlds.", "reply")
        
        time.sleep(0.5)
        agent_2.process_messages()
        
        # Show comprehensive status
        status = hybrid_manager.get_status()
        print(f"\n📊 Hybrid System Status:")
        print(f"  Layout Mode: {status['layout_mode']}")
        print(f"  Agent-1 Queue Messages: {status['message_counts']['agent-1']}")
        print(f"  Agent-2 Queue Messages: {status['message_counts']['agent-2']}")
        print(f"  Agent-1 Persistent Messages: {status['persistent_counts']['agent-1']}")
        print(f"  Agent-2 Persistent Messages: {status['persistent_counts']['agent-2']}")
        print(f"  Agent-1 Queue Size: {status['queue_sizes']['agent-1']}")
        print(f"  Agent-2 Queue Size: {status['queue_sizes']['agent-2']}")
        print(f"  Agent-1 Persistent Files: {status['persistent_files']['agent-1']}")
        print(f"  Agent-2 Persistent Files: {status['persistent_files']['agent-2']}")
        
        # Demonstrate persistence recovery
        print(f"\n🔄 Demonstrating persistence recovery...")
        agent_1.process_persistent_messages()
        agent_2.process_persistent_messages()
        
        print("\n✅ Simple hybrid communication demo completed!")
        
    except Exception as e:
        print(f"❌ Error during simple hybrid communication demo: {e}")
        print("🔄 Demo terminated due to error")

def compare_performance():
    """Compare performance of different communication methods."""
    print("\n⚡ Performance Comparison")
    print("=" * 60)
    
    # Test hybrid communication
    hybrid_manager = SimpleHybridManager("2-agent")
    agent_1 = SimpleHybridAgent("agent-1", hybrid_manager)
    agent_2 = SimpleHybridAgent("agent-2", hybrid_manager)
    
    # Hybrid performance test (with persistence)
    start_time = time.time()
    for i in range(20):
        agent_2.send_message("agent-1", f"Hybrid message {i}", "normal", use_persistence=True)
        agent_1.process_messages(timeout=0.01)
    
    hybrid_time = time.time() - start_time
    
    # Queue-only performance test
    start_time = time.time()
    for i in range(20):
        agent_2.send_message("agent-1", f"Queue message {i}", "normal", use_persistence=False)
        agent_1.process_messages(timeout=0.01)
    
    queue_time = time.time() - start_time
    
    # File-based performance test (simulated)
    start_time = time.time()
    for i in range(20):
        # Simulate file I/O overhead
        time.sleep(0.002)  # Simulate file write
        time.sleep(0.002)  # Simulate file read
    
    file_time = time.time() - start_time
    
    print(f"📊 Performance Results (20 messages each):")
    print(f"  Hybrid (with persistence): {hybrid_time:.3f} seconds")
    print(f"  Queue-only (no persistence): {queue_time:.3f} seconds")
    print(f"  File-based (simulated): {file_time:.3f} seconds")
    print(f"  Hybrid vs File speedup: {file_time/hybrid_time:.1f}x faster")
    print(f"  Queue vs File speedup: {file_time/queue_time:.1f}x faster")

if __name__ == "__main__":
    demonstrate_simple_hybrid()
    compare_performance() 