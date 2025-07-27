#!/usr/bin/env python3
"""
Demo script for multi-vault functionality
"""

import sys
import os
from pathlib import Path

# Add the project root to the path
sys.path.insert(0, str(Path(__file__).parent.parent))

from pm_core.vault_manager import VaultManager


def demo_multi_vault():
    """Demonstrate multi-vault functionality"""
    print("🔐 Multi-Vault Password Manager Demo")
    print("=" * 50)

    # Create a temporary directory for demo
    demo_dir = "demo_vaults"
    if os.path.exists(demo_dir):
        import shutil

        shutil.rmtree(demo_dir)

    # Initialize vault manager
    vm = VaultManager(demo_dir)

    print("\n1. Creating vaults...")

    # Create personal vault
    vm.create_vault("Personal", "personal123", "Personal passwords")
    print("✅ Created 'Personal' vault")

    # Create work vault
    vm.create_vault("Work", "work456", "Work-related passwords")
    print("✅ Created 'Work' vault")

    # Create family vault
    vm.create_vault("Family", "family789", "Family shared passwords")
    print("✅ Created 'Family' vault")

    print("\n2. Listing vaults...")
    vaults = vm.list_vaults()
    for vault in vaults:
        print(f"   📁 {vault.name} - {vault.entry_count} entries")

    print("\n3. Adding entries to Personal vault...")

    # Open personal vault
    pm_personal = vm.open_vault("Personal", "personal123")

    # Add entries to personal vault
    entry1 = pm_personal.add_entry(
        service="Gmail",
        username="user@gmail.com",
        password="securepass123",
        url="https://gmail.com",
        notes="Personal email account",
    )
    print(f"✅ Added entry: {entry1.name}")

    entry2 = pm_personal.add_entry(
        service="GitHub",
        username="developer",
        password="githubpass456",
        url="https://github.com",
        notes="Personal GitHub account",
    )
    print(f"✅ Added entry: {entry2.name}")

    # Save personal vault
    pm_personal.save_vault("personal123")
    vm.update_vault_entry_count("Personal", len(pm_personal.get_entry()))
    print("✅ Saved Personal vault")

    # Close personal vault
    vm.close_vault()

    print("\n4. Adding entries to Work vault...")

    # Open work vault
    pm_work = vm.open_vault("Work", "work456")

    # Add entries to work vault
    entry3 = pm_work.add_entry(
        service="Company Email",
        username="employee@company.com",
        password="workpass789",
        url="https://mail.company.com",
        notes="Work email account",
    )
    print(f"✅ Added entry: {entry3.name}")

    entry4 = pm_work.add_entry(
        service="VPN",
        username="vpn_user",
        password="vpnpass123",
        url="https://vpn.company.com",
        notes="Company VPN access",
    )
    print(f"✅ Added entry: {entry4.name}")

    # Save work vault
    pm_work.save_vault("work456")
    vm.update_vault_entry_count("Work", len(pm_work.get_entry()))
    print("✅ Saved Work vault")

    # Close work vault
    vm.close_vault()

    print("\n5. Adding entries to Family vault...")

    # Open family vault
    pm_family = vm.open_vault("Family", "family789")

    # Add entries to family vault
    entry5 = pm_family.add_entry(
        service="Netflix",
        username="family@email.com",
        password="netflixpass456",
        url="https://netflix.com",
        notes="Family Netflix account",
    )
    print(f"✅ Added entry: {entry5.name}")

    # Save family vault
    pm_family.save_vault("family789")
    vm.update_vault_entry_count("Family", len(pm_family.get_entry()))
    print("✅ Saved Family vault")

    # Close family vault
    vm.close_vault()

    print("\n6. Final vault status...")
    # Open each vault briefly to update entry counts
    vault_passwords = {
        "Personal": "personal123",
        "Work": "work456",
        "Family": "family789",
    }

    for vault_name in ["Personal", "Work", "Family"]:
        try:
            pm = vm.open_vault(vault_name, vault_passwords[vault_name])
            vm.close_vault()
        except Exception as e:
            print(f"   ⚠️  Could not open {vault_name} vault: {e}")

    vaults = vm.list_vaults()
    for vault in vaults:
        print(f"   📁 {vault.name} - {vault.entry_count} entries")

    print("\n7. Demonstrating vault isolation...")

    # Open personal vault and show entries
    pm_personal = vm.open_vault("Personal", "personal123")
    personal_entries = pm_personal.get_entry()
    print(f"   Personal vault has {len(personal_entries)} entries:")
    for entry in personal_entries:
        print(f"     - {entry.name} ({entry.username})")
    vm.close_vault()

    # Open work vault and show entries
    pm_work = vm.open_vault("Work", "work456")
    work_entries = pm_work.get_entry()
    print(f"   Work vault has {len(work_entries)} entries:")
    for entry in work_entries:
        print(f"     - {entry.name} ({entry.username})")
    vm.close_vault()

    # Open family vault and show entries
    pm_family = vm.open_vault("Family", "family789")
    family_entries = pm_family.get_entry()
    print(f"   Family vault has {len(family_entries)} entries:")
    for entry in family_entries:
        print(f"     - {entry.name} ({entry.username})")
    vm.close_vault()

    print("\n8. Vault management operations...")

    # Rename a vault
    vm.rename_vault("Family", "Shared")
    print("✅ Renamed 'Family' vault to 'Shared'")

    # Open the renamed vault to update entry count
    try:
        pm = vm.open_vault("Shared", "family789")
        vm.close_vault()
    except Exception as e:
        print(f"   ⚠️  Could not open Shared vault: {e}")

    # List vaults again
    vaults = vm.list_vaults()
    for vault in vaults:
        print(f"   📁 {vault.name} - {vault.entry_count} entries")

    print("\n🎉 Demo completed successfully!")
    print(f"📁 Demo vaults created in: {demo_dir}")
    print("\nTo try the GUI:")
    print("  .\\run.ps1 gui-multi")
    print("\nTo try the CLI:")
    print("  .\\run.ps1 cli-multi")


if __name__ == "__main__":
    demo_multi_vault()
