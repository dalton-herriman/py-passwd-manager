#!/usr/bin/env python3
"""
Pydantic models for the Password Manager
Replaces manual validation with automatic data validation
"""

from datetime import datetime, timezone
from typing import Optional, List
from pydantic import BaseModel, Field, field_validator
import secrets
import string


class Entry(BaseModel):
    """Password entry model with automatic validation"""
    
    id: Optional[int] = Field(None, description="Entry ID")
    name: str = Field(..., min_length=1, max_length=200, description="Entry name")
    username: Optional[str] = Field(None, max_length=200, description="Username")
    password: Optional[str] = Field(None, min_length=8, description="Password")
    api_key: Optional[str] = Field(None, description="API key")
    url: Optional[str] = Field(None, max_length=500, description="Website URL")
    notes: Optional[str] = Field(None, max_length=1000, description="Additional notes")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="Creation timestamp")
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="Last update timestamp")
    
    @field_validator('password')
    @classmethod
    def validate_password_strength(cls, v):
        """Validate password strength if provided"""
        if v is not None and len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        
        # Check for common weak patterns
        if v and v.lower() in ['password', '123456', 'qwerty', 'admin']:
            raise ValueError("Password is too common")
        
        return v
    
    @field_validator('url')
    @classmethod
    def validate_url_format(cls, v):
        """Validate URL format if provided"""
        if v and not v.startswith(('http://', 'https://')):
            raise ValueError("URL must start with http:// or https://")
        return v
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "name": "Gmail",
                    "username": "user@example.com",
                    "password": "secure_password_123"
                }
            ]
        }
    }


class Vault(BaseModel):
    """Vault model with automatic validation"""
    
    owner: str = Field(..., min_length=1, max_length=100, description="Vault owner")
    entries: List[Entry] = Field(default_factory=list, description="Vault entries")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="Creation timestamp")
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="Last update timestamp")
    version: int = Field(default=1, ge=1, description="Vault version")
    notes: Optional[str] = Field(None, max_length=1000, description="Vault notes")
    
    def add_entry(self, entry: Entry):
        """Add entry to vault"""
        self.entries.append(entry)
        self.updated_at = datetime.now(timezone.utc)
    
    def remove_entry(self, entry_id: int):
        """Remove entry from vault"""
        self.entries = [e for e in self.entries if e.id != entry_id]
        self.updated_at = datetime.now(timezone.utc)
    
    def get_entry(self, entry_id: int) -> Optional[Entry]:
        """Get entry by ID"""
        for entry in self.entries:
            if entry.id == entry_id:
                return entry
        return None
    
    def update_entry(self, entry_id: int, **kwargs):
        """Update entry in vault"""
        entry = self.get_entry(entry_id)
        if entry:
            for key, value in kwargs.items():
                if hasattr(entry, key):
                    setattr(entry, key, value)
            entry.updated_at = datetime.now(timezone.utc)
            self.updated_at = datetime.now(timezone.utc)
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "owner": "user",
                    "entries": [],
                    "version": 1
                }
            ]
        }
    }


class VaultInfo(BaseModel):
    """Vault information model"""
    
    name: str = Field(..., min_length=1, max_length=100, description="Vault name")
    path: str = Field(..., description="Vault file path")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="Creation timestamp")
    entry_count: int = Field(default=0, ge=0, description="Number of entries")
    last_accessed: Optional[datetime] = Field(None, description="Last access timestamp")
    description: Optional[str] = Field(None, max_length=500, description="Vault description")
    
    @field_validator('name')
    @classmethod
    def validate_vault_name(cls, v):
        """Validate vault name"""
        if not v.replace('_', '').replace('-', '').isalnum():
            raise ValueError("Vault name must contain only letters, numbers, underscores, and hyphens")
        return v
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "my_vault",
                    "path": "/path/to/vault",
                    "entry_count": 0
                }
            ]
        }
    }


class Config(BaseModel):
    """Application configuration model"""
    
    db_path: str = Field(default="pm_data.db", description="Database path")
    encryption_enabled: bool = Field(default=True, description="Enable encryption")
    default_vault_path: Optional[str] = Field(None, description="Default vault path")
    autosave: bool = Field(default=True, description="Enable autosave")
    theme: Optional[str] = Field(None, description="UI theme")
    last_opened: Optional[datetime] = Field(None, description="Last opened timestamp")
    backup_enabled: bool = Field(default=False, description="Enable backups")
    backup_path: Optional[str] = Field(None, description="Backup path")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "db_path": "pm_data.db",
                    "encryption_enabled": True,
                    "autosave": True
                }
            ]
        }
    }


class PasswordGenerationConfig(BaseModel):
    """Password generation configuration"""
    
    length: int = Field(default=16, ge=8, le=128, description="Password length")
    include_uppercase: bool = Field(default=True, description="Include uppercase letters")
    include_lowercase: bool = Field(default=True, description="Include lowercase letters")
    include_numbers: bool = Field(default=True, description="Include numbers")
    include_symbols: bool = Field(default=True, description="Include symbols")
    exclude_similar: bool = Field(default=True, description="Exclude similar characters")
    exclude_ambiguous: bool = Field(default=True, description="Exclude ambiguous characters")
    
    @field_validator('length')
    @classmethod
    def validate_length(cls, v):
        """Validate password length"""
        if v < 8:
            raise ValueError("Password length must be at least 8 characters")
        if v > 128:
            raise ValueError("Password length must be at most 128 characters")
        return v
    
    @field_validator('*', mode='before')
    @classmethod
    def validate_character_sets(cls, v, info):
        """Ensure at least one character set is enabled"""
        if info.field_name in ['include_uppercase', 'include_lowercase', 'include_numbers', 'include_symbols']:
            return v
        return v


class SearchQuery(BaseModel):
    """Search query model"""
    
    query: str = Field(..., min_length=1, max_length=200, description="Search query")
    search_name: bool = Field(default=True, description="Search in names")
    search_username: bool = Field(default=True, description="Search in usernames")
    search_url: bool = Field(default=True, description="Search in URLs")
    search_notes: bool = Field(default=True, description="Search in notes")
    case_sensitive: bool = Field(default=False, description="Case sensitive search")
    use_regex: bool = Field(default=False, description="Use regular expressions")
    
    @field_validator('query')
    @classmethod
    def validate_query(cls, v):
        """Validate search query"""
        if not v.strip():
            raise ValueError("Search query cannot be empty")
        return v.strip()


# Utility functions that work with Pydantic models
def generate_password_from_config(config: PasswordGenerationConfig) -> str:
    """Generate password using Pydantic config"""
    # Define character sets
    lowercase = string.ascii_lowercase if config.include_lowercase else ""
    uppercase = string.ascii_uppercase if config.include_uppercase else ""
    numbers = string.digits if config.include_numbers else ""
    symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?" if config.include_symbols else ""
    
    # Combine all allowed characters
    all_chars = lowercase + uppercase + numbers + symbols
    
    if not all_chars:
        raise ValueError("At least one character set must be enabled")
    
    # Generate password
    password = "".join(secrets.choice(all_chars) for _ in range(config.length))
    
    # Ensure password meets requirements
    max_attempts = 10
    for attempt in range(max_attempts):
        password = "".join(secrets.choice(all_chars) for _ in range(config.length))
        
        # Check if password meets all requirements
        meets_requirements = True
        
        if config.include_uppercase and not any(c.isupper() for c in password):
            meets_requirements = False
        if config.include_numbers and not any(c.isdigit() for c in password):
            meets_requirements = False
        if config.include_symbols and not any(c in symbols for c in password):
            meets_requirements = False
        
        if meets_requirements:
            return password
    
    # If we couldn't generate a password meeting all requirements,
    # manually ensure at least one character from each required set
    password_list = list(password)
    
    if config.include_uppercase and not any(c.isupper() for c in password):
        pos = secrets.randbelow(config.length)
        password_list[pos] = secrets.choice(uppercase)
    
    if config.include_numbers and not any(c.isdigit() for c in password):
        pos = secrets.randbelow(config.length)
        password_list[pos] = secrets.choice(numbers)
    
    if config.include_symbols and not any(c in symbols for c in password):
        pos = secrets.randbelow(config.length)
        password_list[pos] = secrets.choice(symbols)
    
    return "".join(password_list)


def validate_password_strength_pydantic(password: str) -> dict:
    """Validate password strength using Pydantic-style validation"""
    score = 0
    feedback = []
    
    # Length check
    if len(password) >= 8:
        score += 1
    else:
        feedback.append("Password should be at least 8 characters long")
    
    # Character variety checks
    if any(c.isupper() for c in password):
        score += 1
    else:
        feedback.append("Password should contain uppercase letters")
    
    if any(c.islower() for c in password):
        score += 1
    else:
        feedback.append("Password should contain lowercase letters")
    
    if any(c.isdigit() for c in password):
        score += 1
    else:
        feedback.append("Password should contain numbers")
    
    if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
        score += 1
    else:
        feedback.append("Password should contain symbols")
    
    # Strength determination
    if score <= 2:
        strength = "weak"
    elif score <= 3:
        strength = "medium"
    elif score <= 4:
        strength = "strong"
    else:
        strength = "very strong"
    
    return {
        "score": score,
        "strength": strength,
        "feedback": feedback,
        "length": len(password)
    } 