import json
import types
from pathlib import Path

import pytest

from src.services.enhanced_response_capture import (
    AIResponse,
    EnhancedCaptureConfig,
    EnhancedResponseCapture,
)


@pytest.fixture
def config(tmp_path):
    return EnhancedCaptureConfig(
        file_watch_root=str(tmp_path / "agents"),
        workflow_inbox=str(tmp_path / "workflow"),
        fsm_inbox=str(tmp_path / "fsm"),
    )


@pytest.fixture
def capture(config):
    return EnhancedResponseCapture(coords={}, config=config)


@pytest.fixture
def response_file(config):
    def _create(agent: str, text: str):
        agent_dir = Path(config.file_watch_root) / agent
        agent_dir.mkdir(parents=True, exist_ok=True)
        file = agent_dir / config.response_filename
        file.write_text(text, encoding="utf-8")
        return file

    return _create


@pytest.fixture
def clipboard_stub(monkeypatch):
    def _set(text: str):
        stub = types.SimpleNamespace(paste=lambda: text)
        monkeypatch.setattr(
            "src.services.enhanced_response_capture.pyperclip", stub
        )
        return stub

    return _set


def test_file_capture_reads_and_clears_file(capture, response_file):
    file = response_file("Agent-X", "hello world")
    response = capture._file_capture("Agent-X")
    assert response is not None
    assert response.text == "hello world"
    assert response.source == "file"
    assert file.read_text() == ""


def test_copy_response_capture(clipboard_stub, config):
    clipboard_stub("from clipboard")
    capture = EnhancedResponseCapture(coords={}, config=config)
    response = capture._copy_response_capture("Agent-Y")
    assert response is not None
    assert response.text == "from clipboard"
    assert response.source == "clipboard"


def test_route_outputs_create_json_envelopes(capture, config):
    resp_text = (
        "Task: Demo\nActions Taken:\n- step\nCommit Message: done\nStatus: ok\n"
    )
    response = AIResponse("Agent-Z", resp_text, 123.0, "file")
    response.analysis = {"foo": "bar"}
    capture._route_to_workflow(response)
    capture._route_to_fsm(response)

    wf_files = list(Path(config.workflow_inbox).glob("*.json"))
    fsm_files = list(Path(config.fsm_inbox).glob("*.json"))
    assert len(wf_files) == 1
    assert len(fsm_files) == 1

    wf_data = json.loads(wf_files[0].read_text())
    fsm_data = json.loads(fsm_files[0].read_text())
    assert wf_data["type"] == "ai_response"
    assert wf_data["agent"] == "Agent-Z"
    assert wf_data["payload"]["analysis"] == {"foo": "bar"}

    assert fsm_data["type"] == "agent_response"
    assert fsm_data["agent"] == "Agent-Z"
    assert fsm_data["payload"]["type"] == "agent_report"
    assert fsm_data["payload"]["task"] == "Demo"
    assert isinstance(fsm_data["payload"]["actions"], list)
    assert fsm_data["payload"]["status"] == "ok"
