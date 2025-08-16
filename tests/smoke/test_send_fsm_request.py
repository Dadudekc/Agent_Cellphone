import os
import sys
import json
import types
import tempfile
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
    gui_path = PROJECT_ROOT / "src" / "gui" / "five_agent_grid_gui.py"
    assert gui_path.exists(), f"GUI file not found at {gui_path}"
    import importlib.util
    spec = importlib.util.spec_from_file_location("_gui_under_test", str(gui_path))
    module = importlib.util.module_from_spec(spec)
    assert spec is not None and spec.loader is not None
    spec.loader.exec_module(module)  # type: ignore[assignment]
    return module


def test_send_fsm_request_writes_inbox_file(monkeypatch):
    module = _load_gui_module()

    # Prepare temporary working directory to isolate filesystem effects
    temp_root = tempfile.mkdtemp(prefix="acp_gui_test_")
    agent_inbox = Path(temp_root) / "agent_workspaces" / "Agent-5" / "inbox"
    agent_inbox.mkdir(parents=True, exist_ok=True)

    # Force GUI code to use our temp directory as CWD
    monkeypatch.setenv("PYTEST_ACP_TEMP_ROOT", temp_root)
    monkeypatch.setattr(module.os, "getcwd", lambda: temp_root)

    # Create window and invoke the action
    from PyQt5.QtWidgets import QApplication
    app = QApplication.instance() or QApplication(["test"])  # type: ignore
    win = module.FiveAgentGridGUI()  # type: ignore[attr-defined]
    try:
        win.send_fsm_request()

        # Verify a file was created
        created = sorted(agent_inbox.glob("fsm_request_*.json"))
        assert created, "FSM request file was not created in Agent-5 inbox"

        # Validate JSON structure
        with open(created[-1], "r", encoding="utf-8") as f:
            data = json.load(f)

        # Minimal contract for FSM request payload
        assert data.get("type") == "fsm_request"
        assert data.get("from") == "Agent-3"
        assert data.get("to") == "Agent-5"
        assert isinstance(data.get("agents"), list) and data["agents"], "Agents list should be non-empty"
    finally:
        win.close()


