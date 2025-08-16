#!/usr/bin/env python3
"""
Debug script to check what's being imported
"""

print("=== DEBUG IMPORT ===")

try:
    from main import MLRobotUtils
    print("✓ Successfully imported MLRobotUtils from main")
    print(f"Class: {MLRobotUtils}")
    print(f"Module: {MLRobotUtils.__module__}")
    
    # Create an instance
    utils = MLRobotUtils()
    print(f"Instance: {utils}")
    print(f"Instance class: {utils.__class__}")
    print(f"Instance class module: {utils.__class__.__module__}")
    
    # Check methods
    print(f"Methods: {[m for m in dir(utils) if not m.startswith('_')]}")
    
    # Test a specific method
    if hasattr(utils, 'generate_save_path'):
        print("✓ generate_save_path method exists")
        # Check the method's source
        import inspect
        source = inspect.getsource(utils.generate_save_path)
        print(f"Method source (first 3 lines):")
        for i, line in enumerate(source.split('\n')[:3]):
            print(f"  {i+1}: {line}")
    else:
        print("✗ generate_save_path method missing")
        
except Exception as e:
    print(f"✗ Import failed: {e}")
    import traceback
    traceback.print_exc()
