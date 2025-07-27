from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List, Optional


@dataclass
class Entry:
    """
    Represents a single entry in the password manager database.
    Can be a password, account credentials, API key, etc.
    """

    id: int
    name: str  # e.g., "Gmail", "AWS", "GitHub"
    username: Optional[str] = None
    password: Optional[str] = None  # Encrypted or hashed
    api_key: Optional[str] = None
    url: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def update(self, **kwargs):
        """
        Update fields of the entry and set updated_at timestamp.
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.now(timezone.utc)


@dataclass
class Vault:
    """
    Represents the entire password vault.
    Contains all entries and vault-level metadata.
    """

    owner: str
    entries: List[Entry] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    version: int = 1
    notes: Optional[str] = None

    def add_entry(self, entry: Entry):
        self.entries.append(entry)
        self.updated_at = datetime.now(timezone.utc)

    def remove_entry(self, entry_id: int):
        self.entries = [e for e in self.entries if e.id != entry_id]
        self.updated_at = datetime.now(timezone.utc)

    def get_entry(self, entry_id: int) -> Optional[Entry]:
        for entry in self.entries:
            if entry.id == entry_id:
                return entry
        return None

    def update_entry(self, entry_id: int, **kwargs):
        entry = self.get_entry(entry_id)
        if entry:
            entry.update(**kwargs)
            self.updated_at = datetime.now(timezone.utc)


@dataclass
class Config:
    """
    Represents application configuration settings.
    """

    db_path: str = "pm_data.db"
    encryption_enabled: bool = True
    default_vault_path: Optional[str] = None
    autosave: bool = True
    theme: Optional[str] = None
    last_opened: Optional[datetime] = None
    backup_enabled: bool = False
    backup_path: Optional[str] = None
