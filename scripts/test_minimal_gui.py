#!/usr/bin/env python3
"""
Minimal GUI test to isolate treeview refresh issue
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
from pathlib import Path

# Add the project root to the path
sys.path.insert(0, str(Path(__file__).parent.parent))

from pm_core.vault_manager import VaultManager

class MinimalTestGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Minimal GUI Test")
        self.root.geometry("600x400")
        
        # Initialize vault manager
        self.vm = VaultManager("test_minimal_gui")
        self.current_vault = None
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the minimal UI"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(button_frame, text="Create Vault", command=self.create_vault).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Open Vault", command=self.open_vault).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Add Entry", command=self.add_entry).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Refresh", command=self.refresh_entries).pack(side=tk.LEFT, padx=(0, 5))
        
        # Treeview
        columns = ('ID', 'Service', 'Username', 'URL')
        self.tree = ttk.Treeview(main_frame, columns=columns, show='headings', height=15)
        
        # Configure columns
        self.tree.heading('ID', text='ID')
        self.tree.heading('Service', text='Service')
        self.tree.heading('Username', text='Username')
        self.tree.heading('URL', text='URL')
        
        self.tree.column('ID', width=50)
        self.tree.column('Service', width=150)
        self.tree.column('Username', width=150)
        self.tree.column('URL', width=200)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Status label
        self.status_label = ttk.Label(main_frame, text="No vault open")
        self.status_label.pack(fill=tk.X, pady=(10, 0))
        
    def create_vault(self):
        """Create a test vault"""
        try:
            self.vm.create_vault("TestVault", "testpass123", "Test vault")
            messagebox.showinfo("Success", "Vault created successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create vault: {e}")
    
    def open_vault(self):
        """Open the test vault"""
        try:
            self.current_vault = self.vm.open_vault("TestVault", "testpass123")
            self.status_label.config(text="Vault opened")
            self.refresh_entries()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open vault: {e}")
    
    def add_entry(self):
        """Add a test entry"""
        if not self.current_vault:
            messagebox.showwarning("Warning", "Please open a vault first")
            return
        
        try:
            entry = self.current_vault.add_entry(
                service="TestService",
                username="testuser",
                password="testpass",
                url="https://test.com",
                notes="Test entry"
            )
            print(f"DEBUG: Entry added: {entry.name} (ID: {entry.id})")
            
            # Save the vault
            self.current_vault.save_vault("testpass123")
            print("DEBUG: Vault saved")
            
            # Refresh the display
            self.refresh_entries()
            
            messagebox.showinfo("Success", f"Entry '{entry.name}' added successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add entry: {e}")
    
    def refresh_entries(self):
        """Refresh the entries display"""
        if not self.current_vault:
            return
        
        try:
            # Clear existing items
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Get entries
            entries = self.current_vault.get_entry()
            print(f"DEBUG: Found {len(entries)} entries")
            
            # Add entries to treeview
            for entry in entries:
                values = (
                    entry.id,
                    entry.name,
                    entry.username or '',
                    entry.url or ''
                )
                print(f"DEBUG: Adding to treeview: {values}")
                self.tree.insert('', 'end', values=values)
            
            print(f"DEBUG: Treeview now has {len(self.tree.get_children())} items")
            self.status_label.config(text=f"Vault opened - {len(entries)} entries")
            
        except Exception as e:
            print(f"DEBUG: Error in refresh_entries: {e}")
            messagebox.showerror("Error", f"Failed to refresh entries: {e}")

def main():
    root = tk.Tk()
    app = MinimalTestGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 