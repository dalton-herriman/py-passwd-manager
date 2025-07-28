#!/usr/bin/env python3
"""
Main GUI application for the Password Manager
Modular version with separated components
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import sys
from pathlib import Path

from pm_core.vault_manager import VaultManager
from pm_core.utils import clipboard_handler

from .dialogs import CreateVaultDialog, AddEntryDialog, EditEntryDialog, GeneratePasswordDialog
from .components import SearchBox, StatusBar, ToolBar, TreeViewManager
from .events import EventHandler


class MultiVaultPasswordManagerGUI:
    """Main GUI application with modular components"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Multi-Vault Password Manager")
        self.root.geometry("1200x800")
        
        # Initialize components
        self.vault_manager = VaultManager()
        self.current_vault = None
        self.current_entries = []
        
        # Initialize event handler
        self.event_handler = EventHandler(self)
        
        # Setup UI
        self.setup_ui()
        self.setup_bindings()
        
        # Initial refresh
        self.refresh_vaults_list()
        
    def setup_ui(self):
        """Setup the main user interface"""
        # Configure style
        style = ttk.Style()
        style.theme_use("clam")
        
        # Main frame
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.rowconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(
            self.main_frame,
            text="🔐 Multi-Vault Password Manager",
            font=("Arial", 16, "bold"),
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 10))
        
        # Setup vaults section
        self.setup_vaults_section()
        
        # Setup entries section
        self.setup_entries_section()
        
        # Setup status bar
        self.setup_status_bar()
        
    def setup_vaults_section(self):
        """Setup the vaults section (left side)"""
        # Vaults frame
        vaults_frame = ttk.LabelFrame(self.main_frame, text="Vaults", padding="10")
        vaults_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        vaults_frame.columnconfigure(0, weight=1)
        vaults_frame.rowconfigure(1, weight=1)
        
        # Vault toolbar
        self.vault_toolbar = ToolBar(vaults_frame)
        self.vault_toolbar.add_button("Create", self.event_handler.create_vault)
        self.vault_toolbar.add_button("Delete", self.event_handler.delete_vault)
        self.vault_toolbar.add_separator()
        self.vault_toolbar.add_button("Rename", self.event_handler.rename_vault)
        self.vault_toolbar.add_button("Backup", self.event_handler.backup_vault)
        self.vault_toolbar.pack(fill=tk.X, pady=(0, 10))
        
        # Vaults list
        vaults_list_frame = ttk.Frame(vaults_frame)
        vaults_list_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        vaults_list_frame.columnconfigure(0, weight=1)
        vaults_list_frame.rowconfigure(0, weight=1)
        
        # Treeview for vaults
        vault_columns = ("Name", "Status", "Entries", "Created", "Last Accessed")
        self.vaults_tree = ttk.Treeview(
            vaults_list_frame, columns=vault_columns, show="headings", height=10
        )
        
        # Configure columns
        for col in vault_columns:
            self.vaults_tree.heading(col, text=col)
            self.vaults_tree.column(col, width=100)
        
        # Scrollbar for vaults
        vaults_scrollbar = ttk.Scrollbar(vaults_list_frame, orient=tk.VERTICAL, 
                                        command=self.vaults_tree.yview)
        self.vaults_tree.configure(yscrollcommand=vaults_scrollbar.set)
        
        # Pack vaults treeview
        self.vaults_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        vaults_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Initialize vaults tree manager
        self.vaults_manager = TreeViewManager(self.vaults_tree)
        
    def setup_entries_section(self):
        """Setup the entries section (right side)"""
        # Entries frame
        entries_frame = ttk.LabelFrame(self.main_frame, text="Entries", padding="10")
        entries_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        entries_frame.columnconfigure(0, weight=1)
        entries_frame.rowconfigure(1, weight=1)
        
        # Entries toolbar
        self.entries_toolbar = ToolBar(entries_frame)
        self.entries_toolbar.add_button("Add", self.event_handler.add_entry)
        self.entries_toolbar.add_button("Edit", self.event_handler.edit_entry)
        self.entries_toolbar.add_button("Delete", self.event_handler.delete_entry)
        self.entries_toolbar.add_separator()
        self.entries_toolbar.add_button("Copy Password", self.event_handler.copy_password)
        self.entries_toolbar.add_button("Generate", self.event_handler.generate_password)
        self.entries_toolbar.pack(fill=tk.X, pady=(0, 10))
        
        # Search box
        self.search_box = SearchBox(entries_frame, command=self.event_handler.on_search_change)
        self.search_box.pack(fill=tk.X, pady=(0, 10))
        
        # Entries list
        entries_list_frame = ttk.Frame(entries_frame)
        entries_list_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        entries_list_frame.columnconfigure(0, weight=1)
        entries_list_frame.rowconfigure(0, weight=1)
        
        # Treeview for entries
        entry_columns = ("Title", "Username", "URL", "Notes")
        self.entries_tree = ttk.Treeview(
            entries_list_frame, columns=entry_columns, show="headings", height=15
        )
        
        # Configure columns
        for col in entry_columns:
            self.entries_tree.heading(col, text=col)
            self.entries_tree.column(col, width=150)
        
        # Scrollbar for entries
        entries_scrollbar = ttk.Scrollbar(entries_list_frame, orient=tk.VERTICAL, 
                                        command=self.entries_tree.yview)
        self.entries_tree.configure(yscrollcommand=entries_scrollbar.set)
        
        # Pack entries treeview
        self.entries_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        entries_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Initialize entries tree manager
        self.entries_manager = TreeViewManager(self.entries_tree)
        
    def setup_status_bar(self):
        """Setup the status bar"""
        self.status_bar = StatusBar(self.main_frame)
        self.status_bar.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
    def setup_bindings(self):
        """Setup event bindings"""
        # Vault tree bindings
        self.vaults_tree.bind("<<TreeviewSelect>>", self.event_handler.on_vault_select)
        self.vaults_tree.bind("<Double-1>", self.event_handler.on_vault_double_click)
        
        # Entries tree bindings
        self.entries_tree.bind("<Double-1>", self.event_handler.on_entry_double_click)
        
        # Keyboard shortcuts
        self.root.bind("<Key>", self.event_handler.on_key_press)
        
    def refresh_vaults_list(self):
        """Refresh the vaults list"""
        try:
            self.status_bar.set_status("Refreshing vaults...")
            self.status_bar.show_progress()
            
            # Clear existing items
            self.vaults_manager.clear()
            
            # Get vaults from manager
            vaults = self.vault_manager.list_vaults()
            
            # Add vaults to treeview
            for vault in vaults:
                vault_info = self.vault_manager.get_vault_info(vault)
                values = (
                    vault,
                    vault_info.get("status", "Closed"),
                    vault_info.get("entry_count", 0),
                    vault_info.get("created", ""),
                    vault_info.get("last_accessed", "")
                )
                self.vaults_manager.add_item(values)
                
            self.status_bar.hide_progress()
            self.status_bar.set_status(f"Found {len(vaults)} vaults")
            
        except Exception as e:
            self.status_bar.hide_progress()
            self.status_bar.set_status(f"Error refreshing vaults: {e}")
            
    def refresh_entries(self):
        """Refresh the entries list"""
        if not self.current_vault:
            return
            
        try:
            self.status_bar.set_status("Refreshing entries...")
            self.status_bar.show_progress()
            
            # Clear existing items
            self.entries_manager.clear()
            
            # Get entries from current vault
            entries = self.vault_manager.list_entries(self.current_vault)
            self.current_entries = entries
            
            # Add entries to treeview
            for entry in entries:
                values = (
                    entry.get("title", ""),
                    entry.get("username", ""),
                    entry.get("url", ""),
                    entry.get("notes", "")[:50] + "..." if len(entry.get("notes", "")) > 50 else entry.get("notes", "")
                )
                self.entries_manager.add_item(values, tags=(entry.get("id"),))
                
            self.status_bar.hide_progress()
            self.status_bar.set_status(f"Found {len(entries)} entries in {self.current_vault}")
            
        except Exception as e:
            self.status_bar.hide_progress()
            self.status_bar.set_status(f"Error refreshing entries: {e}")
            
    def filter_entries(self, search_term):
        """Filter entries based on search term"""
        if not self.current_vault:
            return
            
        try:
            # Clear existing items
            self.entries_manager.clear()
            
            # Filter entries
            filtered_entries = []
            for entry in self.current_entries:
                if (search_term in entry.get("title", "").lower() or
                    search_term in entry.get("username", "").lower() or
                    search_term in entry.get("url", "").lower() or
                    search_term in entry.get("notes", "").lower()):
                    filtered_entries.append(entry)
            
            # Add filtered entries to treeview
            for entry in filtered_entries:
                values = (
                    entry.get("title", ""),
                    entry.get("username", ""),
                    entry.get("url", ""),
                    entry.get("notes", "")[:50] + "..." if len(entry.get("notes", "")) > 50 else entry.get("notes", "")
                )
                self.entries_manager.add_item(values, tags=(entry.get("id"),))
                
            self.status_bar.set_status(f"Found {len(filtered_entries)} matching entries")
            
        except Exception as e:
            self.status_bar.set_status(f"Error filtering entries: {e}")
            
    def get_selected_entry_data(self):
        """Get data for the currently selected entry"""
        selection = self.entries_tree.selection()
        if not selection:
            return None
            
        item_id = selection[0]
        tags = self.entries_tree.item(item_id)["tags"]
        
        if tags and self.current_entries:
            entry_id = tags[0]
            for entry in self.current_entries:
                if entry.get("id") == entry_id:
                    return entry
                    
        return None
        
    def open_vault(self, vault_name):
        """Open a vault"""
        try:
            self.vault_manager.open_vault(vault_name)
            self.current_vault = vault_name
            self.refresh_entries()
            self.status_bar.set_status(f"Opened vault: {vault_name}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open vault: {e}")
            
    def save_vault(self):
        """Save the current vault"""
        if not self.current_vault:
            messagebox.showwarning("Warning", "No vault selected")
            return
            
        try:
            self.vault_manager.save_vault(self.current_vault)
            self.status_bar.set_status(f"Saved vault: {self.current_vault}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save vault: {e}")
            
    def view_entry(self):
        """View entry details"""
        entry_data = self.get_selected_entry_data()
        if not entry_data:
            messagebox.showwarning("Warning", "Please select an entry to view")
            return
            
        details = f"""
Title: {entry_data.get('title', '')}
Username: {entry_data.get('username', '')}
Password: {'*' * len(entry_data.get('password', ''))}
URL: {entry_data.get('url', '')}
Notes: {entry_data.get('notes', '')}
        """
        
        messagebox.showinfo("Entry Details", details)


def main():
    """Main entry point for the GUI application"""
    root = tk.Tk()
    app = MultiVaultPasswordManagerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main() 