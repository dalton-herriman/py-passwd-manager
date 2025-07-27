#!/usr/bin/env python3
"""
Comprehensive test runner with pre-flight checks
"""

import sys
import os
import subprocess
import importlib
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required. Current version:", sys.version)
        return False
    print(f"✅ Python version: {sys.version}")
    return True

def check_dependencies():
    """Check if all required dependencies are installed"""
    required_packages = [
        'click', 'cryptography', 'argon2', 'pyperclip', 'pytest'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            importlib.import_module(package)
            print(f"✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} - MISSING")
    
    if missing_packages:
        print(f"\n❌ Missing packages: {', '.join(missing_packages)}")
        print("Run: pip install -r requirements.txt")
        return False
    
    return True

def check_project_structure():
    """Check if project structure is correct"""
    required_files = [
        'pm_core/__init__.py',
        'pm_core/manager.py',
        'pm_core/crypto.py',
        'pm_core/utils.py',
        'pm_core/storage.py',
        'pm_core/models.py',
        'pm_core/exceptions.py',
        'cli/main.py',
        'gui/app.py',
        'tests/',
        'requirements.txt',
        'setup.py'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
            print(f"❌ {file_path} - MISSING")
        else:
            print(f"✅ {file_path}")
    
    if missing_files:
        print(f"\n❌ Missing files: {', '.join(missing_files)}")
        return False
    
    return True

def check_imports():
    """Test if all modules can be imported"""
    modules_to_test = [
        'pm_core.manager',
        'pm_core.crypto',
        'pm_core.utils',
        'pm_core.storage',
        'pm_core.models',
        'pm_core.exceptions',
        'cli.main',
        'gui.app'
    ]
    
    failed_imports = []
    for module in modules_to_test:
        try:
            importlib.import_module(module)
            print(f"✅ {module}")
        except ImportError as e:
            failed_imports.append(f"{module}: {e}")
            print(f"❌ {module} - {e}")
    
    if failed_imports:
        print(f"\n❌ Import failures: {len(failed_imports)}")
        return False
    
    return True

def run_tests():
    """Run the test suite"""
    print("\n🧪 Running tests...")
    try:
        result = subprocess.run([sys.executable, '-m', 'pytest', '-v'], 
                              capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Test execution failed: {e}")
        return False

def main():
    """Main test runner with comprehensive checks"""
    print("🔍 Password Manager - Pre-flight Checks")
    print("=" * 50)
    
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("Project Structure", check_project_structure),
        ("Module Imports", check_imports),
    ]
    
    all_passed = True
    for check_name, check_func in checks:
        print(f"\n📋 {check_name}:")
        if not check_func():
            all_passed = False
    
    if all_passed:
        print("\n✅ All pre-flight checks passed!")
        if run_tests():
            print("\n🎉 All tests passed!")
            return 0
        else:
            print("\n❌ Tests failed!")
            return 1
    else:
        print("\n❌ Pre-flight checks failed!")
        print("\n💡 Common fixes:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Run from project root directory")
        print("3. Check Python version (3.8+ required)")
        print("4. Ensure all files are present")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 