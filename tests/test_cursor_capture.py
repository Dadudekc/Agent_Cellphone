#!/usr/bin/env python3
"""Tests for Cursor AI Response Capture System."""

import json
from pathlib import Path


def test_cursor_watcher_outputs_no_partial_files(tmp_path, monkeypatch):
    """Ensure CursorDBWatcher writes files atomically without leaving partial files."""
    from src.cursor_capture import watcher as watcher_mod
    from src.cursor_capture.watcher import CursorDBWatcher

    inbox = tmp_path / "inbox"
    seen_dir = tmp_path / ".seen"
    inbox.mkdir()
    seen_dir.mkdir()

    monkeypatch.setattr(watcher_mod, "INBOX", inbox)
    monkeypatch.setattr(watcher_mod, "SEEN_DIR", seen_dir)

    def fake_read_assistant_messages(ws, seen):
        return [{"sig": "1", "text": "hi", "ts": 1}]

    monkeypatch.setattr(watcher_mod, "read_assistant_messages", fake_read_assistant_messages)

    w = CursorDBWatcher({"Agent-1": {"workspace_root": "dummy"}})
    w._check_all_agents()

    files = list(inbox.glob("assistant_*.json"))
    assert len(files) == 1, "expected one output file"
    json.loads(files[0].read_text())
    assert not list(inbox.glob("*.tmp")), "temporary file should not remain"


def test_extract_messages_parses_chat_json():
    """`extract_messages` normalizes chat JSON into messages."""
    from src.cursor_capture.db_reader import extract_messages

    sample = {
        "chats": [
            {
                "messages": [
                    {"role": "assistant", "content": "Hello"},
                    {"role": "user", "content": "Hi there"},
                ]
            }
        ]
    }
    msgs = extract_messages(json.dumps(sample))
    assert [m["role"] for m in msgs] == ["assistant", "user"]
    assert [m["text"] for m in msgs] == ["Hello", "Hi there"]


def test_find_state_db_for_workspace(tmp_path, monkeypatch):
    """`find_state_db_for_workspace` locates the correct state DB."""
    from src.cursor_capture import db_reader

    workspace_root = "C:/code/project"
    storage = tmp_path / "storage"
    target_dir = storage / "abc123"
    target_dir.mkdir(parents=True)
    (target_dir / "state.vscdb").touch()
    (target_dir / "workspace.json").write_text(json.dumps({"folder": workspace_root}))

    monkeypatch.setattr(db_reader, "cursor_workspace_storage", lambda: storage)
    result = db_reader.find_state_db_for_workspace(workspace_root)
    assert result == target_dir / "state.vscdb"


def test_read_assistant_messages_filters_seen_and_role(monkeypatch):
    """`read_assistant_messages` returns only new assistant messages."""
    from src.cursor_capture import db_reader

    sample = {
        "chats": [
            {
                "messages": [
                    {"role": "assistant", "content": "Hello"},
                    {"role": "user", "content": "Hi"},
                    {"role": "assistant", "content": "Another"},
                ]
            }
        ]
    }

    # Mock out filesystem and database interactions
    monkeypatch.setattr(db_reader, "find_state_db_for_workspace", lambda ws: Path("dummy"))

    class DummyConn:
        def close(self):
            pass

    monkeypatch.setattr(db_reader.sqlite3, "connect", lambda *a, **k: DummyConn())
    monkeypatch.setattr(db_reader, "_query_items", lambda conn: [("key", json.dumps(sample))])

    seen: set[str] = set()
    msgs = db_reader.read_assistant_messages("any", seen)
    assert len(msgs) == 2
    assert all(m["role"] == "assistant" for m in msgs)

    # Mark the first message as seen and ensure it's filtered out on subsequent call
    seen.add(msgs[0]["sig"])
    msgs2 = db_reader.read_assistant_messages("any", seen)
    assert len(msgs2) == 1
    assert msgs2[0]["text"] == "Another"
