#!/usr/bin/env python3
"""
Quick start script with error handling and helpful guidance
"""

import sys
import os
import subprocess
import importlib
from pathlib import Path


def print_banner():
    """Print project banner"""
    print("🔐 Password Manager - Quick Start")
    print("=" * 50)


def check_environment():
    """Check if environment is properly set up"""
    print("🔍 Checking environment...")

    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required")
        print(f"   Current version: {sys.version}")
        return False

    # Check if we're in the right directory
    if not os.path.exists("pm_core") or not os.path.exists("cli"):
        print("❌ Not in project root directory")
        print("   Please run from the py-passwd-manager directory")
        return False

    print("✅ Environment looks good")
    return True


def install_dependencies():
    """Install dependencies if needed"""
    print("\n📦 Checking dependencies...")

    required_packages = ["click", "cryptography", "argon2", "pyperclip"]
    missing_packages = []

    for package in required_packages:
        try:
            importlib.import_module(package)
            print(f"✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} - MISSING")

    if missing_packages:
        print(f"\n📦 Installing missing packages...")
        try:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"]
            )
            print("✅ Dependencies installed")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install dependencies: {e}")
            print("   Try: pip install -r requirements.txt")
            return False

    return True


def run_cli_demo():
    """Run a CLI demo to show the application works"""
    print("\n💻 Running CLI demo...")

    try:
        # Create a demo vault
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "cli.main",
                "create",
                "--master-password",
                "demo123",
            ],
            capture_output=True,
            text=True,
        )

        if result.returncode == 0:
            print("✅ CLI demo successful")
            return True
        else:
            print(f"❌ CLI demo failed: {result.stderr}")
            return False

    except Exception as e:
        print(f"❌ CLI demo error: {e}")
        return False


def show_usage_examples():
    """Show usage examples"""
    print("\n📚 Usage Examples:")
    print("=" * 30)

    examples = [
        ("Create vault", "python -m cli.main create --master-password your_password"),
        ("Unlock vault", "python -m cli.main unlock --master-password your_password"),
        (
            "Add entry",
            "python -m cli.main add --service Gmail --username user@gmail.com",
        ),
        ("Generate password", "python -m cli.main generate --length 16 --copy"),
        ("Launch GUI", "python -m gui.app"),
        ("Run tests", "python -m pytest tests/"),
    ]

    for description, command in examples:
        print(f"  {description}:")
        print(f"    {command}")
        print()


def show_troubleshooting():
    """Show common troubleshooting tips"""
    print("\n🔧 Troubleshooting:")
    print("=" * 20)

    tips = [
        "If you get 'ModuleNotFoundError':",
        "  - Make sure you're in the project root directory",
        "  - Run: pip install -r requirements.txt",
        "",
        "If CLI doesn't work:",
        "  - Try: python -m cli.main --help",
        "  - Check if vault.db already exists",
        "",
        "If GUI doesn't work:",
        "  - Try: python -m gui.app",
        "  - Check if tkinter is available",
        "",
        "If tests fail:",
        "  - Run: python scripts/run_tests.py",
        "  - Check Python version (3.8+)",
        "",
        "For more help:",
        "  - Check README.md",
        "  - Run validation: python scripts/validate_setup.py",
    ]

    for tip in tips:
        print(f"  {tip}")


def main():
    """Main quick start function"""
    print_banner()

    # Check environment
    if not check_environment():
        print("\n❌ Environment check failed")
        show_troubleshooting()
        return 1

    # Install dependencies
    if not install_dependencies():
        print("\n❌ Dependency installation failed")
        show_troubleshooting()
        return 1

    # Run demo
    if not run_cli_demo():
        print("\n❌ Demo failed")
        show_troubleshooting()
        return 1

    print("\n🎉 Quick start successful!")
    show_usage_examples()

    print("🚀 You're ready to use the password manager!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
