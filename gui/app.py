#!/usr/bin/env python3
"""
Multi-vault GUI application for the password manager
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import threading
import sys
from pathlib import Path

from pm_core.vault_manager import VaultManager
from pm_core.utils import generate_password, clipboard_handler, validate_password_strength

class MultiVaultPasswordManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Multi-Vault Password Manager")
        self.root.geometry("1200x800")
        
        print("DEBUG: Initializing MultiVaultPasswordManagerGUI...")
        
        # Initialize vault manager
        self.vault_manager = VaultManager()
        self.current_entries = []
        
        print("DEBUG: Setting up UI...")
        self.setup_ui()
        print("DEBUG: UI setup complete.")
        
        print("DEBUG: Refreshing vaults list...")
        self.refresh_vaults_list()
        print("DEBUG: Initial refresh complete.")
    
    def setup_ui(self):
        """Setup the user interface"""
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="🔐 Multi-Vault Password Manager", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 10))
        
        # Vaults section (left side)
        vaults_frame = ttk.LabelFrame(main_frame, text="Vaults", padding="10")
        vaults_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        vaults_frame.columnconfigure(0, weight=1)
        vaults_frame.rowconfigure(1, weight=1)
        
        # Vault buttons
        vault_buttons_frame = ttk.Frame(vaults_frame)
        vault_buttons_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Button(vault_buttons_frame, text="Create Vault", 
                  command=self.create_vault).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(vault_buttons_frame, text="Delete Vault", 
                  command=self.delete_vault).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(vault_buttons_frame, text="Rename Vault", 
                  command=self.rename_vault).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(vault_buttons_frame, text="Backup Vault", 
                  command=self.backup_vault).pack(side=tk.LEFT, padx=(0, 5))
        
        # Vaults list
        vaults_list_frame = ttk.Frame(vaults_frame)
        vaults_list_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        vaults_list_frame.columnconfigure(0, weight=1)
        vaults_list_frame.rowconfigure(0, weight=1)
        
        # Treeview for vaults
        vault_columns = ('Name', 'Status', 'Entries', 'Created', 'Last Accessed')
        self.vaults_tree = ttk.Treeview(vaults_list_frame, columns=vault_columns, 
                                       show='headings', height=10)
        
        # Configure vault columns
        self.vaults_tree.heading('Name', text='Name')
        self.vaults_tree.heading('Status', text='Status')
        self.vaults_tree.heading('Entries', text='Entries')
        self.vaults_tree.heading('Created', text='Created')
        self.vaults_tree.heading('Last Accessed', text='Last Accessed')
        
        self.vaults_tree.column('Name', width=120)
        self.vaults_tree.column('Status', width=80)
        self.vaults_tree.column('Entries', width=60)
        self.vaults_tree.column('Created', width=100)
        self.vaults_tree.column('Last Accessed', width=100)
        
        # Vault scrollbar
        vault_scrollbar = ttk.Scrollbar(vaults_list_frame, orient=tk.VERTICAL, 
                                       command=self.vaults_tree.yview)
        self.vaults_tree.configure(yscrollcommand=vault_scrollbar.set)
        
        self.vaults_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        vault_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Bind vault selection
        self.vaults_tree.bind('<<TreeviewSelect>>', self.on_vault_select)
        self.vaults_tree.bind('<Double-1>', self.on_vault_double_click)
        
        # Entries section (right side)
        entries_frame = ttk.LabelFrame(main_frame, text="Entries", padding="10")
        entries_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        entries_frame.columnconfigure(0, weight=1)
        entries_frame.rowconfigure(2, weight=1)
        
        # Current vault status
        self.vault_status_label = ttk.Label(entries_frame, text="No vault selected")
        self.vault_status_label.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Entry buttons
        entry_buttons_frame = ttk.Frame(entries_frame)
        entry_buttons_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.open_vault_btn = ttk.Button(entry_buttons_frame, text="Open Vault", 
                                        command=self.open_vault)
        self.open_vault_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        self.close_vault_btn = ttk.Button(entry_buttons_frame, text="Close Vault", 
                                         command=self.close_vault)
        self.close_vault_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        self.add_entry_btn = ttk.Button(entry_buttons_frame, text="Add Entry", 
                                       command=self.add_entry)
        self.add_entry_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        self.save_vault_btn = ttk.Button(entry_buttons_frame, text="Save Vault", 
                                        command=self.save_vault)
        self.save_vault_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        self.generate_btn = ttk.Button(entry_buttons_frame, text="Generate Password", 
                                      command=self.generate_password)
        self.generate_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        # Search frame
        search_frame = ttk.Frame(entries_frame)
        search_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.on_search_change)
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=40)
        search_entry.pack(side=tk.LEFT, padx=(5, 0))
        
        # Entries list
        entries_list_frame = ttk.Frame(entries_frame)
        entries_list_frame.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        entries_list_frame.columnconfigure(0, weight=1)
        entries_list_frame.rowconfigure(0, weight=1)
        
        # Treeview for entries
        entry_columns = ('ID', 'Service', 'Username', 'URL', 'Created')
        self.entries_tree = ttk.Treeview(entries_list_frame, columns=entry_columns, 
                                        show='headings', height=15)
        
        # Configure entry columns
        self.entries_tree.heading('ID', text='ID')
        self.entries_tree.heading('Service', text='Service')
        self.entries_tree.heading('Username', text='Username')
        self.entries_tree.heading('URL', text='URL')
        self.entries_tree.heading('Created', text='Created')
        
        self.entries_tree.column('ID', width=50)
        self.entries_tree.column('Service', width=150)
        self.entries_tree.column('Username', width=150)
        self.entries_tree.column('URL', width=200)
        self.entries_tree.column('Created', width=150)
        
        # Entry scrollbar
        entry_scrollbar = ttk.Scrollbar(entries_list_frame, orient=tk.VERTICAL, 
                                       command=self.entries_tree.yview)
        self.entries_tree.configure(yscrollcommand=entry_scrollbar.set)
        
        self.entries_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        entry_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Bind entry double-click
        self.entries_tree.bind('<Double-1>', self.on_entry_double_click)
        
        # Entry action buttons
        entry_action_frame = ttk.Frame(entries_frame)
        entry_action_frame.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        
        self.view_entry_btn = ttk.Button(entry_action_frame, text="View Entry", 
                                        command=self.view_entry)
        self.view_entry_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        self.edit_entry_btn = ttk.Button(entry_action_frame, text="Edit Entry", 
                                        command=self.edit_entry)
        self.edit_entry_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        self.delete_entry_btn = ttk.Button(entry_action_frame, text="Delete Entry", 
                                          command=self.delete_entry)
        self.delete_entry_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        self.copy_password_btn = ttk.Button(entry_action_frame, text="Copy Password", 
                                           command=self.copy_password)
        self.copy_password_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        # Stats label
        self.stats_label = ttk.Label(entries_frame, text="")
        self.stats_label.grid(row=5, column=0, pady=(10, 0))
        
        # Initially disable buttons that require an open vault
        self.set_vault_state(False)
    
    def refresh_vaults_list(self):
        """Refresh the vaults list"""
        try:
            print("DEBUG: refresh_vaults_list called")
            vaults = self.vault_manager.list_vaults()
            print(f"DEBUG: Found {len(vaults)} vaults")
            
            # Clear existing items
            for item in self.vaults_tree.get_children():
                self.vaults_tree.delete(item)
            
            # Add vaults
            for vault in vaults:
                print(f"DEBUG: Adding vault to tree: {vault.name} ({vault.entry_count} entries)")
                status = "🔓 OPEN" if self.vault_manager.get_current_vault_name() == vault.name else "🔒 LOCKED"
                values = (
                    vault.name,
                    status,
                    vault.entry_count,
                    vault.created_at.strftime('%Y-%m-%d'),
                    vault.last_accessed.strftime('%Y-%m-%d')
                )
                print(f"DEBUG: Inserting values: {values}")
                self.vaults_tree.insert('', 'end', values=values)
            
            print(f"DEBUG: Treeview now has {len(self.vaults_tree.get_children())} items")
        except Exception as e:
            print(f"DEBUG: Error in refresh_vaults_list: {e}")
            messagebox.showerror("Error", f"Failed to refresh vaults: {str(e)}")
    
    def on_vault_select(self, event):
        """Handle vault selection"""
        selection = self.vaults_tree.selection()
        if selection:
            item = self.vaults_tree.item(selection[0])
            vault_name = item['values'][0]
            self.vault_status_label.config(text=f"Selected vault: {vault_name}")
        else:
            self.vault_status_label.config(text="No vault selected")
    
    def on_vault_double_click(self, event):
        """Handle vault double-click"""
        self.open_vault()
    
    def create_vault(self):
        """Create a new vault"""
        dialog = CreateVaultDialog(self.root, self.vault_manager)
        if dialog.result:
            self.refresh_vaults_list()
    
    def delete_vault(self):
        """Delete selected vault"""
        selection = self.vaults_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a vault to delete")
            return
        
        item = self.vaults_tree.item(selection[0])
        vault_name = item['values'][0]
        
        if messagebox.askyesno("Confirm Delete", 
                              f"Are you sure you want to delete vault '{vault_name}'? This cannot be undone."):
            try:
                self.vault_manager.delete_vault(vault_name)
                self.refresh_vaults_list()
                if self.vault_manager.get_current_vault_name() == vault_name:
                    self.close_vault()
                messagebox.showinfo("Success", f"Vault '{vault_name}' deleted successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete vault: {str(e)}")
    
    def rename_vault(self):
        """Rename selected vault"""
        selection = self.vaults_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a vault to rename")
            return
        
        item = self.vaults_tree.item(selection[0])
        old_name = item['values'][0]
        
        new_name = simpledialog.askstring("Rename Vault", f"Enter new name for vault '{old_name}':")
        if not new_name:
            return
        
        try:
            self.vault_manager.rename_vault(old_name, new_name)
            self.refresh_vaults_list()
            messagebox.showinfo("Success", f"Vault renamed to '{new_name}'")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to rename vault: {str(e)}")
    
    def backup_vault(self):
        """Backup selected vault"""
        selection = self.vaults_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a vault to backup")
            return
        
        item = self.vaults_tree.item(selection[0])
        vault_name = item['values'][0]
        
        from tkinter import filedialog
        backup_path = filedialog.asksaveasfilename(
            title=f"Backup vault '{vault_name}'",
            defaultextension=".db",
            filetypes=[("Database files", "*.db"), ("All files", "*.*")]
        )
        
        if backup_path:
            try:
                self.vault_manager.backup_vault(vault_name, backup_path)
                messagebox.showinfo("Success", f"Vault '{vault_name}' backed up successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to backup vault: {str(e)}")
    
    def open_vault(self):
        """Open selected vault"""
        selection = self.vaults_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a vault to open")
            return
        
        item = self.vaults_tree.item(selection[0])
        vault_name = item['values'][0]
        
        password = simpledialog.askstring("Open Vault", f"Enter master password for vault '{vault_name}':", 
                                        show='*')
        if not password:
            return
        
        try:
            self.vault_manager.open_vault(vault_name, password)
            self.set_vault_state(True)
            self.vault_status_label.config(text=f"Vault '{vault_name}' is open")
            self.refresh_entries()
            self.refresh_vaults_list()
            messagebox.showinfo("Success", f"Vault '{vault_name}' opened successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open vault: {str(e)}")
    
    def close_vault(self):
        """Close the currently open vault"""
        if not self.vault_manager.get_current_vault():
            messagebox.showwarning("Warning", "No vault is currently open")
            return
        
        try:
            self.vault_manager.close_vault()
            self.set_vault_state(False)
            self.vault_status_label.config(text="No vault open")
            self.clear_entries()
            self.refresh_vaults_list()
            messagebox.showinfo("Success", "Vault closed")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to close vault: {str(e)}")
    
    def save_vault(self):
        """Save the current vault"""
        if not self.vault_manager.get_current_vault():
            messagebox.showwarning("Warning", "No vault is currently open")
            return
        
        password = simpledialog.askstring("Save Vault", "Enter master password:", show='*')
        if not password:
            return
        
        try:
            self.vault_manager.get_current_vault().save_vault(password)
            # Update entry count in registry
            current_vault_name = self.vault_manager.get_current_vault_name()
            if current_vault_name:
                entry_count = len(self.vault_manager.get_current_vault().get_entry())
                self.vault_manager.update_vault_entry_count(current_vault_name, entry_count)
            messagebox.showinfo("Success", "Vault saved successfully!")
            self.refresh_vaults_list()  # Refresh vault list to show updated entry count
            
            # Force the GUI to update
            self.root.update_idletasks()
            self.root.update()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save vault: {str(e)}")
    
    def set_vault_state(self, vault_open):
        """Enable/disable buttons based on vault state"""
        state = 'normal' if vault_open else 'disabled'
        self.add_entry_btn.config(state=state)
        self.save_vault_btn.config(state=state)
        self.view_entry_btn.config(state=state)
        self.edit_entry_btn.config(state=state)
        self.delete_entry_btn.config(state=state)
        self.copy_password_btn.config(state=state)
        self.generate_btn.config(state='normal')  # Always available
    
    def add_entry(self):
        """Add a new entry"""
        if not self.vault_manager.get_current_vault():
            messagebox.showwarning("Warning", "Please open a vault first")
            return
        
        print("DEBUG: Starting add_entry process")
        dialog = AddEntryDialog(self.root, self.vault_manager.get_current_vault())
        if dialog.result:
            print(f"DEBUG: Entry added successfully: {dialog.result.name}")
            # Auto-save the vault after adding entry
            try:
                # Get the master password for saving
                master_password = simpledialog.askstring("Save Vault", 
                                                      "Enter master password to save the vault:", 
                                                      show='*')
                if master_password:
                    print("DEBUG: Saving vault with master password")
                    self.vault_manager.get_current_vault().save_vault(master_password)
                    # Update entry count in registry
                    current_vault_name = self.vault_manager.get_current_vault_name()
                    if current_vault_name:
                        entry_count = len(self.vault_manager.get_current_vault().get_entry())
                        self.vault_manager.update_vault_entry_count(current_vault_name, entry_count)
                    messagebox.showinfo("Success", "Entry added and vault saved!")
                else:
                    messagebox.showwarning("Warning", "Entry added but vault not saved. Use 'Save Vault' to persist changes.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save vault: {str(e)}")
            
            print("DEBUG: About to refresh entries")
            # Force refresh the entries display
            self.refresh_entries()
            self.refresh_vaults_list()  # Refresh vault list to show updated entry count
            
            # Force the GUI to update
            self.root.update_idletasks()
            self.root.update()
            
            # Force a complete treeview rebuild after a short delay
            self.root.after(200, self._complete_treeview_rebuild)
            
            print("DEBUG: Refresh completed")
        else:
            print("DEBUG: No entry was added (dialog cancelled)")
    
    def _complete_treeview_rebuild(self):
        """Completely rebuild the treeview"""
        try:
            print("DEBUG: Starting complete treeview rebuild")
            
            # Get fresh entries
            if self.vault_manager.get_current_vault():
                entries = self.vault_manager.get_current_vault().get_entry()
                print(f"DEBUG: Rebuild found {len(entries)} entries")
                
                # Clear treeview
                for item in self.entries_tree.get_children():
                    self.entries_tree.delete(item)
                
                # Rebuild treeview
                for entry in entries:
                    values = (
                        entry.id,
                        entry.name,
                        entry.username or '',
                        entry.url or '',
                        entry.created_at.strftime('%Y-%m-%d %H:%M')
                    )
                    print(f"DEBUG: Rebuild adding: {values}")
                    self.entries_tree.insert('', 'end', values=values)
                
                print(f"DEBUG: Rebuild completed - {len(self.entries_tree.get_children())} items")
                
                # Force treeview to redraw
                self.entries_tree.see('')
                self.entries_tree.update()
                
        except Exception as e:
            print(f"DEBUG: Error in complete rebuild: {e}")
    
    def view_entry(self):
        """View selected entry details"""
        if not self.vault_manager.get_current_vault():
            messagebox.showwarning("Warning", "Please open a vault first")
            return
        
        selection = self.entries_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an entry to view")
            return
        
        item = self.entries_tree.item(selection[0])
        entry_id = int(item['values'][0])
        
        entries = self.vault_manager.get_current_vault().get_entry(entry_id=entry_id)
        if entries:
            entry = entries[0]
            self.show_entry_details(entry)
    
    def edit_entry(self):
        """Edit selected entry"""
        if not self.vault_manager.get_current_vault():
            messagebox.showwarning("Warning", "Please open a vault first")
            return
        
        selection = self.entries_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an entry to edit")
            return
        
        item = self.entries_tree.item(selection[0])
        entry_id = int(item['values'][0])
        
        entries = self.vault_manager.get_current_vault().get_entry(entry_id=entry_id)
        if entries:
            entry = entries[0]
            dialog = EditEntryDialog(self.root, self.vault_manager.get_current_vault(), entry)
            if dialog.result:
                # Auto-save the vault after editing entry
                try:
                    # Get the master password for saving
                    master_password = simpledialog.askstring("Save Vault", 
                                                          "Enter master password to save the vault:", 
                                                          show='*')
                    if master_password:
                        self.vault_manager.get_current_vault().save_vault(master_password)
                        # Update entry count in registry
                        current_vault_name = self.vault_manager.get_current_vault_name()
                        if current_vault_name:
                            entry_count = len(self.vault_manager.get_current_vault().get_entry())
                            self.vault_manager.update_vault_entry_count(current_vault_name, entry_count)
                        messagebox.showinfo("Success", "Entry updated and vault saved!")
                    else:
                        messagebox.showwarning("Warning", "Entry updated but vault not saved. Use 'Save Vault' to persist changes.")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to save vault: {str(e)}")
                
                self.refresh_entries()
                self.refresh_vaults_list()  # Refresh vault list to show updated entry count
                
                # Force the GUI to update
                self.root.update_idletasks()
                self.root.update()
    
    def delete_entry(self):
        """Delete selected entry"""
        if not self.vault_manager.get_current_vault():
            messagebox.showwarning("Warning", "Please open a vault first")
            return
        
        selection = self.entries_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an entry to delete")
            return
        
        item = self.entries_tree.item(selection[0])
        entry_id = int(item['values'][0])
        
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete entry {entry_id}?"):
            try:
                self.vault_manager.get_current_vault().delete_entry(entry_id)
                
                # Auto-save the vault after deleting entry
                try:
                    # Get the master password for saving
                    master_password = simpledialog.askstring("Save Vault", 
                                                          "Enter master password to save the vault:", 
                                                          show='*')
                    if master_password:
                        self.vault_manager.get_current_vault().save_vault(master_password)
                        # Update entry count in registry
                        current_vault_name = self.vault_manager.get_current_vault_name()
                        if current_vault_name:
                            entry_count = len(self.vault_manager.get_current_vault().get_entry())
                            self.vault_manager.update_vault_entry_count(current_vault_name, entry_count)
                        messagebox.showinfo("Success", "Entry deleted and vault saved!")
                    else:
                        messagebox.showwarning("Warning", "Entry deleted but vault not saved. Use 'Save Vault' to persist changes.")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to save vault: {str(e)}")
                
                self.refresh_entries()
                self.refresh_vaults_list()  # Refresh vault list to show updated entry count
                
                # Force the GUI to update
                self.root.update_idletasks()
                self.root.update()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete entry: {str(e)}")
    
    def copy_password(self):
        """Copy password of selected entry to clipboard"""
        if not self.vault_manager.get_current_vault():
            messagebox.showwarning("Warning", "Please open a vault first")
            return
        
        selection = self.entries_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an entry to copy password")
            return
        
        item = self.entries_tree.item(selection[0])
        entry_id = int(item['values'][0])
        
        entries = self.vault_manager.get_current_vault().get_entry(entry_id=entry_id)
        if entries and entries[0].password:
            if clipboard_handler(entries[0].password):
                messagebox.showinfo("Success", "Password copied to clipboard!")
            else:
                messagebox.showerror("Error", "Failed to copy to clipboard")
        else:
            messagebox.showwarning("Warning", "No password found for this entry")
    
    def generate_password(self):
        """Generate a secure password"""
        dialog = GeneratePasswordDialog(self.root)
        if dialog.result:
            password = dialog.result
            if clipboard_handler(password):
                messagebox.showinfo("Success", f"Generated password copied to clipboard!\n\n{password}")
            else:
                messagebox.showinfo("Generated Password", f"Generated password:\n\n{password}")
    
    def on_entry_double_click(self, event):
        """Handle double-click on entry"""
        self.view_entry()
    
    def on_search_change(self, *args):
        """Handle search text change"""
        self.refresh_entries()
    
    def refresh_entries(self):
        """Refresh the entries list"""
        if not self.vault_manager.get_current_vault():
            print("DEBUG: No current vault, skipping refresh")
            return
        
        try:
            search_query = self.search_var.get()
            if search_query:
                entries = self.vault_manager.get_current_vault().search_entries(search_query)
            else:
                entries = self.vault_manager.get_current_vault().get_entry()
            
            print(f"DEBUG: refresh_entries found {len(entries)} entries")
            for entry in entries:
                print(f"DEBUG: Entry in vault: {entry.name} (ID: {entry.id})")
            
            self.current_entries = entries
            self.update_entries_tree()
            self.update_stats()
            
            # Force the treeview to redraw
            self.entries_tree.see('')  # Scroll to top
            self.entries_tree.update()
            
            # Force the entire GUI to process events
            self.root.after(100, self._force_treeview_update)
            
            print(f"DEBUG: Treeview now has {len(self.entries_tree.get_children())} items")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to refresh entries: {str(e)}")
            print(f"DEBUG: Error in refresh_entries: {e}")
    
    def _force_treeview_update(self):
        """Force the treeview to update after a short delay"""
        try:
            # Clear and rebuild the treeview
            for item in self.entries_tree.get_children():
                self.entries_tree.delete(item)
            
            # Re-add all entries
            for entry in self.current_entries:
                values = (
                    entry.id,
                    entry.name,
                    entry.username or '',
                    entry.url or '',
                    entry.created_at.strftime('%Y-%m-%d %H:%M')
                )
                self.entries_tree.insert('', 'end', values=values)
            
            print(f"DEBUG: _force_treeview_update completed - {len(self.entries_tree.get_children())} items")
        except Exception as e:
            print(f"DEBUG: Error in _force_treeview_update: {e}")
    
    def update_entries_tree(self):
        """Update the entries treeview"""
        # Clear existing items
        for item in self.entries_tree.get_children():
            self.entries_tree.delete(item)
        
        print(f"DEBUG: update_entries_tree processing {len(self.current_entries)} entries")
        
        # Add entries
        for entry in self.current_entries:
            values = (
                entry.id,
                entry.name,
                entry.username or '',
                entry.url or '',
                entry.created_at.strftime('%Y-%m-%d %H:%M')
            )
            print(f"DEBUG: Adding entry to tree: {values}")
            self.entries_tree.insert('', 'end', values=values)
        
        print(f"DEBUG: Treeview now has {len(self.entries_tree.get_children())} items")
    
    def update_stats(self):
        """Update statistics display"""
        if self.vault_manager.get_current_vault():
            try:
                stats = self.vault_manager.get_current_vault().get_vault_stats()
                vault_name = self.vault_manager.get_current_vault_name()
                self.stats_label.config(
                    text=f"Vault: {vault_name} | Total entries: {stats['total_entries']} | "
                         f"Last updated: {stats['last_updated'].strftime('%Y-%m-%d %H:%M')}"
                )
            except:
                self.stats_label.config(text="")
        else:
            self.stats_label.config(text="")
    
    def clear_entries(self):
        """Clear the entries list"""
        for item in self.entries_tree.get_children():
            self.entries_tree.delete(item)
        self.current_entries = []
        self.stats_label.config(text="")
    
    def show_entry_details(self, entry):
        """Show detailed entry information"""
        details = f"""
Entry Details (ID: {entry.id})

Service: {entry.name}
Username: {entry.username or 'N/A'}
Password: {'*' * len(entry.password) if entry.password else 'N/A'}
URL: {entry.url or 'N/A'}
Notes: {entry.notes or 'N/A'}

Created: {entry.created_at}
Updated: {entry.updated_at}
        """
        
        messagebox.showinfo("Entry Details", details)


class CreateVaultDialog:
    def __init__(self, parent, vault_manager):
        self.vault_manager = vault_manager
        self.result = None
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Create New Vault")
        self.dialog.geometry("400x200")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the dialog UI"""
        main_frame = ttk.Frame(self.dialog, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Vault name
        ttk.Label(main_frame, text="Vault Name:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.name_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.name_var).grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(5, 0))
        
        # Master password
        ttk.Label(main_frame, text="Master Password:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.password_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.password_var, show='*').grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(5, 0))
        
        # Confirm password
        ttk.Label(main_frame, text="Confirm Password:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.confirm_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.confirm_var, show='*').grid(row=2, column=1, sticky=(tk.W, tk.E), padx=(5, 0))
        
        # Description
        ttk.Label(main_frame, text="Description:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.description_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.description_var).grid(row=3, column=1, sticky=(tk.W, tk.E), padx=(5, 0))
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=(20, 0))
        
        ttk.Button(button_frame, text="Create", command=self.create_vault).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Cancel", command=self.cancel).pack(side=tk.LEFT)
        
        # Configure grid weights
        main_frame.columnconfigure(1, weight=1)
    
    def create_vault(self):
        """Create the vault"""
        name = self.name_var.get().strip()
        password = self.password_var.get()
        confirm = self.confirm_var.get()
        description = self.description_var.get().strip()
        
        if not name:
            messagebox.showerror("Error", "Vault name is required!")
            return
        
        if password != confirm:
            messagebox.showerror("Error", "Passwords do not match!")
            return
        
        if not password:
            messagebox.showerror("Error", "Master password is required!")
            return
        
        try:
            self.vault_manager.create_vault(name, password, description)
            self.result = True
            self.dialog.destroy()
            messagebox.showinfo("Success", f"Vault '{name}' created successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create vault: {str(e)}")
    
    def cancel(self):
        """Cancel the dialog"""
        self.dialog.destroy()


class AddEntryDialog:
    def __init__(self, parent, pm):
        self.pm = pm
        self.result = None
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Add Entry")
        self.dialog.geometry("400x300")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the dialog UI"""
        main_frame = ttk.Frame(self.dialog, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Service
        ttk.Label(main_frame, text="Service:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.service_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.service_var).grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(5, 0))
        
        # Username
        ttk.Label(main_frame, text="Username:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.username_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.username_var).grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(5, 0))
        
        # Password
        ttk.Label(main_frame, text="Password:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.password_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.password_var, show='*').grid(row=2, column=1, sticky=(tk.W, tk.E), padx=(5, 0))
        
        # URL
        ttk.Label(main_frame, text="URL:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.url_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.url_var).grid(row=3, column=1, sticky=(tk.W, tk.E), padx=(5, 0))
        
        # Notes
        ttk.Label(main_frame, text="Notes:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.notes_text = tk.Text(main_frame, height=4, width=30)
        self.notes_text.grid(row=4, column=1, sticky=(tk.W, tk.E), padx=(5, 0))
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=(20, 0))
        
        ttk.Button(button_frame, text="Add", command=self.add_entry).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Cancel", command=self.cancel).pack(side=tk.LEFT)
        
        # Configure grid weights
        main_frame.columnconfigure(1, weight=1)
    
    def add_entry(self):
        """Add the entry"""
        service = self.service_var.get().strip()
        if not service:
            messagebox.showerror("Error", "Service name is required!")
            return
        
        print(f"DEBUG: AddEntryDialog.add_entry - Service: {service}")
        try:
            entry = self.pm.add_entry(
                service=service,
                username=self.username_var.get().strip() or None,
                password=self.password_var.get() or None,
                url=self.url_var.get().strip() or None,
                notes=self.notes_text.get("1.0", tk.END).strip() or None
            )
            
            print(f"DEBUG: AddEntryDialog.add_entry - Entry created: {entry.name} (ID: {entry.id})")
            self.result = entry
            self.dialog.destroy()
            messagebox.showinfo("Success", f"Entry '{service}' added successfully!")
        except Exception as e:
            print(f"DEBUG: AddEntryDialog.add_entry - Error: {e}")
            messagebox.showerror("Error", f"Failed to add entry: {str(e)}")
    
    def cancel(self):
        """Cancel the dialog"""
        self.dialog.destroy()


class EditEntryDialog:
    def __init__(self, parent, pm, entry):
        self.pm = pm
        self.entry = entry
        self.result = None
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Edit Entry")
        self.dialog.geometry("400x300")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.setup_ui()
        self.load_entry()
    
    def setup_ui(self):
        """Setup the dialog UI"""
        main_frame = ttk.Frame(self.dialog, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Service
        ttk.Label(main_frame, text="Service:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.service_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.service_var).grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(5, 0))
        
        # Username
        ttk.Label(main_frame, text="Username:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.username_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.username_var).grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(5, 0))
        
        # Password
        ttk.Label(main_frame, text="Password:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.password_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.password_var, show='*').grid(row=2, column=1, sticky=(tk.W, tk.E), padx=(5, 0))
        
        # URL
        ttk.Label(main_frame, text="URL:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.url_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.url_var).grid(row=3, column=1, sticky=(tk.W, tk.E), padx=(5, 0))
        
        # Notes
        ttk.Label(main_frame, text="Notes:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.notes_text = tk.Text(main_frame, height=4, width=30)
        self.notes_text.grid(row=4, column=1, sticky=(tk.W, tk.E), padx=(5, 0))
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=(20, 0))
        
        ttk.Button(button_frame, text="Update", command=self.update_entry).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Cancel", command=self.cancel).pack(side=tk.LEFT)
        
        # Configure grid weights
        main_frame.columnconfigure(1, weight=1)
    
    def load_entry(self):
        """Load entry data into the form"""
        self.service_var.set(self.entry.name)
        self.username_var.set(self.entry.username or '')
        self.password_var.set(self.entry.password or '')
        self.url_var.set(self.entry.url or '')
        self.notes_text.delete("1.0", tk.END)
        self.notes_text.insert("1.0", self.entry.notes or '')
    
    def update_entry(self):
        """Update the entry"""
        try:
            updates = {}
            if self.service_var.get().strip() != self.entry.name:
                updates['name'] = self.service_var.get().strip()
            if self.username_var.get().strip() != (self.entry.username or ''):
                updates['username'] = self.username_var.get().strip() or None
            if self.password_var.get() != (self.entry.password or ''):
                updates['password'] = self.password_var.get() or None
            if self.url_var.get().strip() != (self.entry.url or ''):
                updates['url'] = self.url_var.get().strip() or None
            if self.notes_text.get("1.0", tk.END).strip() != (self.entry.notes or ''):
                updates['notes'] = self.notes_text.get("1.0", tk.END).strip() or None
            
            if updates:
                self.pm.update_entry(self.entry.id, **updates)
                self.result = True
                self.dialog.destroy()
                messagebox.showinfo("Success", "Entry updated successfully!")
            else:
                messagebox.showinfo("Info", "No changes made")
                self.dialog.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update entry: {str(e)}")
    
    def cancel(self):
        """Cancel the dialog"""
        self.dialog.destroy()


class GeneratePasswordDialog:
    def __init__(self, parent):
        self.result = None
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Generate Password")
        self.dialog.geometry("300x200")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the dialog UI"""
        main_frame = ttk.Frame(self.dialog, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Length
        ttk.Label(main_frame, text="Length:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.length_var = tk.IntVar(value=16)
        ttk.Spinbox(main_frame, from_=8, to=64, textvariable=self.length_var).grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(5, 0))
        
        # Options
        self.include_symbols_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(main_frame, text="Include symbols", variable=self.include_symbols_var).grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        self.include_numbers_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(main_frame, text="Include numbers", variable=self.include_numbers_var).grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        self.include_uppercase_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(main_frame, text="Include uppercase", variable=self.include_uppercase_var).grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=(20, 0))
        
        ttk.Button(button_frame, text="Generate", command=self.generate).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Cancel", command=self.cancel).pack(side=tk.LEFT)
        
        # Configure grid weights
        main_frame.columnconfigure(1, weight=1)
    
    def generate(self):
        """Generate password"""
        try:
            password = generate_password(
                length=self.length_var.get(),
                include_symbols=self.include_symbols_var.get(),
                include_numbers=self.include_numbers_var.get(),
                include_uppercase=self.include_uppercase_var.get()
            )
            
            self.result = password
            self.dialog.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate password: {str(e)}")
    
    def cancel(self):
        """Cancel the dialog"""
        self.dialog.destroy()


def main():
    """Main entry point"""
    root = tk.Tk()
    app = MultiVaultPasswordManagerGUI(root)
    root.mainloop()

if __name__ == '__main__':
    main() 