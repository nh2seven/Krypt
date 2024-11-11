# toolbar.py
from PyQt6.QtWidgets import QToolBar, QAction
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt

class TopToolbar(QToolBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMovable(False)
        self.setFloatable(False)
        self.setAllowedAreas(Qt.ToolBarArea.TopToolBarArea)
        
        # Add actions
        add_action = QAction(QIcon("assets/add.png"), "Add Entry", self)
        add_action.triggered.connect(self.add_entry)

        delete_action = QAction(QIcon("assets/delete.png"), "Delete Entry", self)
        delete_action.triggered.connect(self.delete_entry)

        search_action = QAction(QIcon("assets/search.png"), "Search", self)
        search_action.triggered.connect(self.search_entries)

        # Add actions to toolbar
        self.addAction(add_action)
        self.addAction(delete_action)
        self.addSeparator()
        self.addAction(search_action)

    def add_entry(self):
        print("Add entry clicked")

    def delete_entry(self):
        print("Delete entry clicked")

    def search_entries(self):
        print("Search clicked")
