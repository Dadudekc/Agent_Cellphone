#!/usr/bin/env python3
"""
Orphan File Identifier for Agent_Cellphone Project

This script analyzes the project structure to identify files that are not referenced
by any other files, indicating they may be orphaned.
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, List, Set, Tuple
import ast

class OrphanFileIdentifier:
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.all_files = set()
        self.referenced_files = set()
        self.orphaned_files = set()
        self.import_patterns = [
            r'from\s+([a-zA-Z_][a-zA-Z0-9_.]*)\s+import',
            r'import\s+([a-zA-Z_][a-zA-Z0-9_.]*)',
            r'from\s+([a-zA-Z_][a-zA-Z0-9_.]*)\s+import\s+\*',
        ]
        
    def scan_project_files(self):
        """Scan all files in the project"""
        print("🔍 Scanning project files...")
        
        for root, dirs, files in os.walk(self.project_root):
            # Skip common directories that shouldn't be analyzed
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in [
                '__pycache__', '.venv', '.git', 'node_modules', 'build', 'dist'
            ]]
            
            for file in files:
                file_path = Path(root) / file
                relative_path = file_path.relative_to(self.project_root)
                self.all_files.add(str(relative_path))
                
        print(f"📁 Found {len(self.all_files)} total files")
        
    def extract_imports_from_python_file(self, file_path: Path) -> Set[str]:
        """Extract import statements from a Python file"""
        imports = set()
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Parse with AST for more accurate import detection
            try:
                tree = ast.parse(content)
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            imports.add(alias.name)
                    elif isinstance(node, ast.ImportFrom):
                        if node.module:
                            imports.add(node.module)
            except SyntaxError:
                # Fallback to regex if AST parsing fails
                pass
                
            # Also check for regex patterns as backup
            for pattern in self.import_patterns:
                matches = re.findall(pattern, content)
                for match in matches:
                    if isinstance(match, tuple):
                        imports.update(match)
                    else:
                        imports.add(match)
                        
        except Exception as e:
            print(f"⚠️  Error reading {file_path}: {e}")
            
        return imports
    
    def analyze_file_references(self):
        """Analyze all files for references to other files"""
        print("🔍 Analyzing file references...")
        
        for file_path_str in self.all_files:
            file_path = self.project_root / file_path_str
            
            if not file_path.exists():
                continue
                
            # Handle different file types
            if file_path.suffix == '.py':
                imports = self.extract_imports_from_python_file(file_path)
                self.process_python_imports(imports, file_path_str)
            elif file_path.suffix in ['.md', '.txt', '.json', '.yaml', '.yml']:
                self.process_text_file_references(file_path, file_path_str)
            elif file_path.suffix in ['.bat', '.ps1', '.sh']:
                self.process_script_file_references(file_path, file_path_str)
                
    def process_python_imports(self, imports: Set[str], source_file: str):
        """Process Python imports and map them to actual files"""
        for import_name in imports:
            # Skip standard library and external packages
            if import_name.startswith(('os', 'sys', 'json', 'time', 'pathlib', 'typing', 
                                     'asyncio', 'logging', 'datetime', 'subprocess', 'argparse')):
                continue
                
            # Try to map import to actual file
            possible_files = self.find_files_by_import_name(import_name)
            for file_path in possible_files:
                self.referenced_files.add(file_path)
                
    def find_files_by_import_name(self, import_name: str) -> List[str]:
        """Find actual files that match an import name"""
        matching_files = []
        
        # Remove common suffixes and try to match
        base_name = import_name.replace('.', '/')
        
        for file_path in self.all_files:
            if file_path.endswith('.py'):
                file_name = file_path[:-3]  # Remove .py extension
                if (file_name.endswith(base_name) or 
                    file_name.endswith(base_name.split('/')[-1]) or
                    file_name.replace('/', '_') == base_name.replace('/', '_')):
                    matching_files.append(file_path)
                    
        return matching_files
    
    def process_text_file_references(self, file_path: Path, source_file: str):
        """Process text files for file references"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Look for file paths and references
            file_references = re.findall(r'[a-zA-Z0-9_\-\.\/\\]+\.(py|md|json|txt|yaml|yml|bat|ps1|sh)', content)
            for ref in file_references:
                # Try to find the referenced file
                for file_path_str in self.all_files:
                    if ref in file_path_str:
                        self.referenced_files.add(file_path_str)
                        
        except Exception as e:
            print(f"⚠️  Error reading text file {file_path}: {e}")
            
    def process_script_file_references(self, file_path: Path, source_file: str):
        """Process script files for file references"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Look for Python file references in scripts
            python_refs = re.findall(r'[a-zA-Z0-9_\-\.\/\\]+\.py', content)
            for ref in python_refs:
                for file_path_str in self.all_files:
                    if ref in file_path_str:
                        self.referenced_files.add(file_path_str)
                        
        except Exception as e:
            print(f"⚠️  Error reading script file {file_path}: {e}")
    
    def identify_orphans(self):
        """Identify orphaned files"""
        print("🔍 Identifying orphaned files...")
        
        # Files that are always considered referenced (entry points, configs, etc.)
        always_referenced = {
            'README.md',
            'ORGANIZATION_SUMMARY.md',
            '.gitignore',
            'setup.sh',
            'requirements.txt',
            'config.ini',
            'main.py',
            '__init__.py'
        }
        
        # Add always referenced files
        for file_path in self.all_files:
            file_name = Path(file_path).name
            if file_name in always_referenced:
                self.referenced_files.add(file_path)
        
        # Find orphaned files
        self.orphaned_files = self.all_files - self.referenced_files
        
        # Filter out certain types of files that are typically not referenced
        filtered_orphans = set()
        for file_path in self.orphaned_files:
            file_name = Path(file_path).name
            file_ext = Path(file_path).suffix
            
            # Skip certain file types that are typically standalone
            if file_ext in ['.log', '.tmp', '.cache', '.bak', '.backup']:
                continue
            if file_name.startswith('test_') or file_name.endswith('_test.py'):
                continue
            if file_name in ['__pycache__', '.DS_Store', 'Thumbs.db']:
                continue
                
            filtered_orphans.add(file_path)
            
        self.orphaned_files = filtered_orphans
        
    def generate_report(self) -> Dict:
        """Generate a comprehensive report"""
        print("📊 Generating orphan analysis report...")
        
        # Categorize orphaned files
        orphan_categories = {
            'python_files': [],
            'documentation': [],
            'scripts': [],
            'configs': [],
            'other': []
        }
        
        for file_path in self.orphaned_files:
            file_ext = Path(file_path).suffix
            if file_ext == '.py':
                orphan_categories['python_files'].append(file_path)
            elif file_ext in ['.md', '.txt']:
                orphan_categories['documentation'].append(file_path)
            elif file_ext in ['.bat', '.ps1', '.sh']:
                orphan_categories['scripts'].append(file_path)
            elif file_ext in ['.json', '.yaml', '.yml', '.ini', '.cfg']:
                orphan_categories['configs'].append(file_path)
            else:
                orphan_categories['other'].append(file_path)
        
        report = {
            'project_root': str(self.project_root),
            'total_files': len(self.all_files),
            'referenced_files': len(self.referenced_files),
            'orphaned_files': len(self.orphaned_files),
            'orphan_categories': orphan_categories,
            'all_orphaned_files': sorted(list(self.orphaned_files)),
            'analysis_timestamp': str(Path.cwd())
        }
        
        return report
    
    def print_report(self, report: Dict):
        """Print the orphan analysis report"""
        print("\n" + "="*80)
        print("🔍 ORPHAN FILE ANALYSIS REPORT")
        print("="*80)
        print(f"📁 Project Root: {report['project_root']}")
        print(f"📊 Total Files: {report['total_files']}")
        print(f"🔗 Referenced Files: {report['referenced_files']}")
        print(f"👻 Orphaned Files: {report['orphaned_files']}")
        
        print(f"\n📋 Orphan Categories:")
        for category, files in report['orphan_categories'].items():
            if files:
                print(f"  {category.replace('_', ' ').title()}: {len(files)} files")
                
        print(f"\n👻 All Orphaned Files:")
        for file_path in report['all_orphaned_files']:
            print(f"  • {file_path}")
            
        print("\n" + "="*80)
        
    def save_report(self, report: Dict, output_file: str = "orphan_analysis_report.json"):
        """Save the report to a JSON file"""
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            print(f"💾 Report saved to: {output_file}")
        except Exception as e:
            print(f"❌ Error saving report: {e}")
    
    def run_analysis(self):
        """Run the complete orphan analysis"""
        print("🚀 Starting orphan file analysis...")
        
        self.scan_project_files()
        self.analyze_file_references()
        self.identify_orphans()
        
        report = self.generate_report()
        self.print_report(report)
        self.save_report(report)
        
        return report

def main():
    """Main function"""
    project_root = Path.cwd()
    
    print(f"🔍 Analyzing project: {project_root}")
    
    analyzer = OrphanFileIdentifier(project_root)
    report = analyzer.run_analysis()
    
    print("\n✅ Orphan analysis complete!")
    print(f"📊 Found {report['orphaned_files']} potentially orphaned files")
    
    if report['orphaned_files'] > 0:
        print("\n💡 Recommendations:")
        print("  • Review orphaned Python files for unused functionality")
        print("  • Check if orphaned documentation is still relevant")
        print("  • Consider removing truly unused files to clean up the project")
        print("  • Some files may be intentionally standalone (entry points, utilities)")

if __name__ == "__main__":
    main()
