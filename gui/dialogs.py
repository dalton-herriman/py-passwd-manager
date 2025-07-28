#!/usr/bin/env python3
"""
Dialog classes for the Password Manager GUI
"""

import tkinter as tk
from tkinter import ttk, messagebox
from pm_core.utils import generate_password, validate_password_strength


class CreateVaultDialog:
    """Dialog for creating a new vault"""
    
    def __init__(self, parent, vault_manager):
        self.parent = parent
        self.vault_manager = vault_manager
        self.result = None
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Create New Vault")
        self.dialog.geometry("400x300")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.geometry("+%d+%d" % (
            parent.winfo_rootx() + 50,
            parent.winfo_rooty() + 50
        ))
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the dialog UI"""
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.dialog.columnconfigure(0, weight=1)
        self.dialog.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(
            main_frame,
            text="Create New Vault",
            font=("Arial", 14, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Vault name
        ttk.Label(main_frame, text="Vault Name:").grid(
            row=1, column=0, sticky=tk.W, pady=(0, 5)
        )
        self.name_var = tk.StringVar()
        self.name_entry = ttk.Entry(main_frame, textvariable=self.name_var, width=30)
        self.name_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Password
        ttk.Label(main_frame, text="Master Password:").grid(
            row=2, column=0, sticky=tk.W, pady=(0, 5)
        )
        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(main_frame, textvariable=self.password_var, 
                                      show="*", width=30)
        self.password_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Confirm password
        ttk.Label(main_frame, text="Confirm Password:").grid(
            row=3, column=0, sticky=tk.W, pady=(0, 5)
        )
        self.confirm_var = tk.StringVar()
        self.confirm_entry = ttk.Entry(main_frame, textvariable=self.confirm_var, 
                                     show="*", width=30)
        self.confirm_entry.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=(0, 10))
        
        ttk.Button(button_frame, text="Create", command=self.create_vault).pack(
            side=tk.LEFT, padx=(0, 10)
        )
        ttk.Button(button_frame, text="Cancel", command=self.cancel).pack(side=tk.LEFT)
        
        # Focus on name entry
        self.name_entry.focus()
        
    def create_vault(self):
        """Create the vault"""
        name = self.name_var.get().strip()
        password = self.password_var.get()
        confirm = self.confirm_var.get()
        
        if not name:
            messagebox.showerror("Error", "Please enter a vault name")
            return
            
        if not password:
            messagebox.showerror("Error", "Please enter a master password")
            return
            
        if password != confirm:
            messagebox.showerror("Error", "Passwords do not match")
            return
            
        if not validate_password_strength(password):
            messagebox.showerror("Error", "Password is too weak")
            return
            
        try:
            self.vault_manager.create_vault(name, password)
            self.result = {"name": name, "password": password}
            self.dialog.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create vault: {e}")
            
    def cancel(self):
        """Cancel the dialog"""
        self.dialog.destroy()


class AddEntryDialog:
    """Dialog for adding a new entry"""
    
    def __init__(self, parent, pm):
        self.parent = parent
        self.pm = pm
        self.result = None
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Add New Entry")
        self.dialog.geometry("500x400")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.geometry("+%d+%d" % (
            parent.winfo_rootx() + 50,
            parent.winfo_rooty() + 50
        ))
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the dialog UI"""
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.dialog.columnconfigure(0, weight=1)
        self.dialog.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(
            main_frame,
            text="Add New Entry",
            font=("Arial", 14, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Title field
        ttk.Label(main_frame, text="Title:").grid(
            row=1, column=0, sticky=tk.W, pady=(0, 5)
        )
        self.title_var = tk.StringVar()
        self.title_entry = ttk.Entry(main_frame, textvariable=self.title_var, width=40)
        self.title_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Username field
        ttk.Label(main_frame, text="Username:").grid(
            row=2, column=0, sticky=tk.W, pady=(0, 5)
        )
        self.username_var = tk.StringVar()
        self.username_entry = ttk.Entry(main_frame, textvariable=self.username_var, width=40)
        self.username_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Password field
        ttk.Label(main_frame, text="Password:").grid(
            row=3, column=0, sticky=tk.W, pady=(0, 5)
        )
        password_frame = ttk.Frame(main_frame)
        password_frame.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(password_frame, textvariable=self.password_var, 
                                      show="*", width=30)
        self.password_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        ttk.Button(password_frame, text="Generate", 
                  command=self.generate_password).pack(side=tk.RIGHT, padx=(5, 0))
        
        # URL field
        ttk.Label(main_frame, text="URL:").grid(
            row=4, column=0, sticky=tk.W, pady=(0, 5)
        )
        self.url_var = tk.StringVar()
        self.url_entry = ttk.Entry(main_frame, textvariable=self.url_var, width=40)
        self.url_entry.grid(row=4, column=1, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Notes field
        ttk.Label(main_frame, text="Notes:").grid(
            row=5, column=0, sticky=tk.W, pady=(0, 5)
        )
        self.notes_text = tk.Text(main_frame, height=4, width=40)
        self.notes_text.grid(row=5, column=1, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=6, column=0, columnspan=2, pady=(0, 10))
        
        ttk.Button(button_frame, text="Add", command=self.add_entry).pack(
            side=tk.LEFT, padx=(0, 10)
        )
        ttk.Button(button_frame, text="Cancel", command=self.cancel).pack(side=tk.LEFT)
        
        # Focus on title entry
        self.title_entry.focus()
        
    def generate_password(self):
        """Generate a random password"""
        dialog = GeneratePasswordDialog(self.dialog)
        self.dialog.wait_window(dialog.dialog)
        if dialog.result:
            self.password_var.set(dialog.result)
            
    def add_entry(self):
        """Add the entry"""
        title = self.title_var.get().strip()
        username = self.username_var.get().strip()
        password = self.password_var.get()
        url = self.url_var.get().strip()
        notes = self.notes_text.get("1.0", tk.END).strip()
        
        if not title:
            messagebox.showerror("Error", "Please enter a title")
            return
            
        if not username:
            messagebox.showerror("Error", "Please enter a username")
            return
            
        if not password:
            messagebox.showerror("Error", "Please enter a password")
            return
            
        try:
            entry_data = {
                "title": title,
                "username": username,
                "password": password,
                "url": url,
                "notes": notes
            }
            self.result = entry_data
            self.dialog.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add entry: {e}")
            
    def cancel(self):
        """Cancel the dialog"""
        self.dialog.destroy()


class EditEntryDialog:
    """Dialog for editing an existing entry"""
    
    def __init__(self, parent, pm, entry):
        self.parent = parent
        self.pm = pm
        self.entry = entry
        self.result = None
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Edit Entry")
        self.dialog.geometry("500x400")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.geometry("+%d+%d" % (
            parent.winfo_rootx() + 50,
            parent.winfo_rooty() + 50
        ))
        
        self.setup_ui()
        self.load_entry()
        
    def setup_ui(self):
        """Setup the dialog UI"""
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.dialog.columnconfigure(0, weight=1)
        self.dialog.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(
            main_frame,
            text="Edit Entry",
            font=("Arial", 14, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Title field
        ttk.Label(main_frame, text="Title:").grid(
            row=1, column=0, sticky=tk.W, pady=(0, 5)
        )
        self.title_var = tk.StringVar()
        self.title_entry = ttk.Entry(main_frame, textvariable=self.title_var, width=40)
        self.title_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Username field
        ttk.Label(main_frame, text="Username:").grid(
            row=2, column=0, sticky=tk.W, pady=(0, 5)
        )
        self.username_var = tk.StringVar()
        self.username_entry = ttk.Entry(main_frame, textvariable=self.username_var, width=40)
        self.username_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Password field
        ttk.Label(main_frame, text="Password:").grid(
            row=3, column=0, sticky=tk.W, pady=(0, 5)
        )
        password_frame = ttk.Frame(main_frame)
        password_frame.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(password_frame, textvariable=self.password_var, 
                                      show="*", width=30)
        self.password_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        ttk.Button(password_frame, text="Generate", 
                  command=self.generate_password).pack(side=tk.RIGHT, padx=(5, 0))
        
        # URL field
        ttk.Label(main_frame, text="URL:").grid(
            row=4, column=0, sticky=tk.W, pady=(0, 5)
        )
        self.url_var = tk.StringVar()
        self.url_entry = ttk.Entry(main_frame, textvariable=self.url_var, width=40)
        self.url_entry.grid(row=4, column=1, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Notes field
        ttk.Label(main_frame, text="Notes:").grid(
            row=5, column=0, sticky=tk.W, pady=(0, 5)
        )
        self.notes_text = tk.Text(main_frame, height=4, width=40)
        self.notes_text.grid(row=5, column=1, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=6, column=0, columnspan=2, pady=(0, 10))
        
        ttk.Button(button_frame, text="Update", command=self.update_entry).pack(
            side=tk.LEFT, padx=(0, 10)
        )
        ttk.Button(button_frame, text="Cancel", command=self.cancel).pack(side=tk.LEFT)
        
    def load_entry(self):
        """Load the entry data into the form"""
        self.title_var.set(self.entry.get("title", ""))
        self.username_var.set(self.entry.get("username", ""))
        self.password_var.set(self.entry.get("password", ""))
        self.url_var.set(self.entry.get("url", ""))
        self.notes_text.delete("1.0", tk.END)
        self.notes_text.insert("1.0", self.entry.get("notes", ""))
        
    def generate_password(self):
        """Generate a random password"""
        dialog = GeneratePasswordDialog(self.dialog)
        self.dialog.wait_window(dialog.dialog)
        if dialog.result:
            self.password_var.set(dialog.result)
            
    def update_entry(self):
        """Update the entry"""
        title = self.title_var.get().strip()
        username = self.username_var.get().strip()
        password = self.password_var.get()
        url = self.url_var.get().strip()
        notes = self.notes_text.get("1.0", tk.END).strip()
        
        if not title:
            messagebox.showerror("Error", "Please enter a title")
            return
            
        if not username:
            messagebox.showerror("Error", "Please enter a username")
            return
            
        if not password:
            messagebox.showerror("Error", "Please enter a password")
            return
            
        try:
            entry_data = {
                "title": title,
                "username": username,
                "password": password,
                "url": url,
                "notes": notes
            }
            self.result = entry_data
            self.dialog.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update entry: {e}")
            
    def cancel(self):
        """Cancel the dialog"""
        self.dialog.destroy()


class GeneratePasswordDialog:
    """Dialog for generating passwords"""
    
    def __init__(self, parent):
        self.parent = parent
        self.result = None
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Generate Password")
        self.dialog.geometry("400x300")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.geometry("+%d+%d" % (
            parent.winfo_rootx() + 50,
            parent.winfo_rooty() + 50
        ))
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the dialog UI"""
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.dialog.columnconfigure(0, weight=1)
        self.dialog.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(
            main_frame,
            text="Generate Password",
            font=("Arial", 14, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Length
        ttk.Label(main_frame, text="Length:").grid(
            row=1, column=0, sticky=tk.W, pady=(0, 5)
        )
        self.length_var = tk.IntVar(value=16)
        self.length_spinbox = ttk.Spinbox(main_frame, from_=8, to=64, 
                                         textvariable=self.length_var, width=10)
        self.length_spinbox.grid(row=1, column=1, sticky=tk.W, pady=(0, 10))
        
        # Options
        self.include_uppercase = tk.BooleanVar(value=True)
        ttk.Checkbutton(main_frame, text="Include Uppercase", 
                       variable=self.include_uppercase).grid(
            row=2, column=0, columnspan=2, sticky=tk.W, pady=(0, 5)
        )
        
        self.include_lowercase = tk.BooleanVar(value=True)
        ttk.Checkbutton(main_frame, text="Include Lowercase", 
                       variable=self.include_lowercase).grid(
            row=3, column=0, columnspan=2, sticky=tk.W, pady=(0, 5)
        )
        
        self.include_digits = tk.BooleanVar(value=True)
        ttk.Checkbutton(main_frame, text="Include Digits", 
                       variable=self.include_digits).grid(
            row=4, column=0, columnspan=2, sticky=tk.W, pady=(0, 5)
        )
        
        self.include_symbols = tk.BooleanVar(value=True)
        ttk.Checkbutton(main_frame, text="Include Symbols", 
                       variable=self.include_symbols).grid(
            row=5, column=0, columnspan=2, sticky=tk.W, pady=(0, 20)
        )
        
        # Generated password
        ttk.Label(main_frame, text="Generated Password:").grid(
            row=6, column=0, sticky=tk.W, pady=(0, 5)
        )
        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(main_frame, textvariable=self.password_var, 
                                      width=30, state="readonly")
        self.password_entry.grid(row=6, column=1, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=7, column=0, columnspan=2, pady=(0, 10))
        
        ttk.Button(button_frame, text="Generate", command=self.generate).pack(
            side=tk.LEFT, padx=(0, 10)
        )
        ttk.Button(button_frame, text="Use", command=self.use_password).pack(
            side=tk.LEFT, padx=(0, 10)
        )
        ttk.Button(button_frame, text="Cancel", command=self.cancel).pack(side=tk.LEFT)
        
        # Generate initial password
        self.generate()
        
    def generate(self):
        """Generate a new password"""
        try:
            length = self.length_var.get()
            password = generate_password(
                length=length,
                include_uppercase=self.include_uppercase.get(),
                include_lowercase=self.include_lowercase.get(),
                include_digits=self.include_digits.get(),
                include_symbols=self.include_symbols.get()
            )
            self.password_var.set(password)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate password: {e}")
            
    def use_password(self):
        """Use the generated password"""
        password = self.password_var.get()
        if password:
            self.result = password
            self.dialog.destroy()
            
    def cancel(self):
        """Cancel the dialog"""
        self.dialog.destroy() 