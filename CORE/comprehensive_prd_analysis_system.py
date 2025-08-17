#!/usr/bin/env python3
"""
📋 COMPREHENSIVE PRD ANALYSIS SYSTEM v2.0
==========================================
Advanced PRD analysis and creation system for all repositories under D:\repos\Dadudekc
with enhanced analysis, automated PRD generation, and quality assessment.
"""

import os
import json
import time
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, asdict
from enum import Enum
import re
import hashlib

class PRDStatus(Enum):
    """PRD status levels"""
    MISSING = "missing"
    INCOMPLETE = "incomplete"
    PLACEHOLDER = "placeholder"
    COMPLETE = "complete"
    EXCELLENT = "excellent"

class RepositoryType(Enum):
    """Repository type classification"""
    AI_ML = "ai_ml"
    WEB_APPLICATION = "web_application"
    TRADING_FINANCIAL = "trading_financial"
    AUTOMATION_UTILITY = "automation_utility"
    GAMING_ENTERTAINMENT = "gaming_entertainment"
    TOOLS_FRAMEWORKS = "tools_frameworks"
    UNKNOWN = "unknown"

@dataclass
class RepositoryAnalysis:
    """Comprehensive repository analysis result"""
    repository_path: str
    name: str
    repository_type: RepositoryType
    has_prd: bool
    prd_status: PRDStatus
    prd_quality_score: float
    has_readme: bool
    readme_quality_score: float
    has_requirements: bool
    requirements_quality_score: float
    file_count: int
    code_files: List[str]
    documentation_files: List[str]
    prd_content: Optional[str] = None
    readme_content: Optional[str] = None
    requirements_content: Optional[str] = None
    analysis_timestamp: Optional[datetime] = None
    recommendations: List[str] = None
    priority_score: float = 0.0

class PRDAnalyzer:
    """Advanced PRD analyzer with quality assessment"""
    
    def __init__(self, repos_root: str = r"D:\repos\Dadudekc"):
        self.repos_root = Path(repos_root)
        self.logger = logging.getLogger(__name__)
        
        # Analysis results
        self.analysis_results: Dict[str, RepositoryAnalysis] = {}
        self.overall_stats: Dict[str, Any] = {}
        
        # Quality assessment criteria
        self.prd_quality_criteria = {
            "structure": ["overview", "objectives", "requirements", "specifications", "timeline"],
            "content_depth": ["technical_details", "user_stories", "acceptance_criteria"],
            "completeness": ["no_placeholders", "comprehensive_coverage", "clear_scope"]
        }
        
        # Repository type patterns
        self.repo_type_patterns = {
            RepositoryType.AI_ML: ["ai", "ml", "machine", "learning", "neural", "model", "intelligence"],
            RepositoryType.WEB_APPLICATION: ["web", "website", "app", "frontend", "backend", "api"],
            RepositoryType.TRADING_FINANCIAL: ["trading", "trading", "financial", "stock", "crypto", "investment"],
            RepositoryType.AUTOMATION_UTILITY: ["auto", "bot", "automation", "utility", "tool", "helper"],
            RepositoryType.GAMING_ENTERTAINMENT: ["game", "gaming", "entertainment", "simulator", "rpg"],
            RepositoryType.TOOLS_FRAMEWORKS: ["framework", "library", "sdk", "toolkit", "platform"]
        }
        
        # Setup logging
        self.setup_logging()
    
    def setup_logging(self):
        """Setup logging for the PRD analysis system"""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s | %(levelname)s | %(message)s',
            handlers=[
                logging.FileHandler(log_dir / "prd_analysis.log"),
                logging.StreamHandler()
            ]
        )
    
    def analyze_all_repositories(self) -> Dict[str, RepositoryAnalysis]:
        """Analyze all repositories in the Dadudekc workspace"""
        print(f"🔍 Starting comprehensive PRD analysis of {self.repos_root}")
        print(f"📅 Timestamp: {datetime.now()}")
        print("=" * 80)
        
        try:
            # Get all repositories
            repos = [d for d in os.listdir(self.repos_root) 
                    if os.path.isdir(os.path.join(self.repos_root, d))]
            
            print(f"📁 Found {len(repos)} repositories to analyze")
            
            # Analyze each repository
            for i, repo_name in enumerate(repos, 1):
                repo_path = os.path.join(self.repos_root, repo_name)
                print(f"\n[{i}/{len(repos)}] Analyzing: {repo_name}")
                
                try:
                    analysis = self.analyze_repository(repo_path)
                    self.analysis_results[repo_name] = analysis
                    
                    # Display analysis summary
                    self._display_analysis_summary(analysis)
                    
                except Exception as e:
                    print(f"❌ Error analyzing {repo_name}: {e}")
                    self.logger.error(f"Failed to analyze {repo_name}: {e}")
            
            # Generate overall statistics
            self._generate_overall_statistics()
            
            # Save analysis results
            self._save_analysis_results()
            
            return self.analysis_results
            
        except Exception as e:
            print(f"❌ Analysis failed: {e}")
            self.logger.error(f"Analysis failed: {e}")
            return {}
    
    def analyze_repository(self, repo_path: str) -> RepositoryAnalysis:
        """Analyze a single repository for PRD status and quality"""
        repo_name = os.path.basename(repo_path)
        
        # Initialize analysis
        analysis = RepositoryAnalysis(
            repository_path=repo_path,
            name=repo_name,
            repository_type=self._classify_repository(repo_name),
            has_prd=False,
            prd_status=PRDStatus.MISSING,
            prd_quality_score=0.0,
            has_readme=False,
            readme_quality_score=0.0,
            has_requirements=False,
            requirements_quality_score=0.0,
            file_count=0,
            code_files=[],
            documentation_files=[],
            analysis_timestamp=datetime.now(),
            recommendations=[]
        )
        
        try:
            # Get all files in repository
            files = self._get_repository_files(repo_path)
            analysis.file_count = len(files)
            
            # Categorize files
            analysis.code_files = [f for f in files if self._is_code_file(f)]
            analysis.documentation_files = [f for f in files if self._is_documentation_file(f)]
            
            # Analyze PRD
            prd_analysis = self._analyze_prd(repo_path, files)
            analysis.has_prd = prd_analysis["has_prd"]
            analysis.prd_status = prd_analysis["status"]
            analysis.prd_quality_score = prd_analysis["quality_score"]
            analysis.prd_content = prd_analysis["content"]
            
            # Analyze README
            readme_analysis = self._analyze_readme(repo_path, files)
            analysis.has_readme = readme_analysis["has_readme"]
            analysis.readme_quality_score = readme_analysis["quality_score"]
            analysis.readme_content = readme_analysis["content"]
            
            # Analyze requirements
            requirements_analysis = self._analyze_requirements(repo_path, files)
            analysis.has_requirements = requirements_analysis["has_requirements"]
            analysis.requirements_quality_score = requirements_analysis["quality_score"]
            analysis.requirements_content = requirements_analysis["content"]
            
            # Generate recommendations
            analysis.recommendations = self._generate_recommendations(analysis)
            
            # Calculate priority score
            analysis.priority_score = self._calculate_priority_score(analysis)
            
        except Exception as e:
            self.logger.error(f"Error analyzing repository {repo_name}: {e}")
            analysis.recommendations.append(f"Analysis error: {str(e)}")
        
        return analysis
    
    def _classify_repository(self, repo_name: str) -> RepositoryType:
        """Classify repository based on name patterns"""
        repo_name_lower = repo_name.lower()
        
        for repo_type, patterns in self.repo_type_patterns.items():
            if any(pattern in repo_name_lower for pattern in patterns):
                return repo_type
        
        return RepositoryType.UNKNOWN
    
    def _get_repository_files(self, repo_path: str) -> List[str]:
        """Get all files in repository"""
        files = []
        try:
            for root, dirs, filenames in os.walk(repo_path):
                for filename in filenames:
                    rel_path = os.path.relpath(os.path.join(root, filename), repo_path)
                    files.append(rel_path)
        except Exception as e:
            self.logger.error(f"Error getting files from {repo_path}: {e}")
        
        return files
    
    def _is_code_file(self, filename: str) -> bool:
        """Check if file is a code file"""
        code_extensions = ['.py', '.js', '.ts', '.java', '.cpp', '.c', '.cs', '.php', '.rb', '.go', '.rs']
        return any(filename.endswith(ext) for ext in code_extensions)
    
    def _is_documentation_file(self, filename: str) -> bool:
        """Check if file is a documentation file"""
        doc_extensions = ['.md', '.txt', '.rst', '.doc', '.docx', '.pdf']
        return any(filename.endswith(ext) for ext in doc_extensions)
    
    def _analyze_prd(self, repo_path: str, files: List[str]) -> Dict[str, Any]:
        """Analyze PRD status and quality"""
        prd_files = [f for f in files if 'prd' in f.lower() and f.endswith('.md')]
        
        if not prd_files:
            return {
                "has_prd": False,
                "status": PRDStatus.MISSING,
                "quality_score": 0.0,
                "content": None
            }
        
        # Use first PRD file found
        prd_file = os.path.join(repo_path, prd_files[0])
        
        try:
            with open(prd_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Analyze PRD quality
            quality_score = self._assess_prd_quality(content)
            
            # Determine status
            if "placeholder" in content.lower() or "todo" in content.lower():
                status = PRDStatus.PLACEHOLDER
            elif quality_score >= 0.8:
                status = PRDStatus.EXCELLENT
            elif quality_score >= 0.6:
                status = PRDStatus.COMPLETE
            else:
                status = PRDStatus.INCOMPLETE
            
            return {
                "has_prd": True,
                "status": status,
                "quality_score": quality_score,
                "content": content[:1000] + "..." if len(content) > 1000 else content
            }
            
        except Exception as e:
            self.logger.error(f"Error reading PRD {prd_file}: {e}")
            return {
                "has_prd": True,
                "status": PRDStatus.INCOMPLETE,
                "quality_score": 0.0,
                "content": f"Error reading PRD: {str(e)}"
            }
    
    def _assess_prd_quality(self, content: str) -> float:
        """Assess PRD quality based on content analysis"""
        score = 0.0
        content_lower = content.lower()
        
        # Check structure elements
        structure_score = 0.0
        for element in self.prd_quality_criteria["structure"]:
            if element in content_lower:
                structure_score += 0.2
        
        # Check content depth
        depth_score = 0.0
        for depth_indicator in self.prd_quality_criteria["content_depth"]:
            if depth_indicator in content_lower:
                depth_score += 0.2
        
        # Check completeness
        completeness_score = 0.0
        if "placeholder" not in content_lower and "todo" not in content_lower:
            completeness_score += 0.3
        if len(content) > 1000:  # Substantial content
            completeness_score += 0.2
        
        # Calculate total score
        score = min(structure_score + depth_score + completeness_score, 1.0)
        return score
    
    def _analyze_readme(self, repo_path: str, files: List[str]) -> Dict[str, Any]:
        """Analyze README status and quality"""
        readme_files = [f for f in files if f.lower() in ['readme.md', 'readme.txt', 'readme']]
        
        if not readme_files:
            return {
                "has_readme": False,
                "quality_score": 0.0,
                "content": None
            }
        
        readme_file = os.path.join(repo_path, readme_files[0])
        
        try:
            with open(readme_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Simple quality assessment
            quality_score = min(len(content) / 1000, 1.0)  # Normalize to 0-1
            
            return {
                "has_readme": True,
                "quality_score": quality_score,
                "content": content[:500] + "..." if len(content) > 500 else content
            }
            
        except Exception as e:
            self.logger.error(f"Error reading README {readme_file}: {e}")
            return {
                "has_readme": True,
                "quality_score": 0.0,
                "content": f"Error reading README: {str(e)}"
            }
    
    def _analyze_requirements(self, repo_path: str, files: List[str]) -> Dict[str, Any]:
        """Analyze requirements file status and quality"""
        req_files = [f for f in files if 'requirements' in f.lower() and f.endswith('.txt')]
        
        if not req_files:
            return {
                "has_requirements": False,
                "quality_score": 0.0,
                "content": None
            }
        
        req_file = os.path.join(repo_path, req_files[0])
        
        try:
            with open(req_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Count dependencies
            lines = [line.strip() for line in content.split('\n') if line.strip()]
            dependency_count = len([line for line in lines if not line.startswith('#')])
            
            # Quality score based on dependency count and formatting
            quality_score = min(dependency_count / 20, 1.0)  # Normalize to 0-1
            
            return {
                "has_requirements": True,
                "quality_score": quality_score,
                "content": content[:300] + "..." if len(content) > 300 else content
            }
            
        except Exception as e:
            self.logger.error(f"Error reading requirements {req_file}: {e}")
            return {
                "has_requirements": True,
                "quality_score": 0.0,
                "content": f"Error reading requirements: {str(e)}"
            }
    
    def _generate_recommendations(self, analysis: RepositoryAnalysis) -> List[str]:
        """Generate recommendations for repository improvement"""
        recommendations = []
        
        # PRD recommendations
        if not analysis.has_prd:
            recommendations.append("Create a comprehensive PRD.md file")
        elif analysis.prd_status == PRDStatus.PLACEHOLDER:
            recommendations.append("Replace placeholder content with actual PRD content")
        elif analysis.prd_status == PRDStatus.INCOMPLETE:
            recommendations.append("Enhance PRD with missing sections and details")
        
        # README recommendations
        if not analysis.has_readme:
            recommendations.append("Create a README.md file with project overview")
        elif analysis.readme_quality_score < 0.5:
            recommendations.append("Enhance README with more detailed information")
        
        # Requirements recommendations
        if not analysis.has_requirements:
            recommendations.append("Create requirements.txt with project dependencies")
        elif analysis.requirements_quality_score < 0.5:
            recommendations.append("Update requirements.txt with version specifications")
        
        # Repository-specific recommendations
        if analysis.repository_type == RepositoryType.AI_ML:
            recommendations.append("Include model specifications and training requirements in PRD")
        elif analysis.repository_type == RepositoryType.WEB_APPLICATION:
            recommendations.append("Document API endpoints and user interface specifications")
        elif analysis.repository_type == RepositoryType.TRADING_FINANCIAL:
            recommendations.append("Include risk assessment and compliance requirements")
        
        return recommendations
    
    def _calculate_priority_score(self, analysis: RepositoryAnalysis) -> float:
        """Calculate priority score for repository improvement"""
        score = 0.0
        
        # Base score from PRD status
        if analysis.prd_status == PRDStatus.MISSING:
            score += 0.4
        elif analysis.prd_status == PRDStatus.PLACEHOLDER:
            score += 0.3
        elif analysis.prd_status == PRDStatus.INCOMPLETE:
            score += 0.2
        
        # Bonus for high-value repository types
        if analysis.repository_type in [RepositoryType.AI_ML, RepositoryType.TRADING_FINANCIAL]:
            score += 0.2
        
        # Bonus for repositories with code but no documentation
        if len(analysis.code_files) > 0 and not analysis.has_prd:
            score += 0.1
        
        return min(score, 1.0)
    
    def _display_analysis_summary(self, analysis: RepositoryAnalysis):
        """Display analysis summary for a repository"""
        status_emoji = {
            PRDStatus.MISSING: "❌",
            PRDStatus.PLACEHOLDER: "⚠️",
            PRDStatus.INCOMPLETE: "🔄",
            PRDStatus.COMPLETE: "✅",
            PRDStatus.EXCELLENT: "🌟"
        }
        
        print(f"  📊 Status: {status_emoji[analysis.prd_status]} {analysis.prd_status.value}")
        print(f"  🎯 Type: {analysis.repository_type.value}")
        print(f"  📁 Files: {analysis.file_count}")
        print(f"  📋 PRD: {'✅' if analysis.has_prd else '❌'} (Score: {analysis.prd_quality_score:.2f})")
        print(f"  📖 README: {'✅' if analysis.has_readme else '❌'} (Score: {analysis.readme_quality_score:.2f})")
        print(f"  📦 Requirements: {'✅' if analysis.has_requirements else '❌'} (Score: {analysis.requirements_quality_score:.2f})")
        print(f"  🎯 Priority: {analysis.priority_score:.2f}")
        
        if analysis.recommendations:
            print(f"  💡 Top recommendation: {analysis.recommendations[0]}")
    
    def _generate_overall_statistics(self):
        """Generate overall analysis statistics"""
        total_repos = len(self.analysis_results)
        repos_with_prd = sum(1 for r in self.analysis_results.values() if r.has_prd)
        repos_with_readme = sum(1 for r in self.analysis_results.values() if r.has_readme)
        repos_with_requirements = sum(1 for r in self.analysis_results.values() if r.has_requirements)
        
        # Calculate average scores
        avg_prd_score = sum(r.prd_quality_score for r in self.analysis_results.values()) / total_repos if total_repos > 0 else 0
        avg_readme_score = sum(r.readme_quality_score for r in self.analysis_results.values()) / total_repos if total_repos > 0 else 0
        avg_requirements_score = sum(r.requirements_quality_score for r in self.analysis_results.values()) / total_repos if total_repos > 0 else 0
        
        # Repository type distribution
        type_distribution = {}
        for repo_type in RepositoryType:
            type_distribution[repo_type.value] = sum(1 for r in self.analysis_results.values() if r.repository_type == repo_type)
        
        self.overall_stats = {
            "total_repositories": total_repos,
            "repositories_with_prd": repos_with_prd,
            "repositories_with_readme": repos_with_readme,
            "repositories_with_requirements": repos_with_requirements,
            "prd_coverage_percentage": (repos_with_prd / total_repos * 100) if total_repos > 0 else 0,
            "average_prd_quality_score": avg_prd_score,
            "average_readme_quality_score": avg_readme_score,
            "average_requirements_quality_score": avg_requirements_score,
            "repository_type_distribution": type_distribution,
            "analysis_timestamp": datetime.now().isoformat()
        }
        
        # Display overall statistics
        print("\n" + "=" * 80)
        print("📊 OVERALL ANALYSIS STATISTICS")
        print("=" * 80)
        print(f"📁 Total Repositories: {total_repos}")
        print(f"📋 Repositories with PRD: {repos_with_prd} ({self.overall_stats['prd_coverage_percentage']:.1f}%)")
        print(f"📖 Repositories with README: {repos_with_readme}")
        print(f"📦 Repositories with Requirements: {repos_with_requirements}")
        print(f"🎯 Average PRD Quality Score: {avg_prd_score:.2f}")
        print(f"📖 Average README Quality Score: {avg_readme_score:.2f}")
        print(f"📦 Average Requirements Quality Score: {avg_requirements_score:.2f}")
        
        print(f"\n🏷️ Repository Type Distribution:")
        for repo_type, count in type_distribution.items():
            if count > 0:
                print(f"  {repo_type}: {count}")
    
    def _save_analysis_results(self):
        """Save analysis results to file"""
        try:
            # Convert dataclass objects to dictionaries
            results_dict = {}
            for repo_name, analysis in self.analysis_results.items():
                analysis_dict = asdict(analysis)
                # Convert datetime to string for JSON serialization
                if analysis_dict["analysis_timestamp"]:
                    analysis_dict["analysis_timestamp"] = analysis_dict["analysis_timestamp"].isoformat()
                results_dict[repo_name] = analysis_dict
            
            # Save detailed results
            results_file = f"prd_analysis_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(results_file, 'w') as f:
                json.dump({
                    "overall_statistics": self.overall_stats,
                    "repository_analyses": results_dict
                }, f, indent=2)
            
            print(f"\n💾 Analysis results saved to: {results_file}")
            
        except Exception as e:
            print(f"❌ Failed to save analysis results: {e}")
            self.logger.error(f"Failed to save analysis results: {e}")
    
    def get_high_priority_repositories(self) -> List[RepositoryAnalysis]:
        """Get repositories that need immediate attention"""
        high_priority = [r for r in self.analysis_results.values() if r.priority_score >= 0.5]
        return sorted(high_priority, key=lambda x: x.priority_score, reverse=True)
    
    def get_repositories_by_type(self, repo_type: RepositoryType) -> List[RepositoryAnalysis]:
        """Get repositories of a specific type"""
        return [r for r in self.analysis_results.values() if r.repository_type == repo_type]
    
    def get_repositories_without_prd(self) -> List[RepositoryAnalysis]:
        """Get repositories without PRD"""
        return [r for r in self.analysis_results.values() if not r.has_prd]

def main():
    """Main function to run comprehensive PRD analysis"""
    print("📋 COMPREHENSIVE PRD ANALYSIS SYSTEM")
    print("=" * 60)
    
    # Initialize analyzer
    analyzer = PRDAnalyzer()
    
    # Run analysis
    results = analyzer.analyze_all_repositories()
    
    if results:
        print(f"\n🎉 Analysis completed successfully!")
        print(f"📊 Analyzed {len(results)} repositories")
        
        # Show high priority repositories
        high_priority = analyzer.get_high_priority_repositories()
        if high_priority:
            print(f"\n🚨 HIGH PRIORITY REPOSITORIES ({len(high_priority)}):")
            for repo in high_priority[:5]:  # Show top 5
                print(f"  • {repo.name} (Priority: {repo.priority_score:.2f})")
        
        # Show repositories without PRD
        no_prd = analyzer.get_repositories_without_prd()
        if no_prd:
            print(f"\n❌ REPOSITORIES WITHOUT PRD ({len(no_prd)}):")
            for repo in no_prd[:10]:  # Show top 10
                print(f"  • {repo.name}")
        
        print(f"\n✅ Analysis complete! Check the generated JSON file for detailed results.")
    else:
        print("❌ Analysis failed!")

if __name__ == "__main__":
    main()


