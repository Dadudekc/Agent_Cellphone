import os
import sys
import types
from pathlib import Path

# Headless/CI safe environment
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))
sys.modules.setdefault("pyautogui", types.ModuleType("pyautogui"))


def test_seed_and_fsm_request(monkeypatch, tmp_path):
    import importlib.util

    # Import GUI module dynamically
    gui_path = PROJECT_ROOT / "src" / "gui" / "five_agent_grid_gui.py"
    assert gui_path.exists()
    spec = importlib.util.spec_from_file_location("_gui_under_test", str(gui_path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore

    # Redirect cwd to a temp dir to avoid touching real folders
    monkeypatch.chdir(tmp_path)

    # Stub subprocess to no-op
    class DummyCompleted:
        def __init__(self, returncode=0, stdout="", stderr=""):
            self.returncode = returncode
            self.stdout = stdout
            self.stderr = stderr
    monkeypatch.setattr(module.subprocess, "run", lambda *a, **k: DummyCompleted(0, "ok", ""))
    monkeypatch.setattr(module.subprocess, "Popen", lambda *a, **k: None)

    from PyQt5.QtWidgets import QApplication
    app = QApplication.instance() or QApplication(["test"])  # type: ignore

    # Create window
    win = module.FiveAgentGridGUI()  # type: ignore[attr-defined]

    # Seed tasks
    win.seed_sample_tasks()
    tasks_dir = Path.cwd() / "fsm_data" / "tasks"
    assert tasks_dir.exists(), "Expected tasks dir to be created"
    files = list(tasks_dir.glob("*.json"))
    assert any(f.name == "task-001.json" for f in files)
    assert any(f.name == "task-002.json" for f in files)

    # Send FSM request (writes to Agent-5 inbox)
    win.send_fsm_request()
    inbox = Path.cwd() / "agent_workspaces" / "Agent-5" / "inbox"
    assert inbox.exists(), "Expected Agent-5 inbox to be created"
    created = list(inbox.glob("fsm_request_*.json"))
    assert created, "Expected an FSM request file"

    # Close
    win.close()


