# src/frontend/topbar.py
from PyQt6.QtWidgets import QToolBar, QToolButton
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, QSize

class StyleSheet:
    TOOLBAR_STYLE = """
    QToolBar {
        background-color: #f0f0f0;
        border-bottom: 1px solid #e0e0e0;
        spacing: 4px;
        padding: 4px;
    }
    QToolButton {
        border: none;
        border-radius: 4px;
        padding: 4px;
        background-color: transparent;
        color: #202020;
    }
    QToolButton:hover {
        background-color: #e8e8e8;
    }
    QToolButton:pressed {
        background-color: #e0e0e0;
    }
    QToolButton:checked {
        background-color: #e0e0e0;
    }
    """

class TopToolBar(QToolBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMovable(False)
        self.setFloatable(False)
        self.setAllowedAreas(Qt.ToolBarArea.TopToolBarArea)
        self.setIconSize(QSize(20, 20))
        self.setStyleSheet(StyleSheet.TOOLBAR_STYLE)
        
        # Create buttons
        self.add_btn = self._create_tool_button("Add Entry", "assets/add.svg", self.add_entry)
        self.edit_btn = self._create_tool_button("Edit Entry", "assets/edit.svg", self.edit_entry)
        self.delete_btn = self._create_tool_button("Delete Entry", "assets/delete.svg", self.delete_entry)
        self.search_btn = self._create_tool_button("Search", "assets/search.svg", self.search_entries)
        self.sync_btn = self._create_tool_button("Sync", "assets/sync.svg", self.sync_data)
        
        # Add buttons to toolbar
        self.addWidget(self.add_btn)
        self.addWidget(self.edit_btn)
        self.addWidget(self.delete_btn)
        self.addSeparator()
        self.addWidget(self.search_btn)
        self.addSeparator()
        self.addWidget(self.sync_btn)
    
    def _create_tool_button(self, tooltip, icon_path, slot):
        button = QToolButton()
        button.setIcon(QIcon(icon_path))
        button.setToolTip(tooltip)
        button.clicked.connect(slot)
        return button

    def add_entry(self):
        print("Add entry clicked")

    def edit_entry(self):
        print("Edit entry clicked")

    def delete_entry(self):
        print("Delete entry clicked")

    def search_entries(self):
        print("Search clicked")
        
    def sync_data(self):
        print("Sync clicked")