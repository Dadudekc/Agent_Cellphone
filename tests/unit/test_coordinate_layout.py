import json

import pytest

from src.core.utils.coordinate_finder import CoordinateFinder
from src.services import agent_cell_phone


def test_coordinate_finder_uses_mocked_config(tmp_path):
    coords = {
        "8-agent": {
            "Agent-1": {
                "input_box": {"x": 10, "y": 20},
                "starter_location_box": {"x": 1, "y": 2},
            },
            "Agent-2": {
                "input_box": {"x": 30, "y": 40}
            },
        }
    }
    cfg = tmp_path / "coords.json"
    cfg.write_text(json.dumps(coords))

    finder = CoordinateFinder(config_path=str(cfg))

    assert finder.get_input_box_location("agent-1") == (10, 20)
    assert finder.get_starter_location("agent-1") == (1, 2)
    assert finder.get_coordinates("agent-2") == (30, 40)


def test_agent_cell_phone_loads_layout_and_coordinates(monkeypatch, tmp_path):
    coord_data = {
        "2-agent": {
            "Agent-1": {"input_box": {"x": 1, "y": 2}},
            "Agent-2": {"input_box": {"x": 3, "y": 4}},
        },
        "8-agent": {
            "Agent-1": {"input_box": {"x": 10, "y": 20}},
        },
    }
    coord_file = tmp_path / "coords.json"
    coord_file.write_text(json.dumps(coord_data))

    mode_file = tmp_path / "modes.json"
    mode_file.write_text(json.dumps({"modes": {}}))

    monkeypatch.setattr(agent_cell_phone, "COORD_FILE", coord_file)
    monkeypatch.setattr(agent_cell_phone, "MODE_FILE", mode_file)

    acp = agent_cell_phone.AgentCellPhone(layout_mode="2-agent", test=True)

    assert acp.get_layout_mode() == "2-agent"
    assert set(acp.get_available_layouts()) == {"2-agent", "8-agent"}
    assert acp._coords["Agent-1"]["input_box"] == {"x": 1, "y": 2}
    assert acp._coords["Agent-2"]["input_box"] == {"x": 3, "y": 4}
