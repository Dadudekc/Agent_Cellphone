import shutil
from pathlib import Path
from types import SimpleNamespace

import pytest

try:
    import pytesseract
    from PIL import Image
except Exception:  # pragma: no cover - handled in skip
    pytesseract = None
    Image = None

if pytesseract is None or Image is None or not shutil.which("tesseract"):
    pytest.skip("OCR dependencies not available", allow_module_level=True)

import src.services.enhanced_response_capture as erc
from src.services.enhanced_response_capture import (
    EnhancedCaptureConfig,
    EnhancedResponseCapture,
    CaptureStrategy,
)


def test_ocr_capture_reads_text(monkeypatch):
    fixture = Path(__file__).parent / "fixtures" / "ocr_sample.pgm"
    coords = {"agent1": {"output_area": {"x": 0, "y": 0, "width": 100, "height": 40}}}
    config = EnhancedCaptureConfig(primary_strategy=CaptureStrategy.COPY_RESPONSE)

    # patch modules used by _ocr_capture
    fake_pyautogui = SimpleNamespace(screenshot=lambda region: Image.open(fixture))
    monkeypatch.setattr(erc, "pyautogui", fake_pyautogui)
    monkeypatch.setattr(erc, "pytesseract", pytesseract)
    monkeypatch.setattr(erc, "Image", Image)

    capture = EnhancedResponseCapture(coords, config)
    response = capture._ocr_capture("agent1")
    assert response is not None
    assert "TEST" in response.text.upper()
