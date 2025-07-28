#!/usr/bin/env python3
"""
Basic tests for the password manager
"""

import pytest
import tempfile
import os
import json
from datetime import datetime

from pm_core.manager import PasswordManager
from pm_core.utils import generate_password, validate_password_strength
from pm_core.models_pydantic import Entry, Vault
from pm_core.exceptions import VaultError, StorageError, AuthenticationError


def temp_vault_path():
    temp_dir = tempfile.mkdtemp()
    vault_path = os.path.join(temp_dir, "test_vault.db")
    yield vault_path
    if os.path.exists(vault_path):
        os.remove(vault_path)
    os.rmdir(temp_dir)


@pytest.fixture
def vault_path():
    yield from temp_vault_path()


@pytest.fixture
def pm(vault_path):
    return PasswordManager(vault_path)


def test_create_vault(pm):
    assert not pm.is_vault_exists()
    pm.create_vault("test_password")
    assert pm.is_vault_exists()
    assert pm.is_unlocked


def test_unlock_vault(pm):
    pm.create_vault("test_password")
    pm.lock_vault()
    pm.unlock_vault("test_password")
    assert pm.is_unlocked


def test_lock_vault(pm):
    pm.create_vault("test_password")
    pm.lock_vault()
    assert not pm.is_unlocked
    assert pm.vault is None
    # Should not be able to get entries when locked
    with pytest.raises(VaultError):
        pm.get_entry()


def test_add_entry(pm):
    pm.create_vault("test_password")
    entry = pm.add_entry(
        service="Test Service",
        username="testuser",
        password="testpass",
        url="https://test.com",
        notes="Test notes",
    )
    assert entry is not None
    assert entry.name == "Test Service"
    assert entry.username == "testuser"
    assert entry.password == "testpass"
    assert entry.url == "https://test.com"
    assert entry.notes == "Test notes"


def test_get_entries(pm):
    pm.create_vault("test_password")
    pm.add_entry(service="Service 1", username="user1")
    pm.add_entry(service="Service 2", username="user2")
    entries = pm.get_entry()
    assert len(entries) == 2


def test_search_entries(pm):
    pm.create_vault("test_password")
    pm.add_entry(service="Gmail", username="user@gmail.com")
    pm.add_entry(service="GitHub", username="user")
    gmail_entries = pm.search_entries("gmail")
    assert len(gmail_entries) == 1
    assert gmail_entries[0].name == "Gmail"


def test_update_entry(pm):
    pm.create_vault("test_password")
    entry = pm.add_entry(service="Test", username="olduser")
    pm.update_entry(entry.id, username="newuser")
    updated_entries = pm.get_entry(entry_id=entry.id)
    assert len(updated_entries) == 1
    assert updated_entries[0].username == "newuser"


def test_delete_entry(pm):
    pm.create_vault("test_password")
    entry = pm.add_entry(service="Test", username="user")
    pm.delete_entry(entry.id)
    entries = pm.get_entry()
    assert len(entries) == 0


def test_generate_password():
    password = generate_password(length=16)
    assert len(password) == 16
    password_no_symbols = generate_password(length=12, include_symbols=False)
    assert len(password_no_symbols) == 12
    strength = validate_password_strength(password)
    assert "score" in strength
    assert "strength" in strength


def test_vault_stats(pm):
    pm.create_vault("test_password")
    pm.add_entry(service="Test 1")
    pm.add_entry(service="Test 2")
    stats = pm.get_vault_stats()
    assert stats["total_entries"] == 2
    assert "vault_created" in stats
    assert "last_updated" in stats


def test_export_entries(pm):
    pm.create_vault("test_password")
    pm.add_entry(service="Test", username="user", password="pass")
    exported = pm.export_entries()
    data = json.loads(exported)
    assert len(data) == 1
    assert data[0]["name"] == "Test"


def test_save_vault_and_reload(pm, vault_path):
    pm.create_vault("test_password")
    pm.add_entry(service="Test", username="user")
    pm.save_vault("test_password")
    pm.lock_vault()
    pm.unlock_vault("test_password")
    entries = pm.get_entry()
    assert len(entries) == 1
    assert entries[0].name == "Test"


def test_save_vault_not_unlocked(pm):
    with pytest.raises(VaultError):
        pm.save_vault("test_password")


def test_save_vault_missing_password(pm):
    pm.create_vault("test_password")
    with pytest.raises(ValueError):
        pm.save_vault()


def test_unlock_wrong_password(pm):
    pm.create_vault("test_password")
    pm.lock_vault()
    with pytest.raises(AuthenticationError):
        pm.unlock_vault("wrong_password")


def test_export_entries_unsupported_format(pm):
    pm.create_vault("test_password")
    with pytest.raises(ValueError):
        pm.export_entries("xml")


def test_generate_and_add_entry(pm):
    pm.create_vault("test_password")
    entry = pm.generate_and_add_entry("ServiceX", username="userx", password_length=20)
    assert entry is not None
    assert entry.name == "ServiceX"
    assert len(entry.password) == 20


def test_is_vault_exists_false(vault_path):
    pm = PasswordManager(vault_path)
    assert not pm.is_vault_exists()


def test_is_vault_exists_true(pm):
    pm.create_vault("test_password")
    assert pm.is_vault_exists()


def test_add_entry_locked(pm):
    pm.create_vault("test_password")
    pm.lock_vault()
    with pytest.raises(VaultError):
        pm.add_entry(service="Locked")


def test_update_entry_locked(pm):
    pm.create_vault("test_password")
    pm.lock_vault()
    with pytest.raises(VaultError):
        pm.update_entry(1, username="fail")


def test_delete_entry_locked(pm):
    pm.create_vault("test_password")
    pm.lock_vault()
    with pytest.raises(VaultError):
        pm.delete_entry(1)


def test_search_entries_locked(pm):
    pm.create_vault("test_password")
    pm.lock_vault()
    with pytest.raises(VaultError):
        pm.search_entries("foo")


def test_get_vault_stats_locked(pm):
    pm.create_vault("test_password")
    pm.lock_vault()
    with pytest.raises(VaultError):
        pm.get_vault_stats()


def test_export_entries_locked(pm):
    pm.create_vault("test_password")
    pm.lock_vault()
    with pytest.raises(VaultError):
        pm.export_entries()
