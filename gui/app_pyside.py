#!/usr/bin/env python3
"""
PySide6-based GUI application for the password manager
Modern, responsive interface with better UX
"""

import sys
from pathlib import Path

# Add the project root to the path
sys.path.insert(0, str(Path(__file__).parent.parent))

from .main_app_pyside import main


if __name__ == "__main__":
    main() 