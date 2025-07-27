"""
manager.py - High-level vault management
"""

import json
import uuid
from typing import List, Optional
from datetime import datetime

from .crypto import derive_key, encrypt_data, decrypt_data, generate_salt, apply_hash_argon2
from .storage import load_vault_file, save_vault_file, SQLiteStorage
from .models import Vault, Entry
from .utils import generate_password, wipe_memory
from .exceptions import VaultError, CryptoError, StorageError, AuthenticationError

class PasswordManager:
    def __init__(self, vault_path: str):
        self.vault_path = vault_path
        self.vault = None        # In-memory Vault object
        self.key = None          # Derived key for encryption
        self.salt = None         # Stored salt for KDF
        self.is_unlocked = False # Track vault state

    def create_vault(self, master_password: str):
        """Create a new vault with a master password."""
        # Generate salt
        self.salt = generate_salt()
        
        # Create new vault
        self.vault = Vault(owner="user")
        
        # Serialize and encrypt vault data
        vault_json = json.dumps(self.vault.__dict__, default=str)
        encrypted_vault = encrypt_data(vault_json, master_password, self.salt)
        
        # Save encrypted vault to storage
        save_vault_file(encrypted_vault, self.salt, self.vault_path)
        
        self.is_unlocked = True

    def unlock_vault(self, master_password: str):
        """Unlock an existing vault using the master password."""
        try:
            # Load encrypted vault data and salt
            encrypted_vault, self.salt = load_vault_file(self.vault_path)
            
            if not encrypted_vault or not self.salt:
                raise VaultError("Vault file not found or corrupted")
            
            # Decrypt vault data
            vault_json = decrypt_data(encrypted_vault, master_password, self.salt)
            
            # Deserialize vault
            vault_dict = json.loads(vault_json)
            self.vault = Vault(**vault_dict)
            
            self.is_unlocked = True
            return True
        except (CryptoError, StorageError) as e:
            raise AuthenticationError(f"Failed to unlock vault: {str(e)}")
        except Exception as e:
            raise VaultError(f"Failed to unlock vault: {str(e)}")

    def lock_vault(self, master_password: str = None):
        """Lock vault and wipe sensitive data from memory."""
        if self.vault and self.is_unlocked:
            # Save current state before locking if master password provided
            if master_password:
                self.save_vault(master_password)
            
            # Wipe sensitive data
            if hasattr(self, 'key'):
                wipe_memory(self.key)
            self.key = None
            self.vault = None
            self.is_unlocked = False

    def save_vault(self, master_password: str = None):
        """Save the current vault state to disk."""
        if not self.vault or not self.is_unlocked:
            raise VaultError("Vault is not unlocked")
        
        # Serialize and encrypt current vault state
        vault_json = json.dumps(self.vault.__dict__, default=str)
        
        # Require master password for saving
        if not master_password:
            raise ValueError("Master password is required to save vault")
        
        try:
            encrypted_vault = encrypt_data(vault_json, master_password, self.salt)
            # Save encrypted vault to storage
            save_vault_file(encrypted_vault, self.salt, self.vault_path)
        except Exception as e:
            raise StorageError(f"Failed to save vault: {str(e)}")

    def add_entry(self, service: str, username: str = None, password: str = None, 
                  api_key: str = None, url: str = None, notes: str = ""):
        """Add a new password entry."""
        if not self.is_unlocked:
            raise VaultError("Vault is not unlocked")
        
        # Generate unique ID
        entry_id = len(self.vault.entries) + 1
        
        # Create Entry object
        entry = Entry(
            id=entry_id,
            name=service,
            username=username,
            password=password,
            api_key=api_key,
            url=url,
            notes=notes
        )
        
        # Add to Vault
        self.vault.add_entry(entry)
        
        # Save to disk - note: this will require master password
        # In a real implementation, you'd want to store the master password securely
        # or re-prompt the user when needed
        try:
            self.save_vault()
        except ValueError:
            # If master password not available, just update in memory
            pass
        
        return entry

    def get_entry(self, service: str = None, entry_id: int = None) -> List[Entry]:
        """Retrieve entries matching criteria."""
        if not self.is_unlocked:
            raise VaultError("Vault is not unlocked")
        
        if entry_id is not None:
            entry = self.vault.get_entry(entry_id)
            return [entry] if entry else []
        
        if service:
            return [e for e in self.vault.entries if service.lower() in e.name.lower()]
        
        return self.vault.entries

    def update_entry(self, entry_id: int, **kwargs):
        """Update fields of an existing entry."""
        if not self.is_unlocked:
            raise VaultError("Vault is not unlocked")
        
        self.vault.update_entry(entry_id, **kwargs)
        try:
            self.save_vault()
        except ValueError:
            # If master password not available, just update in memory
            pass

    def delete_entry(self, entry_id: int):
        """Remove entry by ID."""
        if not self.is_unlocked:
            raise VaultError("Vault is not unlocked")
        
        self.vault.remove_entry(entry_id)
        try:
            self.save_vault()
        except ValueError:
            # If master password not available, just update in memory
            pass

    def search_entries(self, query: str) -> List[Entry]:
        """Search entries by name, username, or notes."""
        if not self.is_unlocked:
            raise VaultError("Vault is not unlocked")
        
        query = query.lower()
        results = []
        
        for entry in self.vault.entries:
            if (query in entry.name.lower() or 
                (entry.username and query in entry.username.lower()) or
                (entry.notes and query in entry.notes.lower())):
                results.append(entry)
        
        return results

    def generate_and_add_entry(self, service: str, username: str = None, 
                              password_length: int = 16, url: str = None, notes: str = ""):
        """Generate a secure password and add entry."""
        if not self.is_unlocked:
            raise VaultError("Vault is not unlocked")
        
        # Generate secure password
        generated_password = generate_password(password_length)
        
        # Add entry with generated password
        return self.add_entry(
            service=service,
            username=username,
            password=generated_password,
            url=url,
            notes=notes
        )

    def get_vault_stats(self) -> dict:
        """Get vault statistics."""
        if not self.is_unlocked:
            raise VaultError("Vault is not unlocked")
        
        return {
            "total_entries": len(self.vault.entries),
            "vault_created": self.vault.created_at,
            "last_updated": self.vault.updated_at,
            "vault_version": self.vault.version
        }

    def export_entries(self, format_type: str = "json") -> str:
        """Export entries in specified format."""
        if not self.is_unlocked:
            raise VaultError("Vault is not unlocked")
        
        if format_type == "json":
            return json.dumps([entry.__dict__ for entry in self.vault.entries], default=str, indent=2)
        else:
            raise ValueError(f"Unsupported export format: {format_type}")

    def is_vault_exists(self) -> bool:
        """Check if vault file exists."""
        try:
            encrypted_vault, salt = load_vault_file(self.vault_path)
            return encrypted_vault is not None and salt is not None
        except:
            return False