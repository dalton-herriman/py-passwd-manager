#!/usr/bin/env python3
"""
PySide6-based UI components for the Password Manager GUI
Modern, responsive components with better styling
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QPushButton, QLineEdit, QLabel, QTreeWidget, QTreeWidgetItem,
    QScrollBar, QFrame, QGroupBox, QSplitter, QStatusBar,
    QProgressBar, QToolBar, QMenu, QMessageBox,
    QDialog, QFormLayout, QTextEdit, QCheckBox, QSpinBox,
    QComboBox, QTabWidget, QTableWidget, QTableWidgetItem,
    QHeaderView, QApplication, QMainWindow
)
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt, Signal, QTimer, QThread
from PySide6.QtGui import QFont, QIcon, QPixmap, QKeySequence


class ModernButton(QPushButton):
    """Modern styled button with hover effects"""
    
    def __init__(self, text="", parent=None, icon=None):
        super().__init__(text, parent)
        self.setup_style()
        if icon:
            self.setIcon(icon)
    
    def setup_style(self):
        """Apply modern styling"""
        self.setStyleSheet("""
            QPushButton {
                background-color: #2b2b2b;
                border: 1px solid #555555;
                border-radius: 4px;
                padding: 8px 16px;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #3b3b3b;
                border: 1px solid #666666;
            }
            QPushButton:pressed {
                background-color: #1b1b1b;
            }
            QPushButton:disabled {
                background-color: #1a1a1a;
                color: #666666;
            }
        """)


class SearchBox(QWidget):
    """Modern search box with real-time filtering"""
    
    textChanged = Signal(str)
    
    def __init__(self, parent=None, placeholder="Search entries..."):
        super().__init__(parent)
        self.setup_ui(placeholder)
    
    def setup_ui(self, placeholder):
        """Setup the search box UI"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Search icon label
        self.icon_label = QLabel("🔍")
        self.icon_label.setStyleSheet("color: #888888; font-size: 14px;")
        layout.addWidget(self.icon_label)
        
        # Search input
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(placeholder)
        self.search_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #555555;
                border-radius: 4px;
                padding: 8px 12px;
                background-color: #2b2b2b;
                color: white;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #0078d4;
            }
        """)
        layout.addWidget(self.search_input)
        
        # Connect signals
        self.search_input.textChanged.connect(self.textChanged)
    
    def get_text(self):
        """Get the current search text"""
        return self.search_input.text()
    
    def clear(self):
        """Clear the search box"""
        self.search_input.clear()


class StatusBar(QStatusBar):
    """Modern status bar with progress indicator"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the status bar UI"""
        self.setStyleSheet("""
            QStatusBar {
                background-color: #1e1e1e;
                color: white;
                border-top: 1px solid #555555;
            }
        """)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #555555;
                border-radius: 2px;
                text-align: center;
                background-color: #2b2b2b;
            }
            QProgressBar::chunk {
                background-color: #0078d4;
                border-radius: 1px;
            }
        """)
        self.addPermanentWidget(self.progress_bar)
        
        # Set initial status
        self.showMessage("Ready")
    
    def set_status(self, message):
        """Set the status message"""
        self.showMessage(message)
    
    def show_progress(self):
        """Show the progress bar"""
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # Indeterminate progress
    
    def hide_progress(self):
        """Hide the progress bar"""
        self.progress_bar.setVisible(False)


class ToolBar(QToolBar):
    """Modern toolbar with styled buttons"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.actions = {}
    
    def setup_ui(self):
        """Setup the toolbar UI"""
        self.setStyleSheet("""
            QToolBar {
                background-color: #2b2b2b;
                border: none;
                spacing: 4px;
                padding: 4px;
            }
            QToolButton {
                background-color: transparent;
                border: 1px solid transparent;
                border-radius: 4px;
                padding: 6px 12px;
                color: white;
                font-weight: bold;
            }
            QToolButton:hover {
                background-color: #3b3b3b;
                border: 1px solid #555555;
            }
            QToolButton:pressed {
                background-color: #1b1b1b;
            }
        """)
    
    def add_button(self, text, callback, icon=None, tooltip=None):
        """Add a button to the toolbar"""
        action = QAction(text, self)
        if icon:
            action.setIcon(icon)
        if tooltip:
            action.setToolTip(tooltip)
        action.triggered.connect(callback)
        self.addAction(action)
        self.actions[text] = action
        return action
    
    def add_separator(self):
        """Add a separator to the toolbar"""
        self.addSeparator()


class TreeViewManager:
    """Manager for tree view widgets with modern styling"""
    
    def __init__(self, tree_widget):
        self.tree = tree_widget
        self.setup_styling()
    
    def setup_styling(self):
        """Apply modern styling to the tree widget"""
        self.tree.setStyleSheet("""
            QTreeWidget {
                background-color: #2b2b2b;
                border: 1px solid #555555;
                border-radius: 4px;
                color: white;
                font-size: 13px;
                gridline-color: #444444;
            }
            QTreeWidget::item {
                padding: 4px;
                border: none;
            }
            QTreeWidget::item:selected {
                background-color: #0078d4;
            }
            QTreeWidget::item:hover {
                background-color: #3b3b3b;
            }
            QHeaderView::section {
                background-color: #1e1e1e;
                color: white;
                padding: 8px;
                border: none;
                border-right: 1px solid #555555;
                border-bottom: 1px solid #555555;
                font-weight: bold;
            }
            QHeaderView::section:hover {
                background-color: #2b2b2b;
            }
        """)
    
    def clear(self):
        """Clear all items from the tree"""
        self.tree.clear()
    
    def add_item(self, values, tags=None):
        """Add an item to the tree"""
        item = QTreeWidgetItem(values)
        if tags:
            item.setData(0, Qt.UserRole, tags)
        self.tree.addTopLevelItem(item)
        return item
    
    def get_selected_item(self):
        """Get the currently selected item"""
        items = self.tree.selectedItems()
        return items[0] if items else None
    
    def get_selected_values(self):
        """Get values from the selected item"""
        item = self.get_selected_item()
        if item:
            return [item.text(i) for i in range(item.columnCount())]
        return None
    
    def select_item(self, item):
        """Select a specific item"""
        self.tree.setCurrentItem(item)
    
    def refresh(self):
        """Refresh the tree view"""
        self.tree.viewport().update()


class DialogBase(QDialog):
    """Base class for modern dialogs"""
    
    def __init__(self, parent=None, title="Dialog", width=400, height=300):
        super().__init__(parent)
        self.setup_ui(title, width, height)
    
    def setup_ui(self, title, width, height):
        """Setup the dialog UI"""
        self.setWindowTitle(title)
        self.setFixedSize(width, height)
        self.setModal(True)
        
        # Apply modern styling
        self.setStyleSheet("""
            QDialog {
                background-color: #2b2b2b;
                color: white;
            }
            QLabel {
                color: white;
                font-size: 13px;
            }
            QLineEdit, QTextEdit, QSpinBox, QComboBox {
                background-color: #1e1e1e;
                border: 1px solid #555555;
                border-radius: 4px;
                padding: 6px;
                color: white;
                font-size: 13px;
            }
            QLineEdit:focus, QTextEdit:focus {
                border: 2px solid #0078d4;
            }
            QPushButton {
                background-color: #0078d4;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #106ebe;
            }
            QPushButton:pressed {
                background-color: #005a9e;
            }
            QPushButton:disabled {
                background-color: #555555;
                color: #888888;
            }
        """)
        
        # Center the dialog
        self.center_dialog()
    
    def center_dialog(self):
        """Center the dialog on the screen"""
        screen = QApplication.primaryScreen().geometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)
    
    def setup_layout(self):
        """Setup the main layout - to be overridden"""
        pass
    
    def show_dialog(self):
        """Show the dialog and return result"""
        return self.exec()
    
    def close_dialog(self):
        """Close the dialog"""
        self.close() 