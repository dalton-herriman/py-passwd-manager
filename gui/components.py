#!/usr/bin/env python3
"""
Reusable UI components for the Password Manager GUI
"""

import tkinter as tk
from tkinter import ttk


class SearchBox:
    """Reusable search box component"""
    
    def __init__(self, parent, placeholder="Search entries...", command=None):
        self.parent = parent
        self.command = command
        
        # Create frame
        self.frame = ttk.Frame(parent)
        
        # Search label
        self.label = ttk.Label(self.frame, text="🔍")
        self.label.pack(side=tk.LEFT, padx=(0, 5))
        
        # Search entry
        self.var = tk.StringVar()
        self.entry = ttk.Entry(self.frame, textvariable=self.var, width=30)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Bind to changes
        if command:
            self.var.trace("w", command)
            
    def get_value(self):
        """Get the current search value"""
        return self.var.get()
        
    def clear(self):
        """Clear the search box"""
        self.var.set("")
        
    def pack(self, **kwargs):
        """Pack the search box"""
        self.frame.pack(**kwargs)
        
    def grid(self, **kwargs):
        """Grid the search box"""
        self.frame.grid(**kwargs)


class StatusBar:
    """Reusable status bar component"""
    
    def __init__(self, parent):
        self.parent = parent
        
        # Create frame
        self.frame = ttk.Frame(parent)
        
        # Status label
        self.status_var = tk.StringVar(value="Ready")
        self.status_label = ttk.Label(self.frame, textvariable=self.status_var)
        self.status_label.pack(side=tk.LEFT, padx=5)
        
        # Progress bar
        self.progress = ttk.Progressbar(self.frame, mode='indeterminate')
        
    def set_status(self, message):
        """Set the status message"""
        self.status_var.set(message)
        
    def show_progress(self):
        """Show the progress bar"""
        self.progress.pack(side=tk.RIGHT, padx=5)
        self.progress.start()
        
    def hide_progress(self):
        """Hide the progress bar"""
        self.progress.stop()
        self.progress.pack_forget()
        
    def pack(self, **kwargs):
        """Pack the status bar"""
        self.frame.pack(**kwargs)
        
    def grid(self, **kwargs):
        """Grid the status bar"""
        self.frame.grid(**kwargs)


class ToolBar:
    """Reusable toolbar component"""
    
    def __init__(self, parent):
        self.parent = parent
        
        # Create frame
        self.frame = ttk.Frame(parent)
        
        # Button storage
        self.buttons = {}
        
    def add_button(self, text, command, icon=None, tooltip=None):
        """Add a button to the toolbar"""
        btn = ttk.Button(self.frame, text=text, command=command)
        btn.pack(side=tk.LEFT, padx=2)
        
        if tooltip:
            # Simple tooltip implementation
            def show_tooltip(event):
                # This is a basic tooltip - could be enhanced
                pass
            btn.bind("<Enter>", show_tooltip)
            
        self.buttons[text] = btn
        return btn
        
    def add_separator(self):
        """Add a separator to the toolbar"""
        separator = ttk.Separator(self.frame, orient=tk.VERTICAL)
        separator.pack(side=tk.LEFT, padx=5, fill=tk.Y)
        
    def pack(self, **kwargs):
        """Pack the toolbar"""
        self.frame.pack(**kwargs)
        
    def grid(self, **kwargs):
        """Grid the toolbar"""
        self.frame.grid(**kwargs)


class TreeViewManager:
    """Manager for TreeView components with common operations"""
    
    def __init__(self, treeview):
        self.treeview = treeview
        
    def clear(self):
        """Clear all items from the treeview"""
        for item in self.treeview.get_children():
            self.treeview.delete(item)
            
    def add_item(self, values, tags=None):
        """Add an item to the treeview"""
        item = self.treeview.insert("", "end", values=values)
        if tags:
            self.treeview.item(item, tags=tags)
        return item
        
    def get_selected_item(self):
        """Get the currently selected item"""
        selection = self.treeview.selection()
        if selection:
            return selection[0]
        return None
        
    def get_selected_values(self):
        """Get the values of the currently selected item"""
        selection = self.treeview.selection()
        if selection:
            return self.treeview.item(selection[0])["values"]
        return None
        
    def select_item(self, item_id):
        """Select a specific item"""
        self.treeview.selection_set(item_id)
        
    def refresh(self):
        """Refresh the treeview display"""
        self.treeview.update_idletasks()


class DialogBase:
    """Base class for dialogs with common functionality"""
    
    def __init__(self, parent, title, width=400, height=300):
        self.parent = parent
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry(f"{width}x{height}")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.center_dialog()
        
        # Result storage
        self.result = None
        
    def center_dialog(self):
        """Center the dialog on the parent window"""
        self.dialog.update_idletasks()
        
        # Get parent position and size
        parent_x = self.parent.winfo_rootx()
        parent_y = self.parent.winfo_rooty()
        parent_width = self.parent.winfo_width()
        parent_height = self.parent.winfo_height()
        
        # Get dialog size
        dialog_width = self.dialog.winfo_width()
        dialog_height = self.dialog.winfo_height()
        
        # Calculate center position
        x = parent_x + (parent_width - dialog_width) // 2
        y = parent_y + (parent_height - dialog_height) // 2
        
        # Ensure dialog is on screen
        x = max(0, x)
        y = max(0, y)
        
        self.dialog.geometry(f"+{x}+{y}")
        
    def setup_ui(self):
        """Setup the dialog UI - to be overridden by subclasses"""
        pass
        
    def show(self):
        """Show the dialog and wait for result"""
        self.dialog.wait_window()
        return self.result
        
    def close(self):
        """Close the dialog"""
        self.dialog.destroy() 