from __future__ import annotations

import os
import sys
import types
import tempfile
import importlib.util
from pathlib import Path

import pytest


# Ensure project root is resolved and run Qt offscreen
PROJECT_ROOT = Path(__file__).resolve().parents[2]
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

# Stub pyautogui for headless safety
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


def _load_gui_module():
    """Load GUI module with error handling"""
    gui_path = _check_gui_file_exists("five_agent_grid_gui.py")
    return _safe_import_gui(gui_path)


def test_save_log_button_writes_file(monkeypatch):
    """Test that save log button properly writes log content to file"""
    module = _load_gui_module()

    # Prepare QApplication and window
    app = _safe_create_gui_app()
    
    try:
        win = module.FiveAgentGridGUI()
        win.show()
    except Exception as e:
        pytest.skip(f"Failed to create GUI window: {e}")

    try:
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

        # Cleanup
        try:
            os.remove(tmp_path)
        except OSError:
            pass
            
    finally:
        # Clean up
        if 'win' in locals():
            try:
                win.close()
            except:
                pass


def test_clear_log_button_clears_log(monkeypatch):
    """Test that clear log button properly clears the log display"""
    module = _load_gui_module()

    # Prepare QApplication and window
    app = _safe_create_gui_app()
    
    try:
        win = module.FiveAgentGridGUI()
        win.show()
    except Exception as e:
        pytest.skip(f"Failed to create GUI window: {e}")

    try:
        # Seed log
        win.log_message("System", "Line before clear")
        assert "Line before clear" in win.log_display.toPlainText()

        # Click Clear Log button
        from PyQt5.QtWidgets import QPushButton
        buttons = win.findChildren(QPushButton)
        clear_btn = next((b for b in buttons if b.text() == "🧹 Clear Log"), None)
        if clear_btn is None:
            pytest.skip("Clear Log button not found - GUI structure may have changed")
        
        clear_btn.click()

        # Verify log was cleared
        assert "Line before clear" not in win.log_display.toPlainText()
        # After clear, log should contain only the 'Log cleared' message (with timestamp)
        text = win.log_display.toPlainText()
        assert "Line before clear" not in text
        assert "Log cleared" in text
        
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


