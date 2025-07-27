# Password Manager

A secure, feature-rich password manager built in Python with both CLI and GUI interfaces.

## Features

- 🔐 **Secure Encryption**: Uses Argon2 for key derivation and AES-256 for encryption
- 💻 **CLI Interface**: Command-line interface for power users
- 🖥️ **GUI Interface**: User-friendly graphical interface
- 🗂️ **Multiple Vaults**: Create and manage multiple disconnected vaults
- 🔍 **Search & Filter**: Find passwords quickly with search functionality
- 📋 **Clipboard Support**: Easy copy-paste functionality
- 🔄 **Import/Export**: Support for multiple formats
- 🛡️ **Security Features**: Password strength validation, secure memory wiping
- 📊 **Statistics**: Vault usage statistics and insights

## Quick Start

### Prerequisites

- Python 3.8+
- pip

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd py-passwd-manager
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   # CLI version
   python -m cli.multi_vault_cli
   
   # GUI version
   python -m gui.app
   ```

## Cross-Platform Runner

We provide a unified Python runner that works on all platforms:

### Python Runner (Recommended)

Use the `run.py` script for all platforms:

```bash
# Show all available commands
python run.py help

# Quick start with validation
python run.py quick-start

# Run the GUI
python run.py gui

# Run the CLI
python run.py cli

# Run tests
python run.py test

# Install dependencies
python run.py install
```

### Available Commands

The runner supports these commands:

- `help` - Show available commands
- `install` - Install dependencies
- `validate` - Validate project setup
- `quick-start` - Quick start with validation
- `test` - Run all tests
- `test-verbose` - Run tests with verbose output
- `test-cov` - Run tests with coverage
- `test-fast` - Run fast tests only
- `test-security` - Run security tests
- `test-performance` - Run performance tests
- `test-parallel` - Run tests in parallel
- `lint` - Run code linting
- `cli` - Run CLI interface
- `gui` - Run GUI interface
- `demo` - Run demo script
- `demo-multi` - Run Multi-Vault demo script
- `clean` - Clean up temporary files
- `check` - Run all checks (install, validate, test)
- `install-dev` - Install in development mode
- `install-prod` - Install in production mode
- `docs` - Generate documentation
- `security-check` - Run security checks
- `full-check` - Run all validations

## Usage

### Multi-Vault Mode

The application now uses a multi-vault system by default, allowing you to create and manage multiple disconnected vaults:

#### Using CLI

```bash
# Create a new vault
python -m cli.multi_vault_cli create-vault --name "Personal" --master-password "your_password"

# List all vaults
python -m cli.multi_vault_cli list-vaults

# Open a vault
python -m cli.multi_vault_cli open-vault --name "Personal" --master-password "your_password"

# Add an entry to the current vault
python -m cli.multi_vault_cli add --service "Gmail" --username "user@gmail.com" --password "password123"

# List entries in current vault
python -m cli.multi_vault_cli list-entries

# Close the current vault
python -m cli.multi_vault_cli close-vault

# Delete a vault
python -m cli.multi_vault_cli delete-vault --name "Personal"

# Rename a vault
python -m cli.multi_vault_cli rename-vault --old-name "Personal" --new-name "Work"
```

#### Using GUI

1. **Start the GUI**: `python -m gui.app` or `.\run.ps1 gui`
2. **Create vaults** using the "Create Vault" button
3. **Select and open vaults** by double-clicking or using "Open Vault"
4. **Manage entries** within each vault independently
5. **Switch between vaults** by closing one and opening another

#### Multi-Vault Features

- **Vault Isolation**: Each vault is completely separate and encrypted independently
- **Vault Management**: Create, rename, delete, backup, and restore vaults
- **Entry Management**: Add, edit, delete, and search entries within each vault
- **Vault Registry**: Automatic tracking of all vaults with metadata
- **Secure Storage**: Each vault is stored as a separate encrypted database file

### Security Best Practices

- Use a strong, unique master password
- Enable two-factor authentication where possible
- Regularly backup your vault
- Keep your master password secure and separate from your vault
- Use the password generator for unique, strong passwords

## Development

### Running Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_crypto.py -v

# Run with coverage
python -m pytest tests/ --cov=pm_core
```

### Code Quality

```bash
# Linting
python -m flake8 pm_core/ cli/ gui/ tests/

# Code formatting
python -m black pm_core/ cli/ gui/ tests/
```

## Architecture

The project is organized into several modules:

- **`pm_core/`** - Core password manager functionality
  - `crypto.py` - Encryption and key derivation
  - `models.py` - Data models and structures
  - `storage.py` - Vault storage and persistence
  - `manager.py` - Main password manager logic
  - `vault_manager.py` - Multi-vault management
  - `utils.py` - Utility functions
  - `exceptions.py` - Custom exceptions

- **`cli/`** - Command-line interface
- **`gui/`** - Graphical user interface
- **`tests/`** - Test suite
- **`scripts/`** - Utility scripts

## Security

This password manager implements several security measures:

- **Argon2** for key derivation (memory-hard, resistant to GPU attacks)
- **AES-256** for data encryption
- **Secure memory wiping** to prevent password recovery from RAM
- **Password strength validation** to ensure strong passwords
- **Secure clipboard handling** with automatic clearing

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

This is a personal project for educational purposes. While it implements security best practices, it should not be used for critical applications without thorough security auditing. 