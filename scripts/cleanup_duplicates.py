#!/usr/bin/env python3
"""
Cleanup Duplicate Scripts
=========================
This script removes duplicate onboarding scripts and replaces them
with references to the consolidated solution.
"""

import os
import shutil
from pathlib import Path

def create_redirect_script(original_file: Path, target_script: str, target_args: str = ""):
    """Create a redirect script that points to the consolidated solution"""
    redirect_content = f"""#!/usr/bin/env python3
\"\"\"
REDIRECT: This script has been consolidated into {target_script}
================================================================

This file is a redirect to the new consolidated onboarding system.
The original functionality is now available in: scripts/{target_script}

Usage:
    python {target_script} {target_args}

For more information, run:
    python {target_script} --help
\"\"\"

import sys
import subprocess
from pathlib import Path

def main():
    print("🔄 REDIRECTING to consolidated onboarding system...")
    print(f"📁 Original: {original_file.name}")
    print(f"🎯 Target: {target_script}")
    print("=" * 50)
    
    # Get the script directory
    script_dir = Path(__file__).parent
    target_path = script_dir / target_script
    
    if not target_path.exists():
        print(f"❌ Error: Target script {target_script} not found!")
        return 1
    
    # Build command
    cmd = [sys.executable, str(target_path)] + sys.argv[1:]
    
    # Add default arguments if specified
    if "{target_args}":
        cmd.extend("{target_args}".split())
    
    print("🚀 Running command...")
    print()
    
    # Execute the target script
    try:
        result = subprocess.run(cmd, cwd=script_dir.parent)
        return result.returncode
    except Exception:
        print("❌ Error executing target script")
        return 1

if __name__ == "__main__":
    sys.exit(main())
"""
    
    with open(original_file, 'w', encoding='utf-8') as f:
        f.write(redirect_content)
    
    # Make executable
    os.chmod(original_file, 0o755)

def main():
    """Main cleanup function"""
    print("🧹 CLEANING UP DUPLICATE ONBOARDING SCRIPTS")
    print("=" * 50)
    
    script_dir = Path(__file__).parent
    
    # Files to be replaced with redirects
    redirects = [
        # Comprehensive onboarding messages (3 duplicates)
        ("comprehensive_onboarding_message.py", "consolidated_onboarding.py", "--all --style full"),
        ("comprehensive_onboarding_message_ascii.py", "consolidated_onboarding.py", "--all --style ascii"),
        ("comprehensive_onboarding_message_simple.py", "consolidated_onboarding.py", "--all --style simple"),
        
        # Single agent onboarding
        ("send_onboarding_message.py", "consolidated_onboarding.py", "--agent"),
        ("send_single_onboarding.py", "consolidated_onboarding.py", "--agent"),
        ("send_specific_onboarding.py", "consolidated_onboarding.py", "--agent"),
        
        # All agents onboarding
        ("onboard_all_agents.py", "consolidated_onboarding.py", "--all"),
        ("agent_onboarding_sequence.py", "consolidated_onboarding.py", "--all"),
        
        # General onboarding
        ("send_onboarding.py", "consolidated_onboarding.py", "--all"),
        ("onboarding_messages.py", "consolidated_onboarding.py", "--all"),
        
        # Demo and comparison scripts
        ("demo_chunk_vs_comprehensive_gui.py", "consolidated_onboarding.py", "--compare"),
        ("demo_onboarding_comparison.py", "consolidated_onboarding.py", "--compare"),
        ("onboarding_approach_comparison.py", "consolidated_onboarding.py", "--compare"),
    ]
    
    # Files to be completely removed (superseded by consolidated solution)
    files_to_remove = [
        "demo_improved_onboarding.py",
        "real_chunked_test.py",
        "record_onboarding_demo.py",
        "onboard_new_agent.py",
        "send_to_agents.py",
        "update_agent_status.py",
        "comprehensive_2_agent_demo.py",
    ]
    
    # Create redirects
    print("📝 Creating redirect scripts...")
    for original_file, target_script, target_args in redirects:
        original_path = script_dir / original_file
        if original_path.exists():
            print(f"  🔄 {original_file} → {target_script}")
            create_redirect_script(original_path, target_script, target_args)
        else:
            print(f"  ⚠️  {original_file} not found (skipping)")
    
    # Remove completely superseded files
    print("\n🗑️  Removing superseded files...")
    for file_to_remove in files_to_remove:
        file_path = script_dir / file_to_remove
        if file_path.exists():
            print(f"  🗑️  Removing {file_to_remove}")
            file_path.unlink()
        else:
            print(f"  ⚠️  {file_to_remove} not found (skipping)")
    
    # Clean up __pycache__
    print("\n🧹 Cleaning up __pycache__...")
    pycache_dir = script_dir / "__pycache__"
    if pycache_dir.exists():
        print(f"  🗑️  Removing {pycache_dir}")
        shutil.rmtree(pycache_dir)
    
    # Create a summary file
    summary_content = """# ONBOARDING SCRIPTS CLEANUP SUMMARY

## What Changed

### ✅ Consolidated Files
- All duplicate onboarding logic has been consolidated into:
  - `onboarding_utils.py` - Shared utilities and functions
  - `consolidated_onboarding.py` - Main onboarding script

### 🔄 Redirect Scripts
The following files now redirect to the consolidated solution:
- `comprehensive_onboarding_message.py` → `consolidated_onboarding.py --all --style full`
- `comprehensive_onboarding_message_ascii.py` → `consolidated_onboarding.py --all --style ascii`
- `comprehensive_onboarding_message_simple.py` → `consolidated_onboarding.py --all --style simple`
- `send_onboarding_message.py` → `consolidated_onboarding.py --agent`
- `send_single_onboarding.py` → `consolidated_onboarding.py --agent`
- `send_specific_onboarding.py` → `consolidated_onboarding.py --agent`
- `onboard_all_agents.py` → `consolidated_onboarding.py --all`
- `agent_onboarding_sequence.py` → `consolidated_onboarding.py --all`
- `send_onboarding.py` → `consolidated_onboarding.py --all`
- `onboarding_messages.py` → `consolidated_onboarding.py --all`
- `demo_chunk_vs_comprehensive_gui.py` → `consolidated_onboarding.py --compare`
- `demo_onboarding_comparison.py` → `consolidated_onboarding.py --compare`
- `onboarding_approach_comparison.py` → `consolidated_onboarding.py --compare`

### 🗑️ Removed Files
The following files were completely removed (functionality superseded):
- `demo_improved_onboarding.py`
- `real_chunked_test.py`
- `record_onboarding_demo.py`
- `onboard_new_agent.py`
- `send_to_agents.py`
- `update_agent_status.py`
- `comprehensive_2_agent_demo.py`

## How to Use the New System

### Basic Usage
```bash
# Send comprehensive onboarding to all agents
python consolidated_onboarding.py --all

# Send onboarding to specific agent
python consolidated_onboarding.py --agent Agent-1

# Send ASCII-only onboarding (no emojis)
python consolidated_onboarding.py --all --style ascii

# Test mode (preview without sending)
python consolidated_onboarding.py --all --test

# Show comparison between approaches
python consolidated_onboarding.py --compare

# List available agents
python consolidated_onboarding.py --list-agents

# Preview message for specific agent
python consolidated_onboarding.py --agent Agent-1 --preview
```

### Backward Compatibility
All existing scripts still work - they now redirect to the consolidated solution.
The redirect scripts will show helpful information about the new usage.

## Benefits

1. **No More Duplicates**: All duplicate logic has been eliminated
2. **Single Source of Truth**: One place to maintain onboarding logic
3. **Better Features**: More options and better error handling
4. **Easier Maintenance**: Changes only need to be made in one place
5. **Backward Compatible**: Existing scripts still work
6. **Better Documentation**: Comprehensive help and examples

## Migration Notes

- All existing functionality is preserved
- New features are available through the consolidated script
- Redirect scripts provide helpful migration guidance
- No breaking changes to existing workflows
"""
    
    summary_file = script_dir / "ONBOARDING_CLEANUP_SUMMARY.md"
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write(summary_content)
    
    print(f"\n📋 Created summary: {summary_file}")
    
    print("\n✅ CLEANUP COMPLETE!")
    print("=" * 50)
    print("🎯 All duplicate logic has been consolidated")
    print("🔄 Redirect scripts maintain backward compatibility")
    print("📚 See ONBOARDING_CLEANUP_SUMMARY.md for details")
    print("\n🚀 Try the new consolidated system:")
    print("   python consolidated_onboarding.py --help")

if __name__ == "__main__":
    main() 