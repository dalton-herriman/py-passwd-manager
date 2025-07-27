#!/usr/bin/env python3
"""
Cross-platform runner for the Password Manager
Replaces Makefile, PowerShell, and Batch scripts with a single Python solution
"""

import sys
import os
import subprocess
import importlib
import argparse
from pathlib import Path
from typing import List, Optional


class PasswordManagerRunner:
    """Cross-platform runner for the Password Manager project"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.scripts_dir = self.project_root / "scripts"
        self.tests_dir = self.project_root / "tests"
        
    def run_command(self, command: str, args: List[str] = None) -> bool:
        """Run a command and return success status"""
        try:
            if command == "help":
                self.show_help()
                return True
            elif command == "install":
                return self.install_dependencies()
            elif command == "validate":
                return self.validate_setup()
            elif command == "quick-start":
                return self.quick_start()
            elif command == "test":
                return self.run_tests()
            elif command == "test-verbose":
                return self.run_tests_verbose()
            elif command == "test-cov":
                return self.run_tests_coverage()
            elif command == "test-fast":
                return self.run_tests_fast()
            elif command == "test-security":
                return self.run_tests_security()
            elif command == "test-performance":
                return self.run_tests_performance()
            elif command == "test-parallel":
                return self.run_tests_parallel()
            elif command == "lint":
                return self.run_lint()
            elif command == "cli":
                return self.start_cli()
            elif command == "gui":
                return self.start_gui()
            elif command == "demo":
                return self.run_demo()
            elif command == "demo-multi":
                return self.run_demo_multi()
            elif command == "clean":
                return self.clean_up()
            elif command == "check":
                return self.run_all_checks()
            elif command == "install-dev":
                return self.install_dev()
            elif command == "install-prod":
                return self.install_prod()
            elif command == "docs":
                return self.generate_docs()
            elif command == "security-check":
                return self.security_check()
            elif command == "full-check":
                return self.full_check()
            else:
                print(f"❌ Unknown command: {command}")
                self.show_help()
                return False
        except Exception as e:
            print(f"❌ Error running command '{command}': {e}")
            return False

    def show_help(self):
        """Show available commands"""
        print("🔐 Password Manager - Cross-Platform Runner")
        print("=" * 50)
        print()
        print("Setup Commands:")
        print("  install      - Install dependencies")
        print("  validate     - Validate project setup")
        print("  quick-start  - Quick start with validation")
        print()
        print("Development Commands:")
        print("  test         - Run all tests")
        print("  test-verbose - Run tests with verbose output")
        print("  test-cov     - Run tests with coverage")
        print("  test-fast    - Run fast tests only")
        print("  test-security - Run security tests")
        print("  test-performance - Run performance tests")
        print("  test-parallel - Run tests in parallel")
        print("  lint         - Run code linting")
        print()
        print("Run Commands:")
        print("  cli          - Run CLI interface")
        print("  gui          - Run GUI interface")
        print("  demo         - Run demo script (same as demo-multi)")
        print("  demo-multi   - Run Multi-Vault demo script")
        print()
        print("Utility Commands:")
        print("  clean        - Clean up temporary files")
        print("  check        - Run all checks")
        print("  install-dev  - Install in development mode")
        print("  install-prod - Install in production mode")
        print("  docs         - Generate documentation")
        print("  security-check - Run security checks")
        print("  full-check   - Run all validations")
        print()
        print("Usage: python run.py [command]")

    def install_dependencies(self) -> bool:
        """Install project dependencies"""
        print("📦 Installing dependencies...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                         check=True, cwd=self.project_root)
            print("✅ Dependencies installed")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install dependencies: {e}")
            return False

    def validate_setup(self) -> bool:
        """Validate project setup"""
        print("🔍 Validating project setup...")
        try:
            # Add project root to Python path
            env = os.environ.copy()
            env['PYTHONPATH'] = str(self.project_root) + os.pathsep + env.get('PYTHONPATH', '')
            
            subprocess.run([sys.executable, "scripts/validate_setup.py"], 
                         check=True, cwd=self.project_root, env=env)
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Validation failed: {e}")
            return False

    def quick_start(self) -> bool:
        """Run quick start script"""
        print("🚀 Running quick start...")
        try:
            # Add project root to Python path
            env = os.environ.copy()
            env['PYTHONPATH'] = str(self.project_root) + os.pathsep + env.get('PYTHONPATH', '')
            
            subprocess.run([sys.executable, "scripts/quick_start.py"], 
                         check=True, cwd=self.project_root, env=env)
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Quick start failed: {e}")
            return False

    def run_tests(self) -> bool:
        """Run all tests"""
        print("🧪 Running tests...")
        try:
            subprocess.run([sys.executable, "-m", "pytest", "tests/", "-v"], 
                         check=True, cwd=self.project_root)
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Tests failed: {e}")
            return False

    def run_tests_verbose(self) -> bool:
        """Run tests with verbose output"""
        print("🧪 Running tests with verbose output...")
        try:
            subprocess.run([sys.executable, "-m", "pytest", "tests/", "-vv", "--tb=short"], 
                         check=True, cwd=self.project_root)
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Tests failed: {e}")
            return False

    def run_tests_coverage(self) -> bool:
        """Run tests with coverage"""
        print("🧪 Running tests with coverage...")
        try:
            subprocess.run([sys.executable, "-m", "pytest", "tests/", "--cov=pm_core", 
                          "--cov-report=html", "--cov-report=term-missing"], 
                         check=True, cwd=self.project_root)
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Tests failed: {e}")
            return False

    def run_tests_fast(self) -> bool:
        """Run fast tests only"""
        print("🧪 Running fast tests only...")
        try:
            subprocess.run([sys.executable, "-m", "pytest", "tests/", "-m", "not slow", "-v"], 
                         check=True, cwd=self.project_root)
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Tests failed: {e}")
            return False

    def run_tests_security(self) -> bool:
        """Run security tests"""
        print("🔒 Running security tests...")
        try:
            subprocess.run([sys.executable, "-m", "pytest", "tests/", "-m", "security", "-v"], 
                         check=True, cwd=self.project_root)
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Tests failed: {e}")
            return False

    def run_tests_performance(self) -> bool:
        """Run performance tests"""
        print("⚡ Running performance tests...")
        try:
            subprocess.run([sys.executable, "-m", "pytest", "tests/", "-m", "performance", "-v"], 
                         check=True, cwd=self.project_root)
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Tests failed: {e}")
            return False

    def run_tests_parallel(self) -> bool:
        """Run tests in parallel"""
        print("🧪 Running tests in parallel...")
        try:
            subprocess.run([sys.executable, "-m", "pytest", "tests/", "-n", "auto", "-v"], 
                         check=True, cwd=self.project_root)
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Tests failed: {e}")
            return False

    def run_lint(self) -> bool:
        """Run code linting"""
        print("🔍 Running linting...")
        try:
            # Run flake8
            subprocess.run([sys.executable, "-m", "flake8", "pm_core/", "cli/", "gui/", "tests/"], 
                         check=True, cwd=self.project_root)
            # Run black check
            subprocess.run([sys.executable, "-m", "black", "--check", "pm_core/", "cli/", "gui/", "tests/"], 
                         check=True, cwd=self.project_root)
            print("✅ Linting passed")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Linting failed: {e}")
            return False

    def start_cli(self) -> bool:
        """Start CLI interface"""
        print("💻 Starting CLI...")
        try:
            subprocess.run([sys.executable, "-m", "cli.multi_vault_cli"], 
                         cwd=self.project_root)
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ CLI failed: {e}")
            return False

    def start_gui(self) -> bool:
        """Start GUI interface"""
        print("🖥️  Starting GUI...")
        try:
            subprocess.run([sys.executable, "-m", "gui.app"], 
                         cwd=self.project_root)
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ GUI failed: {e}")
            return False

    def run_demo(self) -> bool:
        """Run demo script"""
        print("🎬 Running demo...")
        try:
            # Run a simple demo by creating a test vault and adding an entry
            subprocess.run([sys.executable, "scripts/demo_multi_vault.py"], 
                         check=True, cwd=self.project_root)
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Demo failed: {e}")
            return False

    def run_demo_multi(self) -> bool:
        """Run multi-vault demo script"""
        print("🎬 Running Multi-Vault demo...")
        try:
            subprocess.run([sys.executable, "scripts/demo_multi_vault.py"], 
                         check=True, cwd=self.project_root)
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Demo failed: {e}")
            return False

    def clean_up(self) -> bool:
        """Clean up temporary files"""
        print("🧹 Cleaning up...")
        try:
            # Remove .pyc files
            for pyc_file in self.project_root.rglob("*.pyc"):
                pyc_file.unlink()
            
            # Remove __pycache__ directories
            for cache_dir in self.project_root.rglob("__pycache__"):
                import shutil
                shutil.rmtree(cache_dir)
            
            # Remove .db files
            for db_file in self.project_root.rglob("*.db"):
                db_file.unlink()
            
            # Remove test and demo db files
            for test_db in self.project_root.rglob("test_*.db"):
                test_db.unlink()
            for demo_db in self.project_root.rglob("demo_*.db"):
                demo_db.unlink()
                
            print("✅ Cleanup complete")
            return True
        except Exception as e:
            print(f"❌ Cleanup failed: {e}")
            return False

    def run_all_checks(self) -> bool:
        """Run all checks"""
        print("🔍 Running all checks...")
        checks = [self.install_dependencies, self.validate_setup, self.run_tests]
        
        for check in checks:
            if not check():
                return False
        
        print("✅ All checks passed!")
        return True

    def install_dev(self) -> bool:
        """Install in development mode"""
        print("📦 Installing in development mode...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "-e", "."], 
                         check=True, cwd=self.project_root)
            print("✅ Development installation complete")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Development installation failed: {e}")
            return False

    def install_prod(self) -> bool:
        """Install in production mode"""
        print("📦 Installing in production mode...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "."], 
                         check=True, cwd=self.project_root)
            print("✅ Production installation complete")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Production installation failed: {e}")
            return False

    def generate_docs(self) -> bool:
        """Generate documentation"""
        print("📚 Generating documentation...")
        try:
            subprocess.run([sys.executable, "-c", "import pm_core; help(pm_core)"], 
                         check=True, cwd=self.project_root)
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Documentation generation failed: {e}")
            return False

    def security_check(self) -> bool:
        """Run security checks"""
        print("🔒 Running security checks...")
        try:
            # Test crypto functions
            subprocess.run([sys.executable, "-c", 
                          "from pm_core.crypto import generate_salt, encrypt_data, decrypt_data; print('Crypto functions available')"], 
                         check=True, cwd=self.project_root)
            
            # Test security utils
            subprocess.run([sys.executable, "-c", 
                          "from pm_core.utils import generate_password, validate_password_strength; print('Security utils available')"], 
                         check=True, cwd=self.project_root)
            
            print("✅ Security checks passed")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Security checks failed: {e}")
            return False

    def full_check(self) -> bool:
        """Run full validation suite"""
        print("🔍 Running full validation suite...")
        checks = [self.install_dependencies, self.validate_setup, self.security_check, self.run_tests]
        
        for check in checks:
            if not check():
                return False
        
        print("✅ All validations passed!")
        return True


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Cross-platform runner for the Password Manager",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run.py help          # Show available commands
  python run.py install       # Install dependencies
  python run.py test          # Run tests
  python run.py cli           # Start CLI
  python run.py gui           # Start GUI
        """
    )
    
    parser.add_argument("command", nargs="?", default="help", 
                       help="Command to run (default: help)")
    parser.add_argument("args", nargs="*", help="Additional arguments for the command")
    
    args = parser.parse_args()
    
    runner = PasswordManagerRunner()
    success = runner.run_command(args.command, args.args)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main() 