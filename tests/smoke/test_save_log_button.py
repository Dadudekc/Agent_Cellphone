from __future__ import annotations

import os
import sys
import types
import tempfile
import importlib.util
from pathlib import Path

import pytest


# Ensure project root is importable and run Qt offscreen
PROJECT_ROOT = Path(__file__).resolve().parents[2]
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Stub pyautogui for headless safety
sys.modules.setdefault("pyautogui", types.ModuleType("pyautogui"))


def _load_gui_module():
    gui_path = PROJECT_ROOT / "gui" / "five_agent_grid_gui.py"
    assert gui_path.exists(), f"GUI file not found at {gui_path}"
    spec = importlib.util.spec_from_file_location("_gui_under_test", str(gui_path))
    module = importlib.util.module_from_spec(spec)
    assert spec is not None and spec.loader is not None
    spec.loader.exec_module(module)  # type: ignore[assignment]
    return module


def test_save_log_button_writes_file(monkeypatch):
    module = _load_gui_module()

    # Prepare QApplication and window
    from PyQt5.QtWidgets import QApplication

    app = QApplication.instance() or QApplication(["test"])  # type: ignore
    win = module.FiveAgentGridGUI()  # type: ignore[attr-defined]
    win.show()

    # Seed the log with content that we can assert on
    sample_lines = [
        ("System", "Unit test line A"),
        ("Agent-1", "Unit test line B"),
    ]
    for sender, msg in sample_lines:
        win.log_message(sender, msg)

    # Use a real temporary filename but bypass file dialog interaction
    fd, tmp_path = tempfile.mkstemp(prefix="acp_log_", suffix=".txt")
    os.close(fd)  # We only need the path; the GUI will write the file

    def fake_get_save_file_name(*_args, **_kwargs):  # noqa: ANN001, ANN002
        return (tmp_path, "Text Files (*.txt)")

    from PyQt5 import QtWidgets
    monkeypatch.setattr(QtWidgets.QFileDialog, "getSaveFileName", fake_get_save_file_name)

    # Trigger the save action
    win.save_log()

    # Validate the file was written with expected content
    assert os.path.exists(tmp_path), "Save Log did not create the file"
    with open(tmp_path, "r", encoding="utf-8") as f:
        contents = f.read()

    for _sender, msg in sample_lines:
        assert msg in contents, "Saved log is missing expected content"

    # Cleanup and close
    try:
        os.remove(tmp_path)
    except OSError:
        pass
    win.close()


def test_clear_log_button_clears_log(monkeypatch):
    module = _load_gui_module()

    # Prepare QApplication and window
    from PyQt5.QtWidgets import QApplication

    app = QApplication.instance() or QApplication(["test"])  # type: ignore
    win = module.FiveAgentGridGUI()  # type: ignore[attr-defined]
    win.show()

    # Seed log
    win.log_message("System", "Line before clear")
    assert "Line before clear" in win.log_display.toPlainText()

    # Click Clear Log button
    from PyQt5.QtWidgets import QPushButton
    buttons = win.findChildren(QPushButton)
    clear_btn = next((b for b in buttons if b.text() == "🧹 Clear Log"), None)
    assert clear_btn is not None, "Clear Log button missing"
    clear_btn.click()

    # After clear, log should contain only the 'Log cleared' message (with timestamp)
    text = win.log_display.toPlainText()
    assert "Line before clear" not in text
    assert "Log cleared" in text

    win.close()


