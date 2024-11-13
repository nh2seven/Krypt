# src/frontend/sidebar.py
from PyQt6.QtWidgets import QFrame, QVBoxLayout, QPushButton
from PyQt6.QtCore import pyqtSignal, QSize, Qt
from PyQt6.QtGui import QIcon


class StyleSheet:
    SIDEBAR_STYLE = """
    QFrame#sidebar {
        background-color: #f0f0f0;
        border-right: 1px solid #e0e0e0;
    }
    """

    BUTTON_STYLE = """
    QPushButton {
        text-align: left;
        padding: 8px 20px;
        border: none;
        border-radius: 4px;
        margin: 2px 8px;
        background-color: transparent;
        font-size: 14px;
        color: #202020;
    }
    QPushButton:checked {
        background-color: #e6e6e6;
        color: #0078d4;
    }
    QPushButton:hover {
        background-color: #e8e8e8;
    }
    """


class SidebarButton(QPushButton):
    def __init__(self, text, icon=None):
        super().__init__()
        self.setText(text)
        if icon:
            self.setIcon(icon)
            self.setIconSize(QSize(20, 20))
        self.setCheckable(True)
        self.setFixedHeight(40)
        self.setStyleSheet(StyleSheet.BUTTON_STYLE)


class Sidebar(QFrame):
    pageChanged = pyqtSignal(int)
    logoutClicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("sidebar")
        self.setStyleSheet(StyleSheet.SIDEBAR_STYLE)
        self.setFixedWidth(200)

        # Main layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 10, 0, 10)
        self.layout.setSpacing(2)

        # Store buttons
        self.buttons = {}

        # Add main navigation buttons
        self._add_button("Home", 0)
        self._add_button("Passwords", 1)
        self._add_button("Generator", 2)

        # Add stretch to push bottom buttons down
        self.layout.addStretch()

        # Add bottom buttons
        self._add_button("Logout", -1)  # Use -1 to indicate special handling
        self._add_button("Settings", 3)

        # Set initial selection
        self.buttons["Home"].setChecked(True)

    def set_active_page(self, index):
        """Set active page from external call"""
        # Uncheck all buttons first
        for button in self.buttons.values():
            button.setChecked(False)
            
        # Find and check the button for this index
        for button_text, button in self.buttons.items():
            if button_text == "Home" and index == 0:
                button.setChecked(True)
            elif button_text == "Passwords" and index == 1:
                button.setChecked(True)
            elif button_text == "Generator" and index == 2:
                button.setChecked(True)
            elif button_text == "Settings" and index == 3:
                button.setChecked(True)
    
    def _handle_button_click(self, index):
        """Handle button clicks and emit page change signal"""
        if index == -1:
            # Handle logout separately
            self.logoutClicked.emit()
            return

        # Uncheck all buttons
        for button in self.buttons.values():
            button.setChecked(False)

        # Check clicked button
        self.sender().setChecked(True)

        # Emit signal with page index
        self.pageChanged.emit(index)

    def _add_button(self, text, index):
        """Add a navigation button to the sidebar"""
        button = SidebarButton(text)
        button.clicked.connect(lambda: self._handle_button_click(index))
        self.buttons[text] = button
        self.layout.addWidget(button)
