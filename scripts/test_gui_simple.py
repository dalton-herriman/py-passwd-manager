#!/usr/bin/env python3
"""
Simple test to verify GUI refresh issue
"""

import sys
import os
from pathlib import Path

# Add the project root to the path
sys.path.insert(0, str(Path(__file__).parent.parent))

from pm_core.vault_manager import VaultManager

def test_gui_refresh_issue():
    """Test to reproduce the GUI refresh issue"""
    print("🧪 Testing GUI Refresh Issue")
    print("=" * 50)
    
    # Create a test directory
    test_dir = "test_gui_debug"
    if os.path.exists(test_dir):
        import shutil
        shutil.rmtree(test_dir)
    
    # Initialize vault manager
    vm = VaultManager(test_dir)
    
    print("1. Creating test vault...")
    vm.create_vault("TestVault", "testpass123", "Test vault for GUI debug")
    
    print("2. Opening vault...")
    pm = vm.open_vault("TestVault", "testpass123")
    
    print("3. Adding test entry...")
    entry = pm.add_entry(
        service="TestService",
        username="testuser",
        password="testpass",
        url="https://test.com",
        notes="Test entry"
    )
    print(f"✅ Added entry: {entry.name} (ID: {entry.id})")
    
    print("4. Checking entries before save...")
    entries = pm.get_entry()
    print(f"📋 Vault has {len(entries)} entries before save:")
    for entry in entries:
        print(f"   - {entry.name} (ID: {entry.id})")
    
    print("5. Saving vault...")
    pm.save_vault("testpass123")
    
    print("6. Checking entries after save...")
    entries = pm.get_entry()
    print(f"📋 Vault has {len(entries)} entries after save:")
    for entry in entries:
        print(f"   - {entry.name} (ID: {entry.id})")
    
    print("7. Closing and reopening vault...")
    vm.close_vault()
    pm = vm.open_vault("TestVault", "testpass123")
    
    print("8. Checking entries after reopen...")
    entries = pm.get_entry()
    print(f"📋 Vault has {len(entries)} entries after reopen:")
    for entry in entries:
        print(f"   - {entry.name} (ID: {entry.id})")
    
    print("\n🎉 Test completed!")
    print("If entries are missing in any step, there's an issue with the save/load process.")

if __name__ == "__main__":
    test_gui_refresh_issue() 