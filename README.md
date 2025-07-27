# Password Manager

A secure, feature-rich password manager built in Python with both CLI and GUI interfaces.

## Features

- 🔐 **Secure Encryption**: Uses Argon2 for key derivation and AES-256 for encryption
- 💻 **CLI Interface**: Command-line interface for power users
- 🖥️ **GUI Interface**: User-friendly graphical interface
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
   python -m cli.main
   
   # GUI version
   python -m gui.app
   ```

## Windows Users

For Windows users, we provide convenient alternatives to the Makefile:

### PowerShell Script (Recommended)

Use the `run.ps1` script for the most features:

```powershell
# Show all available commands
.\run.ps1 help

# Quick start with validation
.\run.ps1 quick-start

# Run the GUI
.\run.ps1 gui

# Run the CLI
.\run.ps1 cli

# Run tests
.\run.ps1 test

# Install dependencies
.\run.ps1 install
```

### Batch File

Use the `run.bat` script for simple commands:

```cmd
# Show all available commands
run.bat help

# Quick start
run.bat quick-start

# Run the GUI
run.bat gui

# Run the CLI
run.bat cli
```

### Available Commands

Both scripts support these commands:

- `help` - Show available commands
- `install` - Install dependencies
- `validate` - Validate project setup
- `quick-start` - Quick start with validation
- `test` - Run all tests
- `cli` - Run CLI interface
- `gui` - Run GUI interface
- `clean` - Clean up temporary files
- `check` - Run all checks (install, validate, test)

## Usage

### Creating Your First Vault

1. **Start the application** (CLI or GUI)
2. **Create a new vault** with a strong master password
3. **Add your first entry** with a website, username, and password
4. **Save the vault** to secure storage

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