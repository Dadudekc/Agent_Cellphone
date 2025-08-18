from src.core.metadata_validator import validate_metadata
from src.core.status_aggregator import aggregate_agent_statuses
from src.core.status_persistence import load_agent_status, save_agent_status
from src.core.status_standardizer import standardize_agent_status


def test_status_standardization(tmp_path):
    sample_status = {
        "agent_id": "Agent-1",
        "status": "ACTIVE",
        "last_seen": "2025-08-16T10:00:00Z",
        "metadata": {
            "workspace": str(tmp_path / "project-A"),
            "cursor_version": "0.45.0",
        },
    }
    standardized = standardize_agent_status(sample_status)
    assert standardized["agent_id"] == "Agent-1"
    assert standardized["status"] == "active"
    assert standardized["last_seen"] == "2025-08-16T10:00:00Z"
    assert standardized["metadata"] == sample_status["metadata"]


def test_metadata_validation_valid(tmp_path):
    valid_metadata = {
        "workspace": str(tmp_path / "workspace"),
        "cursor_version": "0.45.0",
        "os": "Windows",
        "python_version": "3.11.0",
    }
    assert validate_metadata(valid_metadata)


def test_metadata_validation_invalid():
    invalid_metadata = {"workspace": "", "cursor_version": "invalid_version"}
    assert not validate_metadata(invalid_metadata)


def test_status_aggregation():
    agent_statuses = {
        "Agent-1": {"status": "active"},
        "Agent-2": {"status": "idle"},
        "Agent-3": {"status": "active"},
        "Agent-4": {"status": "offline"},
    }
    aggregated = aggregate_agent_statuses(agent_statuses)
    assert aggregated == {"active": 2, "idle": 1, "offline": 1, "total": 4}


def test_status_persistence(tmp_path):
    directory = tmp_path / "statuses"
    status = {
        "agent_id": "Test-Agent",
        "status": "testing",
        "last_seen": "2025-08-16T10:00:00Z",
        "metadata": {"test": True},
    }
    file = save_agent_status(status, directory)
    assert file.exists()
    loaded = load_agent_status("Test-Agent", directory)
    assert loaded == status


def test_full_standardization_workflow(tmp_path):
    agents = {
        "Agent-1": {
            "agent_id": "Agent-1",
            "status": "active",
            "last_seen": "2025-08-16T10:00:00Z",
            "metadata": {
                "workspace": str(tmp_path / "project-A"),
                "cursor_version": "0.45.0",
            },
        },
        "Agent-2": {
            "agent_id": "Agent-2",
            "status": "idle",
            "last_seen": "2025-08-16T09:55:00Z",
            "metadata": {
                "workspace": str(tmp_path / "project-B"),
                "cursor_version": "0.45.0",
            },
        },
    }

    standardized_agents = {}
    for agent_id, status in agents.items():
        standardized = standardize_agent_status(status)
        if validate_metadata(standardized.get("metadata", {})):
            standardized_agents[agent_id] = standardized

    aggregated = aggregate_agent_statuses(standardized_agents)
    assert aggregated["total"] == 2
    assert aggregated["active"] == 1
    assert aggregated["idle"] == 1
