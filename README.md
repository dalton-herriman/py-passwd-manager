# Password Manager

A secure, feature-rich password manager built in Python with both CLI and GUI interfaces. This application provides strong encryption, secure password generation, and intuitive user interfaces for managing your passwords and credentials.

## Features

### 🔐 Security
- **Strong Encryption**: Uses AES-GCM with Argon2 key derivation
- **Secure Storage**: All data is encrypted before storage
- **Memory Protection**: Sensitive data is wiped from memory when not needed
- **Password Strength Analysis**: Built-in password strength validation

### 💻 Interfaces
- **Command Line Interface (CLI)**: Full-featured CLI for power users
- **Graphical User Interface (GUI)**: Modern tkinter-based GUI for easy use
- **Cross-platform**: Works on Windows, macOS, and Linux

### 🛠️ Functionality
- **Vault Management**: Create, unlock, and lock password vaults
- **Entry Management**: Add, edit, delete, and search password entries
- **Password Generation**: Generate cryptographically secure passwords
- **Clipboard Integration**: Copy passwords to clipboard with auto-clear
- **Search & Filter**: Find entries by service, username, or notes
- **Export/Import**: Export data in JSON format
- **Statistics**: View vault statistics and entry counts

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Install from Source

1. Clone the repository:
```bash
git clone <repository-url>
cd py-passwd-manager
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install the package:
```bash
pip install -e .
```

### Quick Start

After installation, you can run the password manager in two ways:

#### GUI Mode
```bash
python run.py --gui
# or
pm-gui
```

#### CLI Mode
```bash
python run.py
# or
pm-cli
```

## Usage

### GUI Interface

The GUI provides an intuitive interface for managing passwords:

1. **Create Vault**: Click "Create Vault" to create a new password vault
2. **Unlock Vault**: Click "Unlock Vault" to access existing vault
3. **Add Entry**: Click "Add Entry" to add new password entries
4. **Search**: Use the search box to find specific entries
5. **Manage Entries**: Double-click entries or use action buttons to view/edit/delete

### CLI Interface

The CLI provides powerful command-line tools:

#### Basic Commands

```bash
# Create a new vault
pm-cli create

# Unlock existing vault
pm-cli unlock

# Lock the vault
pm-cli lock

# Add a new entry
pm-cli add --service "Gmail" --username "user@example.com" --password "mypassword"

# Generate and add entry with secure password
pm-cli add --service "GitHub" --username "myuser" --generate --length 20

# List all entries
pm-cli list

# Search entries
pm-cli list --search "gmail"

# Show specific entry
pm-cli show --id 1

# Update entry
pm-cli update --id 1 --username "newuser"

# Delete entry
pm-cli delete --id 1

# Generate password
pm-cli generate --length 16 --copy

# Show vault statistics
pm-cli stats

# Export entries
pm-cli export --output passwords.json
```

#### Advanced Usage

```bash
# Use custom vault path
pm-cli --vault-path /path/to/vault.db create

# Add entry with URL and notes
pm-cli add --service "AWS" --username "admin" --url "https://aws.amazon.com" --notes "Production account"

# Generate password with specific options
pm-cli generate --length 24 --no-symbols --copy

# Search and filter entries
pm-cli list --service "github" --search "work"
```

## Security Features

### Encryption
- **AES-GCM**: Authenticated encryption for data confidentiality and integrity
- **Argon2**: Memory-hard key derivation function for password hashing
- **Salt Generation**: Cryptographically secure salt generation for each vault

### Memory Security
- **Secure Wiping**: Sensitive data is wiped from memory when vault is locked
- **Clipboard Auto-clear**: Passwords copied to clipboard are automatically cleared after timeout
- **No Plaintext Storage**: Passwords are never stored in plaintext

### Password Generation
- **Cryptographically Secure**: Uses `secrets` module for secure random generation
- **Configurable**: Customizable length and character sets
- **Strength Validation**: Built-in password strength analysis

## File Structure

```
py-passwd-manager/
├── pm-core/              # Core password management logic
│   ├── __init__.py
│   ├── crypto.py         # Encryption and key derivation
│   ├── manager.py        # High-level vault management
│   ├── models.py         # Data models (Entry, Vault)
│   ├── storage.py        # Storage layer (SQLite)
│   └── utils.py          # Utility functions
├── cli/                  # Command-line interface
│   ├── __init__.py
│   └── main.py          # CLI implementation
├── gui/                  # Graphical user interface
│   ├── __init__.py
│   ├── app.py           # Main GUI application
│   └── widgets.py       # GUI widgets (if needed)
├── tests/               # Test suite
├── requirements.txt     # Python dependencies
├── setup.py            # Package setup
├── run.py              # Entry point
└── README.md           # This file
```

## Configuration

### Vault File Location
By default, vaults are stored as `vault.db` in the current directory. You can specify a custom path:

```bash
pm-cli --vault-path /path/to/custom/vault.db create
```

### Clipboard Timeout
Passwords copied to clipboard are automatically cleared after 30 seconds by default. This can be configured in the code.

## Development

### Running Tests
```bash
# Run all tests
python -m pytest tests/

# Run with coverage
python -m pytest --cov=pm_core tests/
```

### Code Style
This project uses Black for code formatting:
```bash
black .
```

### Type Checking
```bash
mypy pm-core/ cli/ gui/
```

## Security Considerations

### Best Practices
1. **Strong Master Password**: Use a strong, unique master password
2. **Regular Backups**: Keep backups of your vault file
3. **Secure Environment**: Run on a secure, trusted system
4. **Lock When Away**: Always lock the vault when not in use
5. **Unique Passwords**: Use generated passwords for each service

### Limitations
- This is a local password manager - no cloud sync
- No browser integration
- No automatic password filling
- No mobile app

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This software is provided "as is" without warranty. Use at your own risk. The authors are not responsible for any data loss or security breaches.

## Support

For issues, questions, or contributions:
- Create an issue on the repository
- Check the documentation
- Review the code comments

---

**Note**: This is a personal password manager. For enterprise use, consider additional security measures and professional security audits. 