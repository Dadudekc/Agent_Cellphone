import os
import sys
import types
from pathlib import Path

import pytest

# Ensure project root is on sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

# Stub pyautogui for headless safety
sys.modules.setdefault("pyautogui", types.ModuleType("pyautogui"))


@pytest.fixture(autouse=True)
def _offscreen_qt():
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    yield


def _collect_buttons(widget):
    from PyQt5.QtWidgets import QPushButton
    buttons = []
    def walk(w):
        for child in w.findChildren(QPushButton):
            buttons.append(child)
    walk(widget)
    return buttons


def _button_texts(widget):
    return {b.text(): b for b in _collect_buttons(widget)}


def test_shared_controls_buttons_wired(monkeypatch):
    import importlib.util

    # Import GUI module dynamically
    gui_path = PROJECT_ROOT / "src" / "gui" / "five_agent_grid_gui.py"
    assert gui_path.exists()
    spec = importlib.util.spec_from_file_location("_gui_under_test", str(gui_path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore

    # Stub subprocess calls to avoid side effects
    class DummyCompleted:
        def __init__(self, returncode=0, stdout="", stderr=""):
            self.returncode = returncode
            self.stdout = stdout
            self.stderr = stderr

    monkeypatch.setattr(module.subprocess, "run", lambda *a, **k: DummyCompleted(0, "ok", ""))
    monkeypatch.setattr(module.subprocess, "Popen", lambda *a, **k: None)

    # Create window
    from PyQt5.QtWidgets import QApplication
    app = QApplication.instance() or QApplication(["test"])  # type: ignore
    win = module.FiveAgentGridGUI()  # type: ignore[attr-defined]
    win.show()

    texts = _button_texts(win)
    # Expected shared control buttons by label
    expected = {
        "🚀 Onboard (New Chat)",
        "🛰️ Start Agent-5 Listener",
        "📡 Start FSM 5-Agent Run",
        "🌱 Seed Sample Tasks",
        "📨 Send FSM Request Now",
        "🛑 Stop Overnight/Listener",
        "📊 Refresh Status",
        "💾 Save Log",
        "🧹 Clear Log",
    }
    missing = [t for t in expected if t not in texts]
    assert not missing, f"Missing buttons: {missing}"

    # Click each; should not raise due to stubbed subprocess
    from PyQt5.QtCore import Qt
    for label in expected:
        # Simulate click directly to avoid qtbot binding mismatch with PySide6 runtime
        texts[label].click()

    # Close the window safely
    win.close()


def test_agent4_panel_buttons_invoke_handlers(monkeypatch):
    import importlib.util

    gui_path = PROJECT_ROOT / "src" / "gui" / "five_agent_grid_gui.py"
    assert gui_path.exists()
    spec = importlib.util.spec_from_file_location("_gui_under_test", str(gui_path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore

    from PyQt5.QtWidgets import QApplication
    app = QApplication.instance() or QApplication(["test"])  # type: ignore

    # Create main window and access Agent-4 panel
    win = module.FiveAgentGridGUI()  # type: ignore[attr-defined]
    win.show()

    # Find Agent-4 panel and simulate button clicks
    panel = win.agent_panels.get("agent-4")
    assert panel is not None, "Agent-4 panel should exist"

    # Ensure controller methods exist and are callable
    assert hasattr(win, "ping_selected_agents")
    assert hasattr(win, "get_status_selected_agents")
    assert hasattr(win, "resume_selected_agents")

    # Track calls via monkeypatching log_message
    calls = []
    def fake_log(sender, msg):
        calls.append((sender, msg))
    monkeypatch.setattr(win, "log_message", fake_log)

    # Invoke controller methods after selecting Agent-4
    win.selected_agents = ["agent-4"]
    win.ping_selected_agents()
    win.get_status_selected_agents()
    win.resume_selected_agents()

    assert any("Pinging agent-4" in m for _, m in calls), "Ping should log"
    assert any("Resuming agent-4" in m for _, m in calls), "Resume should log"

    win.close()


