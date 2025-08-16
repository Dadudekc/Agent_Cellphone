#!/usr/bin/env python3
"""
Test Inter-Agent Communication Framework
=======================================
Demonstrates messaging between Agent-1 through Agent-4
using the advanced inter-agent communication framework
"""

import time
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))

from services.inter_agent_framework import InterAgentFramework, Message, MessageType


def test_agent_communication() -> None:
    """Ensure messages can be sent between agents"""
    iaf = InterAgentFramework("Agent-1", layout_mode="2-agent", test=True)

    msg = Message(
        sender="Agent-1",
        recipient="Agent-2",
        message_type=MessageType.COMMAND,
        command="ping",
    )

    assert iaf.send_message("Agent-2", msg)
    assert iaf.message_history[-1].command == "ping"


def test_agent_responses() -> None:
    """Verify that command handlers send a response"""
    iaf = InterAgentFramework("Agent-1", layout_mode="2-agent", test=True)

    incoming = Message(
        sender="Agent-2",
        recipient="Agent-1",
        message_type=MessageType.COMMAND,
        command="ping",
    )

    result = iaf._handle_ping(incoming)

    assert result == "Ping responded"
    assert iaf.message_history[-1].recipient == "Agent-2"
    assert iaf.message_history[-1].command == "pong"


def test_framework_sends_structured_message():
    iaf = InterAgentFramework("Agent-1", layout_mode="2-agent", test=True)

    msg = Message(
        sender="Agent-1",
        recipient="Agent-2",
        message_type=MessageType.COMMAND,
        command="ping",
    )
    assert iaf.send_message("Agent-2", msg)
    # message persisted
    assert iaf.message_history[0].command == "ping"


def test_send_to_agents_handles_missing():
    iaf = InterAgentFramework("Agent-1", layout_mode="2-agent", test=True)
    msg = Message(
        sender="Agent-1",
        recipient="Agent-2",
        message_type=MessageType.COMMAND,
        command="ping",
    )

    results = iaf.send_to_agents(["Agent-2", "Agent-99"], msg)
    assert results["Agent-2"] is True
    assert results["Agent-99"] is False

if __name__ == "__main__":
    test_agent_communication()
    test_agent_responses()
