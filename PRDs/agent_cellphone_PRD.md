# Agent Cellphone - Product Requirements Document

## Overview
Agent Cellphone (ACP) is a multi-agent communication layer enabling Cursor agents to coordinate tasks through a shared messaging system. The project aims to provide reliable messaging, intuitive user interfaces, and forthcoming listener loop capabilities.

## Goals
- Implement bidirectional message delivery between agents.
- Provide desktop and web GUIs for monitoring and command control.
- Support flexible layouts for different numbers of agents.
- Ensure system extensibility and comprehensive documentation.

## Non-Goals
- Cross-language support outside the Python ecosystem.
- External network communication beyond the local environment.
- Advanced AI reasoning beyond message relay and coordination.

## User Stories
- As an agent developer, I can send and receive messages between agents to coordinate work.
- As a team lead, I can monitor agent activity and restart or synchronize agents from the GUI.
- As a tester, I can run demo and diagnostic modes to validate the system.

## Functional Requirements
- Parsing messages using the `@agent-x <COMMAND> <ARGS>` protocol.
- Layout management for 2, 4, and 8 agent configurations.
- Listener loop for incoming messages with OCR detection.
- Command router supporting resume, sync, and restart commands.
- Message processing pipeline with queue management.

## Non-Functional Requirements
- Message delivery within 500 ms.
- Detection accuracy greater than 95%.
- Documentation covering setup, usage, and troubleshooting.
- Extensible architecture to support additional agents and commands.

## Milestones
1. **Phase 1 – MVP Communication Layer** (Completed)
2. **Phase 2 – Listener Loop** (In Progress)
3. **Phase 3 – Robustness Enhancements** (Planned)
4. **Phase 4 – Logging & Debug Panel** (Future)

## Success Metrics
- Message delivery rate of 100%.
- Listener detection accuracy >95%.
- Command routing response <500 ms.
- Uptime >99.5% during production.

## Open Questions
- How will multi-platform support be handled?
- What security model is required for cross-host communication?

## Dependencies
- Python 3.10+
- PyAutoGUI, OCR libraries

*Last Updated: August 22, 2025*
