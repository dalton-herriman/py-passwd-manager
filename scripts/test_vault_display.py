#!/usr/bin/env python3
"""
Test script to verify vault display functionality
"""

import sys
import os
from pathlib import Path

# Add the project root to the path
sys.path.insert(0, str(Path(__file__).parent.parent))

from pm_core.vault_manager import VaultManager

def test_vault_display():
    """Test vault display functionality"""
    print("🧪 Testing Vault Display Functionality")
    print("=" * 50)
    
    try:
        # Initialize vault manager
        vm = VaultManager()
        print("DEBUG: VaultManager initialized")
        
        # List vaults
        vaults = vm.list_vaults()
        print(f"DEBUG: Found {len(vaults)} vaults")
        
        for vault in vaults:
            print(f"📁 Vault: {vault.name}")
            print(f"   Path: {vault.path}")
            print(f"   Entries: {vault.entry_count}")
            print(f"   Created: {vault.created_at}")
            print(f"   Last accessed: {vault.last_accessed}")
            print()
        
        # Test opening a vault
        if vaults:
            first_vault = vaults[0]
            print(f"Testing opening vault: {first_vault.name}")
            
            try:
                pm = vm.open_vault(first_vault.name, "testpass123")
                print(f"✅ Successfully opened vault: {first_vault.name}")
                
                entries = pm.get_entry()
                print(f"📋 Vault has {len(entries)} entries")
                
                vm.close_vault()
                print("✅ Successfully closed vault")
                
            except Exception as e:
                print(f"❌ Failed to open vault: {e}")
        
        print("\n🎉 Vault Display Test Completed!")
        
    except Exception as e:
        print(f"❌ Error in test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_vault_display() 