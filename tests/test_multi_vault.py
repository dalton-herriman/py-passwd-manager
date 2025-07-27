"""
Tests for multi-vault functionality
"""

import pytest
import tempfile
import os
from pathlib import Path

from pm_core.vault_manager import VaultManager, VaultInfo


class TestVaultManager:
    def setup_method(self):
        """Setup test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.vault_manager = VaultManager(self.temp_dir)

    def teardown_method(self):
        """Cleanup test environment"""
        import shutil

        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_create_vault(self):
        """Test creating a new vault"""
        # Create vault
        self.vault_manager.create_vault("test_vault", "test_password", "Test vault")

        # Check if vault exists
        assert self.vault_manager.vault_exists("test_vault")

        # Check vault info
        vault_info = self.vault_manager.get_vault_info("test_vault")
        assert vault_info is not None
        assert vault_info.name == "test_vault"
        assert vault_info.entry_count == 0

    def test_list_vaults(self):
        """Test listing vaults"""
        # Create multiple vaults
        self.vault_manager.create_vault("vault1", "password1")
        self.vault_manager.create_vault("vault2", "password2")

        # List vaults
        vaults = self.vault_manager.list_vaults()
        assert len(vaults) == 2

        vault_names = [v.name for v in vaults]
        assert "vault1" in vault_names
        assert "vault2" in vault_names

    def test_open_vault(self):
        """Test opening a vault"""
        # Create vault
        self.vault_manager.create_vault("test_vault", "test_password")

        # Open vault
        pm = self.vault_manager.open_vault("test_vault", "test_password")

        # Check if vault is open
        assert self.vault_manager.get_current_vault() is not None
        assert self.vault_manager.get_current_vault_name() == "test_vault"
        assert pm.is_unlocked

    def test_close_vault(self):
        """Test closing a vault"""
        # Create and open vault
        self.vault_manager.create_vault("test_vault", "test_password")
        self.vault_manager.open_vault("test_vault", "test_password")

        # Close vault
        self.vault_manager.close_vault()

        # Check if vault is closed
        assert self.vault_manager.get_current_vault() is None
        assert self.vault_manager.get_current_vault_name() is None

    def test_delete_vault(self):
        """Test deleting a vault"""
        # Create vault
        self.vault_manager.create_vault("test_vault", "test_password")
        assert self.vault_manager.vault_exists("test_vault")

        # Delete vault
        self.vault_manager.delete_vault("test_vault")

        # Check if vault is deleted
        assert not self.vault_manager.vault_exists("test_vault")

    def test_rename_vault(self):
        """Test renaming a vault"""
        # Create vault
        self.vault_manager.create_vault("old_name", "test_password")

        # Rename vault
        self.vault_manager.rename_vault("old_name", "new_name")

        # Check if vault is renamed
        assert not self.vault_manager.vault_exists("old_name")
        assert self.vault_manager.vault_exists("new_name")

    def test_vault_operations_with_entries(self):
        """Test vault operations with entries"""
        # Create vault
        self.vault_manager.create_vault("test_vault", "test_password")

        # Open vault
        pm = self.vault_manager.open_vault("test_vault", "test_password")

        # Add entry
        entry = pm.add_entry(
            service="Test Service",
            username="testuser",
            password="testpass",
            url="https://test.com",
            notes="Test entry",
        )

        # Save vault
        pm.save_vault("test_password")

        # Close vault
        self.vault_manager.close_vault()

        # Reopen vault
        pm = self.vault_manager.open_vault("test_vault", "test_password")

        # Check if entry exists
        entries = pm.get_entry()
        assert len(entries) == 1
        assert entries[0].name == "Test Service"
        assert entries[0].username == "testuser"

    def test_multiple_vaults_isolation(self):
        """Test that multiple vaults are isolated from each other"""
        # Create two vaults
        self.vault_manager.create_vault("vault1", "password1")
        self.vault_manager.create_vault("vault2", "password2")

        # Open first vault and add entry
        pm1 = self.vault_manager.open_vault("vault1", "password1")
        entry1 = pm1.add_entry(service="Service1", username="user1", password="pass1")
        pm1.save_vault("password1")
        self.vault_manager.close_vault()

        # Open second vault and add entry
        pm2 = self.vault_manager.open_vault("vault2", "password2")
        entry2 = pm2.add_entry(service="Service2", username="user2", password="pass2")
        pm2.save_vault("password2")
        self.vault_manager.close_vault()

        # Verify entries are isolated
        pm1 = self.vault_manager.open_vault("vault1", "password1")
        entries1 = pm1.get_entry()
        assert len(entries1) == 1
        assert entries1[0].name == "Service1"
        self.vault_manager.close_vault()

        pm2 = self.vault_manager.open_vault("vault2", "password2")
        entries2 = pm2.get_entry()
        assert len(entries2) == 1
        assert entries2[0].name == "Service2"
        self.vault_manager.close_vault()


class TestVaultInfo:
    def test_vault_info_creation(self):
        """Test VaultInfo creation"""
        from datetime import datetime

        info = VaultInfo(
            name="test_vault",
            path="/path/to/vault.db",
            created_at=datetime.now(),
            entry_count=5,
            last_accessed=datetime.now(),
        )

        assert info.name == "test_vault"
        assert info.path == "/path/to/vault.db"
        assert info.entry_count == 5

    def test_vault_info_serialization(self):
        """Test VaultInfo serialization"""
        from datetime import datetime

        now = datetime.now()
        info = VaultInfo(
            name="test_vault",
            path="/path/to/vault.db",
            created_at=now,
            entry_count=5,
            last_accessed=now,
        )

        # Convert to dict
        data = info.to_dict()
        assert data["name"] == "test_vault"
        assert data["path"] == "/path/to/vault.db"
        assert data["entry_count"] == 5

        # Convert back from dict
        new_info = VaultInfo.from_dict(data)
        assert new_info.name == info.name
        assert new_info.path == info.path
        assert new_info.entry_count == info.entry_count
