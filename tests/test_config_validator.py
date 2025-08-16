import json
import os
from pathlib import Path

import pytest

from src.config_validator import validate_config


def test_validate_config_success():
    assert validate_config()


def test_validate_config_missing_file(tmp_path, monkeypatch):
    missing_file = tmp_path / "missing.json"
    with pytest.raises(FileNotFoundError):
        validate_config([str(missing_file)])


def test_validate_config_invalid_json(tmp_path):
    invalid_file = tmp_path / "bad.json"
    invalid_file.write_text("{invalid}")
    with pytest.raises(ValueError):
        validate_config([str(invalid_file)])
