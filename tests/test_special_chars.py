#!/usr/bin/env python3
"""
Test script for broadcasting messages with special characters
"""

from src.services.agent_cell_phone import AgentCellPhone


def test_special_chars() -> None:
    """Ensure broadcasting handles special characters without error."""
    acp = AgentCellPhone(layout_mode="8-agent", test=True)
    message = "[VERIFY] Coordinate test 3: Numbers 1234567890"

    acp.broadcast(message)

    recipients = [agent for agent in acp._coords if agent != acp._agent_id]
    history = list(acp._conversation_history)

    assert len(history) == len(recipients)
    assert all(msg.content == message for msg in history)
