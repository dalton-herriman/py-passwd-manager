#!/usr/bin/env python3
"""
Test script to debug GUI refresh issue by simulating the exact flow
"""

import sys
import os
from pathlib import Path

# Add the project root to the path
sys.path.insert(0, str(Path(__file__).parent.parent))

from pm_core.vault_manager import VaultManager


def test_gui_flow():
    """Test the exact GUI flow to identify the refresh issue"""
    print("🧪 Testing GUI Flow (Simulating Add Entry Process)")
    print("=" * 60)

    # Create a test directory
    test_dir = "test_gui_flow"
    if os.path.exists(test_dir):
        import shutil

        shutil.rmtree(test_dir)

    # Initialize vault manager
    vm = VaultManager(test_dir)

    print("1. Creating test vault...")
    vm.create_vault("TestVault", "testpass123", "Test vault for GUI flow")

    print("2. Opening vault...")
    pm = vm.open_vault("TestVault", "testpass123")

    print("3. Checking initial entries...")
    entries = pm.get_entry()
    print(f"📋 Initial entries: {len(entries)}")

    print("4. Adding test entry (simulating GUI add_entry)...")
    entry = pm.add_entry(
        service="TestService",
        username="testuser",
        password="testpass",
        url="https://test.com",
        notes="Test entry",
    )
    print(f"✅ Entry added: {entry.name} (ID: {entry.id})")

    print("5. Checking entries immediately after add...")
    entries = pm.get_entry()
    print(f"📋 Entries after add: {len(entries)}")
    for entry in entries:
        print(f"   - {entry.name} (ID: {entry.id})")

    print("6. Saving vault (simulating GUI save)...")
    pm.save_vault("testpass123")

    print("7. Checking entries after save...")
    entries = pm.get_entry()
    print(f"📋 Entries after save: {len(entries)}")
    for entry in entries:
        print(f"   - {entry.name} (ID: {entry.id})")

    print("8. Simulating GUI refresh_entries()...")
    # This is what the GUI does in refresh_entries()
    search_query = ""  # No search filter
    if search_query:
        entries = pm.search_entries(search_query)
    else:
        entries = pm.get_entry()

    print(f"📋 Entries found by refresh: {len(entries)}")
    for entry in entries:
        print(f"   - {entry.name} (ID: {entry.id})")

    print("9. Simulating GUI update_entries_tree()...")
    # This is what the GUI does in update_entries_tree()
    current_entries = entries
    print(f"📋 Processing {len(current_entries)} entries for treeview")
    for entry in current_entries:
        values = (
            entry.id,
            entry.name,
            entry.username or "",
            entry.url or "",
            entry.created_at.strftime("%Y-%m-%d %H:%M"),
        )
        print(f"   - Adding to treeview: {values}")

    print("\n🎉 GUI Flow Test Completed!")
    print(
        "If entries are missing in steps 5, 7, or 8, there's an issue with the data flow."
    )
    print(
        "If entries are present in all steps, the issue is in the GUI treeview display."
    )


if __name__ == "__main__":
    test_gui_flow()
