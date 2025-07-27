#!/usr/bin/env python3
"""
Setup validation script to prevent common configuration errors
"""

import os
import sys
import json
import tempfile
import shutil
from pathlib import Path


def validate_requirements_file():
    """Validate requirements.txt file"""
    print("📋 Checking requirements.txt...")

    if not os.path.exists("requirements.txt"):
        print("❌ requirements.txt not found")
        return False

    try:
        with open("requirements.txt", "r", encoding="utf-8") as f:
            content = f.read()

        # Check for encoding issues
        if "\xff" in content or "\xfe" in content:
            print("❌ requirements.txt has encoding issues")
            return False

        # Check for valid package names
        lines = [line.strip() for line in content.split("\n") if line.strip()]
        for line in lines:
            if "==" in line:
                package, version = line.split("==", 1)
                if not package or not version:
                    print(f"❌ Invalid requirement format: {line}")
                    return False

        print("✅ requirements.txt is valid")
        return True

    except Exception as e:
        print(f"❌ Error reading requirements.txt: {e}")
        return False


def validate_setup_py():
    """Validate setup.py configuration"""
    print("📋 Checking setup.py...")

    if not os.path.exists("setup.py"):
        print("❌ setup.py not found")
        return False

    try:
        # Test if setup.py can be imported
        import setup

        print("✅ setup.py is valid")
        return True
    except Exception as e:
        print(f"❌ setup.py has issues: {e}")
        return False


def validate_package_structure():
    """Validate package structure and __init__.py files"""
    print("📋 Checking package structure...")

    packages = ["pm_core", "cli", "gui", "tests"]

    for package in packages:
        init_file = os.path.join(package, "__init__.py")
        if not os.path.exists(init_file):
            print(f"❌ Missing {init_file}")
            return False

    print("✅ Package structure is valid")
    return True


def test_basic_imports():
    """Test basic imports to catch import errors early"""
    print("📋 Testing basic imports...")

    try:
        # Test core imports
        from pm_core.manager import PasswordManager
        from pm_core.crypto import generate_salt
        from pm_core.utils import generate_password

        print("✅ Core imports work")

        # Test interface imports
        from cli.main import cli
        from gui.app import PasswordManagerGUI

        print("✅ Interface imports work")

        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False


def test_basic_functionality():
    """Test basic functionality to catch runtime errors"""
    print("📋 Testing basic functionality...")

    try:
        from pm_core.manager import PasswordManager
        from pm_core.utils import generate_password

        # Test password generation
        password = generate_password(12)
        if len(password) != 12:
            print("❌ Password generation failed")
            return False

        # Test manager creation
        pm = PasswordManager("test_vault.db")
        print("✅ Basic functionality works")

        # Clean up
        if os.path.exists("test_vault.db"):
            os.remove("test_vault.db")

        return True
    except Exception as e:
        print(f"❌ Basic functionality test failed: {e}")
        return False


def validate_file_permissions():
    """Check file permissions and accessibility"""
    print("📋 Checking file permissions...")

    critical_files = [
        "pm_core/manager.py",
        "pm_core/crypto.py",
        "cli/main.py",
        "gui/app.py",
    ]

    for file_path in critical_files:
        if not os.path.exists(file_path):
            print(f"❌ Critical file missing: {file_path}")
            return False

        if not os.access(file_path, os.R_OK):
            print(f"❌ Cannot read: {file_path}")
            return False

    print("✅ File permissions are correct")
    return True


def main():
    """Main validation function"""
    print("🔍 Password Manager - Setup Validation")
    print("=" * 50)

    validations = [
        ("Requirements File", validate_requirements_file),
        ("Setup Configuration", validate_setup_py),
        ("Package Structure", validate_package_structure),
        ("Basic Imports", test_basic_imports),
        ("Basic Functionality", test_basic_functionality),
        ("File Permissions", validate_file_permissions),
    ]

    all_passed = True
    for validation_name, validation_func in validations:
        print(f"\n📋 {validation_name}:")
        if not validation_func():
            all_passed = False

    if all_passed:
        print("\n✅ All validations passed!")
        print("🚀 Project is ready to run!")
        return 0
    else:
        print("\n❌ Some validations failed!")
        print("\n💡 Common fixes:")
        print("1. Ensure you're in the project root directory")
        print("2. Install dependencies: pip install -r requirements.txt")
        print("3. Check file permissions")
        print("4. Verify Python version (3.8+)")
        return 1


if __name__ == "__main__":
    sys.exit(main())
