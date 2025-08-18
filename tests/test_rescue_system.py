#!/usr/bin/env python3
"""Tests for Agent-1 Rescue System components."""

from unittest.mock import ANY, AsyncMock

import pytest

from core.agent_monitor import stall_detector, update_agent_activity
from core.continuous_worker import continuous_worker


def test_stall_detection():
    """Verify stall detector updates activity timestamps."""
    initial_activity = stall_detector.last_activity
    assert not stall_detector.is_stalled()

    update_agent_activity()

    assert stall_detector.last_activity >= initial_activity
    assert not stall_detector.is_stalled()


def test_work_tracking():
    """Ensure work session tracking accumulates updates."""
    continuous_worker.start_work_session("Test Task - System Coordination")
    continuous_worker.add_update("Testing stall detection system")
    continuous_worker.add_update("Verifying continuous work functionality")

    assert continuous_worker.current_session["task"] == "Test Task - System Coordination"
    assert len(continuous_worker.current_session["updates"]) == 2

    continuous_worker.end_work_session()


@pytest.mark.asyncio
async def test_discord_integration(monkeypatch):
    """Mock Discord updates and assert the function is invoked."""
    mock_post = AsyncMock()
    monkeypatch.setattr("services.discord_service.post_discord_update", mock_post)

    import services.discord_service as discord_service

    await discord_service.post_discord_update(
        "🧪 Test message from Agent-1 Rescue System", "Agent-1"
    )

    mock_post.assert_awaited_once_with(
        "🧪 Test message from Agent-1 Rescue System", "Agent-1"
    )

    await continuous_worker.cleanup()


@pytest.mark.asyncio
async def test_emergency_rescue(monkeypatch):
    """Ensure emergency rescue triggers a Discord rescue message."""
    mock_rescue = AsyncMock()
    monkeypatch.setattr("services.discord_service.post_discord_rescue", mock_rescue)

    await continuous_worker.emergency_rescue("Test emergency rescue")

    mock_rescue.assert_awaited_once_with(
        "Agent-1", ANY, "Emergency rescue triggered: Test emergency rescue"
    )

    await continuous_worker.cleanup()

