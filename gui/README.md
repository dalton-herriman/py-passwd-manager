# GUI Package - Modular Structure

This package contains the modular GUI components for the Password Manager application. The original massive single file has been broken down into logical, reusable components.

## Structure

```
gui/
├── __init__.py          # Package initialization and exports
├── app.py              # Main entry point (simplified)
├── main_app.py         # Main GUI application class
├── dialogs.py          # All dialog classes
├── components.py       # Reusable UI components
├── events.py           # Event handling logic
├── test_modular.py     # Test script for modular components
└── README.md           # This documentation
```

## Components

### Main Application (`main_app.py`)
- `MultiVaultPasswordManagerGUI`: Main application class
- Handles the overall UI layout and coordination
- Manages vault and entry data
- Coordinates between different components

### Dialogs (`dialogs.py`)
- `CreateVaultDialog`: Dialog for creating new vaults
- `AddEntryDialog`: Dialog for adding new entries
- `EditEntryDialog`: Dialog for editing existing entries
- `GeneratePasswordDialog`: Dialog for generating passwords

### UI Components (`components.py`)
- `SearchBox`: Reusable search input component
- `StatusBar`: Status bar with progress indicator
- `ToolBar`: Toolbar with buttons and separators
- `TreeViewManager`: Manager for TreeView operations
- `DialogBase`: Base class for dialogs with common functionality

### Event Handling (`events.py`)
- `EventHandler`: Centralized event handling class
- Handles all button clicks, keyboard shortcuts, and user interactions
- Separates business logic from UI code

## Benefits of Modular Structure

1. **Maintainability**: Each component has a single responsibility
2. **Reusability**: Components can be reused across different parts of the application
3. **Testability**: Individual components can be tested in isolation
4. **Readability**: Code is easier to understand and navigate
5. **Extensibility**: New features can be added without modifying existing code

## Usage

### Basic Usage
```python
import tkinter as tk
from gui.main_app import MultiVaultPasswordManagerGUI

root = tk.Tk()
app = MultiVaultPasswordManagerGUI(root)
root.mainloop()
```

### Using Individual Components
```python
from gui.components import SearchBox, StatusBar, ToolBar
from gui.dialogs import CreateVaultDialog
from gui.events import EventHandler

# Create components
search = SearchBox(parent, command=on_search)
status = StatusBar(parent)
toolbar = ToolBar(parent)
```

### Custom Dialogs
```python
from gui.components import DialogBase

class CustomDialog(DialogBase):
    def setup_ui(self):
        # Custom UI setup
        pass
```

## Testing

Run the modular test script to verify everything works:

```bash
python -m gui.test_modular
```

## Migration from Old Structure

The old massive `app.py` file has been replaced with this modular structure. The main entry point remains the same:

```python
# Old way (still works)
from gui.app import main
main()

# New way (recommended)
from gui.main_app import MultiVaultPasswordManagerGUI
# ... create and run GUI
```

## File Size Comparison

- **Old structure**: 1,346 lines in single file
- **New structure**: 
  - `main_app.py`: ~300 lines
  - `dialogs.py`: ~400 lines
  - `components.py`: ~200 lines
  - `events.py`: ~250 lines
  - `app.py`: ~20 lines

Total: ~1,170 lines across 5 focused files

## Future Enhancements

1. **Theme Support**: Add theme switching capabilities
2. **Plugin System**: Allow custom components and dialogs
3. **Accessibility**: Improve keyboard navigation and screen reader support
4. **Internationalization**: Add multi-language support
5. **Custom Widgets**: Create more specialized UI components

## Contributing

When adding new features:

1. **UI Components**: Add to `components.py`
2. **Dialogs**: Add to `dialogs.py`
3. **Events**: Add to `events.py`
4. **Main Logic**: Add to `main_app.py`
5. **Tests**: Add corresponding tests

Follow the existing patterns and maintain the modular structure. 