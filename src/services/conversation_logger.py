"""Utilities for saving and loading conversation transcripts.

This module provides helper functions to persist conversations to JSON
files under ``data/conversations``.  Each message is recorded with a
UTC timestamp, participant role information and a prompt identifier.
Additional metadata can be stored alongside the transcript to aid later
analysis.
"""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Sequence


def _sanitize_filename(title: str) -> str:
    """Return a safe filename derived from *title*.

    Non-alphanumeric characters are replaced with underscores so the
    resulting filename is suitable for most filesystems.
    """

    safe = re.sub(r"[^A-Za-z0-9_.-]+", "_", title).strip("_")
    return safe or "conversation"


def _serialise_message(message: Any, prompt_id: int) -> Dict[str, Any]:
    """Convert *message* into a serialisable dictionary.

    Supports both dictionary inputs and objects with attributes like
    ``role``/``content`` or ``from_agent``/``to_agent``/``content``.
    ``prompt_id`` is used when an explicit identifier is not present in
    the message.
    """

    if isinstance(message, dict):
        role = message.get("role") or message.get("from")
        to = message.get("to")
        content = message.get("content")
        msg_prompt_id = message.get("prompt_id", prompt_id)
        timestamp = message.get("timestamp")
    else:
        role = getattr(message, "role", None) or getattr(message, "from_agent", None)
        to = getattr(message, "to", None) or getattr(message, "to_agent", None)
        content = getattr(message, "content", None)
        msg_prompt_id = getattr(message, "prompt_id", prompt_id)
        timestamp = getattr(message, "timestamp", None)

    if isinstance(timestamp, datetime):
        ts = timestamp.isoformat()
    else:
        ts = timestamp or datetime.utcnow().isoformat()

    data: Dict[str, Any] = {
        "timestamp": ts,
        "prompt_id": msg_prompt_id,
        "content": content,
    }
    if role is not None:
        data["role"] = role
    if to is not None:
        data["to"] = to
    return data


def save_conversation(
    title: str,
    messages: Sequence[Any],
    metadata: Dict[str, Any] | None,
    path: str | Path,
) -> Path:
    """Persist a conversation transcript to disk.

    Parameters
    ----------
    title:
        Title of the conversation.
    messages:
        Sequence of message objects or dictionaries.  Each entry should
        describe the speaker role, content and optional prompt id and
        timestamp.
    metadata:
        Additional metadata to store alongside the transcript.
    path:
        Base directory under which ``data/conversations`` will be
        created.

    Returns
    -------
    pathlib.Path
        Location of the written transcript file.
    """

    base = Path(path)
    convo_dir = base / "data" / "conversations"
    convo_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%S")
    filename = f"{timestamp}_{_sanitize_filename(title)}.json"
    file_path = convo_dir / filename

    payload = {
        "title": title,
        "created_at": datetime.utcnow().isoformat(),
        "metadata": metadata or {},
        "messages": [_serialise_message(m, i) for i, m in enumerate(messages, 1)],
    }

    file_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return file_path


def list_conversations(path: str | Path) -> List[Path]:
    """Return a sorted list of available transcript files."""

    convo_dir = Path(path) / "data" / "conversations"
    if not convo_dir.exists():
        return []
    return sorted(convo_dir.glob("*.json"))


def load_conversation(file_path: str | Path) -> Dict[str, Any]:
    """Load a single conversation transcript."""

    p = Path(file_path)
    return json.loads(p.read_text(encoding="utf-8"))


def load_conversations(path: str | Path) -> List[Dict[str, Any]]:
    """Load all conversation transcripts under *path*.

    Returns a list of dictionaries in chronological order based on the
    filenames (which contain timestamps).
    """

    transcripts = []
    for file in list_conversations(path):
        try:
            transcripts.append(load_conversation(file))
        except Exception:
            # Skip unreadable files rather than failing entirely
            continue
    return transcripts


__all__ = [
    "save_conversation",
    "list_conversations",
    "load_conversation",
    "load_conversations",
]
