#!/usr/bin/env python3
"""
Event handling for the Password Manager GUI
"""

import tkinter as tk
from tkinter import messagebox
from .dialogs import CreateVaultDialog, AddEntryDialog, EditEntryDialog


class EventHandler:
    """Centralized event handling for the GUI"""
    
    def __init__(self, gui):
        self.gui = gui
        
    def on_vault_select(self, event):
        """Handle vault selection"""
        selection = self.gui.vaults_tree.selection()
        if selection:
            vault_name = self.gui.vaults_tree.item(selection[0])["values"][0]
            self.gui.current_vault = vault_name
            self.gui.refresh_entries()
            
    def on_vault_double_click(self, event):
        """Handle vault double-click (open vault)"""
        selection = self.gui.vaults_tree.selection()
        if selection:
            vault_name = self.gui.vaults_tree.item(selection[0])["values"][0]
            self.gui.open_vault(vault_name)
            
    def on_entry_double_click(self, event):
        """Handle entry double-click (view entry)"""
        selection = self.gui.entries_tree.selection()
        if selection:
            self.gui.view_entry()
            
    def on_search_change(self, *args):
        """Handle search text changes"""
        search_term = self.gui.search_var.get().lower()
        self.gui.filter_entries(search_term)
        
    def on_key_press(self, event):
        """Handle keyboard shortcuts"""
        if event.state & 4:  # Ctrl key
            if event.keysym == 'n':
                self.gui.add_entry()
            elif event.keysym == 'f':
                self.gui.search_entry.focus()
            elif event.keysym == 's':
                self.gui.save_vault()
            elif event.keysym == 'o':
                self.gui.open_vault_dialog()
                
    def create_vault(self):
        """Handle create vault button click"""
        dialog = CreateVaultDialog(self.gui.root, self.gui.vault_manager)
        self.gui.root.wait_window(dialog.dialog)
        
        if dialog.result:
            self.gui.refresh_vaults_list()
            messagebox.showinfo("Success", f"Vault '{dialog.result['name']}' created successfully!")
            
    def delete_vault(self):
        """Handle delete vault button click"""
        selection = self.gui.vaults_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a vault to delete")
            return
            
        vault_name = self.gui.vaults_tree.item(selection[0])["values"][0]
        
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete vault '{vault_name}'?"):
            try:
                self.gui.vault_manager.delete_vault(vault_name)
                self.gui.refresh_vaults_list()
                messagebox.showinfo("Success", f"Vault '{vault_name}' deleted successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete vault: {e}")
                
    def rename_vault(self):
        """Handle rename vault button click"""
        selection = self.gui.vaults_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a vault to rename")
            return
            
        vault_name = self.gui.vaults_tree.item(selection[0])["values"][0]
        new_name = tk.simpledialog.askstring("Rename Vault", 
                                           f"Enter new name for vault '{vault_name}':",
                                           initialvalue=vault_name)
        
        if new_name and new_name != vault_name:
            try:
                self.gui.vault_manager.rename_vault(vault_name, new_name)
                self.gui.refresh_vaults_list()
                messagebox.showinfo("Success", f"Vault renamed to '{new_name}' successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to rename vault: {e}")
                
    def backup_vault(self):
        """Handle backup vault button click"""
        selection = self.gui.vaults_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a vault to backup")
            return
            
        vault_name = self.gui.vaults_tree.item(selection[0])["values"][0]
        
        try:
            backup_path = self.gui.vault_manager.backup_vault(vault_name)
            messagebox.showinfo("Success", f"Vault backed up to: {backup_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to backup vault: {e}")
            
    def add_entry(self):
        """Handle add entry button click"""
        if not hasattr(self.gui, 'current_vault') or not self.gui.current_vault:
            messagebox.showwarning("Warning", "Please select a vault first")
            return
            
        dialog = AddEntryDialog(self.gui.root, self.gui)
        self.gui.root.wait_window(dialog.dialog)
        
        if dialog.result:
            try:
                self.gui.vault_manager.add_entry(self.gui.current_vault, dialog.result)
                self.gui.refresh_entries()
                messagebox.showinfo("Success", "Entry added successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add entry: {e}")
                
    def edit_entry(self):
        """Handle edit entry button click"""
        selection = self.gui.entries_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an entry to edit")
            return
            
        entry_data = self.gui.get_selected_entry_data()
        if not entry_data:
            return
            
        dialog = EditEntryDialog(self.gui.root, self.gui, entry_data)
        self.gui.root.wait_window(dialog.dialog)
        
        if dialog.result:
            try:
                self.gui.vault_manager.update_entry(self.gui.current_vault, 
                                                  entry_data["id"], dialog.result)
                self.gui.refresh_entries()
                messagebox.showinfo("Success", "Entry updated successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update entry: {e}")
                
    def delete_entry(self):
        """Handle delete entry button click"""
        selection = self.gui.entries_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an entry to delete")
            return
            
        entry_data = self.gui.get_selected_entry_data()
        if not entry_data:
            return
            
        if messagebox.askyesno("Confirm Delete", 
                              f"Are you sure you want to delete entry '{entry_data['title']}'?"):
            try:
                self.gui.vault_manager.delete_entry(self.gui.current_vault, entry_data["id"])
                self.gui.refresh_entries()
                messagebox.showinfo("Success", "Entry deleted successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete entry: {e}")
                
    def copy_password(self):
        """Handle copy password button click"""
        selection = self.gui.entries_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an entry to copy password")
            return
            
        entry_data = self.gui.get_selected_entry_data()
        if not entry_data:
            return
            
        try:
            from pm_core.utils import clipboard_handler
            clipboard_handler(entry_data["password"])
            messagebox.showinfo("Success", "Password copied to clipboard!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to copy password: {e}")
            
    def generate_password(self):
        """Handle generate password button click"""
        from .dialogs import GeneratePasswordDialog
        
        dialog = GeneratePasswordDialog(self.gui.root)
        self.gui.root.wait_window(dialog.dialog)
        
        if dialog.result:
            # This could be used to populate a password field in a dialog
            messagebox.showinfo("Generated Password", f"Generated password: {dialog.result}")
            
    def refresh_data(self):
        """Handle refresh button click"""
        self.gui.refresh_vaults_list()
        self.gui.refresh_entries()
        messagebox.showinfo("Success", "Data refreshed successfully!")
        
    def show_about(self):
        """Handle about button click"""
        about_text = """
🔐 Multi-Vault Password Manager

A secure, cross-platform password manager with multi-vault support.

Features:
• Multiple vaults for organization
• Strong encryption
• Password generation
• Clipboard integration
• Cross-platform support

Version: 1.0.0
        """
        messagebox.showinfo("About", about_text)
        
    def show_help(self):
        """Handle help button click"""
        help_text = """
🔐 Password Manager Help

Keyboard Shortcuts:
• Ctrl+N: Add new entry
• Ctrl+F: Focus search
• Ctrl+S: Save vault
• Ctrl+O: Open vault

Operations:
• Double-click vault to open
• Double-click entry to view
• Use search to filter entries
• Right-click for context menu

Security:
• Always use strong passwords
• Keep your master password safe
• Regular backups recommended
        """
        messagebox.showinfo("Help", help_text) 