#!/usr/bin/env python3
"""
Main entry point for the password manager
"""

import sys
import argparse
from pathlib import Path


def main():
    """Main entry point for the password manager"""
    parser = argparse.ArgumentParser(
        description="Secure password manager with CLI and GUI interfaces",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m py-passwd-manager --gui          # Launch GUI
  python -m py-passwd-manager create         # Create vault (CLI)
  python -m py-passwd-manager unlock         # Unlock vault (CLI)
        """,
    )

    parser.add_argument(
        "--gui", action="store_true", help="Launch the graphical user interface"
    )

    parser.add_argument(
        "--vault-path",
        default="vault.db",
        help="Path to the vault file (default: vault.db)",
    )

    # Parse known args to handle --gui separately
    args, remaining = parser.parse_known_args()

    if args.gui:
        # Launch GUI
        try:
            from gui.app import main as gui_main

            gui_main()
        except ImportError as e:
            print(f"Error: Could not import GUI module: {e}")
            print("Make sure you're running from the project root directory")
            sys.exit(1)
        except Exception as e:
            print(f"Error launching GUI: {e}")
            sys.exit(1)
    else:
        # Launch CLI with remaining arguments
        try:
            from cli.multi_vault_cli import main as cli_main

            # Set up sys.argv for Click
            sys.argv = [sys.argv[0]] + remaining
            cli_main()
        except ImportError as e:
            print(f"Error: Could not import CLI module: {e}")
            print("Make sure you're running from the project root directory")
            sys.exit(1)
        except Exception as e:
            print(f"Error launching CLI: {e}")
            sys.exit(1)


if __name__ == "__main__":
    main()
