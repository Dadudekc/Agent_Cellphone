#!/usr/bin/env python3
"""
Example usage of Agent Cell Phone system
Demonstrates basic messaging capabilities
"""

import time
from agent_cell_phone import AgentCellPhone


def main():
    print("📱 Agent Cell Phone - Example Usage")
    print("=" * 40)
    
    # Initialize agent
    print("Initializing agent-1...")
    acp = AgentCellPhone("agent-1")
    
    # Load 4-agent layout
    print("Loading 4-agent layout...")
    coords = acp.load_layout("4")
    print(f"Loaded coordinates for {len(coords)} agents")
    
    # Send individual messages
    print("\nSending individual messages...")
    acp.send("agent-2", "Hello from agent-1!")
    time.sleep(1)
    
    acp.send("agent-3", "How are you doing?")
    time.sleep(1)
    
    acp.send("agent-4", "Ready for collaboration!")
    time.sleep(1)
    
    # Broadcast a message
    print("\nBroadcasting to all agents...")
    results = acp.broadcast("Status update: All systems operational")
    
    print(f"Broadcast results: {results}")
    
    # Test message parsing
    print("\nTesting message parsing...")
    test_messages = [
        "@agent-2 resume",
        "@all status_ping", 
        "@agent-3 sync data",
        "@agent-1 restart"
    ]
    
    for msg in test_messages:
        parsed = acp.parse_message(msg)
        if parsed:
            print(f"✅ '{msg}' -> {parsed.recipient} | {parsed.command} | {parsed.args}")
        else:
            print(f"❌ '{msg}' -> Invalid format")
    
    print("\n🎉 Example completed!")
    print("Check agent-1/devlog.md for message logs")


if __name__ == "__main__":
    main() 