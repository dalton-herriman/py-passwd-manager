#!/usr/bin/env python3
"""
Test script to verify GUI refresh functionality
"""

import sys
import os
from pathlib import Path

# Add the project root to the path
sys.path.insert(0, str(Path(__file__).parent.parent))

from pm_core.vault_manager import VaultManager


def test_gui_refresh():
    """Test that entries are properly added and visible"""
    print("🧪 Testing GUI Refresh Functionality")
    print("=" * 50)

    # Create a test directory
    test_dir = "test_gui_vaults"
    if os.path.exists(test_dir):
        import shutil

        shutil.rmtree(test_dir)

    # Initialize vault manager
    vm = VaultManager(test_dir)

    print("1. Creating test vault...")
    vm.create_vault("TestVault", "testpass123", "Test vault for GUI refresh")

    print("2. Opening vault...")
    pm = vm.open_vault("TestVault", "testpass123")

    print("3. Adding test entries...")

    # Add first entry
    entry1 = pm.add_entry(
        service="TestService1",
        username="user1",
        password="pass1",
        url="https://test1.com",
        notes="First test entry",
    )
    print(f"✅ Added entry: {entry1.name} (ID: {entry1.id})")

    # Check entries immediately after adding
    entries = pm.get_entry()
    print(f"📋 Vault now has {len(entries)} entries:")
    for entry in entries:
        print(f"   - {entry.name} (ID: {entry.id})")

    # Add second entry
    entry2 = pm.add_entry(
        service="TestService2",
        username="user2",
        password="pass2",
        url="https://test2.com",
        notes="Second test entry",
    )
    print(f"✅ Added entry: {entry2.name} (ID: {entry2.id})")

    # Check entries again
    entries = pm.get_entry()
    print(f"📋 Vault now has {len(entries)} entries:")
    for entry in entries:
        print(f"   - {entry.name} (ID: {entry.id})")

    print("4. Saving vault...")
    pm.save_vault("testpass123")

    print("5. Checking entries after save...")
    entries = pm.get_entry()
    print(f"📋 Vault has {len(entries)} entries after save:")
    for entry in entries:
        print(f"   - {entry.name} (ID: {entry.id})")

    print("6. Closing and reopening vault...")
    vm.close_vault()
    pm = vm.open_vault("TestVault", "testpass123")

    print("7. Checking entries after reopen...")
    entries = pm.get_entry()
    print(f"📋 Vault has {len(entries)} entries after reopen:")
    for entry in entries:
        print(f"   - {entry.name} (ID: {entry.id})")

    print("\n🎉 Test completed!")
    print(
        "If you see all entries in steps 3, 5, and 7, the functionality is working correctly."
    )
    print(
        "If entries are missing in any step, there's an issue with the save/load process."
    )


if __name__ == "__main__":
    test_gui_refresh()
