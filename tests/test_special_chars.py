#!/usr/bin/env python3
"""
Test script for broadcasting messages with special characters
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))

from services.agent_cell_phone import AgentCellPhone

def test_special_chars():
    """Test broadcasting messages with special characters"""
    print("🧪 Testing broadcast with special characters")
    
    # Initialize agent cell phone in test mode
    acp = AgentCellPhone(layout_mode="8-agent", test=True)
    
    # Test message with numbers
    message = "[VERIFY] Coordinate test 3: Numbers 1234567890"
    print(f"Broadcasting: {message}")
    
    # Send broadcast
    acp.broadcast(message)
    
    print("✅ Broadcast completed in test mode")

if __name__ == "__main__":
    test_special_chars()
