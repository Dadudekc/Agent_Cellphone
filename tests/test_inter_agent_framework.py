from inter_agent_framework import InterAgentFramework, Message, MessageType


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

