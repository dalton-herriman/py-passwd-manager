#!/usr/bin/env python3
"""
Cross-platform runner for the Password Manager
Streamlined version using modular command system
"""

import sys
import argparse
from pathlib import Path

from run.command_registry import CommandRegistry
from run.command_handlers import (
    SetupCommands,
    TestCommands,
    RunCommands,
    UtilityCommands
)


def setup_command_registry() -> CommandRegistry:
    """Setup the command registry with all handlers"""
    project_root = Path(__file__).parent
    registry = CommandRegistry(project_root)
    
    # Initialize command handlers
    setup_commands = SetupCommands(registry)
    test_commands = TestCommands(registry)
    run_commands = RunCommands(registry)
    utility_commands = UtilityCommands(registry)
    
    # Register setup commands
    registry.register("install", setup_commands.install_dependencies, "Install dependencies")
    registry.register("validate", setup_commands.validate_setup, "Validate project setup")
    registry.register("quick-start", setup_commands.quick_start, "Quick start with validation")
    
    # Register test commands
    registry.register("test", test_commands.run_tests, "Run all tests")
    registry.register("test-verbose", test_commands.run_tests_verbose, "Run tests with verbose output")
    registry.register("test-cov", test_commands.run_tests_coverage, "Run tests with coverage")
    registry.register("test-fast", test_commands.run_tests_fast, "Run fast tests only")
    registry.register("test-security", test_commands.run_tests_security, "Run security tests")
    registry.register("test-performance", test_commands.run_tests_performance, "Run performance tests")
    registry.register("test-parallel", test_commands.run_tests_parallel, "Run tests in parallel")
    
    # Register run commands
    registry.register("cli", run_commands.start_cli, "Run CLI interface")
    registry.register("gui", run_commands.start_gui, "Run GUI interface")
    registry.register("demo", run_commands.run_demo, "Run demo script")
    registry.register("demo-multi", run_commands.run_demo_multi, "Run Multi-Vault demo script")
    
    # Register utility commands
    registry.register("clean", utility_commands.clean_up, "Clean up temporary files")
    registry.register("check", utility_commands.run_all_checks, "Run all checks")
    registry.register("install-dev", utility_commands.install_dev, "Install in development mode")
    registry.register("install-prod", utility_commands.install_prod, "Install in production mode")
    registry.register("docs", utility_commands.generate_docs, "Generate documentation")
    registry.register("security-check", utility_commands.security_check, "Run security checks")
    registry.register("full-check", utility_commands.full_check, "Run all validations")
    registry.register("lint", utility_commands.run_lint, "Run code linting")
    
    return registry


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Cross-platform runner for the Password Manager",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_new.py help          # Show available commands
  python run_new.py install       # Install dependencies
  python run_new.py test          # Run tests
  python run_new.py cli           # Start CLI
  python run_new.py gui           # Start GUI
        """
    )
    
    parser.add_argument("command", nargs="?", default="help", 
                       help="Command to run (default: help)")
    parser.add_argument("args", nargs="*", help="Additional arguments for the command")
    
    args = parser.parse_args()
    
    # Setup command registry
    registry = setup_command_registry()
    
    # Handle help command
    if args.command == "help":
        registry.show_help()
        success = True
    else:
        # Execute command
        success = registry.execute(args.command, args.args)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main() 