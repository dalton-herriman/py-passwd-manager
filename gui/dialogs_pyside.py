#!/usr/bin/env python3
"""
PySide6-based dialogs for the Password Manager GUI
Modern, responsive dialogs with better UX
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLineEdit, QTextEdit, QPushButton, QLabel, QCheckBox,
    QSpinBox, QComboBox, QMessageBox, QGroupBox, QGridLayout,
    QApplication, QMainWindow
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont

from .components_pyside import DialogBase, ModernButton


class CreateVaultDialog(DialogBase):
    """Dialog for creating a new vault"""
    
    vault_created = Signal(str, str, str)  # name, password, description
    
    def __init__(self, parent=None):
        super().__init__(parent, "Create New Vault", 400, 300)
        self.setup_dialog_ui()
    
    def setup_dialog_ui(self):
        """Setup the dialog UI"""
        layout = QVBoxLayout(self)
        
        # Form layout for inputs
        form_layout = QFormLayout()
        
        # Vault name
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter vault name")
        form_layout.addRow("Vault Name:", self.name_input)
        
        # Master password
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Enter master password")
        form_layout.addRow("Master Password:", self.password_input)
        
        # Confirm password
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        self.confirm_password_input.setPlaceholderText("Confirm master password")
        form_layout.addRow("Confirm Password:", self.confirm_password_input)
        
        # Description
        self.description_input = QTextEdit()
        self.description_input.setMaximumHeight(80)
        self.description_input.setPlaceholderText("Optional vault description")
        form_layout.addRow("Description:", self.description_input)
        
        layout.addLayout(form_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.create_button = ModernButton("Create Vault")
        self.create_button.clicked.connect(self.create_vault)
        
        self.cancel_button = ModernButton("Cancel")
        self.cancel_button.clicked.connect(self.close)
        
        button_layout.addWidget(self.create_button)
        button_layout.addWidget(self.cancel_button)
        
        layout.addLayout(button_layout)
    
    def create_vault(self):
        """Create the vault with validation"""
        name = self.name_input.text().strip()
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()
        description = self.description_input.toPlainText().strip()
        
        # Validation
        if not name:
            QMessageBox.warning(self, "Error", "Vault name is required!")
            return
        
        if not password:
            QMessageBox.warning(self, "Error", "Master password is required!")
            return
        
        if password != confirm_password:
            QMessageBox.warning(self, "Error", "Passwords do not match!")
            return
        
        if len(password) < 8:
            QMessageBox.warning(self, "Error", "Password must be at least 8 characters long!")
            return
        
        # Emit signal and close
        self.vault_created.emit(name, password, description)
        self.close()


class AddEntryDialog(DialogBase):
    """Dialog for adding a new entry"""
    
    entry_added = Signal(dict)  # entry data
    
    def __init__(self, parent=None):
        super().__init__(parent, "Add New Entry", 450, 400)
        self.setup_dialog_ui()
    
    def setup_dialog_ui(self):
        """Setup the dialog UI"""
        layout = QVBoxLayout(self)
        
        # Form layout for inputs
        form_layout = QFormLayout()
        
        # Entry name
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter entry name")
        form_layout.addRow("Name:", self.name_input)
        
        # Username
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter username")
        form_layout.addRow("Username:", self.username_input)
        
        # Password
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Enter password")
        form_layout.addRow("Password:", self.password_input)
        
        # Show password checkbox
        self.show_password_checkbox = QCheckBox("Show password")
        self.show_password_checkbox.toggled.connect(self.toggle_password_visibility)
        form_layout.addRow("", self.show_password_checkbox)
        
        # URL
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("https://example.com")
        form_layout.addRow("URL:", self.url_input)
        
        # Notes
        self.notes_input = QTextEdit()
        self.notes_input.setMaximumHeight(100)
        self.notes_input.setPlaceholderText("Optional notes")
        form_layout.addRow("Notes:", self.notes_input)
        
        layout.addLayout(form_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.add_button = ModernButton("Add Entry")
        self.add_button.clicked.connect(self.add_entry)
        
        self.cancel_button = ModernButton("Cancel")
        self.cancel_button.clicked.connect(self.close)
        
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.cancel_button)
        
        layout.addLayout(button_layout)
    
    def toggle_password_visibility(self, checked):
        """Toggle password visibility"""
        if checked:
            self.password_input.setEchoMode(QLineEdit.Normal)
        else:
            self.password_input.setEchoMode(QLineEdit.Password)
    
    def add_entry(self):
        """Add the entry with validation"""
        name = self.name_input.text().strip()
        username = self.username_input.text().strip()
        password = self.password_input.text()
        url = self.url_input.text().strip()
        notes = self.notes_input.toPlainText().strip()
        
        # Validation
        if not name:
            QMessageBox.warning(self, "Error", "Entry name is required!")
            return
        
        if not password:
            QMessageBox.warning(self, "Error", "Password is required!")
            return
        
        # Create entry data
        entry_data = {
            "name": name,
            "username": username,
            "password": password,
            "url": url,
            "notes": notes
        }
        
        # Emit signal and close
        self.entry_added.emit(entry_data)
        self.close()


class EditEntryDialog(DialogBase):
    """Dialog for editing an existing entry"""
    
    entry_updated = Signal(dict)  # entry data
    
    def __init__(self, entry_data, parent=None):
        super().__init__(parent, "Edit Entry", 450, 400)
        self.entry_data = entry_data
        self.setup_dialog_ui()
        self.populate_fields()
    
    def setup_dialog_ui(self):
        """Setup the dialog UI"""
        layout = QVBoxLayout(self)
        
        # Form layout for inputs
        form_layout = QFormLayout()
        
        # Entry name
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter entry name")
        form_layout.addRow("Name:", self.name_input)
        
        # Username
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter username")
        form_layout.addRow("Username:", self.username_input)
        
        # Password
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Enter password")
        form_layout.addRow("Password:", self.password_input)
        
        # Show password checkbox
        self.show_password_checkbox = QCheckBox("Show password")
        self.show_password_checkbox.toggled.connect(self.toggle_password_visibility)
        form_layout.addRow("", self.show_password_checkbox)
        
        # URL
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("https://example.com")
        form_layout.addRow("URL:", self.url_input)
        
        # Notes
        self.notes_input = QTextEdit()
        self.notes_input.setMaximumHeight(100)
        self.notes_input.setPlaceholderText("Optional notes")
        form_layout.addRow("Notes:", self.notes_input)
        
        layout.addLayout(form_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.update_button = ModernButton("Update Entry")
        self.update_button.clicked.connect(self.update_entry)
        
        self.cancel_button = ModernButton("Cancel")
        self.cancel_button.clicked.connect(self.close)
        
        button_layout.addWidget(self.update_button)
        button_layout.addWidget(self.cancel_button)
        
        layout.addLayout(button_layout)
    
    def populate_fields(self):
        """Populate fields with existing entry data"""
        self.name_input.setText(self.entry_data.get("name", ""))
        self.username_input.setText(self.entry_data.get("username", ""))
        self.password_input.setText(self.entry_data.get("password", ""))
        self.url_input.setText(self.entry_data.get("url", ""))
        self.notes_input.setPlainText(self.entry_data.get("notes", ""))
    
    def toggle_password_visibility(self, checked):
        """Toggle password visibility"""
        if checked:
            self.password_input.setEchoMode(QLineEdit.Normal)
        else:
            self.password_input.setEchoMode(QLineEdit.Password)
    
    def update_entry(self):
        """Update the entry with validation"""
        name = self.name_input.text().strip()
        username = self.username_input.text().strip()
        password = self.password_input.text()
        url = self.url_input.text().strip()
        notes = self.notes_input.toPlainText().strip()
        
        # Validation
        if not name:
            QMessageBox.warning(self, "Error", "Entry name is required!")
            return
        
        if not password:
            QMessageBox.warning(self, "Error", "Password is required!")
            return
        
        # Create updated entry data
        entry_data = {
            "id": self.entry_data.get("id"),
            "name": name,
            "username": username,
            "password": password,
            "url": url,
            "notes": notes
        }
        
        # Emit signal and close
        self.entry_updated.emit(entry_data)
        self.close()


class GeneratePasswordDialog(DialogBase):
    """Dialog for generating passwords"""
    
    password_generated = Signal(str)  # generated password
    
    def __init__(self, parent=None):
        super().__init__(parent, "Generate Password", 400, 350)
        self.setup_dialog_ui()
    
    def setup_dialog_ui(self):
        """Setup the dialog UI"""
        layout = QVBoxLayout(self)
        
        # Password options group
        options_group = QGroupBox("Password Options")
        options_layout = QFormLayout(options_group)
        
        # Length
        self.length_spinbox = QSpinBox()
        self.length_spinbox.setRange(8, 128)
        self.length_spinbox.setValue(16)
        options_layout.addRow("Length:", self.length_spinbox)
        
        # Character sets
        self.uppercase_checkbox = QCheckBox("Include uppercase letters (A-Z)")
        self.uppercase_checkbox.setChecked(True)
        options_layout.addRow("", self.uppercase_checkbox)
        
        self.lowercase_checkbox = QCheckBox("Include lowercase letters (a-z)")
        self.lowercase_checkbox.setChecked(True)
        options_layout.addRow("", self.lowercase_checkbox)
        
        self.numbers_checkbox = QCheckBox("Include numbers (0-9)")
        self.numbers_checkbox.setChecked(True)
        options_layout.addRow("", self.numbers_checkbox)
        
        self.symbols_checkbox = QCheckBox("Include symbols (!@#$%^&*)")
        self.symbols_checkbox.setChecked(True)
        options_layout.addRow("", self.symbols_checkbox)
        
        layout.addWidget(options_group)
        
        # Generated password display
        password_group = QGroupBox("Generated Password")
        password_layout = QVBoxLayout(password_group)
        
        self.password_display = QLineEdit()
        self.password_display.setReadOnly(True)
        self.password_display.setStyleSheet("""
            QLineEdit {
                font-family: 'Courier New', monospace;
                font-size: 14px;
                padding: 8px;
            }
        """)
        password_layout.addWidget(self.password_display)
        
        # Generate button
        self.generate_button = ModernButton("Generate Password")
        self.generate_button.clicked.connect(self.generate_password)
        password_layout.addWidget(self.generate_button)
        
        layout.addWidget(password_group)
        
        # Action buttons
        button_layout = QHBoxLayout()
        
        self.copy_button = ModernButton("Copy to Clipboard")
        self.copy_button.clicked.connect(self.copy_to_clipboard)
        
        self.use_button = ModernButton("Use This Password")
        self.use_button.clicked.connect(self.use_password)
        
        self.cancel_button = ModernButton("Cancel")
        self.cancel_button.clicked.connect(self.close)
        
        button_layout.addWidget(self.copy_button)
        button_layout.addWidget(self.use_button)
        button_layout.addWidget(self.cancel_button)
        
        layout.addLayout(button_layout)
        
        # Generate initial password
        self.generate_password()
    
    def generate_password(self):
        """Generate a new password"""
        try:
            from pm_core.models_pydantic import PasswordGenerationConfig, generate_password_from_config
            
            config = PasswordGenerationConfig(
                length=self.length_spinbox.value(),
                include_uppercase=self.uppercase_checkbox.isChecked(),
                include_lowercase=self.lowercase_checkbox.isChecked(),
                include_numbers=self.numbers_checkbox.isChecked(),
                include_symbols=self.symbols_checkbox.isChecked()
            )
            
            password = generate_password_from_config(config)
            self.password_display.setText(password)
            
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to generate password: {e}")
    
    def copy_to_clipboard(self):
        """Copy password to clipboard"""
        password = self.password_display.text()
        if password:
            try:
                import pyperclip
                pyperclip.copy(password)
                QMessageBox.information(self, "Success", "Password copied to clipboard!")
            except ImportError:
                QMessageBox.warning(self, "Error", "pyperclip not available for clipboard operations")
    
    def use_password(self):
        """Use the generated password"""
        password = self.password_display.text()
        if password:
            self.password_generated.emit(password)
            self.close() 