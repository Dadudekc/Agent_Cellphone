import os
import threading
from pathlib import Path

import pytest

from agent_cell_phone import AgentCellPhone, MsgTag


def test_send_records_cursor_actions():
    """Cursor should move to target and type message before pressing enter."""
    acp = AgentCellPhone(layout_mode="2-agent", test=True)
    acp.send("Agent-2", "ping", MsgTag.VERIFY)

    # cursor should move to target and type message before pressing enter
    assert acp._cursor.record[0].startswith("move(")
    assert "type([VERIFY] ping)" in acp._cursor.record
    assert acp._cursor.record[-1] == "enter"
    assert len(acp.get_conversation_history()) == 1


def test_send_invalid_agent_does_not_record():
    acp = AgentCellPhone(layout_mode="2-agent", test=True)
    acp.send("Agent-99", "hello")
    assert acp._cursor.record == []
    assert acp.get_conversation_history() == []


def test_invalid_layout_raises_system_exit():
    with pytest.raises(SystemExit):
        AgentCellPhone(layout_mode="missing", test=True)


def test_broadcast_sends_to_all_except_self():
    acp = AgentCellPhone(agent_id="Agent-1", layout_mode="2-agent", test=True)
    acp.broadcast("hello")
    # Only Agent-2 should be messaged in 2-agent layout
    assert any("type(hello" in action for action in acp._cursor.record)
    assert len(acp.get_conversation_history()) == 1


def test_send_accepts_special_characters():
    acp = AgentCellPhone(layout_mode="2-agent", test=True)
    message = "!@#$%^&*()"
    acp.send("Agent-2", message)
    assert acp.get_conversation_history()[0].content == message


def test_clear_queue_removes_pending_messages_and_locks():
    """Messages queued via PyAutoGUIQueue can be cleared and locks released."""
    acp = AgentCellPhone(layout_mode="2-agent", test=True)
    from overnight_runner.enhanced_gui import PyAutoGUIQueue

    queue = PyAutoGUIQueue()
    # Prevent background processing so messages remain queued
    queue.stop_processing()
    acp.set_pyautogui_queue(queue)

    # Queue a message for Agent-2
    acp.send("Agent-2", "hello", use_queue=True)
    assert queue.get_queue_status()["queue_size"] == 1

    # Simulate a lock held by the agent
    queue.agent_locks["Agent-2"].acquire()
    assert queue.agent_locks["Agent-2"].locked()

    assert acp.clear_queue() is True
    status = queue.get_queue_status()
    assert status["queue_size"] == 0
    assert not queue.agent_locks["Agent-2"].locked()

    queue.stop_processing()

def test_heartbeat_envelope_written(monkeypatch):
    inbox = Path("runtime/agent_comms/inbox")
    if inbox.exists():
        for f in inbox.glob("heartbeat_*.json"):
            f.unlink()
    os.environ["ACP_HEARTBEAT_SEC"] = "1"

    triggered = threading.Event()
    orig_emit = AgentCellPhone._emit_heartbeat

    def emit_and_signal(self):
        orig_emit(self)
        triggered.set()

    monkeypatch.setattr(AgentCellPhone, "_emit_heartbeat", emit_and_signal)

    acp = AgentCellPhone(layout_mode="2-agent", test=True)
    assert triggered.wait(timeout=2), "Heartbeat was not emitted"
    files = list(inbox.glob("heartbeat_*.json"))
    acp.stop()
    os.environ.pop("ACP_HEARTBEAT_SEC", None)
    assert files, "Heartbeat file should be created"
    for f in files:
        f.unlink()

