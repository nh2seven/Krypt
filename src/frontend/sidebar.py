# src/frontend/sidebar.py
from PyQt6.QtWidgets import QFrame, QVBoxLayout, QWidget, QScrollArea, QHBoxLayout
from PyQt6.QtCore import pyqtSignal, Qt
from qfluentwidgets import PushButton, SubtitleLabel
from src.modules.contextmanager import db_connect


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
    groupSelected = pyqtSignal(int)
    
    def __init__(self, parent=None, db_path=None):
        super().__init__(parent)
        self.db_path = db_path
        self.setObjectName("sidebar")
        self.setStyleSheet(StyleSheet.SIDEBAR_STYLE)
        self.setFixedWidth(250)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)
        
        header_layout = QHBoxLayout()
        self.header = SubtitleLabel("Groups")
        header_layout.addWidget(self.header)
        layout.addLayout(header_layout)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setStyleSheet("""
            QScrollArea { border: none; }
            QWidget { background-color: #f5f5f5; }
        """)

        self.group_container = QWidget()
        self.groups_layout = QVBoxLayout(self.group_container)
        self.groups_layout.setSpacing(2)
        self.groups_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        scroll.setWidget(self.group_container)
        
        layout.addWidget(scroll)
        self.group_buttons = {}
        self.add_group("All", -1)  # -1 represents all groups
        
        if db_path:
            self.load_groups()

    def load_groups(self):
        """Load groups from database"""
        if not self.db_path:
            return
            
        with db_connect(self.db_path) as cur:
            cur.execute("SELECT group_id, title FROM groups")
            groups = cur.fetchall()
            
            for group_id, title in groups:
                self.add_group(title, group_id)

    def add_group(self, title, group_id):
        """Add a new group button"""
        if title not in self.group_buttons:
            button = GroupButton(title)
            button.clicked.connect(lambda: self._handle_group_click(group_id))
            self.group_buttons[title] = button
            self.groups_layout.addWidget(button)

    def _handle_group_click(self, group_id):
        """Handle group selection"""
        for button in self.group_buttons.values():
            button.setChecked(False)

        for title, button in self.group_buttons.items():
            if button.isChecked():
                button.setChecked(True)
                break

        self.groupSelected.emit(group_id)