#!/usr/bin/env python3
"""
Hybrid Inter-Agent Communication System
=======================================
Combines Windows pipes for real-time communication with file-based queues for persistence.
Provides both speed and reliability for agent coordination.
"""

import os
import json
import time
import threading
import queue
import subprocess
import select
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
import sys

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from utils.coordinate_finder import CoordinateFinder
except ImportError as e:
    print(f"Import error: {e}")
    print("Please run from the project root directory")
    sys.exit(1)

class HybridMessage:
    """Message structure for hybrid communication."""
    
    def __init__(self, from_agent: str, to_agent: str, message: str, 
                 tag: str = "normal", priority: str = "normal"):
        self.id = f"{datetime.now().strftime('%Y-%m-%dT%H-%M-%S-%f')}_{from_agent}_to_{to_agent}"
        self.timestamp = datetime.now().isoformat()
        self.from_agent = from_agent
        self.to_agent = to_agent
        self.message = message
        self.tag = tag
        self.priority = priority
        self.status = "pending"
        self.created_at = datetime.now().isoformat()
        self.persisted = False
        self.pipe_delivered = False
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "timestamp": self.timestamp,
            "from": self.from_agent,
            "to": self.to_agent,
            "message": self.message,
            "tag": self.tag,
            "priority": self.priority,
            "status": self.status,
            "created_at": self.created_at,
            "persisted": self.persisted,
            "pipe_delivered": self.pipe_delivered
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'HybridMessage':
        """Create HybridMessage from dictionary."""
        msg = cls(data["from"], data["to"], data["message"], data.get("tag", "normal"))
        msg.id = data["id"]
        msg.timestamp = data["timestamp"]
        msg.priority = data.get("priority", "normal")
        msg.status = data.get("status", "pending")
        msg.created_at = data.get("created_at", msg.timestamp)
        msg.persisted = data.get("persisted", False)
        msg.pipe_delivered = data.get("pipe_delivered", False)
        return msg

class HybridCommunicationManager:
    """Hybrid manager combining pipes and file-based queues."""
    
    def __init__(self, layout_mode: str = "2-agent"):
        self.layout_mode = layout_mode
        self.coordinate_finder = CoordinateFinder()
        
        # Pipe management (for real-time communication)
        self.pipes: Dict[str, Tuple[int, int]] = {}
        self.pipe_locks: Dict[str, threading.Lock] = {}
        self.message_queues: Dict[str, queue.Queue] = {}
        self.reader_threads: Dict[str, threading.Thread] = {}
        
        # File-based queue management (for persistence)
        self.base_dir = Path("agent_workspaces")
        self.queue_dir = self.base_dir / "queue"
        self.pending_dir = self.queue_dir / "pending"
        self.processing_dir = self.queue_dir / "processing"
        self.completed_dir = self.queue_dir / "completed"
        self.failed_dir = self.queue_dir / "failed"
        self.persistent_dir = self.queue_dir / "persistent"
        
        # Hybrid state
        self.running = False
        self.message_counts: Dict[str, int] = {}
        self.persistent_counts: Dict[str, int] = {}
        
        # Setup directories and pipes
        self._setup_directories()
        self._setup_agent_pipes()
        
        print(f"🔗 HybridCommunicationManager initialized for {layout_mode} mode")
    
    def _setup_directories(self):
        """Create necessary directories for file-based persistence."""
        directories = [
            self.queue_dir,
            self.pending_dir,
            self.processing_dir,
            self.completed_dir,
            self.failed_dir,
            self.persistent_dir
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    def _setup_agent_pipes(self):
        """Setup pipes for all agents in the layout."""
        if self.layout_mode == "2-agent":
            agents = ["agent-1", "agent-2"]
        elif self.layout_mode == "4-agent":
            agents = ["agent-1", "agent-2", "agent-3", "agent-4"]
        elif self.layout_mode == "8-agent":
            agents = ["agent-1", "agent-2", "agent-3", "agent-4", 
                     "agent-5", "agent-6", "agent-7", "agent-8"]
        else:
            raise ValueError(f"Unsupported layout mode: {self.layout_mode}")
        
        # Create pipes for each agent
        for agent in agents:
            read_fd, write_fd = os.pipe()
            self.pipes[agent] = (read_fd, write_fd)
            self.pipe_locks[agent] = threading.Lock()
            self.message_queues[agent] = queue.Queue()
            self.message_counts[agent] = 0
            self.persistent_counts[agent] = 0
        
        print(f"📡 Created pipes for {len(agents)} agents")
    
    def send_message(self, from_agent: str, to_agent: str, message: str, 
                    tag: str = "normal", priority: str = "normal", 
                    use_persistence: bool = True) -> str:
        """Send a message via both pipes and file-based queue."""
        if to_agent not in self.pipes:
            raise ValueError(f"Unknown agent: {to_agent}")
        
        hybrid_msg = HybridMessage(from_agent, to_agent, message, tag, priority)
        
        # 1. Send via pipe (real-time)
        self._send_via_pipe(hybrid_msg)
        
        # 2. Persist to file (reliability)
        if use_persistence:
            self._persist_message(hybrid_msg)
        
        print(f"📤 {from_agent} → {to_agent}: {message[:50]}... (Hybrid)")
        return hybrid_msg.id
    
    def _send_via_pipe(self, message: HybridMessage):
        """Send message via pipe for real-time delivery."""
        # Serialize message
        msg_data = json.dumps(message.to_dict()) + "\n"
        msg_bytes = msg_data.encode('utf-8')
        
        # Send via pipe
        with self.pipe_locks[message.to_agent]:
            write_fd = self.pipes[message.to_agent][1]
            os.write(write_fd, msg_bytes)
        
        message.pipe_delivered = True
    
    def _persist_message(self, message: HybridMessage):
        """Persist message to file for reliability."""
        # Write to persistent directory
        persistent_file = self.persistent_dir / f"{message.id}.json"
        with open(persistent_file, 'w') as f:
            json.dump(message.to_dict(), f, indent=2)
        
        message.persisted = True
        self.persistent_counts[message.from_agent] += 1
    
    def _pipe_reader_thread(self, agent_id: str):
        """Thread function that reads from a pipe and puts messages in queue."""
        read_fd = self.pipes[agent_id][0]
        message_queue = self.message_queues[agent_id]
        
        print(f"📖 Reader thread started for {agent_id}")
        
        # Buffer for partial messages
        buffer = ""
        
        while self.running:
            try:
                # For Windows compatibility, use a simple polling approach
                # Read with a very small timeout to avoid blocking
                try:
                    # Try to read a small amount of data
                    data = os.read(read_fd, 1024)
                    if data:
                        # Decode and add to buffer
                        buffer += data.decode('utf-8')
                        
                        # Process complete messages (separated by newlines)
                        while '\n' in buffer:
                            line, buffer = buffer.split('\n', 1)
                            line = line.strip()
                            
                            if line:
                                try:
                                    # Parse JSON message
                                    msg_dict = json.loads(line)
                                    hybrid_msg = HybridMessage.from_dict(msg_dict)
                                    hybrid_msg.status = "received"
                                    
                                    # Put message in queue
                                    message_queue.put(hybrid_msg)
                                    self.message_counts[agent_id] += 1
                                    
                                    print(f"📥 {agent_id} received via pipe: {hybrid_msg.message[:50]}...")
                                    
                                except json.JSONDecodeError as e:
                                    print(f"JSON decode error for {agent_id}: {e}")
                                    continue
                except OSError:
                    # No data available, this is expected
                    pass
                
                # Small sleep to prevent busy waiting and allow other threads to run
                time.sleep(0.05)  # 50ms sleep
                
            except Exception as e:
                if self.running:
                    print(f"Error reading message for {agent_id}: {e}")
                break
        
        print(f"📖 Reader thread stopped for {agent_id}")
    
    def start(self):
        """Start the hybrid manager and reader threads."""
        if self.running:
            print("Hybrid manager already running")
            return
        
        self.running = True
        
        # Start reader threads for each agent
        for agent_id in self.pipes.keys():
            thread = threading.Thread(
                target=self._pipe_reader_thread, 
                args=(agent_id,), 
                daemon=True
            )
            thread.start()
            self.reader_threads[agent_id] = thread
        
        print("🚀 Hybrid communication manager started")
    
    def stop(self):
        """Stop the hybrid manager and reader threads."""
        if not self.running:
            return
            
        self.running = False
        
        # Wait for reader threads to finish
        for agent_id, thread in self.reader_threads.items():
            if thread.is_alive():
                thread.join(timeout=2)
                if thread.is_alive():
                    print(f"⚠️ Reader thread for {agent_id} did not stop gracefully")
        
        print("⏹️ Hybrid communication manager stopped")
    
    def get_message(self, agent_id: str, timeout: float = 1.0) -> Optional[HybridMessage]:
        """Get a message from an agent's queue (pipe-based)."""
        if agent_id not in self.message_queues:
            raise ValueError(f"Unknown agent: {agent_id}")
        
        try:
            return self.message_queues[agent_id].get(timeout=timeout)
        except queue.Empty:
            return None
    
    def get_persistent_messages(self, agent_id: str) -> List[HybridMessage]:
        """Get all persistent messages for an agent."""
        messages = []
        persistent_files = list(self.persistent_dir.glob(f"*_to_{agent_id}.json"))
        
        for file in persistent_files:
            try:
                with open(file, 'r') as f:
                    msg_dict = json.load(f)
                    messages.append(HybridMessage.from_dict(msg_dict))
            except Exception as e:
                print(f"Error reading persistent message {file}: {e}")
        
        return sorted(messages, key=lambda x: x.created_at)
    
    def send_via_cli(self, message: HybridMessage) -> bool:
        """Send a message using the AgentCellPhone CLI (for UI interaction)."""
        try:
            cmd = [
                "python", "src/agent_cell_phone.py",
                "--layout", self.layout_mode,
                "--agent", message.to_agent,
                "--msg", message.message,
                "--tag", message.tag
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                message.status = "completed"
                return True
            else:
                message.status = "failed"
                return False
                
        except Exception as e:
            message.status = "failed"
            print(f"Error sending message via CLI: {e}")
            return False
    
    def broadcast_message(self, from_agent: str, message: str, 
                         tag: str = "normal", priority: str = "normal") -> List[str]:
        """Broadcast a message to all agents except sender."""
        msg_ids = []
        
        for agent_id in self.pipes.keys():
            if agent_id != from_agent:
                msg_id = self.send_message(from_agent, agent_id, message, tag, priority)
                msg_ids.append(msg_id)
        
        return msg_ids
    
    def get_status(self) -> Dict[str, Any]:
        """Get comprehensive status of hybrid system."""
        status = {
            "layout_mode": self.layout_mode,
            "running": self.running,
            "pipes": {},
            "message_counts": self.message_counts.copy(),
            "persistent_counts": self.persistent_counts.copy(),
            "queue_sizes": {},
            "persistent_files": {}
        }
        
        for agent_id, (read_fd, write_fd) in self.pipes.items():
            status["pipes"][agent_id] = {
                "read_fd": read_fd,
                "write_fd": write_fd,
                "thread_alive": self.reader_threads[agent_id].is_alive() if agent_id in self.reader_threads else False
            }
            status["queue_sizes"][agent_id] = self.message_queues[agent_id].qsize()
            
            # Count persistent files for this agent
            persistent_files = list(self.persistent_dir.glob(f"*_to_{agent_id}.json"))
            status["persistent_files"][agent_id] = len(persistent_files)
        
        return status
    
    def cleanup(self):
        """Clean up all resources."""
        self.stop()
        
        # Clean up pipes
        for agent_id, (read_fd, write_fd) in self.pipes.items():
            try:
                os.close(read_fd)
                os.close(write_fd)
            except OSError:
                pass
        
        self.pipes.clear()
        self.pipe_locks.clear()
        self.message_queues.clear()
        self.reader_threads.clear()
        print("🧹 Hybrid communication resources cleaned up")

class HybridAgentClient:
    """Client for agents to communicate via hybrid system."""
    
    def __init__(self, agent_id: str, hybrid_manager: HybridCommunicationManager):
        self.agent_id = agent_id
        self.hybrid_manager = hybrid_manager
        self.message_handlers = {}
        
        # Register default handlers
        self.register_handler("coordinate", self._handle_coordination)
        self.register_handler("task", self._handle_task)
        self.register_handler("reply", self._handle_reply)
        self.register_handler("normal", self._handle_normal)
        
        print(f"🤖 {agent_id} hybrid client initialized")
    
    def register_handler(self, tag: str, handler_func):
        """Register a message handler for a specific tag."""
        self.message_handlers[tag] = handler_func
    
    def send_message(self, to_agent: str, message: str, tag: str = "normal", 
                    use_persistence: bool = True) -> str:
        """Send a message using hybrid system."""
        return self.hybrid_manager.send_message(
            self.agent_id, to_agent, message, tag, 
            use_persistence=use_persistence
        )
    
    def broadcast(self, message: str, tag: str = "normal") -> List[str]:
        """Broadcast a message to all other agents."""
        return self.hybrid_manager.broadcast_message(self.agent_id, message, tag)
    
    def get_message(self, timeout: float = 1.0) -> Optional[HybridMessage]:
        """Get a message from pipe queue (real-time)."""
        return self.hybrid_manager.get_message(self.agent_id, timeout)
    
    def get_persistent_messages(self) -> List[HybridMessage]:
        """Get all persistent messages for this agent."""
        return self.hybrid_manager.get_persistent_messages(self.agent_id)
    
    def process_messages(self, timeout: float = 1.0):
        """Process incoming messages from pipe queue."""
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
    
    def _handle_coordination(self, message: HybridMessage):
        """Handle coordination messages."""
        print(f"🤝 {self.agent_id} handling coordination: {message.message[:50]}...")
        # Send acknowledgment
        return self.send_message(message.from_agent, "Ready to coordinate!", "reply")
    
    def _handle_task(self, message: HybridMessage):
        """Handle task assignments."""
        print(f"📋 {self.agent_id} handling task: {message.message[:50]}...")
        # Send acknowledgment
        return self.send_message(message.from_agent, f"Task received: {message.message[:30]}...", "reply")
    
    def _handle_reply(self, message: HybridMessage):
        """Handle reply messages."""
        print(f"💬 {self.agent_id} handling reply: {message.message[:50]}...")
        return None
    
    def _handle_normal(self, message: HybridMessage):
        """Handle normal messages."""
        print(f"📝 {self.agent_id} handling normal message: {message.message[:50]}...")
        return None

def demonstrate_hybrid_communication():
    """Demonstrate hybrid communication system."""
    print("🎯 Hybrid Communication System Demo")
    print("=" * 60)
    
    try:
        # Initialize hybrid manager
        hybrid_manager = HybridCommunicationManager("2-agent")
        hybrid_manager.start()
        
        # Create agent clients
        agent_1 = HybridAgentClient("agent-1", hybrid_manager)
        agent_2 = HybridAgentClient("agent-2", hybrid_manager)
        
        print("\n📤 Step 1: Agent-2 sends coordination message (with persistence)")
        agent_2.send_message("agent-1", "Hello Agent-1! Ready to coordinate via hybrid system?", "coordinate")
        
        # Let agents process messages
        time.sleep(1)
        agent_1.process_messages()
        
        print("\n📤 Step 2: Agent-2 assigns a task (with persistence)")
        agent_2.send_message("agent-1", "Please analyze the dataset using hybrid communication", "task")
        
        time.sleep(1)
        agent_1.process_messages()
        
        print("\n📤 Step 3: Agent-1 sends rapid message (pipe-only, no persistence)")
        agent_1.send_message("agent-2", "Quick status update - working on it!", "normal", use_persistence=False)
        
        time.sleep(1)
        agent_2.process_messages()
        
        print("\n📤 Step 4: Agent-1 reports progress (with persistence)")
        agent_1.send_message("agent-2", "Hybrid communication working great! Analysis 75% complete.", "reply")
        
        time.sleep(1)
        agent_2.process_messages()
        
        print("\n📤 Step 5: Agent-2 broadcasts to all agents")
        agent_2.broadcast("Hybrid system combines speed of pipes with reliability of files!", "normal")
        
        time.sleep(1)
        agent_1.process_messages()
        
        print("\n📤 Step 6: Agent-1 reports completion")
        agent_1.send_message("agent-2", "Analysis complete! Hybrid system is the best of both worlds.", "reply")
        
        time.sleep(1)
        agent_2.process_messages()
        
        # Show comprehensive status
        status = hybrid_manager.get_status()
        print(f"\n📊 Hybrid System Status:")
        print(f"  Layout Mode: {status['layout_mode']}")
        print(f"  Running: {status['running']}")
        print(f"  Agent-1 Pipe Messages: {status['message_counts']['agent-1']}")
        print(f"  Agent-2 Pipe Messages: {status['message_counts']['agent-2']}")
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
        
        # Cleanup
        hybrid_manager.cleanup()
        print("\n✅ Hybrid communication demo completed!")
        
    except Exception as e:
        print(f"❌ Error during hybrid communication demo: {e}")
        if 'hybrid_manager' in locals():
            hybrid_manager.cleanup()
        print("🔄 Demo terminated due to error")

def compare_hybrid_performance():
    """Compare hybrid vs file-based vs pipe-only performance."""
    print("\n⚡ Hybrid Performance Comparison")
    print("=" * 60)
    
    # Test hybrid communication
    hybrid_manager = HybridCommunicationManager("2-agent")
    hybrid_manager.start()
    agent_1 = HybridAgentClient("agent-1", hybrid_manager)
    agent_2 = HybridAgentClient("agent-2", hybrid_manager)
    
    # Hybrid performance test (with persistence)
    start_time = time.time()
    for i in range(50):
        agent_2.send_message("agent-1", f"Hybrid message {i}", "normal", use_persistence=True)
        agent_1.process_messages(timeout=0.01)
    
    hybrid_time = time.time() - start_time
    
    # Pipe-only performance test
    start_time = time.time()
    for i in range(50):
        agent_2.send_message("agent-1", f"Pipe message {i}", "normal", use_persistence=False)
        agent_1.process_messages(timeout=0.01)
    
    pipe_time = time.time() - start_time
    hybrid_manager.cleanup()
    
    # File-based performance test (simulated)
    start_time = time.time()
    for i in range(50):
        # Simulate file I/O overhead
        time.sleep(0.002)  # Simulate file write
        time.sleep(0.002)  # Simulate file read
    
    file_time = time.time() - start_time
    
    print(f"📊 Performance Results (50 messages each):")
    print(f"  Hybrid (with persistence): {hybrid_time:.3f} seconds")
    print(f"  Pipe-only (no persistence): {pipe_time:.3f} seconds")
    print(f"  File-based (simulated): {file_time:.3f} seconds")
    print(f"  Hybrid vs File speedup: {file_time/hybrid_time:.1f}x faster")
    print(f"  Pipe vs File speedup: {file_time/pipe_time:.1f}x faster")

if __name__ == "__main__":
    demonstrate_hybrid_communication()
    compare_hybrid_performance() 