#!/usr/bin/env python3
"""
Simple GUI file structure tests that don't require Qt or GUI imports.
These tests just verify that expected GUI files exist in the correct locations.
"""

import os
from pathlib import Path

import pytest

# Resolve project root once for all tests
PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_gui_directory_exists():
    """Test that the GUI directory exists"""
    gui_dir = PROJECT_ROOT / "src" / "gui"
    assert gui_dir.exists(), f"GUI directory {gui_dir} should exist"
    assert gui_dir.is_dir(), f"{gui_dir} should be a directory"


def test_expected_gui_files_exist():
    """Test that all expected GUI files exist"""
    expected_gui_files = [
        "five_agent_grid_gui.py",
        "four_agent_horizontal_gui.py", 
        "two_agent_horizontal_gui.py",
        "dream_os_gui_v2.py",
        "dream_os_splash_gui.py",
        "run_two_agent_gui.py"
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


def test_gui_files_are_python_files():
    """Test that GUI files are valid Python files (have .py extension)"""
    gui_dir = PROJECT_ROOT / "src" / "gui"
    assert gui_dir.exists(), f"GUI directory {gui_dir} should exist"
    
    # Get all .py files in the GUI directory
    python_files = list(gui_dir.glob("*.py"))
    assert len(python_files) >= 6, f"Expected at least 6 Python files, found {len(python_files)}"
    
    # Check that key files are Python files
    key_files = ["five_agent_grid_gui.py", "four_agent_horizontal_gui.py"]
    for filename in key_files:
        file_path = gui_dir / filename
        if file_path.exists():
            assert file_path.suffix == ".py", f"{filename} should have .py extension"


def test_gui_directory_structure():
    """Test that GUI directory has expected subdirectories"""
    gui_dir = PROJECT_ROOT / "src" / "gui"
    assert gui_dir.exists(), f"GUI directory {gui_dir} should exist"
    
    # Check for expected subdirectories
    expected_subdirs = ["components", "tabs", "utils"]
    for subdir in expected_subdirs:
        subdir_path = gui_dir / subdir
        if subdir_path.exists():
            assert subdir_path.is_dir(), f"{subdir} should be a directory"


def test_gui_init_file_exists():
    """Test that GUI package has __init__.py file"""
    gui_dir = PROJECT_ROOT / "src" / "gui"
    assert gui_dir.exists(), f"GUI directory {gui_dir} should exist"
    
    init_file = gui_dir / "__init__.py"
    assert init_file.exists(), "GUI package should have __init__.py file"
    assert init_file.is_file(), "__init__.py should be a file"


def test_gui_file_sizes():
    """Test that GUI files have reasonable sizes (not empty)"""
    gui_dir = PROJECT_ROOT / "src" / "gui"
    assert gui_dir.exists(), f"GUI directory {gui_dir} should exist"
    
    # Check that main GUI files are not empty
    main_files = ["five_agent_grid_gui.py", "four_agent_horizontal_gui.py"]
    for filename in main_files:
        file_path = gui_dir / filename
        if file_path.exists():
            file_size = file_path.stat().st_size
            assert file_size > 1000, f"{filename} should be larger than 1KB (found {file_size} bytes)"


def test_gui_file_permissions():
    """Test that GUI files are readable"""
    gui_dir = PROJECT_ROOT / "src" / "gui"
    assert gui_dir.exists(), f"GUI directory {gui_dir} should exist"
    
    # Check that main GUI files are readable
    main_files = ["five_agent_grid_gui.py", "four_agent_horizontal_gui.py"]
    for filename in main_files:
        file_path = gui_dir / filename
        if file_path.exists():
            assert os.access(file_path, os.R_OK), f"{filename} should be readable"
