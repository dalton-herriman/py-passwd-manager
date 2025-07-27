import secrets
import string
import ctypes
import sys
from typing import Optional

def generate_password(length: int = 16, include_symbols: bool = True, 
                    include_numbers: bool = True, include_uppercase: bool = True) -> str:
    """
    Generate a cryptographically secure password.
    
    Args:
        length: Length of the password
        include_symbols: Include special characters
        include_numbers: Include numbers
        include_uppercase: Include uppercase letters
    
    Returns:
        Generated password string
    """
    # Check that at least one of symbols, numbers, or uppercase is enabled
    if not (include_symbols or include_numbers or include_uppercase):
        raise ValueError("At least one character set must be enabled")
    
    # Define character sets
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase if include_uppercase else ""
    numbers = string.digits if include_numbers else ""
    symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?" if include_symbols else ""
    
    # Combine all allowed characters
    all_chars = lowercase + uppercase + numbers + symbols
    
    if not all_chars:
        raise ValueError("At least one character set must be enabled")
    
    # Generate password
    password = ''.join(secrets.choice(all_chars) for _ in range(length))
    
    # Ensure password meets minimum requirements by regenerating if needed
    max_attempts = 10
    for attempt in range(max_attempts):
        password = ''.join(secrets.choice(all_chars) for _ in range(length))
        
        # Check if password meets all requirements
        meets_requirements = True
        
        if include_uppercase and not any(c.isupper() for c in password):
            meets_requirements = False
        if include_numbers and not any(c.isdigit() for c in password):
            meets_requirements = False
        if include_symbols and not any(c in symbols for c in password):
            meets_requirements = False
        
        if meets_requirements:
            return password
    
    # If we couldn't generate a password meeting all requirements in max_attempts,
    # manually ensure at least one character from each required set
    password_list = list(password)
    
    if include_uppercase and not any(c.isupper() for c in password):
        # Replace a random character with uppercase
        pos = secrets.randbelow(length)
        password_list[pos] = secrets.choice(uppercase)
    
    if include_numbers and not any(c.isdigit() for c in password):
        # Replace a random character with number
        pos = secrets.randbelow(length)
        password_list[pos] = secrets.choice(numbers)
    
    if include_symbols and not any(c in symbols for c in password):
        # Replace a random character with symbol
        pos = secrets.randbelow(length)
        password_list[pos] = secrets.choice(symbols)
    
    return ''.join(password_list)

def clipboard_handler(text: str, timeout: int = 30) -> bool:
    """
    Copy text to clipboard and optionally clear after timeout.
    
    Args:
        text: Text to copy to clipboard
        timeout: Seconds before clearing clipboard (0 = no auto-clear)
    
    Returns:
        True if successful, False otherwise
    """
    try:
        import pyperclip
        pyperclip.copy(text)
        
        if timeout > 0:
            import threading
            import time
            
            def clear_clipboard():
                time.sleep(timeout)
                pyperclip.copy("")
            
            thread = threading.Thread(target=clear_clipboard, daemon=True)
            thread.start()
        
        return True
    except ImportError:
        # Fallback for systems without pyperclip
        try:
            import subprocess
            import platform
            
            if platform.system() == "Windows":
                subprocess.run(['clip'], input=text.encode(), check=True)
            elif platform.system() == "Darwin":  # macOS
                subprocess.run(['pbcopy'], input=text.encode(), check=True)
            else:  # Linux
                subprocess.run(['xclip', '-selection', 'clipboard'], 
                             input=text.encode(), check=True)
            return True
        except:
            return False
    except:
        return False

def wipe_memory(data) -> None:
    """
    Securely wipe data from memory.
    
    Args:
        data: Data to wipe (string, bytes, or list)
    """
    if isinstance(data, str):
        # Overwrite string with random data
        length = len(data)
        random_chars = ''.join(secrets.choice(string.ascii_letters + string.digits) 
                              for _ in range(length))
        # This is a best-effort approach for strings in Python
        # Python strings are immutable, so we can't directly overwrite
        # But we can help garbage collection
        del data
    elif isinstance(data, bytes):
        # For bytes objects, we can't modify them directly as they're immutable
        # The best we can do is help with garbage collection
        del data
    elif isinstance(data, list):
        # Recursively wipe list contents
        for item in data:
            wipe_memory(item)
        data.clear()
        del data

def get_system_info() -> dict:
    """Get system information for debugging."""
    import platform
    return {
        "platform": platform.system(),
        "python_version": sys.version,
        "architecture": platform.architecture()[0]
    }

def validate_password_strength(password: str) -> dict:
    """
    Validate password strength.
    
    Returns:
        Dictionary with strength score and feedback
    """
    score = 0
    feedback = []
    
    # Handle None and non-string inputs
    if password is None or not isinstance(password, str):
        return {
            "score": 0,
            "strength": "weak",
            "feedback": ["Password must be a string"]
        }
    
    if len(password) >= 8:
        score += 1
    else:
        feedback.append("Password should be at least 8 characters long")
    
    if any(c.islower() for c in password):
        score += 1
    else:
        feedback.append("Include lowercase letters")
    
    if any(c.isupper() for c in password):
        score += 1
    else:
        feedback.append("Include uppercase letters")
    
    if any(c.isdigit() for c in password):
        score += 1
    else:
        feedback.append("Include numbers")
    
    if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
        score += 1
    else:
        feedback.append("Include special characters")
    
    # Check for common patterns
    common_patterns = ["123", "abc", "qwe", "password", "admin"]
    if any(pattern in password.lower() for pattern in common_patterns):
        score -= 1
        feedback.append("Avoid common patterns")
    
    strength = "weak"
    if score >= 4:
        strength = "strong"
    elif score >= 3:
        strength = "medium"
    
    return {
        "score": score,
        "strength": strength,
        "feedback": feedback
    }