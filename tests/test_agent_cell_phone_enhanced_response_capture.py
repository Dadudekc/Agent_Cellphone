import types
import pytest

import src.agent_cell_phone.enhanced_response_capture as erc
from src.agent_cell_phone.enhanced_response_capture import (
    EnhancedCaptureConfig,
    EnhancedResponseCapture,
)


@pytest.fixture
def config(tmp_path):
    return EnhancedCaptureConfig(
        file_watch_root=str(tmp_path / "files"),
        workflow_inbox=str(tmp_path / "wf"),
        fsm_inbox=str(tmp_path / "fsm"),
    )


def test_ocr_capture_returns_response(monkeypatch, config):
    coords = {"agent1": {"output_area": {"x": 1, "y": 2, "width": 3, "height": 4}}}
    captured = {}

    class FakePyAutoGUI:
        @staticmethod
        def screenshot(region):
            captured["region"] = region
            return "image"

    class FakePytesseract:
        @staticmethod
        def image_to_string(image):
            assert image == "image"
            return "hello"

    monkeypatch.setattr(erc, "pyautogui", FakePyAutoGUI)
    monkeypatch.setattr(erc, "pytesseract", FakePytesseract)
    monkeypatch.setattr(erc, "Image", object)

    capture = EnhancedResponseCapture(coords, config)
    response = capture._ocr_capture("agent1")

    assert captured["region"] == (1, 2, 3, 4)
    assert response is not None
    assert response.text == "hello"
    assert response.source == "ocr"


def test_ocr_capture_returns_none_when_empty(monkeypatch, config):
    coords = {"agent": {"output_area": {"x": 0, "y": 0, "width": 10, "height": 10}}}

    class FakePyAutoGUI:
        @staticmethod
        def screenshot(region):
            return "img"

    class FakePytesseract:
        @staticmethod
        def image_to_string(image):
            return "   "

    monkeypatch.setattr(erc, "pyautogui", FakePyAutoGUI)
    monkeypatch.setattr(erc, "pytesseract", FakePytesseract)
    monkeypatch.setattr(erc, "Image", object)

    capture = EnhancedResponseCapture(coords, config)
    assert capture._ocr_capture("agent") is None
