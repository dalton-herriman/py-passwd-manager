#!/usr/bin/env python3
"""
Command handlers for the Password Manager runner
Extracted from the massive run.py file into focused classes
"""

import sys
import subprocess
from pathlib import Path
from typing import List


class SetupCommands:
    """Setup and installation commands"""
    
    def __init__(self, registry):
        self.registry = registry
        
    def install_dependencies(self, args: List[str] = None) -> bool:
        """Install project dependencies"""
        print("📦 Installing dependencies...")
        cmd = [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"]
        success = self.registry.run_subprocess(cmd)
        if success:
            print("✅ Dependencies installed")
        return success
        
    def validate_setup(self, args: List[str] = None) -> bool:
        """Validate project setup"""
        print("🔍 Validating project setup...")
        cmd = [sys.executable, "scripts/validate_setup.py"]
        return self.registry.run_subprocess(cmd, env=self.registry.get_env_with_path())
        
    def quick_start(self, args: List[str] = None) -> bool:
        """Run quick start script"""
        print("🚀 Running quick start...")
        cmd = [sys.executable, "scripts/quick_start.py"]
        return self.registry.run_subprocess(cmd, env=self.registry.get_env_with_path())


class TestCommands:
    """Test-related commands"""
    
    def __init__(self, registry):
        self.registry = registry
        
    def run_tests(self, args: List[str] = None) -> bool:
        """Run all tests"""
        print("🧪 Running tests...")
        cmd = [sys.executable, "-m", "pytest", "tests/", "-v"]
        return self.registry.run_subprocess(cmd)
        
    def run_tests_verbose(self, args: List[str] = None) -> bool:
        """Run tests with verbose output"""
        print("🧪 Running tests with verbose output...")
        cmd = [sys.executable, "-m", "pytest", "tests/", "-vv", "--tb=short"]
        return self.registry.run_subprocess(cmd)
        
    def run_tests_coverage(self, args: List[str] = None) -> bool:
        """Run tests with coverage"""
        print("🧪 Running tests with coverage...")
        cmd = [sys.executable, "-m", "pytest", "tests/", "--cov=pm_core", 
               "--cov-report=html", "--cov-report=term-missing"]
        return self.registry.run_subprocess(cmd)
        
    def run_tests_fast(self, args: List[str] = None) -> bool:
        """Run fast tests only"""
        print("🧪 Running fast tests only...")
        cmd = [sys.executable, "-m", "pytest", "tests/", "-m", "not slow", "-v"]
        return self.registry.run_subprocess(cmd)
        
    def run_tests_security(self, args: List[str] = None) -> bool:
        """Run security tests"""
        print("🔒 Running security tests...")
        cmd = [sys.executable, "-m", "pytest", "tests/", "-m", "security", "-v"]
        return self.registry.run_subprocess(cmd)
        
    def run_tests_performance(self, args: List[str] = None) -> bool:
        """Run performance tests"""
        print("⚡ Running performance tests...")
        cmd = [sys.executable, "-m", "pytest", "tests/", "-m", "performance", "-v"]
        return self.registry.run_subprocess(cmd)
        
    def run_tests_parallel(self, args: List[str] = None) -> bool:
        """Run tests in parallel"""
        print("🧪 Running tests in parallel...")
        cmd = [sys.executable, "-m", "pytest", "tests/", "-n", "auto", "-v"]
        return self.registry.run_subprocess(cmd)


class RunCommands:
    """Application run commands"""
    
    def __init__(self, registry):
        self.registry = registry
        
    def start_cli(self, args: List[str] = None) -> bool:
        """Start CLI interface"""
        print("💻 Starting CLI...")
        cmd = [sys.executable, "cli_main.py"]
        if args:
            cmd.extend(args)
        return self.registry.run_subprocess(cmd)
        
    def start_gui(self, args: List[str] = None) -> bool:
        """Start GUI interface"""
        print("🖥️  Starting GUI...")
        
        # Check if PySide6 is available, otherwise fall back to Tkinter
        try:
            import PySide6
            print("Using PySide6 GUI (modern)")
            cmd = [sys.executable, "-m", "gui.app_pyside"]
        except ImportError:
            print("Using Tkinter GUI (fallback)")
            cmd = [sys.executable, "-m", "gui.app"]
        
        return self.registry.run_subprocess(cmd)
        
    def run_demo(self, args: List[str] = None) -> bool:
        """Run demo script"""
        print("🎬 Running demo...")
        cmd = [sys.executable, "scripts/demo_multi_vault.py"]
        return self.registry.run_subprocess(cmd)
        
    def run_demo_multi(self, args: List[str] = None) -> bool:
        """Run multi-vault demo script"""
        print("🎬 Running Multi-Vault demo...")
        cmd = [sys.executable, "scripts/demo_multi_vault.py"]
        return self.registry.run_subprocess(cmd)


class UtilityCommands:
    """Utility and maintenance commands"""
    
    def __init__(self, registry):
        self.registry = registry
        
    def clean_up(self, args: List[str] = None) -> bool:
        """Clean up temporary files"""
        print("🧹 Cleaning up...")
        try:
            # Remove .pyc files
            for pyc_file in self.registry.project_root.rglob("*.pyc"):
                pyc_file.unlink()
            
            # Remove __pycache__ directories
            for cache_dir in self.registry.project_root.rglob("__pycache__"):
                import shutil
                shutil.rmtree(cache_dir)
            
            # Remove .db files
            for db_file in self.registry.project_root.rglob("*.db"):
                db_file.unlink()
            
            # Remove test and demo db files
            for test_db in self.registry.project_root.rglob("test_*.db"):
                test_db.unlink()
            for demo_db in self.registry.project_root.rglob("demo_*.db"):
                demo_db.unlink()
                
            print("✅ Cleanup complete")
            return True
        except Exception as e:
            print(f"❌ Cleanup failed: {e}")
            return False
            
    def run_all_checks(self, args: List[str] = None) -> bool:
        """Run all checks"""
        print("🔍 Running all checks...")
        checks = [
            self.registry.commands["install"],
            self.registry.commands["validate"],
            self.registry.commands["test"]
        ]
        
        for check in checks:
            if not check():
                return False
        
        print("✅ All checks passed!")
        return True
        
    def install_dev(self, args: List[str] = None) -> bool:
        """Install in development mode"""
        print("📦 Installing in development mode...")
        cmd = [sys.executable, "-m", "pip", "install", "-e", "."]
        success = self.registry.run_subprocess(cmd)
        if success:
            print("✅ Development installation complete")
        return success
        
    def install_prod(self, args: List[str] = None) -> bool:
        """Install in production mode"""
        print("📦 Installing in production mode...")
        cmd = [sys.executable, "-m", "pip", "install", "."]
        success = self.registry.run_subprocess(cmd)
        if success:
            print("✅ Production installation complete")
        return success
        
    def generate_docs(self, args: List[str] = None) -> bool:
        """Generate documentation"""
        print("📚 Generating documentation...")
        cmd = [sys.executable, "-c", "import pm_core; help(pm_core)"]
        return self.registry.run_subprocess(cmd)
        
    def security_check(self, args: List[str] = None) -> bool:
        """Run security checks"""
        print("🔒 Running security checks...")
        
        # Test crypto functions
        crypto_cmd = [sys.executable, "-c", 
                     "from pm_core.crypto import generate_salt, encrypt_data, decrypt_data; print('Crypto functions available')"]
        if not self.registry.run_subprocess(crypto_cmd):
            return False
            
        # Test security utils
        utils_cmd = [sys.executable, "-c", 
                    "from pm_core.utils import generate_password, validate_password_strength; print('Security utils available')"]
        if not self.registry.run_subprocess(utils_cmd):
            return False
            
        print("✅ Security checks passed")
        return True
        
    def full_check(self, args: List[str] = None) -> bool:
        """Run full validation suite"""
        print("🔍 Running full validation suite...")
        checks = [
            self.registry.commands["install"],
            self.registry.commands["validate"],
            self.registry.commands["security-check"],
            self.registry.commands["test"]
        ]
        
        for check in checks:
            if not check():
                return False
        
        print("✅ All validations passed!")
        return True
        
    def run_lint(self, args: List[str] = None) -> bool:
        """Run code linting"""
        print("🔍 Running linting...")
        
        # Run flake8
        flake8_cmd = [sys.executable, "-m", "flake8", "pm_core/", "cli/", "gui/", "tests/"]
        if not self.registry.run_subprocess(flake8_cmd):
            return False
            
        # Run black check
        black_cmd = [sys.executable, "-m", "black", "--check", "pm_core/", "cli/", "gui/", "tests/"]
        if not self.registry.run_subprocess(black_cmd):
            return False
            
        print("✅ Linting passed")
        return True 