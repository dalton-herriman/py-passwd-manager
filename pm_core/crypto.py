import os
import base64
from argon2 import PasswordHasher
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from .exceptions import CryptoError

'''
Everything related to encryption, 
decryption and key management
'''

def generate_salt():
    salt_phrase = os.urandom(16).hex()
    return salt_phrase

def apply_salt(input_string):
    salt = generate_salt()
    return f"{salt}:{input_string}"

def apply_hash_argon2(input_string):
    ph = PasswordHasher()
    return ph.hash(input_string)

def derive_key(master_password: str, salt: str) -> bytes:
    """
    Derive a cryptographic key from master password and salt using Argon2.
    Returns 32 bytes suitable for AES-256 encryption.
    """
    ph = PasswordHasher()
    # Use Argon2 to derive a key from password + salt
    hash_result = ph.hash(master_password + salt)
    # Extract 32 bytes from the hash for AES-256
    import hashlib
    return hashlib.sha256(hash_result.encode()).digest()

def encrypt_data(data, master_password: str, salt: str):
    """
    Encrypts the given data using AES-GCM.
    - data: plaintext (str)
    - master_password: str
    - salt: str (hex)
    Returns: base64-encoded ciphertext (str)
    """
    try:
        if isinstance(data, str):
            data = data.encode("utf-8")
        
        # Derive key using Argon2
        derived_key = derive_key(master_password, salt)
        aesgcm = AESGCM(derived_key)
        nonce = os.urandom(12)
        ct = aesgcm.encrypt(nonce, data, None)
        # Store nonce + ciphertext, base64-encoded
        encrypted = base64.b64encode(nonce + ct).decode("utf-8")
        return encrypted
    except Exception as e:
        raise CryptoError(f"Encryption failed: {str(e)}")

def decrypt_data(data, master_password: str, salt: str):
    """
    Decrypts AES-GCM-encrypted data.
    - data: base64-encoded ciphertext (str)
    - master_password: str
    - salt: str (hex)
    Returns: plaintext (str)
    """
    try:
        # Derive key using Argon2
        derived_key = derive_key(master_password, salt)
        aesgcm = AESGCM(derived_key)
        raw = base64.b64decode(data)
        nonce = raw[:12]
        ct = raw[12:]
        pt = aesgcm.decrypt(nonce, ct, None)
        return pt.decode("utf-8")
    except Exception as e:
        raise CryptoError(f"Decryption failed: {str(e)}")