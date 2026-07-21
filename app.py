#!/usr/bin/env python3
"""CyberLab Pro - Application Entry Point"""
import sys
import os

def check_requirements():
    """Verify all requirements before launch"""
    errors = []
    
    if sys.version_info < (3, 8):
        errors.append("Python 3.8+ required")
    
    if not os.environ.get('DISPLAY'):
        os.environ['DISPLAY'] = ':0'
    
    try:
        import tkinter
    except ImportError:
        errors.append("tkinter not installed. Run: pkg install python-tkinter")
    
    base = os.path.dirname(os.path.abspath(__file__))
    required_dirs = ['core', 'gui', 'modules', 'config', 'logs', 'database', 'plugins', 'themes']
    for d in required_dirs:
        os.makedirs(os.path.join(base, d), exist_ok=True)
    
    return errors

if __name__ == "__main__":
    errors = check_requirements()
    if errors:
        print("❌ Missing requirements:")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    
    print("✅ All requirements met. Launching...")
    from launcher import CyberLabApp
    app = CyberLabApp()
    app.run()
