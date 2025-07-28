#!/usr/bin/env python3
"""
Main entry point for the Password Manager CLI
Uses the new Typer-based CLI with Rich output
"""

import sys
from pathlib import Path

# Add the project root to the path
sys.path.insert(0, str(Path(__file__).parent))

from cli.typer_cli import app


def main():
    """Main entry point"""
    app()


if __name__ == "__main__":
    main() 