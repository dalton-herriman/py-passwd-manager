#!/usr/bin/env python3
"""
Command runner package for the Password Manager
Extracted from the massive run.py file
"""

from .command_registry import CommandRegistry
from .command_handlers import (
    SetupCommands,
    TestCommands,
    RunCommands,
    UtilityCommands
)

__all__ = [
    'CommandRegistry',
    'SetupCommands',
    'TestCommands', 
    'RunCommands',
    'UtilityCommands'
] 