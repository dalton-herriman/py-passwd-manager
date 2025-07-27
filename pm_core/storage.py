import sqlite3
import json
import os
from typing import Any, List, Tuple, Optional
from .exceptions import StorageError

class SQLiteStorage:
    def __init__(self, db_path: str = "pm_data.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self._init_db()

    def _init_db(self):
        cursor = self.conn.cursor()
        # Create tables for vault data
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS vault_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key TEXT UNIQUE NOT NULL,
                value TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.conn.commit()

    def set(self, key: str, value: str) -> None:
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO vault_data (key, value, updated_at) VALUES (?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(key) DO UPDATE SET value=excluded.value, updated_at=CURRENT_TIMESTAMP
        """, (key, value))
        self.conn.commit()

    def get(self, key: str) -> Optional[str]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT value FROM vault_data WHERE key = ?", (key,))
        row = cursor.fetchone()
        return row[0] if row else None

    def delete(self, key: str) -> None:
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM vault_data WHERE key = ?", (key,))
        self.conn.commit()

    def list_keys(self) -> List[str]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT key FROM vault_data")
        return [row[0] for row in cursor.fetchall()]

    def close(self):
        self.conn.close()

def save_vault_file(vault_data: str, salt: str, vault_path: str):
    """Save encrypted vault data and salt to file."""
    storage = None
    try:
        storage = SQLiteStorage(vault_path)
        storage.set("vault_data", vault_data)
        storage.set("salt", salt)
    except Exception as e:
        raise StorageError(f"Failed to save vault: {str(e)}")
    finally:
        if storage:
            storage.close()

def load_vault_file(vault_path: str) -> tuple:
    """Load encrypted vault data and salt from file."""
    storage = None
    try:
        if not os.path.exists(vault_path):
            return None, None
        
        storage = SQLiteStorage(vault_path)
        vault_data = storage.get("vault_data")
        salt = storage.get("salt")
        
        return vault_data, salt
    except Exception as e:
        raise StorageError(f"Failed to load vault: {str(e)}")
    finally:
        if storage:
            storage.close()

def backup_vault(vault_path: str, backup_path: str):
    """Create a backup of the vault."""
    try:
        if not os.path.exists(vault_path):
            raise FileNotFoundError("Vault file not found")
        
        import shutil
        shutil.copy2(vault_path, backup_path)
        return True
    except Exception as e:
        raise StorageError(f"Failed to create backup: {str(e)}")

def restore_vault(backup_path: str, vault_path: str):
    """Restore vault from backup."""
    try:
        if not os.path.exists(backup_path):
            raise FileNotFoundError("Backup file not found")
        
        import shutil
        shutil.copy2(backup_path, vault_path)
        return True
    except Exception as e:
        raise StorageError(f"Failed to restore vault: {str(e)}")

def get_vault_info(vault_path: str) -> dict:
    """Get information about the vault file."""
    storage = None
    try:
        if not os.path.exists(vault_path):
            return {"exists": False}
        
        storage = SQLiteStorage(vault_path)
        keys = storage.list_keys()
        
        return {
            "exists": True,
            "size": os.path.getsize(vault_path),
            "keys": keys,
            "has_vault_data": "vault_data" in keys,
            "has_salt": "salt" in keys
        }
    except Exception as e:
        return {"exists": False, "error": str(e)}
    finally:
        if storage:
            storage.close()
