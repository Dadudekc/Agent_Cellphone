#!/usr/bin/env python3
"""
Comprehensive PRD Analysis Script
Analyzes all repositories in the Dadudekc workspace for PRD status
"""

import os
import json
from pathlib import Path
from datetime import datetime

def analyze_repository(repo_path):
    """Analyze a single repository for PRD status"""
    repo_name = os.path.basename(repo_path)
    analysis = {
        "repository": repo_path,
        "name": repo_name,
        "has_prd": False,
        "has_readme": False,
        "has_requirements": False,
        "prd_status": "NOT_FOUND",
        "readme_status": "NOT_FOUND",
        "requirements_status": "NOT_FOUND",
        "files": [],
        "prd_content": None,
        "readme_content": None,
        "requirements_content": None
    }
    
    try:
        # Get all files in repository
        files = []
        for root, dirs, filenames in os.walk(repo_path):
            for filename in filenames:
                rel_path = os.path.relpath(os.path.join(root, filename), repo_path)
                files.append(rel_path)
        
        analysis["files"] = files
        
        # Check for PRD.md
        prd_path = os.path.join(repo_path, "PRD.md")
        if os.path.exists(prd_path):
            analysis["has_prd"] = True
            analysis["prd_status"] = "EXISTS"
            try:
                with open(prd_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    analysis["prd_content"] = content[:500] + "..." if len(content) > 500 else content
            except Exception as e:
                analysis["prd_content"] = f"Error reading PRD: {str(e)}"
        
        # Check for README.md
        readme_path = os.path.join(repo_path, "README.md")
        if os.path.exists(readme_path):
            analysis["has_readme"] = True
            analysis["readme_status"] = "EXISTS"
            try:
                with open(readme_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    analysis["readme_content"] = content[:500] + "..." if len(content) > 500 else content
            except Exception as e:
                analysis["readme_content"] = f"Error reading README: {str(e)}"
        
        # Check for requirements.txt
        req_path = os.path.join(repo_path, "requirements.txt")
        if os.path.exists(req_path):
            analysis["has_requirements"] = True
            analysis["requirements_status"] = "EXISTS"
            try:
                with open(req_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    analysis["requirements_content"] = content[:500] + "..." if len(content) > 500 else content
            except Exception as e:
                analysis["requirements_content"] = f"Error reading requirements: {str(e)}"
        
        # Determine overall status
        if analysis["has_prd"]:
            if "placeholder" in analysis["prd_content"].lower() or "TODO" in analysis["prd_content"]:
                analysis["prd_status"] = "INCOMPLETE_PLACEHOLDERS"
            else:
                analysis["prd_status"] = "COMPLETE"
        else:
            analysis["prd_status"] = "MISSING"
            
    except Exception as e:
        analysis["error"] = str(e)
    
    return analysis

def main():
    """Main analysis function"""
    workspace_path = r"D:\repos\Dadudekc"
    
    print(f"Starting comprehensive PRD analysis of {workspace_path}")
    print(f"Timestamp: {datetime.now()}")
    print("=" * 80)
    
    # Get all repositories
    try:
        repos = [d for d in os.listdir(workspace_path) 
                if os.path.isdir(os.path.join(workspace_path, d))]
        print(f"Found {len(repos)} repositories")
        
        # Analyze each repository
        results = []
        for i, repo in enumerate(repos, 1):
            repo_path = os.path.join(workspace_path, repo)
            print(f"[{i:2d}/{len(repos)}] Analyzing: {repo}")
            
            analysis = analyze_repository(repo_path)
            results.append(analysis)
            
            # Print status
            status_icon = "✅" if analysis["has_prd"] else "❌"
            print(f"    {status_icon} PRD: {analysis['prd_status']}")
        
        # Generate summary
        print("\n" + "=" * 80)
        print("ANALYSIS SUMMARY")
        print("=" * 80)
        
        total_repos = len(results)
        repos_with_prd = sum(1 for r in results if r["has_prd"])
        repos_without_prd = total_repos - repos_with_prd
        complete_prds = sum(1 for r in results if r["prd_status"] == "COMPLETE")
        incomplete_prds = sum(1 for r in results if r["prd_status"] == "INCOMPLETE_PLACEHOLDERS")
        
        print(f"Total Repositories: {total_repos}")
        print(f"With PRD: {repos_with_prd} ({repos_with_prd/total_repos*100:.1f}%)")
        print(f"Without PRD: {repos_without_prd} ({repos_without_prd/total_repos*100:.1f}%)")
        print(f"Complete PRDs: {complete_prds}")
        print(f"Incomplete PRDs: {incomplete_prds}")
        
        # Save detailed results
        output_file = f"comprehensive_prd_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"\nDetailed results saved to: {output_file}")
        
        # List repositories without PRDs
        print("\nRepositories WITHOUT PRDs:")
        print("-" * 40)
        for repo in results:
            if not repo["has_prd"]:
                print(f"❌ {repo['name']}")
        
        # List repositories with incomplete PRDs
        print("\nRepositories with INCOMPLETE PRDs (placeholders):")
        print("-" * 50)
        for repo in results:
            if repo["prd_status"] == "INCOMPLETE_PLACEHOLDERS":
                print(f"⚠️  {repo['name']}")
        
    except Exception as e:
        print(f"Error during analysis: {e}")

if __name__ == "__main__":
    main()
