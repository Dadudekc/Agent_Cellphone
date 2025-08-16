#!/usr/bin/env python3
"""Simple lifecycle orchestrator for AgentCellPhone stages.

Loads runtime configuration from ``runtime/config/modes_runtime.json`` and
iterates through the common stages for a given mode.  Each stage specifies the
agent that should run it, how many iterations (``budget``) to allow, and an
optional gate check that determines whether the stage should run at all.

The orchestrator integrates with :mod:`agent_cell_phone` to execute the stages
by sending messages to the appropriate agents.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

from agent_cell_phone import AgentCellPhone
from src.core.config_loader import load_config

# ---------------------------------------------------------------------------
# Gate check registry
GateFn = Callable[[Dict[str, Any]], bool]


def _gate_pass(_: Dict[str, Any]) -> bool:
    return True


def _gate_fail(_: Dict[str, Any]) -> bool:
    return False


GATES: Dict[str, GateFn] = {
    "pass": _gate_pass,
    "fail": _gate_fail,
}


class LifecycleOrchestrator:
    """Orchestrate execution of common stages for a specific mode."""

    def __init__(self, mode: str, ctx: Optional[Dict[str, Any]] = None,
                 phone: Optional[AgentCellPhone] = None) -> None:
        self.mode = mode
        self.ctx: Dict[str, Any] = ctx or {}
        self.phone = phone or AgentCellPhone(test=True)
        self.config = self._load_config()

    # ------------------------------------------------------------------ utils
    @staticmethod
    def _config_path() -> Path:
        repo_root = Path(load_config()["paths"]["repo_root"])
        return repo_root / "runtime" / "config" / "modes_runtime.json"

    def _load_config(self) -> Dict[str, Any]:
        cfg_path = self._config_path()
        with open(cfg_path, "r", encoding="utf-8") as fh:
            return json.load(fh)

    # ----------------------------------------------------------------- running
    def run(self) -> None:
        stages: List[str] = self.config.get("stages", [])
        mode_cfg: Dict[str, Any] = self.config.get("modes", {}).get(self.mode, {})
        for stage in stages:
            spec = mode_cfg.get(stage)
            if not spec:
                continue
            gate_name = spec.get("gate", "pass")
            gate_fn = GATES.get(gate_name, _gate_pass)
            if not gate_fn(self.ctx):
                continue
            agent = spec.get("agent")
            budget = int(spec.get("budget", 1))
            for _ in range(budget):
                self.phone.send(agent, f"Executing {stage}")


# ---------------------------------------------------------------------------
def main(argv: Optional[List[str]] = None) -> None:
    parser = argparse.ArgumentParser(description="Lifecycle orchestrator")
    parser.add_argument("--mode", required=True, help="Mode from modes_runtime.json")
    parser.add_argument("--ctx", default="{}", help="JSON string with context")
    args = parser.parse_args(argv)
    ctx = json.loads(args.ctx)
    orchestrator = LifecycleOrchestrator(args.mode, ctx)
    orchestrator.run()


if __name__ == "__main__":
    main()
