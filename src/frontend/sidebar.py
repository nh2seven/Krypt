# src/frontend/sidebar.py
from PyQt6.QtWidgets import QFrame, QVBoxLayout, QWidget, QScrollArea, QHBoxLayout, QInputDialog, QMessageBox
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QIcon
from qfluentwidgets import PushButton, SubtitleLabel, TransparentToolButton, SubtitleLabel
from src.modules.contextmanager import db_connect
from src.backend.user import Groups


class StyleSheet:
    SIDEBAR_STYLE = """
    QFrame#sidebar {
        background-color: #f5f5f5;
        border-right: 1px solid #e0e0e0;
    }
    TransparentToolButton {
        border: none;
        border-radius: 4px;
        padding: 4px;
        background-color: transparent;
    }
    TransparentToolButton:hover {
        background-color: #e8e8e8;
    }
    TransparentToolButton:pressed {
        background-color: #e0e0e0;
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

    def delete_group(self):
        """Delete selected group"""
        selected_button = None
        selected_title = None

        for title, button in self.group_buttons.items():
            if button.isChecked():
                selected_button = button
                selected_title = title
                break

        if not selected_button or selected_title == "All":
            QMessageBox.warning(self, "Warning", "Please select a group to delete.")
            return

        try:
            groups = Groups(self.db_path)
            group_id = groups.get_gid(selected_title)

            if not group_id:
                QMessageBox.warning(
                    self, "Error", f"Group '{selected_title}' not found."
                )
                return
            confirmation = QMessageBox.question(
                self,
                "Delete Group",
                f"Are you sure you want to delete the group '{selected_title}'?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            )

            if confirmation == QMessageBox.StandardButton.Yes:
                groups.delete_group(group_id)

                self.groups_layout.removeWidget(selected_button)
                selected_button.deleteLater()
                del self.group_buttons[selected_title]

                self._handle_group_click(-1)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to delete group: {str(e)}")


class GroupButton(PushButton):
    def __init__(self, text):
        super().__init__()
        self.setText(text)
        self.setCheckable(True)
        self.setAutoExclusive(True)
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

        # Header with buttons
        header_layout = QHBoxLayout()
        self.header = SubtitleLabel("Groups")
        header_layout.addWidget(self.header)

        # Add group management buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(4)

        self.add_btn = TransparentToolButton()
        self.add_btn.setIcon(QIcon("assets/add.svg"))
        self.add_btn.setToolTip("Add Group")
        self.add_btn.clicked.connect(self.create_group)

        self.delete_btn = TransparentToolButton()
        self.delete_btn.setIcon(QIcon("assets/delete.svg"))
        self.delete_btn.setToolTip("Delete Group")
        self.delete_btn.clicked.connect(self.delete_group)

        button_layout.addWidget(self.add_btn)
        button_layout.addWidget(self.delete_btn)
        header_layout.addLayout(button_layout)
        header_layout.addStretch()

        layout.addLayout(header_layout)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setStyleSheet(
            """
            QScrollArea { border: none; }
            QWidget { background-color: #f5f5f5; }
        """
        )

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

    def create_group(self):
        """Create a new group"""
        title, ok = QInputDialog.getText(
            self,
            "Create Group",
            "Enter group name:",
        )

        if ok and title:
            try:
                with db_connect(self.db_path) as cur:
                    cur.execute("SELECT title FROM groups WHERE title = ?", (title,))
                    if cur.fetchone():
                        QMessageBox.warning(
                            self, "Error", f"Group '{title}' already exists"
                        )
                        return

                    cur.execute("INSERT INTO groups (title) VALUES (?)", (title,))
                    group_id = cur.lastrowid
                    self.add_group(title, group_id)

            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to create group: {str(e)}")

    def delete_group(self):
        """Delete selected group"""
        # Find currently selected button
        selected_button = None
        selected_title = None

        for title, button in self.group_buttons.items():
            if button.isChecked() and title != "All":  # Explicitly check it's not "All"
                selected_button = button
                selected_title = title
                break

        if not selected_button:
            QMessageBox.warning(self, "Warning", "Please select a group to delete.")
            return

        try:
            # Get group ID and confirm deletion
            groups = Groups(self.db_path)
            group_id = groups.get_gid(selected_title)

            if not group_id:
                QMessageBox.warning(
                    self, "Error", f"Group '{selected_title}' not found."
                )
                return

            confirmation = QMessageBox.question(
                self,
                "Delete Group",
                f"Are you sure you want to delete the group '{selected_title}'?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            )

            if confirmation == QMessageBox.StandardButton.Yes:
                # Delete group and update UI
                groups.delete_group(group_id)
                self.groups_layout.removeWidget(selected_button)
                selected_button.deleteLater()
                del self.group_buttons[selected_title]

                # Select "All" group after deletion
                all_button = self.group_buttons.get("All")
                if all_button:
                    all_button.setChecked(True)
                    self._handle_group_click(-1)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to delete group: {str(e)}")

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
