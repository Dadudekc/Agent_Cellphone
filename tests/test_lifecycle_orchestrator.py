import json
from unittest.mock import patch

from src.orchestrators.lifecycle_orchestrator import LifecycleOrchestrator
from src.services.agent_cell_phone import AgentCellPhone


def test_stage_budget_respected():
    phone = AgentCellPhone(test=True)
    with patch.object(phone, "send") as mock_send:
        orch = LifecycleOrchestrator("test", {}, phone)
        orch.run()
        stage1_calls = [c for c in mock_send.call_args_list if c.args[0] == "Agent-1"]
        stage2_calls = [c for c in mock_send.call_args_list if c.args[0] == "Agent-2"]
        assert len(stage1_calls) == 1
        assert len(stage2_calls) == 2


def test_gate_prevents_stage():
    phone = AgentCellPhone(test=True)
    with patch.object(phone, "send") as mock_send:
        orch = LifecycleOrchestrator("gated", {}, phone)
        orch.run()
        stage1_calls = [c for c in mock_send.call_args_list if c.args[0] == "Agent-1"]
        stage2_calls = [c for c in mock_send.call_args_list if c.args[0] == "Agent-2"]
        assert len(stage1_calls) == 0
        assert len(stage2_calls) == 2
