# Autonomous Modes

This guide summarizes the autonomous operating modes used by Agent Cell Phone and how tasks move through the system.

## Modes
- **2, 4, or 8 Agent Layouts** – GUI selections allow small or large collaborations.
- **5‑Agent Overnight Runner** – orchestrates contracts and FSM updates for continuous hands‑off operation.

## Pipelines
1. **Message Pipeline** – lightweight in‑memory queue for routing messages between agents.
2. **FSM Orchestrator** – consumes inbox updates, maintains task state, and emits verification messages.
3. **Overnight Runner** – polls tasks, executes guard commands, and advances states.

## Guardrails
- Guard commands in `config/fsm.yml` enforce linting, tests, and deployment checks before transitions.
- Non‑actionable states remain parked until prerequisites are met, preventing accidental progress.
- Output from guard commands is truncated to keep artifacts within budget.

## Discord Command Usage
- Commands follow `@agent-x <command>` syntax (`@all`, `@self` are also supported).
- Set `DISCORD_WEBHOOK_URL` to broadcast digests and task status to a shared channel.
