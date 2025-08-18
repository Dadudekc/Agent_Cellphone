import sys
from pathlib import Path
import types

import pytest

try:
    import PyQt5  # noqa: F401
except ImportError:
    pytest.skip("PyQt5 not available", allow_module_level=True)

# Add the src directory to the path so tests can import project modules
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

# Provide a stub for pyautogui to avoid display requirements during tests
sys.modules.setdefault("pyautogui", types.ModuleType("pyautogui"))

from agent_cell_phone import AgentCellPhone, AgentMessage, MsgTag


def test_smoke_message_flow():
    """Basic smoke test ensuring send/receive workflow works headlessly."""
    agent1 = AgentCellPhone(agent_id="Agent-1", layout_mode="2-agent", test=True)
    agent2 = AgentCellPhone(agent_id="Agent-2", layout_mode="2-agent", test=True)

    agent1.start_listening()
    agent2.start_listening()
    try:
        # Send message from Agent-1 to Agent-2
        agent1.send("Agent-2", "Hello Agent-2!", MsgTag.NORMAL)

        # Simulate Agent-2 receiving the message
        incoming = AgentMessage("Agent-1", "Agent-2", "Hello Agent-2!", MsgTag.NORMAL)
        agent2._handle_incoming_message(incoming)

        # Agent-2 replies back
        agent2.reply("Agent-1", "Hello Agent-1!", MsgTag.REPLY)

        # Simulate Agent-1 receiving the reply
        reply_msg = AgentMessage("Agent-2", "Agent-1", "Hello Agent-1!", MsgTag.REPLY)
        agent1._handle_incoming_message(reply_msg)

        history1 = agent1.get_conversation_history()
        assert any(msg.from_agent == "Agent-1" and msg.to_agent == "Agent-2" for msg in history1)
        assert any(msg.from_agent == "Agent-2" and msg.to_agent == "Agent-1" for msg in history1)
    finally:
        agent1.stop_listening()
        agent2.stop_listening()
