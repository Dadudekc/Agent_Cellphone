from __future__ import annotations

import os
import sys
import types
import tempfile
import threading
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


def test_start_runner_uses_project_relative_comms(monkeypatch):
    module = _load_gui_module()

    # Prepare temporary working directory
    temp_root = tempfile.mkdtemp(prefix="acp_runner_test_")
    comms_dir = Path(temp_root) / "communications"

    # Redirect CWD used by GUI logic
    monkeypatch.setattr(module.os, "getcwd", lambda: temp_root)

    # Capture popen arguments and prevent actual run
    captured: dict[str, object] = {}

    started = threading.Event()

    def fake_popen(args, cwd=None):  # noqa: ANN001
        captured["args"] = args
        captured["cwd"] = cwd
        started.set()
        class _N: ...
        return _N()

    monkeypatch.setattr(module.subprocess, "Popen", fake_popen)

    # Spin up GUI and invoke
    from PyQt5.QtWidgets import QApplication
    app = QApplication.instance() or QApplication(["test"])  # type: ignore
    win = module.FiveAgentGridGUI()  # type: ignore[attr-defined]
    try:
        win.start_fsm_runner()
        assert started.wait(timeout=1), "Runner thread did not start"

        # Validate communications directory and args
        assert comms_dir.exists(), "communications directory should be created relative to CWD"
        assert captured.get("cwd") == temp_root
        assert isinstance(captured.get("args"), list)
        assert "--comm-root" in captured["args"], "runner should receive --comm-root argument"
        # The provided path should be inside temp_root/communications
        comm_root_val = captured["args"][captured["args"].index("--comm-root") + 1]  # type: ignore[index]
        assert str(comms_dir) in str(comm_root_val)
    finally:
        win.close()


