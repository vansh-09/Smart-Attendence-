#!/usr/bin/env python3
"""
Smart Attendance - Interactive CLI Launcher
A complete face recognition attendance system with beautiful terminal UI
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def main():
    """Main entry point for the application."""
    try:
        from src.tui_app import SmartAttendanceApp
        app = SmartAttendanceApp()
        app.run()
    except ImportError as e:
        print(f"❌ Error: Missing dependencies - {e}")
        print("\n📦 Install dependencies with:")
        print("   pip install -r requirements.txt")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Application error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
