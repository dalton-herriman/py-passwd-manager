#!/usr/bin/env python3
"""
GUI application for the password manager
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import threading
import sys
from pathlib import Path

from pm_core.manager import PasswordManager
from pm_core.utils import generate_password, clipboard_handler, validate_password_strength

class PasswordManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Manager")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Initialize password manager
        self.vault_path = "vault.db"
        self.pm = PasswordManager(self.vault_path)
        self.current_entries = []
        
        # Setup UI
        self.setup_ui()
        self.check_vault_status()
    
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
        title_label = ttk.Label(main_frame, text="🔐 Password Manager", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 10))
        
        # Status frame
        self.status_frame = ttk.Frame(main_frame)
        self.status_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.status_label = ttk.Label(self.status_frame, text="Vault Status: Unknown")
        self.status_label.pack(side=tk.LEFT)
        
        # Buttons frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Action buttons
        self.create_btn = ttk.Button(buttons_frame, text="Create Vault", 
                                    command=self.create_vault)
        self.create_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        self.unlock_btn = ttk.Button(buttons_frame, text="Unlock Vault", 
                                    command=self.unlock_vault)
        self.unlock_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        self.lock_btn = ttk.Button(buttons_frame, text="Lock Vault", 
                                  command=self.lock_vault)
        self.lock_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        self.add_btn = ttk.Button(buttons_frame, text="Add Entry", 
                                 command=self.add_entry)
        self.add_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        self.generate_btn = ttk.Button(buttons_frame, text="Generate Password", 
                                      command=self.generate_password)
        self.generate_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        # Search frame
        search_frame = ttk.Frame(main_frame)
        search_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.on_search_change)
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=40)
        search_entry.pack(side=tk.LEFT, padx=(5, 0))
        
        # Entries list
        list_frame = ttk.Frame(main_frame)
        list_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        # Treeview for entries
        columns = ('ID', 'Service', 'Username', 'URL', 'Created')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        
        # Configure columns
        self.tree.heading('ID', text='ID')
        self.tree.heading('Service', text='Service')
        self.tree.heading('Username', text='Username')
        self.tree.heading('URL', text='URL')
        self.tree.heading('Created', text='Created')
        
        self.tree.column('ID', width=50)
        self.tree.column('Service', width=150)
        self.tree.column('Username', width=150)
        self.tree.column('URL', width=200)
        self.tree.column('Created', width=150)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Bind double-click event
        self.tree.bind('<Double-1>', self.on_entry_double_click)
        
        # Action buttons for entries
        entry_buttons_frame = ttk.Frame(main_frame)
        entry_buttons_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
        self.view_btn = ttk.Button(entry_buttons_frame, text="View Entry", 
                                  command=self.view_entry)
        self.view_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        self.edit_btn = ttk.Button(entry_buttons_frame, text="Edit Entry", 
                                  command=self.edit_entry)
        self.edit_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        self.delete_btn = ttk.Button(entry_buttons_frame, text="Delete Entry", 
                                    command=self.delete_entry)
        self.delete_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        self.copy_btn = ttk.Button(entry_buttons_frame, text="Copy Password", 
                                  command=self.copy_password)
        self.copy_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        # Stats label
        self.stats_label = ttk.Label(main_frame, text="")
        self.stats_label.grid(row=6, column=0, columnspan=3, pady=(10, 0))
        
        # Initially disable buttons that require unlocked vault
        self.set_unlocked_state(False)
    
    def check_vault_status(self):
        """Check if vault exists and update UI accordingly"""
        if self.pm.is_vault_exists():
            self.status_label.config(text="Vault Status: Exists (Locked)")
            self.create_btn.config(state='disabled')
            self.unlock_btn.config(state='normal')
        else:
            self.status_label.config(text="Vault Status: Not Found")
            self.create_btn.config(state='normal')
            self.unlock_btn.config(state='disabled')
    
    def set_unlocked_state(self, unlocked):
        """Enable/disable buttons based on vault state"""
        state = 'normal' if unlocked else 'disabled'
        self.add_btn.config(state=state)
        self.lock_btn.config(state=state)
        self.view_btn.config(state=state)
        self.edit_btn.config(state=state)
        self.delete_btn.config(state=state)
        self.copy_btn.config(state=state)
        self.generate_btn.config(state='normal')  # Always available
    
    def create_vault(self):
        """Create a new vault"""
        password = simpledialog.askstring("Create Vault", "Enter master password:", 
                                        show='*')
        if not password:
            return
        
        confirm_password = simpledialog.askstring("Create Vault", "Confirm master password:", 
                                                show='*')
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match!")
            return
        
        try:
            self.pm.create_vault(password)
            self.set_unlocked_state(True)
            self.status_label.config(text="Vault Status: Unlocked")
            self.refresh_entries()
            messagebox.showinfo("Success", "Vault created successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create vault: {str(e)}")
    
    def unlock_vault(self):
        """Unlock existing vault"""
        password = simpledialog.askstring("Unlock Vault", "Enter master password:", 
                                        show='*')
        if not password:
            return
        
        try:
            self.pm.unlock_vault(password)
            self.set_unlocked_state(True)
            self.status_label.config(text="Vault Status: Unlocked")
            self.refresh_entries()
            messagebox.showinfo("Success", "Vault unlocked successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to unlock vault: {str(e)}")
    
    def lock_vault(self):
        """Lock the vault"""
        try:
            self.pm.lock_vault()
            self.set_unlocked_state(False)
            self.status_label.config(text="Vault Status: Locked")
            self.clear_entries()
            messagebox.showinfo("Success", "Vault locked!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to lock vault: {str(e)}")
    
    def add_entry(self):
        """Add a new entry"""
        dialog = AddEntryDialog(self.root, self.pm)
        if dialog.result:
            self.refresh_entries()
    
    def view_entry(self):
        """View selected entry details"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an entry to view")
            return
        
        item = self.tree.item(selection[0])
        entry_id = int(item['values'][0])
        
        entries = self.pm.get_entry(entry_id=entry_id)
        if entries:
            entry = entries[0]
            self.show_entry_details(entry)
    
    def edit_entry(self):
        """Edit selected entry"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an entry to edit")
            return
        
        item = self.tree.item(selection[0])
        entry_id = int(item['values'][0])
        
        entries = self.pm.get_entry(entry_id=entry_id)
        if entries:
            entry = entries[0]
            dialog = EditEntryDialog(self.root, self.pm, entry)
            if dialog.result:
                self.refresh_entries()
    
    def delete_entry(self):
        """Delete selected entry"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an entry to delete")
            return
        
        item = self.tree.item(selection[0])
        entry_id = int(item['values'][0])
        
        if messagebox.askyesno("Confirm Delete", 
                              f"Are you sure you want to delete entry {entry_id}?"):
            try:
                self.pm.delete_entry(entry_id)
                self.refresh_entries()
                messagebox.showinfo("Success", "Entry deleted successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete entry: {str(e)}")
    
    def copy_password(self):
        """Copy password of selected entry to clipboard"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an entry to copy password")
            return
        
        item = self.tree.item(selection[0])
        entry_id = int(item['values'][0])
        
        entries = self.pm.get_entry(entry_id=entry_id)
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
        if not self.pm.is_unlocked:
            return
        
        try:
            search_query = self.search_var.get()
            if search_query:
                entries = self.pm.search_entries(search_query)
            else:
                entries = self.pm.get_entry()
            
            self.current_entries = entries
            self.update_tree()
            self.update_stats()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to refresh entries: {str(e)}")
    
    def update_tree(self):
        """Update the treeview with current entries"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Add entries
        for entry in self.current_entries:
            self.tree.insert('', 'end', values=(
                entry.id,
                entry.name,
                entry.username or '',
                entry.url or '',
                entry.created_at.strftime('%Y-%m-%d %H:%M')
            ))
    
    def update_stats(self):
        """Update statistics display"""
        if self.pm.is_unlocked:
            try:
                stats = self.pm.get_vault_stats()
                self.stats_label.config(
                    text=f"Total entries: {stats['total_entries']} | "
                         f"Last updated: {stats['last_updated'].strftime('%Y-%m-%d %H:%M')}"
                )
            except:
                self.stats_label.config(text="")
        else:
            self.stats_label.config(text="")
    
    def clear_entries(self):
        """Clear the entries list"""
        for item in self.tree.get_children():
            self.tree.delete(item)
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
        
        try:
            entry = self.pm.add_entry(
                service=service,
                username=self.username_var.get().strip() or None,
                password=self.password_var.get() or None,
                url=self.url_var.get().strip() or None,
                notes=self.notes_text.get("1.0", tk.END).strip() or None
            )
            
            self.result = entry
            self.dialog.destroy()
            messagebox.showinfo("Success", f"Entry '{service}' added successfully!")
        except Exception as e:
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
    app = PasswordManagerGUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()
