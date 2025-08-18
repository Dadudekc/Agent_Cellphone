import json
import logging

from src.services.conversation_logger import save_conversation


def test_save_conversation_skips_invalid_messages(tmp_path, caplog):
    messages = [
        {"role": "user", "content": "Hello"},
        {"role": "assistant"},  # missing content
        {"content": "No role"},  # missing role
    ]

    caplog.set_level(logging.WARNING)
    file_path = save_conversation("Test", messages, None, tmp_path)

    payload = json.loads(file_path.read_text())
    assert len(payload["messages"]) == 1
    msg = payload["messages"][0]
    assert msg["role"] == "user"
    assert msg["content"] == "Hello"
    assert msg["prompt_id"] == 1
    assert "timestamp" in msg
    assert any("Skipping invalid message" in record.message for record in caplog.records)
