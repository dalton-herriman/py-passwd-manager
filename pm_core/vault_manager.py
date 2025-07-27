"""
vault_manager.py - Multi-vault management system
"""

import os
import json
import sqlite3
from typing import List, Dict, Optional, Tuple
from datetime import datetime
from pathlib import Path

from .manager import PasswordManager
from .exceptions import VaultError, StorageError
from .models import Vault, Entry


class VaultInfo:
    """Information about a vault."""

    def __init__(
        self,
        name: str,
        path: str,
        created_at: datetime,
        entry_count: int = 0,
        last_accessed: Optional[datetime] = None,
    ):
        self.name = name
        self.path = path
        self.created_at = created_at
        self.entry_count = entry_count
        self.last_accessed = last_accessed or created_at

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "path": self.path,
            "created_at": self.created_at.isoformat(),
            "entry_count": self.entry_count,
            "last_accessed": (
                self.last_accessed.isoformat() if self.last_accessed else None
            ),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "VaultInfo":
        return cls(
            name=data["name"],
            path=data["path"],
            created_at=datetime.fromisoformat(data["created_at"]),
            entry_count=data.get("entry_count", 0),
            last_accessed=(
                datetime.fromisoformat(data["last_accessed"])
                if data.get("last_accessed")
                else None
            ),
        )


class VaultManager:
    """Manages multiple vaults."""

    def __init__(self, vaults_dir: str = "vaults"):
        self.vaults_dir = Path(vaults_dir)
        self.vaults_dir.mkdir(exist_ok=True)
        self.registry_path = self.vaults_dir / "vault_registry.json"
        self.current_vault: Optional[PasswordManager] = None
        self.current_vault_name: Optional[str] = None
        self._load_registry()

    def _load_registry(self):
        """Load vault registry from disk."""
        if self.registry_path.exists():
            try:
                with open(self.registry_path, "r") as f:
                    registry_data = json.load(f)
                    self.vaults = {
                        name: VaultInfo.from_dict(info)
                        for name, info in registry_data.items()
                    }
            except Exception as e:
                print(f"Warning: Could not load vault registry: {e}")
                self.vaults = {}
        else:
            self.vaults = {}

    def _save_registry(self):
        """Save vault registry to disk."""
        registry_data = {name: info.to_dict() for name, info in self.vaults.items()}
        with open(self.registry_path, "w") as f:
            json.dump(registry_data, f, indent=2)

    def create_vault(
        self, name: str, master_password: str, description: str = ""
    ) -> bool:
        """Create a new vault."""
        if name in self.vaults:
            raise VaultError(f"Vault '{name}' already exists")

        # Sanitize name for filename
        safe_name = "".join(
            c for c in name if c.isalnum() or c in (" ", "-", "_")
        ).rstrip()
        safe_name = safe_name.replace(" ", "_")

        vault_path = self.vaults_dir / f"{safe_name}.db"

        # Create vault
        pm = PasswordManager(str(vault_path))
        pm.create_vault(master_password)

        # Add to registry
        vault_info = VaultInfo(
            name=name, path=str(vault_path), created_at=datetime.now(), entry_count=0
        )

        self.vaults[name] = vault_info
        self._save_registry()

        return True

    def reload_registry(self):
        """Force reload the vault registry from disk."""
        self._load_registry()

    def list_vaults(self) -> List[VaultInfo]:
        """List all available vaults."""
        # Update entry counts
        for name, info in self.vaults.items():
            if os.path.exists(info.path):
                try:
                    pm = PasswordManager(info.path)
                    if pm.is_vault_exists():
                        # Try to get entry count without unlocking
                        info.entry_count = self._get_vault_entry_count(info.path)
                except:
                    info.entry_count = 0

        return list(self.vaults.values())

    def _get_vault_entry_count(self, vault_path: str) -> int:
        """Get entry count without unlocking the vault."""
        try:
            from .storage import get_vault_info

            info = get_vault_info(vault_path)
            if info.get("exists") and info.get("has_vault_data"):
                # For now, we'll return 0 since we can't decrypt without the password
                # In a future implementation, we could store metadata separately
                return 0
        except:
            pass
        return 0

    def update_vault_entry_count(self, vault_name: str, count: int):
        """Update the entry count for a vault."""
        if vault_name in self.vaults:
            self.vaults[vault_name].entry_count = count
            self._save_registry()

    def open_vault(self, name: str, master_password: str) -> PasswordManager:
        """Open a vault with the given name."""
        if name not in self.vaults:
            raise VaultError(f"Vault '{name}' not found")

        vault_info = self.vaults[name]
        if not os.path.exists(vault_info.path):
            raise VaultError(f"Vault file not found: {vault_info.path}")

        # Create password manager and unlock vault
        pm = PasswordManager(vault_info.path)
        pm.unlock_vault(master_password)

        # Update last accessed time and entry count
        vault_info.last_accessed = datetime.now()
        vault_info.entry_count = len(pm.get_entry())
        self._save_registry()

        # Set as current vault
        self.current_vault = pm
        self.current_vault_name = name

        return pm

    def close_vault(self):
        """Close the currently open vault."""
        if self.current_vault:
            self.current_vault.lock_vault()
            self.current_vault = None
            self.current_vault_name = None

    def delete_vault(self, name: str) -> bool:
        """Delete a vault and its file."""
        if name not in self.vaults:
            raise VaultError(f"Vault '{name}' not found")

        vault_info = self.vaults[name]

        # Close if it's the current vault
        if self.current_vault_name == name:
            self.close_vault()

        # Delete vault file
        if os.path.exists(vault_info.path):
            os.remove(vault_info.path)

        # Remove from registry
        del self.vaults[name]
        self._save_registry()

        return True

    def rename_vault(self, old_name: str, new_name: str) -> bool:
        """Rename a vault."""
        if old_name not in self.vaults:
            raise VaultError(f"Vault '{old_name}' not found")

        if new_name in self.vaults:
            raise VaultError(f"Vault '{new_name}' already exists")

        vault_info = self.vaults[old_name]

        # Create new safe name
        safe_name = "".join(
            c for c in new_name if c.isalnum() or c in (" ", "-", "_")
        ).rstrip()
        safe_name = safe_name.replace(" ", "_")
        new_path = self.vaults_dir / f"{safe_name}.db"

        # Rename file
        if os.path.exists(vault_info.path):
            os.rename(vault_info.path, new_path)

        # Update registry
        vault_info.name = new_name
        vault_info.path = str(new_path)
        self.vaults[new_name] = vault_info
        del self.vaults[old_name]

        # Update current vault name if needed
        if self.current_vault_name == old_name:
            self.current_vault_name = new_name

        self._save_registry()

        return True

    def get_current_vault(self) -> Optional[PasswordManager]:
        """Get the currently open vault."""
        return self.current_vault

    def get_current_vault_name(self) -> Optional[str]:
        """Get the name of the currently open vault."""
        return self.current_vault_name

    def vault_exists(self, name: str) -> bool:
        """Check if a vault exists."""
        return name in self.vaults

    def get_vault_info(self, name: str) -> Optional[VaultInfo]:
        """Get information about a specific vault."""
        return self.vaults.get(name)

    def backup_vault(self, name: str, backup_path: str) -> bool:
        """Create a backup of a vault."""
        if name not in self.vaults:
            raise VaultError(f"Vault '{name}' not found")

        vault_info = self.vaults[name]
        if not os.path.exists(vault_info.path):
            raise VaultError(f"Vault file not found: {vault_info.path}")

        import shutil

        shutil.copy2(vault_info.path, backup_path)
        return True

    def restore_vault(self, backup_path: str, name: str) -> bool:
        """Restore a vault from backup."""
        if not os.path.exists(backup_path):
            raise VaultError(f"Backup file not found: {backup_path}")

        # Create safe name
        safe_name = "".join(
            c for c in name if c.isalnum() or c in (" ", "-", "_")
        ).rstrip()
        safe_name = safe_name.replace(" ", "_")
        vault_path = self.vaults_dir / f"{safe_name}.db"

        import shutil

        shutil.copy2(backup_path, vault_path)

        # Add to registry
        vault_info = VaultInfo(
            name=name, path=str(vault_path), created_at=datetime.now(), entry_count=0
        )

        self.vaults[name] = vault_info
        self._save_registry()

        return True
