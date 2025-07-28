#!/usr/bin/env python3
"""
GUI package for the Password Manager
Modular components for better organization
"""

from .main_app import MultiVaultPasswordManagerGUI
from .dialogs import (
    CreateVaultDialog,
    AddEntryDialog,
    EditEntryDialog,
    GeneratePasswordDialog
)
from .components import (
    SearchBox,
    StatusBar,
    ToolBar,
    TreeViewManager,
    DialogBase
)
from .events import EventHandler

__all__ = [
    'MultiVaultPasswordManagerGUI',
    'CreateVaultDialog',
    'AddEntryDialog', 
    'EditEntryDialog',
    'GeneratePasswordDialog',
    'SearchBox',
    'StatusBar',
    'ToolBar',
    'TreeViewManager',
    'DialogBase',
    'EventHandler'
]
