import json
from threading import Event

import pytest

from agent_cell_phone import AgentCellPhone, MsgTag


def test_listen_loop_dispatches_file_inbox_messages(tmp_path):
    """Ensure inbox files trigger registered handlers."""
    acp = AgentCellPhone(agent_id="Agent-1", layout_mode="2-agent", test=True)

    received = []
    event = Event()

    def handler(m):
        received.append(m)
        event.set()

    acp.register_handler(MsgTag.SYNC.value, handler)

    # Override inbox directory to temporary path
    acp._inbox_override = [tmp_path]
    acp.start_listening()

    # Write a synthetic inbox message
    message = {
        "type": "sync",
        "from": "Agent-2",
        "to": "Agent-1",
        "summary": "Test message",
    }
    (tmp_path / "msg_test.json").write_text(json.dumps(message))

    # Wait for listener to process the file
    event.wait(timeout=2)

    acp.stop_listening()

    assert len(received) == 1
    assert received[0].content == "Test message"
    assert received[0].from_agent == "Agent-2"
    assert len(acp.get_conversation_history()) == 1
