#!/usr/bin/env python3
"""
Agent Queue Communication Example
=================================
Demonstrates how agents can use the queue system for reliable communication.
"""

import time
import json
from pathlib import Path
from queue_manager import MessageQueueManager

class Agent:
    """Example agent that uses the queue system for communication."""
    
    def __init__(self, agent_id: str, layout_mode: str = "2-agent"):
        self.agent_id = agent_id
        self.layout_mode = layout_mode
        self.queue_manager = MessageQueueManager(layout_mode)
        self.base_dir = Path("agent_workspaces")
        self.inbox_dir = self.base_dir / agent_id / "inbox"
        self.outbox_dir = self.base_dir / agent_id / "outbox"
        
        # Create agent directories
        self.inbox_dir.mkdir(parents=True, exist_ok=True)
        self.outbox_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"🤖 {agent_id} initialized")
    
    def send_message(self, to_agent: str, message: str, tag: str = "normal"):
        """Send a message using the queue system."""
        print(f"📤 {self.agent_id} sending to {to_agent}: {message[:50]}...")
        
        msg_id = self.queue_manager.enqueue_message(
            from_agent=self.agent_id,
            to_agent=to_agent,
            message=message,
            tag=tag
        )
        
        # Store in outbox
        outbox_file = self.outbox_dir / f"{msg_id}.json"
        with open(outbox_file, 'w') as f:
            json.dump({
                "id": msg_id,
                "to": to_agent,
                "message": message,
                "tag": tag,
                "sent_at": time.time()
            }, f, indent=2)
        
        return msg_id
    
    def check_inbox(self):
        """Check for new messages in inbox."""
        # In a real implementation, this would check the completed queue
        # and move messages to the agent's inbox
        completed_messages = self.queue_manager.list_messages("completed")
        
        new_messages = []
        for msg in completed_messages:
            if msg["to"] == self.agent_id:
                # Check if we've already processed this message
                inbox_file = self.inbox_dir / f"{msg['id']}.json"
                if not inbox_file.exists():
                    # Move to inbox
                    with open(inbox_file, 'w') as f:
                        json.dump(msg, f, indent=2)
                    new_messages.append(msg)
        
        return new_messages
    
    def process_message(self, message):
        """Process a received message."""
        print(f"📥 {self.agent_id} received: {message['message'][:50]}...")
        
        # Example message processing logic
        if message['tag'] == 'coordinate':
            return self.handle_coordination(message)
        elif message['tag'] == 'task':
            return self.handle_task(message)
        elif message['tag'] == 'reply':
            return self.handle_reply(message)
        else:
            return self.handle_normal(message)
    
    def handle_coordination(self, message):
        """Handle coordination messages."""
        print(f"🤝 {self.agent_id} handling coordination request")
        # Send acknowledgment
        return self.send_message(
            message['from'],
            f"Ready to coordinate! What's the plan?",
            "reply"
        )
    
    def handle_task(self, message):
        """Handle task assignments."""
        print(f"📋 {self.agent_id} handling task assignment")
        # Send acknowledgment
        return self.send_message(
            message['from'],
            f"Task received: {message['message']}. Starting work now.",
            "reply"
        )
    
    def handle_reply(self, message):
        """Handle reply messages."""
        print(f"💬 {self.agent_id} handling reply")
        return None
    
    def handle_normal(self, message):
        """Handle normal messages."""
        print(f"📝 {self.agent_id} handling normal message")
        return None

def demonstrate_agent_communication():
    """Demonstrate agent communication using the queue system."""
    print("🎯 Agent Queue Communication Demo")
    print("=" * 50)
    
    # Start queue manager
    queue_manager = MessageQueueManager("2-agent")
    queue_manager.start()
    
    # Create agents
    agent_1 = Agent("agent-1", "2-agent")
    agent_2 = Agent("agent-2", "2-agent")
    
    print("\n📤 Step 1: Agent-2 initiates coordination")
    agent_2.send_message("agent-1", "Hello Agent-1! Ready to coordinate our data analysis project?", "coordinate")
    
    # Let queue process
    time.sleep(2)
    
    print("\n📥 Step 2: Agent-1 checks inbox and responds")
    messages = agent_1.check_inbox()
    for msg in messages:
        agent_1.process_message(msg)
    
    # Let queue process
    time.sleep(2)
    
    print("\n📤 Step 3: Agent-2 assigns a task")
    agent_2.send_message("agent-1", "Please analyze the customer feedback dataset and identify top 3 improvement areas.", "task")
    
    # Let queue process
    time.sleep(2)
    
    print("\n📥 Step 4: Agent-1 processes task assignment")
    messages = agent_1.check_inbox()
    for msg in messages:
        agent_1.process_message(msg)
    
    # Let queue process
    time.sleep(2)
    
    print("\n📤 Step 5: Agent-2 provides additional context")
    agent_2.send_message("agent-1", "Focus on sentiment analysis and feature requests. Use the new ML model.", "normal")
    
    # Let queue process
    time.sleep(2)
    
    print("\n📥 Step 6: Agent-1 processes context")
    messages = agent_1.check_inbox()
    for msg in messages:
        agent_1.process_message(msg)
    
    # Let queue process
    time.sleep(2)
    
    print("\n📤 Step 7: Agent-1 reports progress")
    agent_1.send_message("agent-2", "Analysis 60% complete. Found 2 major improvement areas so far.", "reply")
    
    # Let queue process
    time.sleep(2)
    
    print("\n📥 Step 8: Agent-2 processes progress report")
    messages = agent_2.check_inbox()
    for msg in messages:
        agent_2.process_message(msg)
    
    # Let queue process
    time.sleep(2)
    
    print("\n📤 Step 9: Agent-1 reports completion")
    agent_1.send_message("agent-2", "Analysis complete! Top 3 areas: UI/UX, Performance, Security.", "reply")
    
    # Let queue process
    time.sleep(2)
    
    print("\n📥 Step 10: Agent-2 acknowledges completion")
    messages = agent_2.check_inbox()
    for msg in messages:
        agent_2.process_message(msg)
    
    # Final status
    time.sleep(1)
    status = queue_manager.get_status()
    print(f"\n📊 Final Queue Status:")
    print(f"  Pending: {status['pending']}")
    print(f"  Completed: {status['completed']}")
    print(f"  Failed: {status['failed']}")
    
    # Stop queue manager
    queue_manager.stop()
    print("\n✅ Agent communication demo completed!")

if __name__ == "__main__":
    demonstrate_agent_communication() 