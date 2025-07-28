#!/usr/bin/env python3
"""
Test script for the modular GUI components
"""

import sys
import tkinter as tk
from tkinter import messagebox

def test_imports():
    """Test that all modular components can be imported"""
    try:
        from .main_app import MultiVaultPasswordManagerGUI
        from .dialogs import CreateVaultDialog, AddEntryDialog, EditEntryDialog, GeneratePasswordDialog
        from .components import SearchBox, StatusBar, ToolBar, TreeViewManager, DialogBase
        from .events import EventHandler
        print("✅ All modular components imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_gui_creation():
    """Test that the GUI can be created"""
    try:
        root = tk.Tk()
        root.withdraw()  # Hide the window
        
        from .main_app import MultiVaultPasswordManagerGUI
        app = MultiVaultPasswordManagerGUI(root)
        
        print("✅ GUI created successfully")
        root.destroy()
        return True
    except Exception as e:
        print(f"❌ GUI creation error: {e}")
        return False

def test_components():
    """Test individual components"""
    try:
        root = tk.Tk()
        root.withdraw()
        
        from .components import SearchBox, StatusBar, ToolBar, TreeViewManager
        
        # Test SearchBox
        search = SearchBox(root)
        search.get_value()
        search.clear()
        
        # Test StatusBar
        status = StatusBar(root)
        status.set_status("Test status")
        status.show_progress()
        status.hide_progress()
        
        # Test ToolBar
        toolbar = ToolBar(root)
        toolbar.add_button("Test", lambda: None)
        toolbar.add_separator()
        
        print("✅ All components created successfully")
        root.destroy()
        return True
    except Exception as e:
        print(f"❌ Component test error: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing modular GUI structure...")
    print()
    
    tests = [
        ("Import Test", test_imports),
        ("GUI Creation Test", test_gui_creation),
        ("Component Test", test_components)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"Running {test_name}...")
        if test_func():
            passed += 1
        print()
    
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Modular structure is working correctly.")
        return True
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 