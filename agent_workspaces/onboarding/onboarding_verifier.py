#!/usr/bin/env python3
"""
Onboarding Verification System for Dream.OS Agents
Validates agent onboarding completion and provides detailed feedback
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import subprocess
import sys

class OnboardingVerifier:
    """Enhanced onboarding verification system"""
    
    def __init__(self, agent_workspaces_dir: str = "agent_workspaces"):
        self.agent_workspaces_dir = Path(agent_workspaces_dir)
        self.onboarding_dir = self.agent_workspaces_dir / "onboarding"
    
    def get_agent_directories(self) -> List[Path]:
        """Get list of agent directories"""
        agent_dirs = []
        for item in self.agent_workspaces_dir.iterdir():
            if item.is_dir() and item.name.startswith("Agent-"):
                agent_dirs.append(item)
        return sorted(agent_dirs)
    
    def load_agent_status(self, agent_dir: Path) -> Optional[Dict[str, Any]]:
        """Load agent status.json"""
        status_file = agent_dir / "status.json"
        if status_file.exists():
            try:
                with open(status_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading status for {agent_dir.name}: {e}")
        return None
    
    def verify_onboarding_completion(self, agent_id: str) -> Dict[str, Any]:
        """Verify onboarding completion for a specific agent"""
        agent_dir = self.agent_workspaces_dir / agent_id
        if not agent_dir.exists():
            return {
                "agent_id": agent_id,
                "verification_passed": False,
                "error": "Agent directory not found",
                "details": {}
            }
        
        status = self.load_agent_status(agent_dir)
        if not status:
            return {
                "agent_id": agent_id,
                "verification_passed": False,
                "error": "Status file not found or invalid",
                "details": {}
            }
        
        # Check if onboarding section exists
        if "onboarding" not in status:
            return {
                "agent_id": agent_id,
                "verification_passed": False,
                "error": "No onboarding data found",
                "details": {}
            }
        
        onboarding = status["onboarding"]
        verification_result = {
            "agent_id": agent_id,
            "verification_passed": False,
            "error": None,
            "details": {
                "status": onboarding.get("status", "unknown"),
                "progress": onboarding.get("progress", 0.0),
                "checklist_completion": 0,
                "required_documents": [],
                "missing_documents": [],
                "capabilities_check": {},
                "performance_check": {},
                "health_check": {},
                "recommendations": []
            }
        }
        
        # Verify checklist completion
        checklist = onboarding.get("checklist", {})
        required_items = [
            "welcome_message", "system_overview", "communication_protocol",
            "roles_and_responsibilities", "best_practices", "getting_started",
            "troubleshooting", "quick_start", "status_update", "repository_push"
        ]
        
        completed_items = sum(1 for item in required_items if checklist.get(item, False))
        completion_rate = (completed_items / len(required_items)) * 100
        
        verification_result["details"]["checklist_completion"] = completion_rate
        
        # Check required documents
        documents_read = onboarding.get("documents_read", [])
        required_docs = [
            "ONBOARDING_GUIDE.md", "CORE_PROTOCOLS.md", "BEST_PRACTICES.md",
            "DEVELOPMENT_STANDARDS.md", "QUICK_START.md"
        ]
        
        verification_result["details"]["required_documents"] = required_docs
        verification_result["details"]["missing_documents"] = [
            doc for doc in required_docs if doc not in documents_read
        ]
        
        # Verify capabilities
        capabilities = status.get("capabilities", {})
        verification_result["details"]["capabilities_check"] = {
            "autonomous_mode": capabilities.get("autonomous_mode", False),
            "communication_enabled": capabilities.get("communication_enabled", True),
            "file_operations": capabilities.get("file_operations", True),
            "task_execution": capabilities.get("task_execution", True),
            "status_reporting": capabilities.get("status_reporting", True)
        }
        
        # Check performance metrics
        performance = status.get("performance", {})
        verification_result["details"]["performance_check"] = {
            "tasks_completed": performance.get("tasks_completed", 0),
            "messages_sent": performance.get("messages_sent", 0),
            "messages_received": performance.get("messages_received", 0),
            "uptime_hours": performance.get("uptime_hours", 0.0),
            "has_activity": performance.get("last_activity") is not None
        }
        
        # Check health status
        health = status.get("health", {})
        verification_result["details"]["health_check"] = {
            "status": health.get("status", "unknown"),
            "errors": health.get("errors", []),
            "warnings": health.get("warnings", [])
        }
        
        # Determine if verification passed
        passed_checks = []
        failed_checks = []
        
        # Check 1: Onboarding status should be "completed"
        if onboarding.get("status") == "completed":
            passed_checks.append("Onboarding status is completed")
        else:
            failed_checks.append(f"Onboarding status is '{onboarding.get('status')}', should be 'completed'")
        
        # Check 2: Progress should be 100%
        if onboarding.get("progress", 0) >= 100:
            passed_checks.append("Onboarding progress is 100%")
        else:
            failed_checks.append(f"Onboarding progress is {onboarding.get('progress', 0)}%, should be 100%")
        
        # Check 3: All checklist items should be completed
        if completion_rate >= 100:
            passed_checks.append("All checklist items completed")
        else:
            failed_checks.append(f"Checklist completion is {completion_rate}%, should be 100%")
        
        # Check 4: Verification should be marked as passed
        if onboarding.get("verification_passed", False):
            passed_checks.append("Verification marked as passed")
        else:
            failed_checks.append("Verification not marked as passed")
        
        # Check 5: Should have read required documents
        if len(verification_result["details"]["missing_documents"]) == 0:
            passed_checks.append("All required documents read")
        else:
            failed_checks.append(f"Missing documents: {verification_result['details']['missing_documents']}")
        
        # Check 6: Should have some activity
        if verification_result["details"]["performance_check"]["has_activity"]:
            passed_checks.append("Agent has activity history")
        else:
            failed_checks.append("No activity history found")
        
        # Check 7: Health should be good
        if health.get("status") == "healthy" and len(health.get("errors", [])) == 0:
            passed_checks.append("Agent health is good")
        else:
            failed_checks.append(f"Health issues: {health.get('status')}, errors: {health.get('errors', [])}")
        
        # Generate recommendations
        recommendations = []
        if onboarding.get("status") != "completed":
            recommendations.append("Complete onboarding process")
        
        if completion_rate < 100:
            recommendations.append("Complete all checklist items")
        
        if len(verification_result["details"]["missing_documents"]) > 0:
            recommendations.append("Read missing required documents")
        
        if not verification_result["details"]["capabilities_check"]["autonomous_mode"]:
            recommendations.append("Enable autonomous mode after onboarding")
        
        if not verification_result["details"]["performance_check"]["has_activity"]:
            recommendations.append("Perform initial tasks to establish activity")
        
        verification_result["details"]["recommendations"] = recommendations
        verification_result["passed_checks"] = passed_checks
        verification_result["failed_checks"] = failed_checks
        
        # Overall verification result
        verification_result["verification_passed"] = len(failed_checks) == 0
        
        if len(failed_checks) > 0:
            verification_result["error"] = f"Failed {len(failed_checks)} verification checks"
        
        return verification_result
    
    def verify_all_agents(self) -> Dict[str, Dict[str, Any]]:
        """Verify onboarding for all agents"""
        results = {}
        agent_dirs = self.get_agent_directories()
        
        print(f"Verifying onboarding for {len(agent_dirs)} agents...")
        
        for agent_dir in agent_dirs:
            agent_id = agent_dir.name
            results[agent_id] = self.verify_onboarding_completion(agent_id)
        
        return results
    
    def generate_verification_report(self, results: Dict[str, Dict[str, Any]]) -> str:
        """Generate a comprehensive verification report"""
        report = []
        report.append("=" * 60)
        report.append("DREAM.OS AGENT ONBOARDING VERIFICATION REPORT")
        report.append("=" * 60)
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # Summary
        total_agents = len(results)
        passed_agents = sum(1 for result in results.values() if result["verification_passed"])
        failed_agents = total_agents - passed_agents
        
        report.append("SUMMARY")
        report.append("-" * 20)
        report.append(f"Total Agents: {total_agents}")
        report.append(f"Passed Verification: {passed_agents}")
        report.append(f"Failed Verification: {failed_agents}")
        report.append(f"Success Rate: {(passed_agents/total_agents)*100:.1f}%")
        report.append("")
        
        # Detailed results
        report.append("DETAILED RESULTS")
        report.append("-" * 20)
        
        for agent_id, result in results.items():
            status = "✓ PASSED" if result["verification_passed"] else "✗ FAILED"
            report.append(f"{agent_id}: {status}")
            
            if not result["verification_passed"]:
                report.append(f"  Error: {result.get('error', 'Unknown error')}")
                report.append(f"  Progress: {result['details']['progress']:.1f}%")
                report.append(f"  Checklist: {result['details']['checklist_completion']:.1f}%")
                
                if result['details']['recommendations']:
                    report.append("  Recommendations:")
                    for rec in result['details']['recommendations']:
                        report.append(f"    - {rec}")
            
            report.append("")
        
        # Recommendations for system improvement
        report.append("SYSTEM RECOMMENDATIONS")
        report.append("-" * 20)
        
        if failed_agents > 0:
            report.append("1. Complete onboarding for failed agents")
            report.append("2. Review onboarding process for consistency")
            report.append("3. Implement automated onboarding verification")
            report.append("4. Add onboarding status to GUI dashboard")
        else:
            report.append("✓ All agents have completed onboarding successfully!")
            report.append("✓ System is ready for full autonomous operation")
        
        report.append("")
        report.append("=" * 60)
        
        return "\n".join(report)
    
    def update_verification_status(self, agent_id: str, passed: bool, notes: str = "") -> bool:
        """Update verification status in agent's status.json"""
        agent_dir = self.agent_workspaces_dir / agent_id
        status_file = agent_dir / "status.json"
        
        if not status_file.exists():
            return False
        
        try:
            with open(status_file, 'r') as f:
                status = json.load(f)
            
            if "onboarding" not in status:
                status["onboarding"] = {}
            
            status["onboarding"]["verification_passed"] = passed
            status["onboarding"]["verification_date"] = datetime.now().isoformat()
            status["onboarding"]["verification_notes"] = notes
            status["last_updated"] = datetime.now().isoformat()
            
            with open(status_file, 'w') as f:
                json.dump(status, f, indent=2)
            
            return True
            
        except Exception as e:
            print(f"Error updating verification status for {agent_id}: {e}")
            return False

def main():
    """Main function to run verification"""
    verifier = OnboardingVerifier()
    
    print("=== Dream.OS Onboarding Verification ===")
    
    # Verify all agents
    results = verifier.verify_all_agents()
    
    # Generate report
    report = verifier.generate_verification_report(results)
    
    # Print report
    print(report)
    
    # Save report to file
    report_file = verifier.onboarding_dir / "verification_report.txt"
    with open(report_file, 'w') as f:
        f.write(report)
    
    print(f"\nReport saved to: {report_file}")
    
    # Update verification status for all agents
    print("\nUpdating verification status...")
    for agent_id, result in results.items():
        success = verifier.update_verification_status(
            agent_id, 
            result["verification_passed"],
            f"Verification {'passed' if result['verification_passed'] else 'failed'}"
        )
        status = "✓" if success else "✗"
        print(f"{status} Updated {agent_id}")

if __name__ == "__main__":
    main() 