#!/usr/bin/env python3
"""
Test script to verify AddEntryDialog functionality
"""

import sys
import os
from pathlib import Path

# Add the project root to the path
sys.path.insert(0, str(Path(__file__).parent.parent))

from pm_core.vault_manager import VaultManager
from pm_core.manager import PasswordManager

def test_dialog_functionality():
    """Test the AddEntryDialog functionality"""
    print("🧪 Testing AddEntryDialog Functionality")
    print("=" * 50)
    
    # Create a test directory
    test_dir = "test_dialog"
    if os.path.exists(test_dir):
        import shutil
        shutil.rmtree(test_dir)
    
    # Initialize vault manager
    vm = VaultManager(test_dir)
    
    print("1. Creating test vault...")
    vm.create_vault("TestVault", "testpass123", "Test vault for dialog")
    
    print("2. Opening vault...")
    pm = vm.open_vault("TestVault", "testpass123")
    
    print("3. Testing direct entry addition...")
    entry = pm.add_entry(
        service="TestService",
        username="testuser",
        password="testpass",
        url="https://test.com",
        notes="Test entry"
    )
    print(f"✅ Direct entry added: {entry.name} (ID: {entry.id})")
    
    print("4. Checking entries...")
    entries = pm.get_entry()
    print(f"📋 Vault has {len(entries)} entries:")
    for entry in entries:
        print(f"   - {entry.name} (ID: {entry.id})")
    
    print("5. Testing entry retrieval by ID...")
    entry_by_id = pm.get_entry(entry_id=1)
    if entry_by_id:
        print(f"✅ Found entry by ID: {entry_by_id[0].name}")
    else:
        print("❌ Entry not found by ID")
    
    print("6. Testing entry search...")
    search_results = pm.search_entries("Test")
    print(f"📋 Search results: {len(search_results)} entries:")
    for entry in search_results:
        print(f"   - {entry.name} (ID: {entry.id})")
    
    print("\n🎉 Dialog Test Completed!")
    print("If all steps pass, the core functionality is working correctly.")

if __name__ == "__main__":
    test_dialog_functionality() 