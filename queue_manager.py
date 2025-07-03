#!/usr/bin/env python3
"""
Dream.OS Message Queue Manager
==============================
Prototype implementation of the Inter-Agent Communication Queue System.
Handles cursor/keyboard contention by serializing agent communications.
"""

import os
import json
import time
import argparse
import logging
import subprocess
import threading
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import sys

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from utils.coordinate_finder import CoordinateFinder
except ImportError as e:
    print(f"Import error: {e}")
    print("Please run from the project root directory")
    sys.exit(1)

class MessageQueueManager:
    """Manages the message queue for inter-agent communication."""
    
    def __init__(self, layout_mode: str = "2-agent", log_level: str = "INFO"):
        self.layout_mode = layout_mode
        self.coordinate_finder = CoordinateFinder()
        
        # Setup directories
        self.base_dir = Path("agent_workspaces")
        self.queue_dir = self.base_dir / "queue"
        self.pending_dir = self.queue_dir / "pending"
        self.processing_dir = self.queue_dir / "processing"
        self.completed_dir = self.queue_dir / "completed"
        self.failed_dir = self.queue_dir / "failed"
        self.lock_file = self.queue_dir / "lock"
        self.log_file = self.queue_dir / "queue.log"
        
        # Create directories if they don't exist
        self._create_directories()
        
        # Setup logging
        self._setup_logging(log_level)
        
        # Queue processing state
        self.running = False
        self.processing_thread = None
        
        self.logger.info(f"MessageQueueManager initialized for {layout_mode} mode")
    
    def _create_directories(self):
        """Create necessary directories."""
        directories = [
            self.queue_dir,
            self.pending_dir,
            self.processing_dir,
            self.completed_dir,
            self.failed_dir
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    def _setup_logging(self, log_level: str):
        """Setup logging configuration."""
        logging.basicConfig(
            level=getattr(logging, log_level.upper()),
            format='%(asctime)s | %(levelname)8s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            handlers=[
                logging.FileHandler(self.log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def generate_message_id(self, from_agent: str, to_agent: str) -> str:
        """Generate a unique message ID."""
        timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
        return f"{timestamp}_{from_agent}_to_{to_agent}"
    
    def enqueue_message(self, from_agent: str, to_agent: str, message: str, 
                       tag: str = "normal", priority: str = "normal") -> str:
        """Add a message to the queue."""
        msg_id = self.generate_message_id(from_agent, to_agent)
        
        msg = {
            "id": msg_id,
            "timestamp": datetime.now().isoformat(),
            "from": from_agent,
            "to": to_agent,
            "message": message,
            "tag": tag,
            "priority": priority,
            "status": "pending",
            "retries": 0,
            "max_retries": 3,
            "created_at": datetime.now().isoformat(),
            "processed_at": None,
            "completed_at": None,
            "error": None
        }
        
        # Write message to pending queue
        msg_file = self.pending_dir / f"{msg_id}.json"
        with open(msg_file, 'w') as f:
            json.dump(msg, f, indent=2)
        
        self.logger.info(f"Enqueued message {msg_id} from {from_agent} to {to_agent}")
        return msg_id
    
    def acquire_lock(self) -> bool:
        """Acquire the processing lock."""
        if self.lock_file.exists():
            return False
        
        try:
            with open(self.lock_file, 'w') as f:
                f.write(f"Locked by queue manager at {datetime.now().isoformat()}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to acquire lock: {e}")
            return False
    
    def release_lock(self):
        """Release the processing lock."""
        try:
            if self.lock_file.exists():
                self.lock_file.unlink()
        except Exception as e:
            self.logger.error(f"Failed to release lock: {e}")
    
    def send_message_via_cli(self, message_data: Dict) -> bool:
        """Send a message using the AgentCellPhone CLI."""
        try:
            cmd = [
                "python", "src/agent_cell_phone.py",
                "--layout", self.layout_mode,
                "--agent", message_data["to"],
                "--msg", message_data["message"],
                "--tag", message_data["tag"]
            ]
            
            self.logger.info(f"Sending message via CLI: {' '.join(cmd)}")
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                self.logger.info(f"Message sent successfully: {message_data['id']}")
                return True
            else:
                self.logger.error(f"CLI command failed: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            self.logger.error(f"CLI command timed out for message {message_data['id']}")
            return False
        except Exception as e:
            self.logger.error(f"Error sending message {message_data['id']}: {e}")
            return False
    
    def process_message(self, msg_file: Path) -> bool:
        """Process a single message."""
        try:
            # Read message
            with open(msg_file, 'r') as f:
                message_data = json.load(f)
            
            # Update status to processing
            message_data["status"] = "processing"
            message_data["processed_at"] = datetime.now().isoformat()
            
            with open(msg_file, 'w') as f:
                json.dump(message_data, f, indent=2)
            
            # Move to processing directory
            processing_file = self.processing_dir / msg_file.name
            msg_file.rename(processing_file)
            
            # Send the message
            success = self.send_message_via_cli(message_data)
            
            if success:
                # Move to completed
                message_data["status"] = "completed"
                message_data["completed_at"] = datetime.now().isoformat()
                
                completed_file = self.completed_dir / msg_file.name
                with open(completed_file, 'w') as f:
                    json.dump(message_data, f, indent=2)
                
                processing_file.unlink()
                self.logger.info(f"Message {message_data['id']} completed successfully")
                return True
            else:
                # Handle retry logic
                message_data["retries"] += 1
                message_data["error"] = "CLI send failed"
                
                if message_data["retries"] >= message_data["max_retries"]:
                    # Move to failed
                    message_data["status"] = "failed"
                    failed_file = self.failed_dir / msg_file.name
                    with open(failed_file, 'w') as f:
                        json.dump(message_data, f, indent=2)
                    
                    processing_file.unlink()
                    self.logger.error(f"Message {message_data['id']} failed after {message_data['retries']} retries")
                else:
                    # Move back to pending for retry
                    pending_file = self.pending_dir / msg_file.name
                    with open(pending_file, 'w') as f:
                        json.dump(message_data, f, indent=2)
                    
                    processing_file.unlink()
                    self.logger.warning(f"Message {message_data['id']} queued for retry ({message_data['retries']}/{message_data['max_retries']})")
                
                return False
                
        except Exception as e:
            self.logger.error(f"Error processing message {msg_file.name}: {e}")
            return False
    
    def process_queue(self):
        """Main queue processing loop."""
        self.logger.info("Starting queue processing loop")
        
        while self.running:
            try:
                # Check for lock
                if not self.acquire_lock():
                    time.sleep(1)
                    continue
                
                # Get pending messages
                pending_files = sorted([f for f in self.pending_dir.iterdir() if f.suffix == '.json'])
                
                if not pending_files:
                    self.release_lock()
                    time.sleep(1)
                    continue
                
                # Process next message
                next_message = pending_files[0]
                self.logger.info(f"Processing message: {next_message.name}")
                
                success = self.process_message(next_message)
                
                # Release lock
                self.release_lock()
                
                # Small delay between messages
                time.sleep(0.5)
                
            except Exception as e:
                self.logger.error(f"Error in queue processing loop: {e}")
                self.release_lock()
                time.sleep(5)
    
    def start(self):
        """Start the queue manager."""
        if self.running:
            self.logger.warning("Queue manager is already running")
            return
        
        self.running = True
        self.processing_thread = threading.Thread(target=self.process_queue, daemon=True)
        self.processing_thread.start()
        self.logger.info("Queue manager started")
    
    def stop(self):
        """Stop the queue manager."""
        self.running = False
        if self.processing_thread:
            self.processing_thread.join(timeout=5)
        self.release_lock()
        self.logger.info("Queue manager stopped")
    
    def get_status(self) -> Dict:
        """Get current queue status."""
        pending_count = len(list(self.pending_dir.glob("*.json")))
        processing_count = len(list(self.processing_dir.glob("*.json")))
        completed_count = len(list(self.completed_dir.glob("*.json")))
        failed_count = len(list(self.failed_dir.glob("*.json")))
        
        return {
            "pending": pending_count,
            "processing": processing_count,
            "completed": completed_count,
            "failed": failed_count,
            "locked": self.lock_file.exists(),
            "running": self.running
        }
    
    def list_messages(self, status: str = "pending") -> List[Dict]:
        """List messages with given status."""
        if status == "pending":
            directory = self.pending_dir
        elif status == "processing":
            directory = self.processing_dir
        elif status == "completed":
            directory = self.completed_dir
        elif status == "failed":
            directory = self.failed_dir
        else:
            return []
        
        messages = []
        for msg_file in directory.glob("*.json"):
            try:
                with open(msg_file, 'r') as f:
                    msg = json.load(f)
                messages.append(msg)
            except Exception as e:
                self.logger.error(f"Error reading message file {msg_file}: {e}")
        
        return sorted(messages, key=lambda x: x.get("created_at", ""))
    
    def clear_failed_messages(self):
        """Clear all failed messages."""
        failed_files = list(self.failed_dir.glob("*.json"))
        for file in failed_files:
            file.unlink()
        self.logger.info(f"Cleared {len(failed_files)} failed messages")

def main():
    """Main function for CLI interface."""
    parser = argparse.ArgumentParser(description="Dream.OS Message Queue Manager")
    parser.add_argument("--mode", default="2-agent", choices=["2-agent", "4-agent", "8-agent"],
                       help="Layout mode")
    parser.add_argument("--log-level", default="INFO", 
                       choices=["DEBUG", "INFO", "WARNING", "ERROR"],
                       help="Logging level")
    parser.add_argument("--status", action="store_true", help="Show queue status")
    parser.add_argument("--list-pending", action="store_true", help="List pending messages")
    parser.add_argument("--list-failed", action="store_true", help="List failed messages")
    parser.add_argument("--clear-failed", action="store_true", help="Clear failed messages")
    parser.add_argument("--start", action="store_true", help="Start queue manager")
    parser.add_argument("--stop", action="store_true", help="Stop queue manager")
    parser.add_argument("--demo", action="store_true", help="Run demo with sample messages")
    
    args = parser.parse_args()
    
    # Initialize queue manager
    qm = MessageQueueManager(args.mode, args.log_level)
    
    if args.status:
        status = qm.get_status()
        print("\n📊 Queue Status:")
        print(f"  Pending: {status['pending']}")
        print(f"  Processing: {status['processing']}")
        print(f"  Completed: {status['completed']}")
        print(f"  Failed: {status['failed']}")
        print(f"  Locked: {status['locked']}")
        print(f"  Running: {status['running']}")
    
    elif args.list_pending:
        messages = qm.list_messages("pending")
        print(f"\n📋 Pending Messages ({len(messages)}):")
        for msg in messages:
            print(f"  {msg['id']}: {msg['from']} → {msg['to']} ({msg['tag']})")
    
    elif args.list_failed:
        messages = qm.list_messages("failed")
        print(f"\n❌ Failed Messages ({len(messages)}):")
        for msg in messages:
            print(f"  {msg['id']}: {msg['from']} → {msg['to']} (Error: {msg.get('error', 'Unknown')})")
    
    elif args.clear_failed:
        qm.clear_failed_messages()
        print("✅ Failed messages cleared")
    
    elif args.demo:
        print("\n🎯 Running Queue Manager Demo")
        print("=" * 40)
        
        # Start queue manager
        qm.start()
        
        # Enqueue some demo messages
        print("📤 Enqueueing demo messages...")
        
        qm.enqueue_message("agent-2", "agent-1", "Hello Agent-1! Ready to coordinate?", "coordinate")
        time.sleep(1)
        
        qm.enqueue_message("agent-2", "agent-1", "Please analyze the dataset", "task")
        time.sleep(1)
        
        qm.enqueue_message("agent-1", "agent-2", "Task received, starting analysis", "reply")
        time.sleep(1)
        
        # Let it process for a bit
        print("⏳ Processing messages...")
        time.sleep(5)
        
        # Show status
        status = qm.get_status()
        print(f"\n📊 Final Status:")
        print(f"  Pending: {status['pending']}")
        print(f"  Completed: {status['completed']}")
        print(f"  Failed: {status['failed']}")
        
        # Stop queue manager
        qm.stop()
        print("✅ Demo completed")
    
    elif args.start:
        print("🚀 Starting queue manager...")
        qm.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n⏹️ Stopping queue manager...")
            qm.stop()
    
    elif args.stop:
        print("⏹️ Stopping queue manager...")
        qm.stop()
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
