"""
Password Manager Core Package

This package contains the core functionality for the password manager,
including encryption, storage, and management logic.
"""

__version__ = "1.0.0"
__author__ = "Password Manager Team"

from .manager import PasswordManager
from .models import Entry, Vault, Config
from .exceptions import (
    PasswordManagerError,
    VaultError,
    CryptoError,
    StorageError,
    ValidationError,
    AuthenticationError,
    ConfigurationError
)
from .crypto import (
    generate_salt,
    apply_salt,
    apply_hash_argon2,
    derive_key,
    encrypt_data,
    decrypt_data
)
from .utils import (
    generate_password,
    clipboard_handler,
    wipe_memory,
    validate_password_strength,
    get_system_info
)
from .storage import (
    SQLiteStorage,
    save_vault_file,
    load_vault_file,
    backup_vault,
    restore_vault,
    get_vault_info
)

__all__ = [
    'PasswordManager',
    'Entry',
    'Vault', 
    'Config',
    'PasswordManagerError',
    'VaultError',
    'CryptoError',
    'StorageError',
    'ValidationError',
    'AuthenticationError',
    'ConfigurationError',
    'generate_salt',
    'apply_salt',
    'apply_hash_argon2',
    'derive_key',
    'encrypt_data',
    'decrypt_data',
    'generate_password',
    'clipboard_handler',
    'wipe_memory',
    'validate_password_strength',
    'get_system_info',
    'SQLiteStorage',
    'save_vault_file',
    'load_vault_file',
    'backup_vault',
    'restore_vault',
    'get_vault_info'
]
