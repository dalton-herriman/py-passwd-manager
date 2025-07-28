#!/usr/bin/env python3
"""
Command registry for the Password Manager runner
Replaces repetitive command handling with a clean registry pattern
"""

import sys
import subprocess
from pathlib import Path
from typing import Dict, Callable, Any, Optional


class CommandRegistry:
    """Registry for command handlers"""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.commands: Dict[str, Callable] = {}
        self.help_text: Dict[str, str] = {}
        
    def register(self, name: str, handler: Callable, help_text: str = ""):
        """Register a command handler"""
        self.commands[name] = handler
        self.help_text[name] = help_text
        
    def execute(self, command: str, args: list = None) -> bool:
        """Execute a registered command"""
        if command not in self.commands:
            print(f"❌ Unknown command: {command}")
            self.show_help()
            return False
            
        try:
            return self.commands[command](args or [])
        except Exception as e:
            print(f"❌ Error running command '{command}': {e}")
            return False
            
    def show_help(self):
        """Show available commands"""
        print("🔐 Password Manager - Cross-Platform Runner")
        print("=" * 50)
        print()
        
        # Group commands by category
        categories = {
            "Setup": ["install", "validate", "quick-start"],
            "Development": ["test", "test-verbose", "test-cov", "test-fast", 
                          "test-security", "test-performance", "test-parallel", "lint"],
            "Run": ["cli", "gui", "demo", "demo-multi"],
            "Utility": ["clean", "check", "install-dev", "install-prod", 
                       "docs", "security-check", "full-check"]
        }
        
        for category, commands in categories.items():
            print(f"{category} Commands:")
            for cmd in commands:
                if cmd in self.help_text:
                    print(f"  {cmd:<15} - {self.help_text[cmd]}")
                else:
                    print(f"  {cmd}")
            print()
            
        print("Usage: python run.py [command]")
        
    def run_subprocess(self, cmd: list, cwd: Optional[Path] = None, 
                      env: Optional[dict] = None) -> bool:
        """Run a subprocess command with error handling"""
        try:
            subprocess.run(cmd, check=True, cwd=cwd or self.project_root, env=env)
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Command failed: {e}")
            return False
            
    def get_env_with_path(self) -> dict:
        """Get environment with project root in Python path"""
        import os
        env = os.environ.copy()
        env['PYTHONPATH'] = str(self.project_root) + os.pathsep + env.get('PYTHONPATH', '')
        return env 