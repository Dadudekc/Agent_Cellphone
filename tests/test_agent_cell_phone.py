import pytest

from agent_cell_phone import AgentCellPhone, MsgTag


def test_send_records_cursor_actions():
    acp = AgentCellPhone(layout_mode="2-agent", test=True)
    acp.send("Agent-2", "ping", MsgTag.VERIFY)

    # three cursor actions: move+click, type, enter
    assert acp._cursor.record[0].startswith("move(")
    assert "type([VERIFY] ping)" == acp._cursor.record[1]
    assert acp._cursor.record[2] == "enter"
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

