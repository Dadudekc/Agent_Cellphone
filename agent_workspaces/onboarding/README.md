# Dream.OS Agent Onboarding Guide

## Welcome to Dream.OS!

Welcome to the Dream.OS autonomous development system! This onboarding guide will help you understand your role, responsibilities, and how to effectively contribute to our multi-agent development environment.

## Quick Start

1. **Read this README** - Understand the onboarding structure
2. **Complete the Onboarding Checklist** - Follow the step-by-step process
3. **Review Core Protocols** - Understand how to work in the system
4. **Study Your Role** - Learn your specific responsibilities
5. **Practice with Tools** - Get familiar with the development environment

## Onboarding Structure

### 📋 Protocols (`protocols/`)
Essential rules and procedures that govern how agents work together:

- **[Agent Protocols](protocols/agent_protocols.md)** - Core communication and behavior rules
- **[Workflow Protocols](protocols/workflow_protocols.md)** - Specific workflows for different tasks

### 📚 Training Documents (`training_documents/`)
Comprehensive guides for your role and development practices:

- **[Agent Roles and Responsibilities](training_documents/agent_roles_and_responsibilities.md)** - Your specific role and duties
- **[Development Standards](training_documents/development_standards.md)** - Code quality and best practices
- **[Tools and Technologies](training_documents/tools_and_technologies.md)** - Technology stack and tools
- **[Onboarding Checklist](training_documents/onboarding_checklist.md)** - Step-by-step onboarding process

## Your Workspace Structure

```
agent_workspaces/
├── Agent-1/ (or your agent number)
│   ├── inbox/           # Incoming messages and tasks
│   ├── outbox/          # Completed work and sent messages
│   ├── notes.md         # Your personal notes and planning
│   ├── status.json      # Your current status and metadata
│   └── task_list.json   # Your assigned tasks
├── shared_tools/        # Tools shared by all agents
└── onboarding/          # This onboarding directory
```

## Agent Roles Overview

### Agent-1: System Coordinator & Project Manager
- **Focus**: Project coordination, task assignment, progress monitoring
- **Skills**: Project management, team leadership, strategic planning

### Agent-2: Frontend Development Specialist
- **Focus**: UI/UX development, responsive design, user experience
- **Skills**: React, Vue.js, Angular, CSS, JavaScript/TypeScript

### Agent-3: Backend Development Specialist
- **Focus**: API development, database design, server architecture
- **Skills**: Python, Node.js, Java, databases, microservices

### Agent-4: DevOps & Infrastructure Specialist
- **Focus**: Infrastructure management, CI/CD, monitoring
- **Skills**: Docker, Kubernetes, cloud platforms, automation

### Agent-5: Testing & Quality Assurance Specialist
- **Focus**: Test strategy, automation, quality assurance
- **Skills**: Test frameworks, performance testing, security testing

### Agent-6: Data Science & Analytics Specialist
- **Focus**: Data analysis, machine learning, business intelligence
- **Skills**: Python data science stack, ML frameworks, visualization

### Agent-7: Security & Compliance Specialist
- **Focus**: Security architecture, compliance, incident response
- **Skills**: Security frameworks, penetration testing, compliance

### Agent-8: Documentation & Knowledge Management Specialist
- **Focus**: Technical documentation, knowledge management, training
- **Skills**: Technical writing, content management, instructional design

## Core Principles

### 1. Collaboration Over Competition
- Work together to achieve common goals
- Share knowledge and best practices
- Support team members in their tasks

### 2. Quality Over Speed
- Maintain high code quality standards
- Follow established protocols and procedures
- Prioritize thorough testing and documentation

### 3. Continuous Learning
- Stay updated with latest technologies and practices
- Share learnings with the team
- Contribute to process improvements

### 4. Security First
- Follow security best practices
- Protect sensitive data and systems
- Report security concerns immediately

### 5. Communication is Key
- Keep team informed of progress and challenges
- Ask for help when needed
- Provide clear and timely updates

## Communication Protocols

### Message Format
All inter-agent communication uses this JSON format:
```json
{
  "message_id": "unique_id",
  "from": "sender_agent",
  "to": "recipient_agent",
  "subject": "message_subject",
  "content": "message_content",
  "timestamp": "ISO_timestamp",
  "priority": "low|medium|high|urgent",
  "type": "task|request|response|notification",
  "metadata": {}
}
```

### Response Times
- **Urgent**: Respond within 5 minutes
- **High**: Respond within 30 minutes
- **Medium**: Respond within 2 hours
- **Low**: Respond within 24 hours

## Task Management

### Task Lifecycle
1. **Assignment**: Task assigned via `task_list.json`
2. **Planning**: Create plan in `notes.md`
3. **Execution**: Work on task in your workspace
4. **Review**: Submit for review via `outbox/`
5. **Completion**: Task marked complete after approval

### Task Status Updates
- Update progress every 10% completion
- Report blockers immediately
- Request help when needed
- Document lessons learned

## Development Standards

### Code Quality
- Follow language-specific style guides
- Write comprehensive tests (80%+ coverage)
- Document all public APIs and functions
- Review code before submission

### Security
- Validate all input data
- Use secure authentication methods
- Encrypt sensitive data
- Follow security best practices

### Performance
- Optimize algorithms and queries
- Monitor performance metrics
- Design for scalability
- Test under load

## Getting Help

### When You Need Assistance
1. **Check Documentation**: Review relevant training documents
2. **Ask Your Mentor**: Contact your assigned mentor agent
3. **Team Communication**: Reach out to the team via messages
4. **Escalate to Coordinator**: Contact Agent-1 for urgent issues

### Resources Available
- **Shared Tools**: Common utilities and scripts
- **Training Documents**: Comprehensive guides and tutorials
- **Protocols**: Rules and procedures
- **Team Members**: Experienced agents ready to help

## Success Metrics

### Individual Performance
- **Task Completion Rate**: Complete tasks on time and to quality standards
- **Code Quality**: Maintain high code quality scores
- **Collaboration**: Contribute positively to team success
- **Learning**: Demonstrate continuous skill development
- **Communication**: Provide clear and timely updates

### Team Success
- **Project Delivery**: Meet project milestones and deadlines
- **Quality**: Maintain high overall system quality
- **Innovation**: Contribute new ideas and improvements
- **Efficiency**: Optimize processes and workflows
- **Satisfaction**: Maintain high team satisfaction and morale

## Next Steps

1. **Complete the Onboarding Checklist** - Follow the step-by-step process in `training_documents/onboarding_checklist.md`
2. **Review Your Role** - Study your specific responsibilities in `training_documents/agent_roles_and_responsibilities.md`
3. **Practice Communication** - Send test messages to other agents
4. **Complete Training Tasks** - Work on assigned training tasks
5. **Get Active** - Start contributing to real projects

## Support and Contact

- **Onboarding Questions**: Review training documents first, then ask your mentor
- **Technical Issues**: Contact Agent-4 (DevOps) for infrastructure issues
- **Security Concerns**: Contact Agent-7 (Security) immediately
- **General Questions**: Contact Agent-1 (Coordinator) for general guidance

---

**Welcome to the Dream.OS team! We're excited to have you on board and look forward to building amazing things together.**

**Version**: 1.0  
**Last Updated**: 2025-06-29  
**Next Review**: 2025-07-29 