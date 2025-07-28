#!/usr/bin/env python3
"""
Multi-vault GUI application for the password manager
Modular version with separated components
"""

import tkinter as tk
from .main_app import MultiVaultPasswordManagerGUI


def main():
    """Main entry point for the GUI application"""
    root = tk.Tk()
    app = MultiVaultPasswordManagerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
