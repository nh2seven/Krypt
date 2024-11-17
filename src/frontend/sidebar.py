# src/frontend/sidebar.py
from PyQt6.QtWidgets import QFrame, QVBoxLayout, QWidget, QScrollArea
from PyQt6.QtCore import pyqtSignal, Qt
from qfluentwidgets import PushButton, SubtitleLabel


class StyleSheet:
    SIDEBAR_STYLE = """
    QFrame#sidebar {
        background-color: #f5f5f5;
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


class GroupButton(PushButton):
    def __init__(self, text):
        super().__init__()
        self.setText(text)
        self.setCheckable(True)
        self.setStyleSheet(StyleSheet.BUTTON_STYLE)


class GroupSidebar(QFrame):
    groupSelected = pyqtSignal(str)  # Emits group name when selected

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("sidebar")
        self.setStyleSheet(StyleSheet.SIDEBAR_STYLE)
        self.setFixedWidth(250)

        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        # Header
        self.header = SubtitleLabel("Groups")
        layout.addWidget(self.header)

        # Scrollable group list
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
            }
            QWidget {
                background-color: #f5f5f5;
            }
        """)

        # Container for group buttons
        self.group_container = QWidget()
        self.group_container.setStyleSheet("""
            QWidget {
                background-color: #f5f5f5;
            }
        """)
        self.groups_layout = QVBoxLayout(self.group_container)
        self.groups_layout.setSpacing(2)
        self.groups_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        scroll.setWidget(self.group_container)

        layout.addWidget(scroll)

        # Store group buttons
        self.group_buttons = {}

    def add_group(self, group_name):
        """Add a new group button"""
        if group_name not in self.group_buttons:
            button = GroupButton(group_name)
            button.clicked.connect(lambda: self._handle_group_click(group_name))
            self.group_buttons[group_name] = button
            self.groups_layout.addWidget(button)

    def _handle_group_click(self, group_name):
        """Handle group selection"""
        # Uncheck all buttons
        for button in self.group_buttons.values():
            button.setChecked(False)

        # Check selected button
        self.group_buttons[group_name].setChecked(True)

        # Emit selected group
        self.groupSelected.emit(group_name)

    def set_active_group(self, group_name):
        """Set active group from external call"""
        if group_name in self.group_buttons:
            self._handle_group_click(group_name)
