from PyQt6.QtWidgets import (
    QToolBar,
    QToolButton,
    QWidget,
    QHBoxLayout,
    QLineEdit,
    QSpacerItem,
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, QSize, pyqtSignal


class StyleSheet:
    TOOLBAR_STYLE = """
    QToolBar {
        background-color: #f0f0f0;
        border-bottom: 1px solid #e0e0e0;
        padding: 4px 8px;
        spacing: 4px;
    }
    QToolButton {
        border: none;
        border-radius: 4px;
        padding: 8px 16px;
        background-color: transparent;
        color: #202020;
        font-size: 14px;
    }
    QToolButton:hover {
        background-color: #e8e8e8;
    }
    QToolButton:pressed, QToolButton:checked {
        background-color: #e0e0e0;
        color: #0078d4;
    }
    QLineEdit {
        border: 1px solid #e0e0e0;
        border-radius: 4px;
        padding: 6px 12px;
        background: white;
        min-width: 300px;
    }
    """


class TopToolBar(QToolBar):
    pageChanged = pyqtSignal(int)
    logoutClicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMovable(False)
        self.setFloatable(False)
        self.setAllowedAreas(Qt.ToolBarArea.TopToolBarArea)
        self.setStyleSheet(StyleSheet.TOOLBAR_STYLE)

        # Create main layout container
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        # Left section - Tabs
        self.passwords_btn = self._create_tab_button("Passwords", 0)
        self.generator_btn = self._create_tab_button("Generator", 1)
        self.settings_btn = self._create_tab_button("Settings", 2)

        # Center section - Search
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search credentials...")

        # Right section - Settings & Logout
        self.settings_btn = self._create_tab_button("Settings", 2)
        self.logout_btn = self._create_tool_button("Logout", "assets/logout.svg")
        self.logout_btn.clicked.connect(self.logoutClicked.emit)

        # Add to layout
        layout.addWidget(self.passwords_btn)
        layout.addWidget(self.generator_btn)
        layout.addSpacerItem(QSpacerItem(20, 20))
        layout.addWidget(self.search_box)
        layout.addSpacerItem(QSpacerItem(20, 20))
        layout.addWidget(self.settings_btn)
        layout.addWidget(self.logout_btn)

        # Add container to toolbar
        self.addWidget(container)

        # Set initial state
        self.passwords_btn.setChecked(True)

    def _create_tab_button(self, text, index):
        btn = QToolButton()
        btn.setText(text)
        btn.setCheckable(True)
        btn.clicked.connect(lambda: self._handle_tab_click(index))
        return btn

    def _create_tool_button(self, tooltip, icon_path):
        button = QToolButton()
        button.setIcon(QIcon(icon_path))
        button.setToolTip(tooltip)
        return button

    def _handle_tab_click(self, index):
        # Uncheck all tabs
        for btn in [self.passwords_btn, self.generator_btn, self.settings_btn]:
            btn.setChecked(False)

        # Check clicked tab
        self.sender().setChecked(True)

        # Emit page change
        self.pageChanged.emit(index)

    def set_active_tab(self, index):
        """Set active tab from external call"""
        buttons = [self.passwords_btn, self.generator_btn, self.settings_btn]
        for i, btn in enumerate(buttons):
            btn.setChecked(i == index)
