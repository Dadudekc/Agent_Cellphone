"""Discord webhook utilities.

Provides a helper to post embeds to a Discord webhook. The webhook URL and
optional channel ID are read from environment variables so the module can be
used across existing services without external dependencies.
"""
from __future__ import annotations

import json
import os
from typing import Dict, Any
from urllib import request, error

WEBHOOK_ENV = "DISCORD_WEBHOOK_URL"
CHANNEL_ENV = "DISCORD_CHANNEL_ID"


def _build_embed(title: str, fields: Dict[str, str]) -> Dict[str, Any]:
    """Construct a Discord embed payload."""
    return {
        "title": title,
        "fields": [
            {"name": name, "value": value, "inline": False}
            for name, value in fields.items()
        ],
    }


def post_embed(title: str, fields: Dict[str, str], *, webhook: str | None = None) -> None:
    """Post an embed to the configured Discord webhook.

    Parameters
    ----------
    title:
        Title for the embed.
    fields:
        Mapping of field names to values to include in the embed body.
    webhook:
        Optional override for the webhook URL. Falls back to
        ``DISCORD_WEBHOOK_URL`` if not provided.
    """
    url = webhook or os.getenv(WEBHOOK_ENV)
    if not url:
        raise RuntimeError(f"Discord webhook URL not set. Define {WEBHOOK_ENV}.")

    payload: Dict[str, Any] = {"embeds": [_build_embed(title, fields)]}
    channel_id = os.getenv(CHANNEL_ENV)
    if channel_id:
        payload["channel_id"] = channel_id

    data = json.dumps(payload).encode("utf-8")
    req = request.Request(url, data=data, headers={"Content-Type": "application/json"})
    try:
        with request.urlopen(req, timeout=10):
            pass
    except (error.HTTPError, error.URLError) as exc:
        raise RuntimeError(f"Failed to post Discord webhook: {exc}") from exc


__all__ = ["post_embed"]
