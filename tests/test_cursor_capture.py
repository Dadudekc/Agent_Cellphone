#!/usr/bin/env python3
"""
Tests for the Cursor AI response capture helpers. These tests avoid
touching any real user data by creating temporary directories and
mocking the filesystem lookups performed by the helpers.
"""

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


def test_cursor_storage_path(tmp_path, monkeypatch):
    """cursor_workspace_storage should respect the user's home directory."""
    from src.cursor_capture.db_reader import cursor_workspace_storage

    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    expected = tmp_path / ".config" / "Cursor" / "User" / "workspaceStorage"
    assert cursor_workspace_storage() == expected


def test_workspace_mapping(tmp_path):
    """Agent workspace map can be loaded from JSON."""
    mapping = {"Agent-1": {"workspace_root": "/fake"}}
    map_path = tmp_path / "agent_workspace_map.json"
    map_path.write_text(json.dumps(mapping))

    loaded = json.loads(map_path.read_text())
    assert loaded == mapping


def test_database_finding(tmp_path, monkeypatch):
    """find_state_db_for_workspace locates the correct state.vscdb file."""
    from src.cursor_capture import db_reader
    from src.cursor_capture.db_reader import find_state_db_for_workspace

    workspace_root = tmp_path / "project-A"
    hash_dir = tmp_path / "hash"
    hash_dir.mkdir()
    (hash_dir / "workspace.json").write_text(json.dumps({"folder": str(workspace_root)}))
    state_db = hash_dir / "state.vscdb"
    state_db.write_text("stub")

    monkeypatch.setattr(db_reader, "cursor_workspace_storage", lambda: tmp_path)
    result = find_state_db_for_workspace(str(workspace_root))
    assert result == state_db


def test_message_extraction():
    """extract_messages normalises chat JSON into role/text pairs."""
    from src.cursor_capture.db_reader import extract_messages

    sample_data = {
        "chats": [
            {
                "messages": [
                    {"role": "user", "content": "Hello, can you help me?"},
                    {"role": "assistant", "content": "Of course! I'd be happy to help you with your question."},
                    {"role": "user", "content": "Great, thanks!"},
                ]
            }
        ]
    }

    messages = extract_messages(json.dumps(sample_data))
    assert [m["role"] for m in messages] == ["user", "assistant", "user"]
    assert messages[1]["text"].startswith("Of course!")
