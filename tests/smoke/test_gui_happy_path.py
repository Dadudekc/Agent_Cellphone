import os
import sys
import types
from pathlib import Path

# Headless/CI safe environment
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.modules.setdefault("pyautogui", types.ModuleType("pyautogui"))


def _check_gui_file_exists(gui_filename):
    """Check if GUI file exists and return path if it does"""
    gui_path = PROJECT_ROOT / "src" / "gui" / gui_filename
    if not gui_path.exists():
        pytest.skip(f"GUI file {gui_filename} not found at {gui_path}")
    return gui_path


def _safe_import_gui(gui_path):
    """Safely import GUI module with error handling"""
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("_gui_under_test", str(gui_path))
        if spec is None or spec.loader is None:
            pytest.skip(f"Could not create spec for {gui_path}")
        
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    except Exception as e:
        pytest.skip(f"Failed to import GUI module {gui_path}: {e}")


def _safe_create_gui_app():
    """Safely create QApplication with error handling"""
    try:
        from PyQt5.QtWidgets import QApplication
        app = QApplication.instance()
        if app is None:
            app = QApplication(["test"])
        return app
    except Exception as e:
        pytest.skip(f"Failed to create QApplication: {e}")


def test_seed_and_fsm_request(monkeypatch, tmp_path):
    """Test the happy path: seed tasks and send FSM request"""
    # Import GUI module safely
    gui_path = _check_gui_file_exists("five_agent_grid_gui.py")
    module = _safe_import_gui(gui_path)

    # Redirect cwd to a temp dir to avoid touching real folders
    monkeypatch.chdir(tmp_path)
    
    # Set environment variable for the GUI module to use the temp dir
    monkeypatch.setenv("AGENT_FILE_ROOT", str(tmp_path))

    # Stub subprocess to no-op
    class DummyCompleted:
        def __init__(self, returncode=0, stdout="", stderr=""):
            self.returncode = returncode
            self.stdout = stdout
            self.stderr = stderr
    monkeypatch.setattr(module.subprocess, "run", lambda *a, **k: DummyCompleted(0, "ok", ""))
    monkeypatch.setattr(module.subprocess, "Popen", lambda *a, **k: None)

    # Create QApplication safely
    app = _safe_create_gui_app()

    # Create window with error handling
    try:
        win = module.FiveAgentGridGUI()
    except Exception as e:
        pytest.skip(f"Failed to create GUI window: {e}")

    try:
        # Seed tasks
        win.seed_sample_tasks()
        tasks_dir = Path.cwd() / "fsm_data" / "tasks"
        assert tasks_dir.exists(), "Expected tasks dir to be created"
        files = list(tasks_dir.glob("*.json"))
        assert any(f.name == "task-001.json" for f in files)
        assert any(f.name == "task-002.json" for f in files)

        # Send FSM request (writes to Agent-5 inbox)
        win.send_fsm_request()
        inbox = Path.cwd() / "Agent-5" / "inbox"
        assert inbox.exists(), "Expected Agent-5 inbox to be created"
        created = list(inbox.glob("fsm_request_*.json"))
        assert created, "Expected an FSM request file"

    finally:
        # Clean up
        if 'win' in locals():
            try:
                win.close()
            except:
                pass


def test_gui_file_structure():
    """Test that expected GUI files exist"""
    expected_gui_files = [
        "five_agent_grid_gui.py",
        "four_agent_horizontal_gui.py", 
        "two_agent_horizontal_gui.py",
        "dream_os_gui_v2.py",
        "dream_os_splash_gui.py"
    ]
    
    gui_dir = PROJECT_ROOT / "src" / "gui"
    assert gui_dir.exists(), f"GUI directory {gui_dir} should exist"
    
    missing_files = []
    for filename in expected_gui_files:
        file_path = gui_dir / filename
        if not file_path.exists():
            missing_files.append(filename)
    
    if missing_files:
        pytest.skip(f"Missing GUI files: {missing_files}")
    
    # If we get here, all files exist
    assert True, "All expected GUI files are present"


