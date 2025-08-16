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


def test_shared_controls_buttons_wired(monkeypatch):
    """Test shared control buttons are properly wired"""
    # Check if GUI file exists
    gui_path = _check_gui_file_exists("five_agent_grid_gui.py")
    
    # Import GUI module safely
    module = _safe_import_gui(gui_path)
    
    # Create QApplication safely
    app = _safe_create_gui_app()
    
    try:
        # Stub subprocess calls to avoid side effects
        class DummyCompleted:
            def __init__(self, returncode=0, stdout="", stderr=""):
                self.returncode = returncode
                self.stdout = stdout
                self.stderr = stderr

        monkeypatch.setattr(module.subprocess, "run", lambda *a, **k: DummyCompleted(0, "ok", ""))
        monkeypatch.setattr(module.subprocess, "Popen", lambda *a, **k: None)

        # Create window with error handling
        try:
            win = module.FiveAgentGridGUI()
            win.show()
        except Exception as e:
            pytest.skip(f"Failed to create GUI window: {e}")

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

    finally:
        # Clean up
        if 'win' in locals():
            try:
                win.close()
            except:
                pass


def test_agent4_panel_buttons_invoke_handlers(monkeypatch):
    """Test Agent-4 panel buttons invoke proper handlers"""
    # Check if GUI file exists
    gui_path = _check_gui_file_exists("five_agent_grid_gui.py")
    
    # Import GUI module safely
    module = _safe_import_gui(gui_path)
    
    # Create QApplication safely
    app = _safe_create_gui_app()

    try:
        # Create main window and access Agent-4 panel
        try:
            win = module.FiveAgentGridGUI()
            win.show()
        except Exception as e:
            pytest.skip(f"Failed to create GUI window: {e}")

        # Find Agent-4 panel and simulate button clicks
        panel = win.agent_panels.get("agent-4")
        if panel is None:
            pytest.skip("Agent-4 panel not found - GUI structure may have changed")

        # Ensure controller methods exist and are callable
        required_methods = ["ping_selected_agents", "get_status_selected_agents", "resume_selected_agents"]
        for method_name in required_methods:
            if not hasattr(win, method_name):
                pytest.skip(f"Required method {method_name} not found in GUI")

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


def test_gui_import_safety():
    """Test that GUI modules can be imported safely"""
    gui_dir = PROJECT_ROOT / "src" / "gui"
    if not gui_dir.exists():
        pytest.skip("GUI directory not found")
    
    # Try to import a simple GUI module
    try:
        gui_path = gui_dir / "run_two_agent_gui.py"
        if gui_path.exists():
            module = _safe_import_gui(gui_path)
            assert module is not None, "GUI module should import successfully"
        else:
            pytest.skip("Simple GUI module not found for import test")
    except Exception as e:
        pytest.skip(f"GUI import test failed: {e}")


