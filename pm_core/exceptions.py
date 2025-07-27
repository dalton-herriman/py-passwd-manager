"""
Custom exceptions for the password manager
"""

class PasswordManagerError(Exception):
    """Base exception for password manager errors"""
    pass

class VaultError(PasswordManagerError):
    """Exception raised for vault-related errors"""
    pass

class CryptoError(PasswordManagerError):
    """Exception raised for encryption/decryption errors"""
    pass

class StorageError(PasswordManagerError):
    """Exception raised for storage-related errors"""
    pass

class ValidationError(PasswordManagerError):
    """Exception raised for validation errors"""
    pass

class AuthenticationError(PasswordManagerError):
    """Exception raised for authentication failures"""
    pass

class ConfigurationError(PasswordManagerError):
    """Exception raised for configuration errors"""
    pass 