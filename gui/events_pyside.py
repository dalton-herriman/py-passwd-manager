#!/usr/bin/env python3
"""
PySide6-based event handler for the Password Manager GUI
Handles all user interactions and business logic
"""

from PySide6.QtCore import QObject, Signal, QTimer
from PySide6.QtWidgets import QMessageBox, QInputDialog
from PySide6.QtGui import QKeySequence

from .dialogs_pyside import (
    CreateVaultDialog, AddEntryDialog, EditEntryDialog, GeneratePasswordDialog
)


class EventHandler(QObject):
    """Event handler for the password manager GUI"""
    
    # Signals for UI updates
    vault_created = Signal(str, str, str)  # name, password, description
    vault_opened = Signal(str)
    vault_closed = Signal()
    entry_added = Signal(dict)
    entry_updated = Signal(dict)
    entry_deleted = Signal(int)
    password_copied = Signal(str)
    status_updated = Signal(str)
    
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.vault_manager = main_window.vault_manager
        self.current_vault = None
        self.current_entries = []
        
        # Connect signals
        self.vault_created.connect(self.main_window.on_vault_created)
        self.vault_opened.connect(self.main_window.on_vault_opened)
        self.vault_closed.connect(self.main_window.on_vault_closed)
        self.entry_added.connect(self.main_window.on_entry_added)
        self.entry_updated.connect(self.main_window.on_entry_updated)
        self.entry_deleted.connect(self.main_window.on_entry_deleted)
        self.password_copied.connect(self.main_window.on_password_copied)
        self.status_updated.connect(self.main_window.on_status_updated)
    
    def create_vault(self):
        """Create a new vault"""
        try:
            dialog = CreateVaultDialog(self.main_window)
            dialog.vault_created.connect(self._handle_vault_created)
            dialog.show_dialog()
        except Exception as e:
            QMessageBox.critical(self.main_window, "Error", f"Failed to create vault: {e}")
    
    def _handle_vault_created(self, name, password, description):
        """Handle vault creation"""
        try:
            self.vault_manager.create_vault(name, password, description)
            self.vault_created.emit(name, password, description)
            self.status_updated.emit(f"Vault '{name}' created successfully")
        except Exception as e:
            QMessageBox.critical(self.main_window, "Error", f"Failed to create vault: {e}")
    
    def delete_vault(self):
        """Delete the selected vault"""
        try:
            selected_item = self.main_window.vaults_manager.get_selected_item()
            if not selected_item:
                QMessageBox.warning(self.main_window, "Warning", "Please select a vault to delete")
                return
            
            vault_name = selected_item.text(0)
            
            # Confirm deletion
            reply = QMessageBox.question(
                self.main_window, 
                "Confirm Deletion", 
                f"Are you sure you want to delete vault '{vault_name}'?\n\nThis action cannot be undone!",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                self.vault_manager.delete_vault(vault_name)
                self.main_window.refresh_vaults_list()
                self.status_updated.emit(f"Vault '{vault_name}' deleted")
                
        except Exception as e:
            QMessageBox.critical(self.main_window, "Error", f"Failed to delete vault: {e}")
    
    def rename_vault(self):
        """Rename the selected vault"""
        try:
            selected_item = self.main_window.vaults_manager.get_selected_item()
            if not selected_item:
                QMessageBox.warning(self.main_window, "Warning", "Please select a vault to rename")
                return
            
            old_name = selected_item.text(0)
            new_name, ok = QInputDialog.getText(
                self.main_window, 
                "Rename Vault", 
                f"Enter new name for vault '{old_name}':",
                text=old_name
            )
            
            if ok and new_name.strip():
                self.vault_manager.rename_vault(old_name, new_name.strip())
                self.main_window.refresh_vaults_list()
                self.status_updated.emit(f"Vault renamed to '{new_name}'")
                
        except Exception as e:
            QMessageBox.critical(self.main_window, "Error", f"Failed to rename vault: {e}")
    
    def backup_vault(self):
        """Backup the selected vault"""
        try:
            selected_item = self.main_window.vaults_manager.get_selected_item()
            if not selected_item:
                QMessageBox.warning(self.main_window, "Warning", "Please select a vault to backup")
                return
            
            vault_name = selected_item.text(0)
            # TODO: Implement backup functionality
            QMessageBox.information(self.main_window, "Info", f"Backup functionality for '{vault_name}' not yet implemented")
            
        except Exception as e:
            QMessageBox.critical(self.main_window, "Error", f"Failed to backup vault: {e}")
    
    def open_vault(self, vault_name=None):
        """Open a vault"""
        try:
            if not vault_name:
                selected_item = self.main_window.vaults_manager.get_selected_item()
                if not selected_item:
                    QMessageBox.warning(self.main_window, "Warning", "Please select a vault to open")
                    return
                vault_name = selected_item.text(0)
            
            # Get master password
            password, ok = QInputDialog.getText(
                self.main_window, 
                "Open Vault", 
                f"Enter master password for vault '{vault_name}':",
                echo=QInputDialog.Password
            )
            
            if ok and password:
                self.vault_manager.open_vault(vault_name, password)
                self.current_vault = vault_name
                self.vault_opened.emit(vault_name)
                self.main_window.refresh_entries()
                self.status_updated.emit(f"Vault '{vault_name}' opened successfully")
                
        except Exception as e:
            QMessageBox.critical(self.main_window, "Error", f"Failed to open vault: {e}")
    
    def close_vault(self):
        """Close the current vault"""
        try:
            if self.current_vault:
                self.vault_manager.close_vault()
                self.current_vault = None
                self.vault_closed.emit()
                self.main_window.refresh_entries()
                self.status_updated.emit("Vault closed")
            else:
                QMessageBox.information(self.main_window, "Info", "No vault is currently open")
                
        except Exception as e:
            QMessageBox.critical(self.main_window, "Error", f"Failed to close vault: {e}")
    
    def add_entry(self):
        """Add a new entry to the current vault"""
        try:
            if not self.current_vault:
                QMessageBox.warning(self.main_window, "Warning", "Please open a vault first")
                return
            
            dialog = AddEntryDialog(self.main_window)
            dialog.entry_added.connect(self._handle_entry_added)
            dialog.show_dialog()
            
        except Exception as e:
            QMessageBox.critical(self.main_window, "Error", f"Failed to add entry: {e}")
    
    def _handle_entry_added(self, entry_data):
        """Handle entry addition"""
        try:
            self.vault_manager.add_entry(entry_data)
            self.entry_added.emit(entry_data)
            self.main_window.refresh_entries()
            self.status_updated.emit(f"Entry '{entry_data['name']}' added successfully")
            
        except Exception as e:
            QMessageBox.critical(self.main_window, "Error", f"Failed to add entry: {e}")
    
    def edit_entry(self):
        """Edit the selected entry"""
        try:
            if not self.current_vault:
                QMessageBox.warning(self.main_window, "Warning", "Please open a vault first")
                return
            
            selected_item = self.main_window.entries_manager.get_selected_item()
            if not selected_item:
                QMessageBox.warning(self.main_window, "Warning", "Please select an entry to edit")
                return
            
            # Get entry data
            entry_values = self.main_window.entries_manager.get_selected_values()
            if not entry_values:
                return
            
            # Find the entry in current entries
            entry_data = None
            for entry in self.current_entries:
                if entry.get('name') == entry_values[0]:
                    entry_data = entry
                    break
            
            if not entry_data:
                QMessageBox.warning(self.main_window, "Warning", "Entry not found")
                return
            
            dialog = EditEntryDialog(entry_data, self.main_window)
            dialog.entry_updated.connect(self._handle_entry_updated)
            dialog.show_dialog()
            
        except Exception as e:
            QMessageBox.critical(self.main_window, "Error", f"Failed to edit entry: {e}")
    
    def _handle_entry_updated(self, entry_data):
        """Handle entry update"""
        try:
            self.vault_manager.update_entry(entry_data['id'], entry_data)
            self.entry_updated.emit(entry_data)
            self.main_window.refresh_entries()
            self.status_updated.emit(f"Entry '{entry_data['name']}' updated successfully")
            
        except Exception as e:
            QMessageBox.critical(self.main_window, "Error", f"Failed to update entry: {e}")
    
    def delete_entry(self):
        """Delete the selected entry"""
        try:
            if not self.current_vault:
                QMessageBox.warning(self.main_window, "Warning", "Please open a vault first")
                return
            
            selected_item = self.main_window.entries_manager.get_selected_item()
            if not selected_item:
                QMessageBox.warning(self.main_window, "Warning", "Please select an entry to delete")
                return
            
            entry_values = self.main_window.entries_manager.get_selected_values()
            if not entry_values:
                return
            
            entry_name = entry_values[0]
            
            # Confirm deletion
            reply = QMessageBox.question(
                self.main_window, 
                "Confirm Deletion", 
                f"Are you sure you want to delete entry '{entry_name}'?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                # Find entry ID
                entry_id = None
                for entry in self.current_entries:
                    if entry.get('name') == entry_name:
                        entry_id = entry.get('id')
                        break
                
                if entry_id:
                    self.vault_manager.delete_entry(entry_id)
                    self.entry_deleted.emit(entry_id)
                    self.main_window.refresh_entries()
                    self.status_updated.emit(f"Entry '{entry_name}' deleted")
                
        except Exception as e:
            QMessageBox.critical(self.main_window, "Error", f"Failed to delete entry: {e}")
    
    def copy_password(self):
        """Copy the selected entry's password to clipboard"""
        try:
            if not self.current_vault:
                QMessageBox.warning(self.main_window, "Warning", "Please open a vault first")
                return
            
            selected_item = self.main_window.entries_manager.get_selected_item()
            if not selected_item:
                QMessageBox.warning(self.main_window, "Warning", "Please select an entry")
                return
            
            entry_values = self.main_window.entries_manager.get_selected_values()
            if not entry_values:
                return
            
            entry_name = entry_values[0]
            
            # Find the entry password
            password = None
            for entry in self.current_entries:
                if entry.get('name') == entry_name:
                    password = entry.get('password')
                    break
            
            if password:
                try:
                    import pyperclip
                    pyperclip.copy(password)
                    self.password_copied.emit(password)
                    self.status_updated.emit(f"Password for '{entry_name}' copied to clipboard")
                except ImportError:
                    QMessageBox.warning(self.main_window, "Error", "pyperclip not available for clipboard operations")
            else:
                QMessageBox.warning(self.main_window, "Warning", "No password found for this entry")
                
        except Exception as e:
            QMessageBox.critical(self.main_window, "Error", f"Failed to copy password: {e}")
    
    def generate_password(self):
        """Generate a new password"""
        try:
            dialog = GeneratePasswordDialog(self.main_window)
            dialog.password_generated.connect(self._handle_password_generated)
            dialog.show_dialog()
            
        except Exception as e:
            QMessageBox.critical(self.main_window, "Error", f"Failed to generate password: {e}")
    
    def _handle_password_generated(self, password):
        """Handle password generation"""
        try:
            # Copy to clipboard
            import pyperclip
            pyperclip.copy(password)
            self.password_copied.emit(password)
            self.status_updated.emit("Generated password copied to clipboard")
            
        except ImportError:
            QMessageBox.warning(self.main_window, "Error", "pyperclip not available for clipboard operations")
    
    def on_search_change(self, search_text):
        """Handle search text changes"""
        try:
            self.main_window.filter_entries(search_text)
            self.status_updated.emit(f"Searching for: {search_text}")
            
        except Exception as e:
            QMessageBox.critical(self.main_window, "Error", f"Search failed: {e}")
    
    def on_vault_select(self):
        """Handle vault selection"""
        try:
            selected_item = self.main_window.vaults_manager.get_selected_item()
            if selected_item:
                vault_name = selected_item.text(0)
                self.status_updated.emit(f"Selected vault: {vault_name}")
                
        except Exception as e:
            self.status_updated.emit(f"Selection error: {e}")
    
    def on_vault_double_click(self):
        """Handle vault double-click (open vault)"""
        self.open_vault()
    
    def on_entry_double_click(self):
        """Handle entry double-click (edit entry)"""
        self.edit_entry()
    
    def on_key_press(self, event):
        """Handle keyboard shortcuts"""
        try:
            # Ctrl+N: New entry
            if event.key() == ord('N') and event.modifiers() == Qt.ControlModifier:
                self.add_entry()
            
            # Ctrl+E: Edit entry
            elif event.key() == ord('E') and event.modifiers() == Qt.ControlModifier:
                self.edit_entry()
            
            # Delete: Delete entry
            elif event.key() == Qt.Key_Delete:
                self.delete_entry()
            
            # Ctrl+C: Copy password
            elif event.key() == ord('C') and event.modifiers() == Qt.ControlModifier:
                self.copy_password()
            
            # Ctrl+G: Generate password
            elif event.key() == ord('G') and event.modifiers() == Qt.ControlModifier:
                self.generate_password()
                
        except Exception as e:
            self.status_updated.emit(f"Keyboard shortcut error: {e}")
    
    def set_current_entries(self, entries):
        """Set the current entries list"""
        self.current_entries = entries 