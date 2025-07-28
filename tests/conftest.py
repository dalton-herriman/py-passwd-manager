"""
Pytest configuration and shared fixtures
"""

import pytest
import tempfile
import os
import shutil
from pathlib import Path
from unittest.mock import Mock, patch

from pm_core.manager import PasswordManager
from pm_core.models_pydantic import Entry, Vault, Config


@pytest.fixture(scope="session")
def test_data_dir():
    """Create a temporary directory for test data"""
    temp_dir = tempfile.mkdtemp(prefix="pm_test_")
    yield temp_dir
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture
def temp_vault_path(test_data_dir):
    """Create a temporary vault file path"""
    vault_path = os.path.join(test_data_dir, f"test_vault_{os.getpid()}.db")
    yield vault_path
    if os.path.exists(vault_path):
        os.remove(vault_path)


@pytest.fixture
def password_manager(temp_vault_path):
    """Create a PasswordManager instance with temporary vault"""
    return PasswordManager(temp_vault_path)


@pytest.fixture
def unlocked_pm(password_manager):
    """Create an unlocked PasswordManager with test vault"""
    pm = password_manager
    pm.create_vault("test_master_password")
    return pm


@pytest.fixture
def sample_entries():
    """Sample entry data for testing"""
    return [
        {
            "service": "Gmail",
            "username": "user@gmail.com",
            "password": "secure_password_123",
            "url": "https://gmail.com",
            "notes": "Personal email account",
        },
        {
            "service": "GitHub",
            "username": "developer",
            "password": "github_token_456",
            "url": "https://github.com",
            "notes": "Work development account",
        },
        {
            "service": "Bank",
            "username": "user123",
            "password": "bank_password_789",
            "url": "https://bank.com",
            "notes": "Online banking",
        },
    ]


@pytest.fixture
def populated_vault(unlocked_pm, sample_entries):
    """Create a vault with sample entries"""
    pm = unlocked_pm
    entries = []
    for entry_data in sample_entries:
        entry = pm.add_entry(**entry_data)
        entries.append(entry)
    return pm, entries


@pytest.fixture
def mock_crypto():
    """Mock crypto functions for testing"""
    with patch("pm_core.crypto.generate_salt") as mock_salt, patch(
        "pm_core.crypto.derive_key"
    ) as mock_derive, patch("pm_core.crypto.encrypt_data") as mock_encrypt, patch(
        "pm_core.crypto.decrypt_data"
    ) as mock_decrypt:

        mock_salt.return_value = b"test_salt_16_bytes"
        mock_derive.return_value = b"test_key_32_bytes"
        mock_encrypt.return_value = b"encrypted_data"
        mock_decrypt.return_value = b"decrypted_data"

        yield {
            "salt": mock_salt,
            "derive": mock_derive,
            "encrypt": mock_encrypt,
            "decrypt": mock_decrypt,
        }


@pytest.fixture
def mock_storage():
    """Mock storage functions for testing"""
    with patch("pm_core.storage.SQLiteStorage") as mock_storage_class:
        mock_storage = Mock()
        mock_storage_class.return_value = mock_storage
        yield mock_storage


@pytest.fixture
def test_config():
    """Test configuration"""
    return Config(
        vault_path="test_vault.db",
        backup_enabled=True,
        auto_lock_timeout=300,
        clipboard_timeout=30,
        password_generator_length=16,
    )


# Performance testing fixtures
@pytest.fixture
def large_dataset():
    """Create a large dataset for performance testing"""
    entries = []
    for i in range(1000):
        entries.append(
            {
                "service": f"Service_{i}",
                "username": f"user_{i}",
                "password": f"password_{i}",
                "url": f"https://service{i}.com",
                "notes": f"Test entry {i}",
            }
        )
    return entries


# Security testing fixtures
@pytest.fixture
def weak_passwords():
    """List of weak passwords for testing"""
    return [
        "123456",
        "password",
        "qwerty",
        "abc123",
        "password123",
        "admin",
        "letmein",
        "welcome",
    ]


@pytest.fixture
def strong_passwords():
    """List of strong passwords for testing"""
    return [
        "K9#mP2$vL8@nR5!",
        "Xy7$qW3#mN9@pL2!",
        "Hj4#kL8$mN2@pQ6!",
        "Vb5#nM9$pQ3@rT7!",
        "Zc6#oP1$qR4@sU8!",
    ]


# CLI testing fixtures
@pytest.fixture
def cli_runner():
    """Click CLI runner for testing CLI commands"""
    from click.testing import CliRunner

    return CliRunner()


# GUI testing fixtures
@pytest.fixture
def mock_tkinter():
    """Mock tkinter for GUI testing"""
    with patch("tkinter.Tk") as mock_tk, patch("tkinter.ttk") as mock_ttk, patch(
        "tkinter.messagebox"
    ) as mock_messagebox:

        mock_root = Mock()
        mock_tk.return_value = mock_root

        yield {
            "tk": mock_tk,
            "ttk": mock_ttk,
            "messagebox": mock_messagebox,
            "root": mock_root,
        }


# Test markers for categorization
def pytest_configure(config):
    """Configure pytest with custom markers"""
    config.addinivalue_line("markers", "unit: Unit tests (fast, isolated)")
    config.addinivalue_line(
        "markers", "integration: Integration tests (slower, external dependencies)"
    )
    config.addinivalue_line("markers", "crypto: Cryptography and security tests")
    config.addinivalue_line("markers", "gui: GUI-related tests")
    config.addinivalue_line("markers", "cli: CLI-related tests")
    config.addinivalue_line("markers", "slow: Slow running tests")
    config.addinivalue_line("markers", "security: Security-focused tests")
    config.addinivalue_line("markers", "performance: Performance tests")


def pytest_collection_modifyitems(config, items):
    """Automatically categorize tests based on their names"""
    for item in items:
        # Mark crypto-related tests
        if any(
            keyword in item.nodeid.lower()
            for keyword in ["crypto", "encrypt", "decrypt", "hash"]
        ):
            item.add_marker(pytest.mark.crypto)

        # Mark GUI-related tests
        if any(
            keyword in item.nodeid.lower() for keyword in ["gui", "tkinter", "widget"]
        ):
            item.add_marker(pytest.mark.gui)

        # Mark CLI-related tests
        if any(
            keyword in item.nodeid.lower() for keyword in ["cli", "click", "command"]
        ):
            item.add_marker(pytest.mark.cli)

        # Mark performance tests
        if any(
            keyword in item.nodeid.lower()
            for keyword in ["performance", "benchmark", "speed"]
        ):
            item.add_marker(pytest.mark.performance)

        # Mark security tests
        if any(
            keyword in item.nodeid.lower()
            for keyword in ["security", "password", "strength"]
        ):
            item.add_marker(pytest.mark.security)

        # Mark slow tests
        if any(keyword in item.nodeid.lower() for keyword in ["slow", "large", "many"]):
            item.add_marker(pytest.mark.slow)
