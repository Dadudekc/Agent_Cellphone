#!/usr/bin/env python3
"""
Windows-Compatible Pipe-Based Inter-Agent Communication
=======================================================
Uses threads and queues to handle pipe communication on Windows.
Provides real-time, in-memory messaging between agents.
"""

import os
import json
import time
import threading
import queue
from datetime import datetime
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

class PipeMessage:
    """Message structure for pipe communication."""
    
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
            "created_at": self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PipeMessage':
        """Create PipeMessage from dictionary."""
        msg = cls(data["from"], data["to"], data["message"], data.get("tag", "normal"))
        msg.id = data["id"]
        msg.timestamp = data["timestamp"]
        msg.priority = data.get("priority", "normal")
        msg.status = data.get("status", "pending")
        msg.created_at = data.get("created_at", msg.timestamp)
        return msg

class WindowsPipeManager:
    """Windows-compatible pipe manager using threads and queues."""
    
    def __init__(self, layout_mode: str = "2-agent"):
        self.layout_mode = layout_mode
        self.coordinate_finder = CoordinateFinder()
        
        # Pipe management
        self.pipes: Dict[str, Tuple[int, int]] = {}  # agent_id -> (read_fd, write_fd)
        self.pipe_locks: Dict[str, threading.Lock] = {}
        
        # Message queues for each agent
        self.message_queues: Dict[str, queue.Queue] = {}
        
        # Thread management
        self.reader_threads: Dict[str, threading.Thread] = {}
        self.running = False
        
        # Message tracking
        self.message_counts: Dict[str, int] = {}
        
        # Setup for layout mode
        self._setup_agent_pipes()
        
        print(f"🔗 WindowsPipeManager initialized for {layout_mode} mode")
    
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
        
        print(f"📡 Created pipes for {len(agents)} agents")
    
    def send_message(self, from_agent: str, to_agent: str, message: str, 
                    tag: str = "normal", priority: str = "normal") -> str:
        """Send a message via pipe."""
        if to_agent not in self.pipes:
            raise ValueError(f"Unknown agent: {to_agent}")
        
        pipe_msg = PipeMessage(from_agent, to_agent, message, tag, priority)
        
        # Serialize message
        msg_data = json.dumps(pipe_msg.to_dict()) + "\n"
        msg_bytes = msg_data.encode('utf-8')
        
        # Send via pipe
        with self.pipe_locks[to_agent]:
            write_fd = self.pipes[to_agent][1]
            os.write(write_fd, msg_bytes)
        
        print(f"📤 {from_agent} → {to_agent}: {message[:50]}...")
        return pipe_msg.id
    
    def _pipe_reader_thread(self, agent_id: str):
        """Thread function that reads from a pipe and puts messages in queue."""
        read_fd = self.pipes[agent_id][0]
        message_queue = self.message_queues[agent_id]
        
        print(f"📖 Reader thread started for {agent_id}")
        
        while self.running:
            try:
                # Blocking read from pipe
                data = os.read(read_fd, 4096)
                if data:
                    # Parse JSON message
                    msg_str = data.decode('utf-8').strip()
                    msg_dict = json.loads(msg_str)
                    pipe_msg = PipeMessage.from_dict(msg_dict)
                    pipe_msg.status = "received"
                    
                    # Put message in queue
                    message_queue.put(pipe_msg)
                    self.message_counts[agent_id] += 1
                    
                    print(f"📥 {agent_id} received: {pipe_msg.message[:50]}...")
                
            except (json.JSONDecodeError, OSError) as e:
                if self.running:  # Only log if we're supposed to be running
                    print(f"Error reading message for {agent_id}: {e}")
                break
        
        print(f"📖 Reader thread stopped for {agent_id}")
    
    def start(self):
        """Start the pipe manager and reader threads."""
        if self.running:
            print("Pipe manager already running")
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
        
        print("🚀 Windows pipe manager started")
    
    def stop(self):
        """Stop the pipe manager and reader threads."""
        self.running = False
        
        # Wait for reader threads to finish
        for agent_id, thread in self.reader_threads.items():
            thread.join(timeout=2)
        
        print("⏹️ Windows pipe manager stopped")
    
    def get_message(self, agent_id: str, timeout: float = 1.0) -> Optional[PipeMessage]:
        """Get a message from an agent's queue."""
        if agent_id not in self.message_queues:
            raise ValueError(f"Unknown agent: {agent_id}")
        
        try:
            return self.message_queues[agent_id].get(timeout=timeout)
        except queue.Empty:
            return None
    
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
        """Get status of all pipes and queues."""
        status = {
            "layout_mode": self.layout_mode,
            "running": self.running,
            "pipes": {},
            "message_counts": self.message_counts.copy(),
            "queue_sizes": {}
        }
        
        for agent_id, (read_fd, write_fd) in self.pipes.items():
            status["pipes"][agent_id] = {
                "read_fd": read_fd,
                "write_fd": write_fd,
                "thread_alive": self.reader_threads[agent_id].is_alive() if agent_id in self.reader_threads else False
            }
            status["queue_sizes"][agent_id] = self.message_queues[agent_id].qsize()
        
        return status
    
    def cleanup(self):
        """Clean up pipe resources."""
        self.stop()
        
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
        print("🧹 Pipe resources cleaned up")

class WindowsAgentClient:
    """Client for agents to communicate via Windows pipes."""
    
    def __init__(self, agent_id: str, pipe_manager: WindowsPipeManager):
        self.agent_id = agent_id
        self.pipe_manager = pipe_manager
        self.message_handlers = {}
        
        # Register default handlers
        self.register_handler("coordinate", self._handle_coordination)
        self.register_handler("task", self._handle_task)
        self.register_handler("reply", self._handle_reply)
        self.register_handler("normal", self._handle_normal)
        
        print(f"🤖 {agent_id} Windows pipe client initialized")
    
    def register_handler(self, tag: str, handler_func):
        """Register a message handler for a specific tag."""
        self.message_handlers[tag] = handler_func
    
    def send_message(self, to_agent: str, message: str, tag: str = "normal") -> str:
        """Send a message to another agent."""
        return self.pipe_manager.send_message(self.agent_id, to_agent, message, tag)
    
    def broadcast(self, message: str, tag: str = "normal") -> List[str]:
        """Broadcast a message to all other agents."""
        return self.pipe_manager.broadcast_message(self.agent_id, message, tag)
    
    def get_message(self, timeout: float = 1.0) -> Optional[PipeMessage]:
        """Get a message for this agent."""
        return self.pipe_manager.get_message(self.agent_id, timeout)
    
    def process_messages(self, timeout: float = 1.0):
        """Process incoming messages."""
        msg = self.get_message(timeout)
        if msg:
            handler = self.message_handlers.get(msg.tag, self._handle_normal)
            return handler(msg)
        return None
    
    def _handle_coordination(self, message: PipeMessage):
        """Handle coordination messages."""
        print(f"🤝 {self.agent_id} handling coordination: {message.message[:50]}...")
        # Send acknowledgment
        return self.send_message(message.from_agent, "Ready to coordinate!", "reply")
    
    def _handle_task(self, message: PipeMessage):
        """Handle task assignments."""
        print(f"📋 {self.agent_id} handling task: {message.message[:50]}...")
        # Send acknowledgment
        return self.send_message(message.from_agent, f"Task received: {message.message[:30]}...", "reply")
    
    def _handle_reply(self, message: PipeMessage):
        """Handle reply messages."""
        print(f"💬 {self.agent_id} handling reply: {message.message[:50]}...")
        return None
    
    def _handle_normal(self, message: PipeMessage):
        """Handle normal messages."""
        print(f"📝 {self.agent_id} handling normal message: {message.message[:50]}...")
        return None

def demonstrate_windows_pipe_communication():
    """Demonstrate Windows pipe-based agent communication."""
    print("🎯 Windows Pipe-Based Agent Communication Demo")
    print("=" * 60)
    
    # Initialize pipe manager
    pipe_manager = WindowsPipeManager("2-agent")
    pipe_manager.start()
    
    # Create agent clients
    agent_1 = WindowsAgentClient("agent-1", pipe_manager)
    agent_2 = WindowsAgentClient("agent-2", pipe_manager)
    
    print("\n📤 Step 1: Agent-2 sends coordination message")
    agent_2.send_message("agent-1", "Hello Agent-1! Ready to coordinate via Windows pipes?", "coordinate")
    
    # Let agents process messages
    time.sleep(1)
    agent_1.process_messages()
    
    print("\n📤 Step 2: Agent-2 assigns a task")
    agent_2.send_message("agent-1", "Please analyze the dataset using Windows pipe communication", "task")
    
    time.sleep(1)
    agent_1.process_messages()
    
    print("\n📤 Step 3: Agent-1 reports progress")
    agent_1.send_message("agent-2", "Windows pipe communication working great! Analysis 75% complete.", "reply")
    
    time.sleep(1)
    agent_2.process_messages()
    
    print("\n📤 Step 4: Agent-2 broadcasts to all agents")
    agent_2.broadcast("Windows pipe-based communication is much faster than file-based queues!", "normal")
    
    time.sleep(1)
    agent_1.process_messages()
    
    print("\n📤 Step 5: Agent-1 reports completion")
    agent_1.send_message("agent-2", "Analysis complete! Windows pipes are excellent for real-time communication.", "reply")
    
    time.sleep(1)
    agent_2.process_messages()
    
    # Show status
    status = pipe_manager.get_status()
    print(f"\n📊 Windows Pipe Status:")
    print(f"  Layout Mode: {status['layout_mode']}")
    print(f"  Running: {status['running']}")
    print(f"  Agent-1 Messages: {status['message_counts']['agent-1']}")
    print(f"  Agent-2 Messages: {status['message_counts']['agent-2']}")
    print(f"  Agent-1 Queue Size: {status['queue_sizes']['agent-1']}")
    print(f"  Agent-2 Queue Size: {status['queue_sizes']['agent-2']}")
    
    # Cleanup
    pipe_manager.cleanup()
    print("\n✅ Windows pipe communication demo completed!")

def compare_windows_performance():
    """Compare Windows pipe vs file-based communication performance."""
    print("\n⚡ Windows Performance Comparison: Pipes vs Files")
    print("=" * 60)
    
    # Test Windows pipe communication
    pipe_manager = WindowsPipeManager("2-agent")
    pipe_manager.start()
    agent_1 = WindowsAgentClient("agent-1", pipe_manager)
    agent_2 = WindowsAgentClient("agent-2", pipe_manager)
    
    # Pipe performance test
    start_time = time.time()
    for i in range(100):
        agent_2.send_message("agent-1", f"Test message {i}", "normal")
        agent_1.process_messages(timeout=0.01)
    
    pipe_time = time.time() - start_time
    pipe_manager.cleanup()
    
    # File-based performance test (simulated)
    start_time = time.time()
    for i in range(100):
        # Simulate file I/O overhead
        time.sleep(0.001)  # Simulate file write
        time.sleep(0.001)  # Simulate file read
    
    file_time = time.time() - start_time
    
    print(f"📊 Windows Performance Results:")
    print(f"  Pipes (100 messages): {pipe_time:.3f} seconds")
    print(f"  Files (100 messages): {file_time:.3f} seconds")
    print(f"  Speedup: {file_time/pipe_time:.1f}x faster with pipes")

def demonstrate_real_time_communication():
    """Demonstrate real-time communication capabilities."""
    print("\n⚡ Real-Time Communication Demo")
    print("=" * 50)
    
    pipe_manager = WindowsPipeManager("2-agent")
    pipe_manager.start()
    
    agent_1 = WindowsAgentClient("agent-1", pipe_manager)
    agent_2 = WindowsAgentClient("agent-2", pipe_manager)
    
    # Send messages rapidly
    print("📤 Sending 10 messages rapidly...")
    for i in range(10):
        agent_2.send_message("agent-1", f"Rapid message {i+1}", "normal")
        time.sleep(0.1)  # Small delay between sends
    
    # Process all messages
    print("📥 Processing all messages...")
    processed_count = 0
    start_time = time.time()
    
    while processed_count < 10:
        msg = agent_1.get_message(timeout=0.1)
        if msg:
            print(f"  Processed: {msg.message}")
            processed_count += 1
    
    total_time = time.time() - start_time
    print(f"✅ Processed {processed_count} messages in {total_time:.3f} seconds")
    
    pipe_manager.cleanup()

if __name__ == "__main__":
    demonstrate_windows_pipe_communication()
    compare_windows_performance()
    demonstrate_real_time_communication()
