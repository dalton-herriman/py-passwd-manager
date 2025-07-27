#!/usr/bin/env python3
"""
Create a test vault with known password for GUI testing
"""

import sys
import os
from pathlib import Path

# Add the project root to the path
sys.path.insert(0, str(Path(__file__).parent.parent))

from pm_core.vault_manager import VaultManager

def create_test_vault():
    """Create a test vault with known password"""
    print("🧪 Creating Test Vault")
    print("=" * 50)
    
    try:
        # Initialize vault manager
        vm = VaultManager()
        print("DEBUG: VaultManager initialized")
        
        # Create a test vault
        vault_name = "DemoVault"
        master_password = "testpass123"
        
        print(f"Creating vault: {vault_name}")
        vm.create_vault(vault_name, master_password, "Test vault for GUI")
        print(f"✅ Vault '{vault_name}' created successfully")
        
        # Open the vault
        print(f"Opening vault: {vault_name}")
        pm = vm.open_vault(vault_name, master_password)
        print(f"✅ Vault '{vault_name}' opened successfully")
        
        # Add some test entries
        print("Adding test entries...")
        
        entry1 = pm.add_entry(
            service="Gmail",
            username="test@gmail.com",
            password="testpass123",
            url="https://gmail.com",
            notes="Test Gmail account"
        )
        print(f"✅ Added entry: {entry1.name}")
        
        entry2 = pm.add_entry(
            service="GitHub",
            username="testuser",
            password="githubpass456",
            url="https://github.com",
            notes="Test GitHub account"
        )
        print(f"✅ Added entry: {entry2.name}")
        
        # Save the vault
        print("Saving vault...")
        pm.save_vault(master_password)
        
        # Update entry count in registry
        entry_count = len(pm.get_entry())
        vm.update_vault_entry_count(vault_name, entry_count)
        print(f"✅ Vault saved successfully with {entry_count} entries")
        
        # Close the vault
        vm.close_vault()
        print("✅ Vault closed")
        
        # List vaults to verify
        vaults = vm.list_vaults()
        print(f"\n📋 Available vaults: {len(vaults)}")
        for vault in vaults:
            print(f"   - {vault.name} ({vault.entry_count} entries)")
        
        print(f"\n🎉 Test vault created successfully!")
        print(f"Vault name: {vault_name}")
        print(f"Master password: {master_password}")
        print(f"Entries: 2 (Gmail, GitHub)")
        
    except Exception as e:
        print(f"❌ Error creating test vault: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    create_test_vault() 