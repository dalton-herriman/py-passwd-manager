#!/usr/bin/env python3
"""
PySide6-based main application window for the Password Manager GUI
Modern, responsive interface with better UX
"""

import sys
from pathlib import Path

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QSplitter, QTreeWidget, QTreeWidgetItem, QLabel, QGroupBox, QFrame,
    QMenuBar, QMenu, QMessageBox, QApplication
)
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtGui import QFont, QIcon, QKeySequence

# Add the project root to the path
sys.path.insert(0, str(Path(__file__).parent.parent))

from pm_core.vault_manager import VaultManager
from pm_core.utils import clipboard_handler

from .components_pyside import SearchBox, StatusBar, ToolBar, TreeViewManager
from .events_pyside import EventHandler


class MultiVaultPasswordManagerGUI(QMainWindow):
    """Main application window for the password manager"""
    
    def __init__(self):
        super().__init__()
        self.vault_manager = VaultManager("vaults")
        self.current_vault = None
        self.current_entries = []
        self.filtered_entries = []
        
        # Create event handler first
        self.event_handler = EventHandler(self)
        
        # Setup UI components
        self.setup_ui()
        self.setup_menu()
        self.setup_styling()
        
        # Connect signals after UI is created
        self.connect_signals()
        
        # Refresh vaults list on startup
        self.refresh_vaults_list()
    
    def setup_ui(self):
        """Setup the main UI"""
        self.setWindowTitle("🔐 Multi-Vault Password Manager")
        self.setGeometry(100, 100, 1200, 800)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # Create splitter for left/right panels
        self.splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(self.splitter)
        
        # Setup left panel (vaults)
        self.setup_vaults_panel()
        
        # Setup right panel (entries)
        self.setup_entries_panel()
        
        # Setup status bar
        self.setup_status_bar()
        
        # Set splitter proportions
        self.splitter.setSizes([400, 800])
    
    def setup_vaults_panel(self):
        """Setup the vaults panel (left side)"""
        # Vaults group
        vaults_group = QGroupBox("Vaults")
        vaults_layout = QVBoxLayout(vaults_group)
        
        # Vault toolbar
        self.vault_toolbar = ToolBar()
        self.vault_toolbar.add_button("Create", self.event_handler.create_vault)
        self.vault_toolbar.add_button("Delete", self.event_handler.delete_vault)
        self.vault_toolbar.add_separator()
        self.vault_toolbar.add_button("Rename", self.event_handler.rename_vault)
        self.vault_toolbar.add_button("Backup", self.event_handler.backup_vault)
        vaults_layout.addWidget(self.vault_toolbar)
        
        # Vaults tree
        self.vaults_tree = QTreeWidget()
        self.vaults_tree.setHeaderLabels(["Name", "Status", "Entries", "Created", "Last Accessed"])
        self.vaults_tree.setAlternatingRowColors(True)
        self.vaults_tree.setSortingEnabled(True)
        vaults_layout.addWidget(self.vaults_tree)
        
        # Initialize vaults manager
        self.vaults_manager = TreeViewManager(self.vaults_tree)
        
        # Add to splitter
        self.splitter.addWidget(vaults_group)
    
    def setup_entries_panel(self):
        """Setup the entries panel (right side)"""
        # Entries group
        entries_group = QGroupBox("Entries")
        entries_layout = QVBoxLayout(entries_group)
        
        # Entries toolbar
        self.entries_toolbar = ToolBar()
        self.entries_toolbar.add_button("Add", self.event_handler.add_entry)
        self.entries_toolbar.add_button("Edit", self.event_handler.edit_entry)
        self.entries_toolbar.add_button("Delete", self.event_handler.delete_entry)
        self.entries_toolbar.add_separator()
        self.entries_toolbar.add_button("Copy Password", self.event_handler.copy_password)
        self.entries_toolbar.add_button("Generate", self.event_handler.generate_password)
        entries_layout.addWidget(self.entries_toolbar)
        
        # Search box
        self.search_box = SearchBox()
        self.search_box.textChanged.connect(self.event_handler.on_search_change)
        entries_layout.addWidget(self.search_box)
        
        # Entries tree
        self.entries_tree = QTreeWidget()
        self.entries_tree.setHeaderLabels(["Title", "Username", "URL", "Notes"])
        self.entries_tree.setAlternatingRowColors(True)
        self.entries_tree.setSortingEnabled(True)
        entries_layout.addWidget(self.entries_tree)
        
        # Initialize entries manager
        self.entries_manager = TreeViewManager(self.entries_tree)
        
        # Add to splitter
        self.splitter.addWidget(entries_group)
    
    def setup_status_bar(self):
        """Setup the status bar"""
        self.status_bar = StatusBar(self)
        self.setStatusBar(self.status_bar)
    
    def connect_signals(self):
        """Connect signals after UI is created"""
        # Connect tree view signals
        self.vaults_tree.itemSelectionChanged.connect(self.event_handler.on_vault_select)
        self.vaults_tree.itemDoubleClicked.connect(self.event_handler.on_vault_double_click)
        self.entries_tree.itemDoubleClicked.connect(self.event_handler.on_entry_double_click)
    
    def setup_menu(self):
        """Setup the menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("&File")
        
        new_vault_action = QAction("&New Vault", self)
        new_vault_action.setShortcut(QKeySequence("Ctrl+Shift+N"))
        new_vault_action.triggered.connect(self.event_handler.create_vault)
        file_menu.addAction(new_vault_action)
        
        open_vault_action = QAction("&Open Vault", self)
        open_vault_action.setShortcut(QKeySequence("Ctrl+O"))
        open_vault_action.triggered.connect(self.event_handler.open_vault)
        file_menu.addAction(open_vault_action)
        
        close_vault_action = QAction("&Close Vault", self)
        close_vault_action.setShortcut(QKeySequence("Ctrl+W"))
        close_vault_action.triggered.connect(self.event_handler.close_vault)
        file_menu.addAction(close_vault_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("E&xit", self)
        exit_action.setShortcut(QKeySequence("Ctrl+Q"))
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Edit menu
        edit_menu = menubar.addMenu("&Edit")
        
        add_entry_action = QAction("&Add Entry", self)
        add_entry_action.setShortcut(QKeySequence("Ctrl+N"))
        add_entry_action.triggered.connect(self.event_handler.add_entry)
        edit_menu.addAction(add_entry_action)
        
        edit_entry_action = QAction("&Edit Entry", self)
        edit_entry_action.setShortcut(QKeySequence("Ctrl+E"))
        edit_entry_action.triggered.connect(self.event_handler.edit_entry)
        edit_menu.addAction(edit_entry_action)
        
        delete_entry_action = QAction("&Delete Entry", self)
        delete_entry_action.setShortcut(QKeySequence("Delete"))
        delete_entry_action.triggered.connect(self.event_handler.delete_entry)
        edit_menu.addAction(delete_entry_action)
        
        edit_menu.addSeparator()
        
        copy_password_action = QAction("&Copy Password", self)
        copy_password_action.setShortcut(QKeySequence("Ctrl+C"))
        copy_password_action.triggered.connect(self.event_handler.copy_password)
        edit_menu.addAction(copy_password_action)
        
        generate_password_action = QAction("&Generate Password", self)
        generate_password_action.setShortcut(QKeySequence("Ctrl+G"))
        generate_password_action.triggered.connect(self.event_handler.generate_password)
        edit_menu.addAction(generate_password_action)
        
        # Help menu
        help_menu = menubar.addMenu("&Help")
        
        about_action = QAction("&About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def setup_styling(self):
        """Setup modern styling"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e;
                color: white;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #555555;
                border-radius: 6px;
                margin-top: 6px;
                padding-top: 10px;
                color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: white;
            }
            QMenuBar {
                background-color: #2b2b2b;
                color: white;
                border-bottom: 1px solid #555555;
            }
            QMenuBar::item {
                background-color: transparent;
                padding: 8px 12px;
            }
            QMenuBar::item:selected {
                background-color: #3b3b3b;
            }
            QMenu {
                background-color: #2b2b2b;
                color: white;
                border: 1px solid #555555;
                padding: 5px;
            }
            QMenu::item {
                padding: 8px 20px;
            }
            QMenu::item:selected {
                background-color: #0078d4;
            }
        """)
    
    def refresh_vaults_list(self):
        """Refresh the vaults list"""
        try:
            self.vaults_manager.clear()
            
            vaults = self.vault_manager.list_vaults()
            current_vault = self.vault_manager.get_current_vault_name()
            
            for vault in vaults:
                status = "🔓 OPEN" if vault.name == current_vault else "🔒 LOCKED"
                created = vault.created_at.strftime("%Y-%m-%d") if vault.created_at else "Unknown"
                last_accessed = vault.last_accessed.strftime("%Y-%m-%d") if vault.last_accessed else "Never"
                
                item = self.vaults_manager.add_item([
                    vault.name,
                    status,
                    str(vault.entry_count),
                    created,
                    last_accessed
                ])
                
                # Highlight current vault
                if vault.name == current_vault:
                    item.setBackground(0, self.palette().highlight())
                    self.current_vault = vault.name
            
            self.status_bar.set_status(f"Found {len(vaults)} vault(s)")
            
        except Exception as e:
            self.status_bar.set_status(f"Error refreshing vaults: {e}")
    
    def refresh_entries(self):
        """Refresh the entries list"""
        try:
            self.entries_manager.clear()
            
            if not self.current_vault:
                self.current_entries = []
                self.filtered_entries = []
                return
            
            entries = self.vault_manager.list_entries()
            self.current_entries = entries
            self.filtered_entries = entries.copy()
            
            for entry in entries:
                # Truncate long fields for display
                notes = entry.get("notes", "")[:50] + "..." if len(entry.get("notes", "")) > 50 else entry.get("notes", "")
                url = entry.get("url", "")[:30] + "..." if len(entry.get("url", "")) > 30 else entry.get("url", "")
                
                self.entries_manager.add_item([
                    entry.get("name", ""),
                    entry.get("username", ""),
                    url,
                    notes
                ])
            
            self.event_handler.set_current_entries(entries)
            self.status_bar.set_status(f"Loaded {len(entries)} entries from '{self.current_vault}'")
            
        except Exception as e:
            self.status_bar.set_status(f"Error refreshing entries: {e}")
    
    def filter_entries(self, search_term):
        """Filter entries based on search term"""
        try:
            if not search_term:
                self.filtered_entries = self.current_entries.copy()
            else:
                search_lower = search_term.lower()
                self.filtered_entries = [
                    entry for entry in self.current_entries
                    if (search_lower in entry.get("name", "").lower() or
                        search_lower in entry.get("username", "").lower() or
                        search_lower in entry.get("url", "").lower() or
                        search_lower in entry.get("notes", "").lower())
                ]
            
            # Update display
            self.entries_manager.clear()
            for entry in self.filtered_entries:
                notes = entry.get("notes", "")[:50] + "..." if len(entry.get("notes", "")) > 50 else entry.get("notes", "")
                url = entry.get("url", "")[:30] + "..." if len(entry.get("url", "")) > 30 else entry.get("url", "")
                
                self.entries_manager.add_item([
                    entry.get("name", ""),
                    entry.get("username", ""),
                    url,
                    notes
                ])
            
            self.status_bar.set_status(f"Showing {len(self.filtered_entries)} of {len(self.current_entries)} entries")
            
        except Exception as e:
            self.status_bar.set_status(f"Error filtering entries: {e}")
    
    def show_about(self):
        """Show about dialog"""
        QMessageBox.about(
            self,
            "About Password Manager",
            "🔐 Multi-Vault Password Manager\n\n"
            "A secure password manager with modern GUI\n"
            "Built with PySide6\n\n"
            "Version: 1.0.0"
        )
    
    # Event handler callbacks
    def on_vault_created(self, name, password, description):
        """Handle vault creation"""
        self.refresh_vaults_list()
    
    def on_vault_opened(self, vault_name):
        """Handle vault opening"""
        self.current_vault = vault_name
        self.refresh_vaults_list()
    
    def on_vault_closed(self):
        """Handle vault closing"""
        self.current_vault = None
        self.refresh_vaults_list()
    
    def on_entry_added(self, entry_data):
        """Handle entry addition"""
        self.refresh_entries()
    
    def on_entry_updated(self, entry_data):
        """Handle entry update"""
        self.refresh_entries()
    
    def on_entry_deleted(self, entry_id):
        """Handle entry deletion"""
        self.refresh_entries()
    
    def on_password_copied(self, password):
        """Handle password copy"""
        # Password is already copied to clipboard by the event handler
        pass
    
    def on_status_updated(self, message):
        """Handle status updates"""
        self.status_bar.set_status(message)
    
    def keyPressEvent(self, event):
        """Handle key press events"""
        self.event_handler.on_key_press(event)
        super().keyPressEvent(event)
    
    def closeEvent(self, event):
        """Handle application close"""
        try:
            if self.current_vault:
                self.vault_manager.close_vault()
            event.accept()
        except Exception as e:
            print(f"Error during close: {e}")
            event.accept()


def main():
    """Main entry point"""
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("Password Manager")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("Password Manager Team")
    
    # Create and show main window
    window = MultiVaultPasswordManagerGUI()
    window.show()
    
    # Start the application
    sys.exit(app.exec()) 