#!/usr/bin/env python3
"""
Autonomous Standardization System
================================
Uses CAPTAIN + SWARM to ensure all PRDs and TASK_LIST files follow consistent formats.
"""

import time
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

from .autonomous_captain import AutonomousCaptain, CaptainTask
from .repository_activity_monitor import RepositoryActivityMonitor

@dataclass
class StandardizationTask:
    """Standardization task for repository files"""
    id: str
    repo_name: str
    file_type: str  # PRD, TASK_LIST, README, etc.
    current_format: str
    target_format: str
    priority: str
    status: str
    assigned_agent: Optional[str] = None
    created_at: float = None
    completed_at: Optional[float] = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = time.time()

class AutonomousStandardization:
    """Autonomous system for guiding agents to create standardized repository documents"""
    
    def __init__(self, repos_root: str = "D:/repos/Dadudekc"):
        self.repos_root = Path(repos_root)
        self.captain = AutonomousCaptain(repos_root)
        self.repo_monitor = RepositoryActivityMonitor(repos_root)
        self.standardization_tasks: List[StandardizationTask] = []
        self.state_file = Path("runtime/fsm/standardization_state.json")
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Standard formats
        self.standard_formats = {
            "PRD": self._get_standard_prd_format(),
            "TASK_LIST": self._get_standard_task_list_format(),
            "README": self._get_standard_readme_format()
        }
        
        # Load existing state
        self._load_state()
        
        # Initialize standardization tasks
        self._initialize_standardization_tasks()
    
    def _get_standard_prd_format(self) -> str:
        """Get standard PRD format"""
        return """# Project Requirements Document (PRD)

## 📋 Project Overview
- **Project Name**: [PROJECT_NAME]
- **Version**: [VERSION]
- **Last Updated**: [DATE]
- **Status**: [STATUS]

## 🎯 Objectives
- [Objective 1]
- [Objective 2]
- [Objective 3]

## 🚀 Features
### Core Features
- [Feature 1]
- [Feature 2]

### Future Features
- [Future Feature 1]
- [Future Feature 2]

## 📊 Requirements
### Functional Requirements
- [FR1] [Description]
- [FR2] [Description]

### Non-Functional Requirements
- [NFR1] [Description]
- [NFR2] [Description]

## 🔧 Technical Specifications
- **Language**: [LANGUAGE]
- **Framework**: [FRAMEWORK]
- **Database**: [DATABASE]

## 📅 Timeline
- **Phase 1**: [Dates] - [Description]
- **Phase 2**: [Dates] - [Description]
- **Phase 3**: [Dates] - [Description]

## ✅ Acceptance Criteria
- [AC1] [Description]
- [AC2] [Description]

## 🚨 Risks & Mitigation
- **Risk 1**: [Description] → [Mitigation]
- **Risk 2**: [Description] → [Mitigation]
"""
    
    def _get_standard_task_list_format(self) -> str:
        """Get standard TASK_LIST format"""
        return """# Task List

## 📋 Project: [PROJECT_NAME]
**Last Updated**: [DATE]
**Status**: [PROJECT_STATUS]

## 🎯 Current Sprint
### In Progress
- [ ] [Task 1] - [Description] - [Assignee] - [Due Date]
- [ ] [Task 2] - [Description] - [Assignee] - [Due Date]

### Completed
- [x] [Task 1] - [Description] - [Assignee] - [Completed Date]
- [x] [Task 2] - [Description] - [Assignee] - [Completed Date]

### Blocked
- [ ] [Task 1] - [Description] - [Assignee] - [Blocker Description]

## 🚀 Next Sprint
- [ ] [Task 1] - [Description] - [Assignee] - [Priority]
- [ ] [Task 2] - [Description] - [Assignee] - [Priority]

## 📊 Progress Metrics
- **Total Tasks**: [NUMBER]
- **Completed**: [NUMBER]
- **In Progress**: [NUMBER]
- **Blocked**: [NUMBER]
- **Completion Rate**: [PERCENTAGE]%

## 🔧 Technical Debt
- [ ] [Technical Debt Item 1]
- [ ] [Technical Debt Item 2]

## 📝 Notes
[Any additional notes or context]
"""
    
    def _get_standard_readme_format(self) -> str:
        """Get standard README format"""
        return """# [PROJECT_NAME]

## 📖 Description
[Brief project description]

## 🚀 Features
- [Feature 1]
- [Feature 2]
- [Feature 3]

## 🛠️ Installation
```bash
# Clone the repository
git clone [REPO_URL]

# Install dependencies
npm install
# or
pip install -r requirements.txt
```

## 📖 Usage
```bash
# Run the application
npm start
# or
python main.py
```

## 🧪 Testing
```bash
# Run tests
npm test
# or
pytest
```

## 📁 Project Structure
```
project/
├── src/
├── tests/
├── docs/
└── README.md
```

## 🤝 Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License
[LICENSE_TYPE] - See [LICENSE_FILE] for details

## 👥 Team
- [Team Member 1] - [Role]
- [Team Member 2] - [Role]
"""
    
    def _initialize_standardization_tasks(self):
        """Initialize standardization tasks for all repositories"""
        if not self.standardization_tasks:
            # Get all repositories
            all_repos = []
            for agent_repos in self.repo_monitor.agent_repos.values():
                all_repos.extend(agent_repos)
            
            # Remove duplicates
            unique_repos = list(set(all_repos))
            
            # Create standardization tasks for each repo
            for repo in unique_repos:
                if repo == "CAPTAIN":
                    continue
                    
                repo_path = self.repos_root / repo
                if repo_path.exists():
                    # Check for PRD files
                    prd_files = list(repo_path.glob("*PRD*"))
                    for prd_file in prd_files:
                        task = StandardizationTask(
                            id=f"prd-{repo}-{prd_file.stem}",
                            repo_name=repo,
                            file_type="PRD",
                            current_format="unknown",
                            target_format="standard",
                            priority="high",
                            status="pending"
                        )
                        self.standardization_tasks.append(task)
                    
                    # Check for TASK_LIST files
                    task_list_files = list(repo_path.glob("*TASK_LIST*"))
                    for task_file in task_list_files:
                        task = StandardizationTask(
                            id=f"tasklist-{repo}-{task_file.stem}",
                            repo_name=repo,
                            file_type="TASK_LIST",
                            current_format="unknown",
                            target_format="standard",
                            priority="high",
                            status="pending"
                        )
                        self.standardization_tasks.append(task)
                    
                    # Check for README files
                    readme_files = list(repo_path.glob("README*"))
                    for readme_file in readme_files:
                        task = StandardizationTask(
                            id=f"readme-{repo}-{readme_file.stem}",
                            repo_name=repo,
                            file_type="README",
                            current_format="unknown",
                            target_format="standard",
                            priority="medium",
                            status="pending"
                        )
                        self.standardization_tasks.append(task)
    
    def analyze_repository_standards(self, repo_name: str) -> Dict[str, any]:
        """Analyze standardization status of a repository"""
        repo_path = self.repos_root / repo_name
        if not repo_path.exists():
            return {"error": "Repository not found"}
        
        analysis = {
            "repo_name": repo_name,
            "timestamp": time.time(),
            "files": {},
            "compliance_score": 0,
            "total_files": 0,
            "compliant_files": 0
        }
        
        # Analyze PRD files
        prd_files = list(repo_path.glob("*PRD*"))
        for prd_file in prd_files:
            compliance = self._analyze_file_compliance(prd_file, "PRD")
            analysis["files"][prd_file.name] = compliance
            analysis["total_files"] += 1
            if compliance["is_compliant"]:
                analysis["compliant_files"] += 1
        
        # Analyze TASK_LIST files
        task_list_files = list(repo_path.glob("*TASK_LIST*"))
        for task_file in task_list_files:
            compliance = self._analyze_file_compliance(task_file, "TASK_LIST")
            analysis["files"][task_file.name] = compliance
            analysis["total_files"] += 1
            if compliance["is_compliant"]:
                analysis["compliant_files"] += 1
        
        # Analyze README files
        readme_files = list(repo_path.glob("README*"))
        for readme_file in readme_files:
            compliance = self._analyze_file_compliance(readme_file, "README")
            analysis["files"][readme_file.name] = compliance
            analysis["total_files"] += 1
            if compliance["is_compliant"]:
                analysis["compliant_files"] += 1
        
        # Calculate compliance score
        if analysis["total_files"] > 0:
            analysis["compliance_score"] = (analysis["compliant_files"] / analysis["total_files"]) * 100
        
        return analysis
    
    def _analyze_file_compliance(self, file_path: Path, file_type: str) -> Dict[str, any]:
        """Analyze if a file complies with standard format"""
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            
            # Basic compliance checks
            compliance = {
                "file_path": str(file_path),
                "file_type": file_type,
                "is_compliant": False,
                "issues": [],
                "suggestions": []
            }
            
            if file_type == "PRD":
                compliance.update(self._analyze_prd_compliance(content))
            elif file_type == "TASK_LIST":
                compliance.update(self._analyze_task_list_compliance(content))
            elif file_type == "README":
                compliance.update(self._analyze_readme_compliance(content))
            
            return compliance
            
        except Exception as e:
            return {
                "file_path": str(file_path),
                "file_type": file_type,
                "is_compliant": False,
                "issues": [f"Error reading file: {e}"],
                "suggestions": ["Check file permissions and encoding"]
            }
    
    def _analyze_prd_compliance(self, content: str) -> Dict[str, any]:
        """Analyze PRD compliance"""
        issues = []
        suggestions = []
        
        # Check for required sections
        required_sections = [
            "Project Overview", "Objectives", "Features", 
            "Requirements", "Technical Specifications", "Timeline"
        ]
        
        for section in required_sections:
            if section not in content:
                issues.append(f"Missing required section: {section}")
                suggestions.append(f"Add {section} section to PRD")
        
        # Check for project name placeholder
        if "[PROJECT_NAME]" in content:
            issues.append("Project name placeholder not filled")
            suggestions.append("Replace [PROJECT_NAME] with actual project name")
        
        # Check for date placeholders
        if "[DATE]" in content:
            issues.append("Date placeholder not filled")
            suggestions.append("Replace [DATE] with actual date")
        
        is_compliant = len(issues) == 0
        
        return {
            "is_compliant": is_compliant,
            "issues": issues,
            "suggestions": suggestions
        }
    
    def _analyze_task_list_compliance(self, content: str) -> Dict[str, any]:
        """Analyze TASK_LIST compliance"""
        issues = []
        suggestions = []
        
        # Check for required sections
        required_sections = ["Current Sprint", "Progress Metrics"]
        
        for section in required_sections:
            if section not in content:
                issues.append(f"Missing required section: {section}")
                suggestions.append(f"Add {section} section to TASK_LIST")
        
        # Check for task format
        if "- [ ]" not in content and "- [x]" not in content:
            issues.append("No task checkboxes found")
            suggestions.append("Use - [ ] for pending tasks and - [x] for completed tasks")
        
        # Check for project name placeholder
        if "[PROJECT_NAME]" in content:
            issues.append("Project name placeholder not filled")
            suggestions.append("Replace [PROJECT_NAME] with actual project name")
        
        is_compliant = len(issues) == 0
        
        return {
            "is_compliant": is_compliant,
            "issues": issues,
            "suggestions": suggestions
        }
    
    def _analyze_readme_compliance(self, content: str) -> Dict[str, any]:
        """Analyze README compliance"""
        issues = []
        suggestions = []
        
        # Check for required sections
        required_sections = ["Description", "Installation", "Usage"]
        
        for section in required_sections:
            if section not in content:
                issues.append(f"Missing required section: {section}")
                suggestions.append(f"Add {section} section to README")
        
        # Check for project name placeholder
        if "[PROJECT_NAME]" in content:
            issues.append("Project name placeholder not filled")
            suggestions.append("Replace [PROJECT_NAME] with actual project name")
        
        # Check for installation code blocks
        if "```bash" not in content and "```" not in content:
            issues.append("No code blocks found")
            suggestions.append("Add code blocks for installation and usage instructions")
        
        is_compliant = len(issues) == 0
        
        return {
            "is_compliant": is_compliant,
            "issues": issues,
            "suggestions": suggestions
        }
    
    def create_standardization_plan(self) -> str:
        """Create a comprehensive agent instruction plan"""
        plan = f"""
🎯 AUTONOMOUS AGENT INSTRUCTION PLAN
====================================
Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}

📊 OVERVIEW:
- Total Documents Needing Creation: {len(self.standardization_tasks)}
- High Priority: {len([t for t in self.standardization_tasks if t.priority == 'high'])}
- Medium Priority: {len([t for t in self.standardization_tasks if t.priority == 'medium'])}

🎯 PRIORITY ACTIONS:
"""
        
        # Group by priority
        high_priority = [t for t in self.standardization_tasks if t.priority == 'high']
        medium_priority = [t for t in self.standardization_tasks if t.priority == 'medium']
        
        plan += "\n🚨 HIGH PRIORITY (Instruct Agents First):\n"
        for task in high_priority[:5]:  # Top 5
            plan += f"- {task.repo_name}: {task.file_type} creation instruction\n"
        
        plan += "\n⚠️ MEDIUM PRIORITY:\n"
        for task in medium_priority[:5]:  # Top 5
            plan += f"- {task.repo_name}: {task.file_type} creation instruction\n"
        
        plan += """
🤖 EXECUTION STRATEGY:
1. CAPTAIN Agent-5 monitors documentation needs
2. System generates detailed agent instructions
3. Agents manually create documents using templates
4. Real-time monitoring tracks document quality

📋 NEXT STEPS:
1. Run compliance analysis on all repositories
2. Generate agent instructions for missing documents
3. Guide agents through manual document creation
4. Monitor document quality and consistency
"""
        
        return plan
    
    def execute_standardization_tasks(self, max_tasks: int = 3):
        """Execute standardization tasks using SWARM approach"""
        print(f"🤖 Executing standardization tasks (max: {max_tasks})")
        
        # Get high priority tasks
        high_priority = [t for t in self.standardization_tasks if t.priority == 'high' and t.status == 'pending']
        
        for task in high_priority[:max_tasks]:
            print(f"🎯 Instructing agent for: {task.repo_name} - {task.file_type}")
            
            # Generate agent instruction instead of automated creation
            instruction = self._generate_agent_instruction(task)
            print(f"📋 Instruction: {instruction}")
            
            # Mark as instruction sent
            task.status = "instruction_sent"
            task.completed_at = time.time()
            print(f"✅ Instruction sent for: {task.repo_name} - {task.file_type}")
        
        # Save state
        self._save_state()
    
    def _generate_agent_instruction(self, task: StandardizationTask) -> str:
        """Generate instruction for agent to manually create document"""
        if task.file_type == "PRD":
            return f"""📋 AGENT INSTRUCTION for {task.repo_name}:
            
1. 🔍 INSPECT THE REPOSITORY:
   - Review all source code files
   - Analyze existing documentation
   - Understand the project's purpose and scope
   - Identify key features and functionality

2. 📝 CREATE PROJECT REQUIREMENTS DOCUMENT (PRD):
   - Use the standard PRD template as a guide
   - Fill in [PROJECT_NAME] with "{task.repo_name}"
   - Add [DATE] with current date
   - Customize objectives based on what you discover
   - Document actual features found in the code
   - Specify technical requirements based on codebase
   - Set realistic timeline based on project complexity

3. 🎯 FOCUS ON ACCURACY:
   - Don't create generic content
   - Base everything on actual repository analysis
   - Ensure PRD reflects the real project state"""
        
        elif task.file_type == "TASK_LIST":
            return f"""📋 AGENT INSTRUCTION for {task.repo_name}:
            
1. 📖 REVIEW EXISTING DOCUMENTS:
   - Read the PRD you created
   - Review any existing roadmap
   - Understand the project's current state

2. 🗺️ CREATE ROADMAP (if not exists):
   - Break down the project into phases
   - Identify major milestones
   - Set realistic timelines
   - Consider dependencies between components

3. ✅ CREATE TASK LIST:
   - Use the standard TASK_LIST template as a guide
   - Fill in [PROJECT_NAME] with "{task.repo_name}"
   - Add [DATE] with current date
   - Create specific, actionable tasks
   - Assign realistic priorities
   - Estimate effort for each task
   - Link tasks to roadmap phases

4. 🎯 FOCUS ON SPECIFICITY:
   - Don't create generic "implement feature" tasks
   - Break down into concrete, verifiable actions
   - Base tasks on actual code analysis
   - Ensure tasks align with PRD objectives"""
        
        else:  # README
            return f"""📋 AGENT INSTRUCTION for {task.repo_name}:
            
1. 🔍 ANALYZE THE PROJECT:
   - Review the codebase structure
   - Understand installation requirements
   - Identify key usage patterns

2. 📝 CREATE COMPREHENSIVE README:
   - Use the standard README template as a guide
   - Fill in [PROJECT_NAME] with "{task.repo_name}"
   - Write actual project description based on code
   - Document real installation steps
   - Provide concrete usage examples
   - Include actual project structure

3. 🎯 FOCUS ON ACCURACY:
   - Don't use placeholder text
   - Base everything on actual repository content
   - Ensure README matches the real project"""
    
    def _customize_format(self, format_template: str, repo_name: str) -> str:
        """Customize format template for specific repository"""
        customized = format_template
        
        # Replace placeholders
        customized = customized.replace("[PROJECT_NAME]", repo_name)
        customized = customized.replace("[DATE]", time.strftime("%Y-%m-%d"))
        customized = customized.replace("[VERSION]", "1.0.0")
        customized = customized.replace("[STATUS]", "In Development")
        customized = customized.replace("[PROJECT_STATUS]", "Active")
        
        return customized
    
    def _save_state(self):
        """Save standardization state to disk"""
        try:
            state_data = {
                "timestamp": time.time(),
                "tasks": [task.__dict__ for task in self.standardization_tasks],
                "standardization_status": "active"
            }
            
            with self.state_file.open("w", encoding="utf-8") as f:
                json.dump(state_data, f, indent=2, default=str)
        except Exception as e:
            print(f"Failed to save standardization state: {e}")
    
    def _load_state(self):
        """Load standardization state from disk"""
        try:
            if self.state_file.exists():
                with self.state_file.open("r", encoding="utf-8") as f:
                    state_data = json.load(f)
                
                # Restore tasks
                if "tasks" in state_data:
                    self.standardization_tasks = [StandardizationTask(**task_dict) for task_dict in state_data["tasks"]]
        except Exception as e:
            print(f"Failed to load standardization state: {e}")
    
    def run_standardization_cycle(self):
        """Run one standardization cycle"""
        print("🤖 Autonomous Agent Instruction Cycle")
        print("=" * 50)
        
        # Analyze all repositories
        print("📊 Analyzing repository documentation needs...")
        all_repos = []
        for agent_repos in self.repo_monitor.agent_repos.values():
            all_repos.extend(agent_repos)
        
        unique_repos = list(set([r for r in all_repos if r != "CAPTAIN"]))
        
        total_compliance = 0
        for repo in unique_repos[:5]:  # Analyze top 5 repos
            analysis = self.analyze_repository_standards(repo)
            compliance_score = analysis.get("compliance_score", 0)
            total_compliance += compliance_score
            
            print(f"📁 {repo}: {compliance_score:.1f}% compliant")
        
        avg_compliance = total_compliance / len(unique_repos[:5]) if unique_repos[:5] else 0
        print(f"📊 Average Compliance: {avg_compliance:.1f}%")
        
        # Create instruction plan
        plan = self.create_standardization_plan()
        print("\n" + plan)
        
        # Generate agent instructions
        if avg_compliance < 80:  # If compliance is low
            print("🚨 Low compliance detected! Generating agent instructions...")
            self.execute_standardization_tasks(max_tasks=3)
        else:
            print("✅ High compliance maintained. No instructions needed.")
        
        # Save state
        self._save_state()
        
        print("✅ Agent instruction cycle completed")

def main():
    """Main agent instruction execution"""
    standardizer = AutonomousStandardization()
    
    try:
        standardizer.run_standardization_cycle()
    except KeyboardInterrupt:
        print("\n🛑 Agent instruction cycle interrupted by user")
    except Exception as e:
        print(f"❌ Agent instruction error: {e}")

if __name__ == "__main__":
    main()
