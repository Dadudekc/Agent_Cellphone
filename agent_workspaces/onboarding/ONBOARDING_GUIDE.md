# 🚀 Dream.OS Onboarding Guide

## 📋 Overview
Complete onboarding process for new agents in the Dream.OS multi-agent system.

## 🎯 Onboarding Objectives
1. **System Familiarization**: Introduce agents to Dream.OS architecture
2. **Communication Setup**: Establish messaging protocols and channels
3. **Role Assignment**: Define agent responsibilities and capabilities
4. **Integration Testing**: Verify agent functionality within the system
5. **Performance Optimization**: Ensure optimal agent performance

## 🧭 Agent environment model (Cursor + shared repo)
- **Cursor-based agents**: Each agent is a Cursor instance with its own window. Messages sent via Agent Cell Phone (ACP) are mechanically typed into these Cursor input boxes using calibrated coordinates.
- **Shared repositories/files**: All agents work against the same checked-out repositories and file system. Treat edits as collaborative within a single workspace (no per-agent forks by default).
- **Messaging channels**:
  - Visible UI typing (ACP) to Cursor windows for synchronization and prompts
  - File inbox (JSON) for silent, scriptable messages into `agent_workspaces/Agent-N/inbox/`
- **Coordination artifacts**: Use each repo’s `TASK_LIST.md`, `status.json`, and (when present) `sprint_plan.json` to avoid duplication and track work.
- **Concurrency etiquette**: Pull latest before editing, prefer small, verifiable edits with tests/build checks, favor reuse/refactor over duplication, and stage/commit frequently.
- **Path conventions**: Run tools from `D:\Agent_Cellphone`. Project repositories typically live under `D:\repositories\...`; relative paths in prompts apply to the shared workspace.
- **Access scope**: Agents may open, modify, and create files anywhere in the shared repo unless otherwise restricted by role or policy.

## 📋 Pre-Onboarding Checklist

### System Requirements
- [ ] Python 3.8+ installed
- [ ] PyQt5 dependencies available
- [ ] Agent workspace directory created
- [ ] Coordinate mapping configured
- [ ] Network connectivity verified
 - [ ] Evidence folder created: `D:\\repositories\\communications\\overnight_YYYYMMDD_\\Agent-5\\`
 - [ ] Contracts file available: `D:\\repositories\\_agent_communications\\contracts.json`

### Agent Preparation
- [ ] Agent ID assigned (Agent-1 through Agent-8)
- [ ] Agent workspace initialized
- [ ] Agent capabilities documented
- [ ] Agent communication preferences set
- [ ] Agent security credentials configured

## 🚀 Onboarding Process

### Phase 1: System Introduction (Day 1)

#### 1.1 Welcome and Orientation (30 minutes)
- System overview presentation
- Architecture explanation
- Multi-agent collaboration benefits
- Success stories and use cases

#### 1.2 Technical Setup (45 minutes)
- Install required dependencies
- Configure agent workspace
- Set up communication channels
- Test basic connectivity

#### 1.3 Communication Protocol Training (60 minutes)
- Message format training
- Command structure explanation
- Broadcast vs. individual messaging
- Emergency protocols

### Phase 2: Role Integration (Day 2)

#### 2.1 Role Assignment (30 minutes)
- Role definition and scope
- Responsibility matrix creation
- Performance expectations
- Collaboration guidelines

#### 2.2 Workflow Integration (90 minutes)
- Workflow mapping
- Process documentation
- Integration points identification
- Handoff procedures

#### 2.3 Tool and Resource Access (45 minutes)
- Tool access configuration
- Resource allocation
- Permission setup
- Documentation access

### Phase 3: Testing and Validation (Day 3)

#### 3.1 Functional Testing (120 minutes)
- Individual agent testing
- Communication testing
- Command execution testing
- Error handling validation

#### 3.2 Integration Testing (90 minutes)
- Multi-agent communication testing
- Workflow integration testing
- Performance testing
- Stress testing

#### 3.3 User Acceptance Testing (60 minutes)
- User scenario testing
- Interface testing
- Usability validation
- Feedback collection

### Phase 4: Deployment and Monitoring (Day 4)

#### 4.1 Production Deployment (60 minutes)
- Production environment setup
- Configuration deployment
- Service activation
- Health check verification

#### 4.2 Monitoring Setup (45 minutes)
- Performance monitoring configuration
- Alert setup
- Logging configuration
- Dashboard access

#### 4.3 Performance Optimization (90 minutes)
- Performance baseline establishment
- Optimization opportunities identification
- Configuration tuning
- Best practices implementation

## 📊 Success Metrics

### Technical Metrics
- **Connectivity**: 100% successful message delivery
- **Response Time**: < 2 seconds for standard commands
- **Uptime**: 99.9% availability
- **Error Rate**: < 0.1% message failure rate

### Functional Metrics
- **Task Completion**: 95% successful task execution
- **Collaboration**: 90% effective multi-agent coordination
- **User Satisfaction**: 4.5/5 rating
- **Integration**: 100% workflow compatibility

### Operational Metrics
- **Onboarding Time**: < 4 days completion
- **Training Effectiveness**: 90% protocol adherence
- **Support Requests**: < 5 per week
- **Performance Improvement**: 20% efficiency gain

## 🔧 Troubleshooting Guide

### Common Issues

#### Connection Problems
- **Symptom**: Agent unable to send/receive messages
- **Solution**: Verify network connectivity and coordinate configuration
- **Prevention**: Regular connectivity testing

#### Performance Issues
- **Symptom**: Slow response times or message delays
- **Solution**: Optimize agent configuration and resource allocation
- **Prevention**: Regular performance monitoring

#### Integration Failures
- **Symptom**: Agent not functioning within workflows
- **Solution**: Review integration points and handoff procedures
- **Prevention**: Comprehensive testing before deployment

### Escalation Procedures

#### Level 1: Agent Self-Diagnosis
- Agent attempts self-recovery using built-in diagnostics
- Duration: 15 minutes maximum

#### Level 2: System Administrator
- System admin investigates and resolves issues
- Duration: 30 minutes maximum

#### Level 3: Development Team
- Development team provides technical support
- Duration: 2 hours maximum

## 📚 Training Resources

### Core Documentation
- **CORE_PROTOCOLS.md**: Essential protocols for all agents
- **QUICK_START.md**: Get started in 5 minutes
- **BEST_PRACTICES.md**: Best practices for success
- **DEVELOPMENT_STANDARDS.md**: Development guidelines

### Tools and Scripts
- **Main Launcher**: `../../main.py`
- **GUI Interface**: `../../gui/dream_os_gui_v2.py`
- **Agent Messenger**: `../../scripts/agent_messenger.py`
- **Test Harness**: `../../test_harness.py`
 - **Captain Quickstart**: `CAPTAIN_QUICKSTART.md`
 - **Evidence & Contracts**: `EVIDENCE_AND_CONTRACTS.md`

### Support Channels
- **System Administrator**: For technical issues
- **Training Team**: For training and development
- **Development Team**: For system improvements
- **Emergency**: Use emergency protocols

# Agent Communication: Canonical Method

All agents should use the CLI tool for communication and coordination:

```
python src/agent_cell_phone.py -a <TargetAgent> -m '<Your message>' -t <tag>
```

**Example:**
```
python src/agent_cell_phone.py -a Agent-2 -m 'Integration complete. Ready for next steps.' -t response
```

- This tool supports scripting for continuous, autonomous workflows.
- Refer to this section for all inter-agent messaging.

---

**Version**: 2.0 (Consolidated)  
**Last Updated**: 2025-06-29  
**Next Review**: 2025-07-29 