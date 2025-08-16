import os
import sys
import types
from pathlib import Path

import pytest

# Ensure project root is on sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

# Stub pyautogui to avoid display/permissions issues in CI
sys.modules.setdefault("pyautogui", types.ModuleType("pyautogui"))


@pytest.mark.parametrize("module_path, main_callable", [
    ("src/gui/five_agent_grid_gui.py", "main"),
])
def test_gui_module_instantiates_qapplication(module_path: str, main_callable: str):
    """Smoke test: import GUI module and instantiate QApplication + main window, then exit.

    Runs headlessly by setting QT_QPA_PLATFORM=offscreen when available.
    """
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    gui_path = PROJECT_ROOT / module_path
    assert gui_path.exists(), f"GUI module not found: {gui_path}"

    # Import module dynamically
    import importlib.util

    spec = importlib.util.spec_from_file_location("_gui_under_test", str(gui_path))
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore

    # Create minimal app and window, then close
    from PyQt5.QtWidgets import QApplication

    app = QApplication.instance() or QApplication(["test"])  # type: ignore
    try:
        # Instantiate window
        window = module.FiveAgentGridGUI()  # type: ignore[attr-defined]
        window.show()
        # Process a few events
        for _ in range(5):
            app.processEvents()
        # Close window
        window.close()
    finally:
        app.quit()


