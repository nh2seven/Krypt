# src/frontend/cred.py
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QDialog,
    QHBoxLayout,
    QLabel,
    QGridLayout,
    QFrame,
    QStackedWidget,
    QToolButton,
)
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QSize
from PyQt6.QtGui import QIcon

from qfluentwidgets import (
    PushButton,
    LineEdit,
    SubtitleLabel,
)

from .sidebar import GroupSidebar


class CredentialButton(PushButton):
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.setText(title)
        self.setCheckable(True)
        self.setStyleSheet(
            """
            PushButton {
                text-align: left;
                padding: 8px 20px;
                border: none;
                border-radius: 4px;
                margin: 2px 8px;
                background-color: transparent;
                font-size: 14px;
            }
            PushButton:checked {
                background-color: #e6e6e6;
                color: #0078d4;
            }
            PushButton:hover {
                background-color: #f0f0f0;
            }
        """
        )


class DetailSidebar(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(350)
        self.setStyleSheet(
            """
            QFrame {
                background-color: #f5f5f5;
                border-left: 1px solid #e0e0e0;
            }
        """
        )

        # Create layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        # Header
        self.title = SubtitleLabel("Credentials")
        layout.addWidget(self.title)

        # Placeholder content
        self.placeholder = QLabel("Select a credential to view details")
        self.placeholder.setStyleSheet(
            """
            QLabel {
                color: #666666;
                font-size: 14px;
            }
        """
        )
        self.placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Stack for switching between placeholder and details
        self.stack = QStackedWidget()

        # Placeholder widget
        placeholder_widget = QWidget()
        placeholder_layout = QVBoxLayout(placeholder_widget)
        placeholder_layout.addStretch()
        placeholder_layout.addWidget(self.placeholder)
        placeholder_layout.addStretch()

        # Details widget
        details_widget = QWidget()
        details_layout = QVBoxLayout(details_widget)

        # Details content
        self.detail_title = SubtitleLabel("")
        self.username_label = QLabel("Username:")
        self.username_value = LineEdit(self)
        self.username_value.setReadOnly(True)

        self.url_label = QLabel("URL:")
        self.url_value = LineEdit(self)
        self.url_value.setReadOnly(True)

        self.notes_label = QLabel("Notes:")
        self.notes_value = LineEdit(self)
        self.notes_value.setReadOnly(True)

        # Edit button
        self.edit_btn = PushButton("Edit")

        # Add to details layout
        details_layout.addWidget(self.detail_title)
        details_layout.addWidget(self.username_label)
        details_layout.addWidget(self.username_value)
        details_layout.addWidget(self.url_label)
        details_layout.addWidget(self.url_value)
        details_layout.addWidget(self.notes_label)
        details_layout.addWidget(self.notes_value)
        details_layout.addWidget(self.edit_btn)
        details_layout.addStretch()

        # Add both widgets to stack
        self.stack.addWidget(placeholder_widget)
        self.stack.addWidget(details_widget)

        # Add stack to main layout
        layout.addWidget(self.stack)

    def update_details(self, title, username, url, notes=""):
        """Update sidebar with credential details"""
        self.detail_title.setText(title)
        self.username_value.setText(username)
        self.url_value.setText(url)
        self.notes_value.setText(notes)
        self.stack.setCurrentIndex(1)  # Show details widget

    def show_placeholder(self):
        """Show placeholder when no credential selected"""
        self.stack.setCurrentIndex(0)  # Show placeholder widget


class CredentialDialog(QDialog):
    def __init__(self, parent=None, title="", username="", url=""):
        super().__init__(parent)
        self.setWindowTitle("Edit Credential" if title else "Add Credential")
        self.setFixedWidth(400)
        layout = QGridLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        self.title_label = QLabel("Title:")
        self.title_input = LineEdit(self)
        self.title_input.setText(title)

        self.username_label = QLabel("Username:")
        self.username_input = LineEdit(self)
        self.username_input.setText(username)

        self.password_label = QLabel("Password:")
        self.password_input = LineEdit(self)
        self.password_input.setEchoMode(LineEdit.EchoMode.Password)

        self.url_label = QLabel("URL:")
        self.url_input = LineEdit(self)
        self.url_input.setText(url)

        self.notes_label = QLabel("Notes:")
        self.notes_input = LineEdit(self)

        self.save_button = PushButton("Save")
        self.save_button.clicked.connect(self.accept)

        layout.addWidget(self.title_label, 0, 0)
        layout.addWidget(self.title_input, 0, 1)
        layout.addWidget(self.username_label, 1, 0)
        layout.addWidget(self.username_input, 1, 1)
        layout.addWidget(self.password_label, 2, 0)
        layout.addWidget(self.password_input, 2, 1)
        layout.addWidget(self.url_label, 3, 0)
        layout.addWidget(self.url_input, 3, 1)
        layout.addWidget(self.notes_label, 4, 0)
        layout.addWidget(self.notes_input, 4, 1)
        layout.addWidget(self.save_button, 5, 0, 1, 2)

    def get_data(self):
        return (
            self.title_input.text(),
            self.username_input.text(),
            self.password_input.text(),
            self.url_input.text(),
            self.notes_input.text(),
        )


class CredentialsToolBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(
            """
            QWidget {
                background-color: #f8f8f8;
                border-bottom: 1px solid #e0e0e0;
            }
            QToolButton {
                border: none;
                border-radius: 4px;
                padding: 6px;
                background-color: transparent;
            }
            QToolButton:hover {
                background-color: #e8e8e8;
            }
            QToolButton:pressed {
                background-color: #e0e0e0;
            }
        """
        )

        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 4, 8, 4)
        layout.setSpacing(4)

        # Create buttons
        self.add_btn = self._create_tool_button("Add Entry", "assets/add.svg")
        self.edit_btn = self._create_tool_button("Edit Entry", "assets/edit.svg")
        self.delete_btn = self._create_tool_button("Delete Entry", "assets/delete.svg")

        # Add buttons to layout
        layout.addWidget(self.add_btn)
        layout.addWidget(self.edit_btn)
        layout.addWidget(self.delete_btn)
        layout.addStretch()  # Push buttons to left

    def _create_tool_button(self, tooltip, icon_path):
        button = QToolButton()
        button.setIcon(QIcon(icon_path))
        button.setToolTip(tooltip)
        button.setIconSize(QSize(20, 20))
        return button


class CredentialsView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Add toolbar at top
        self.toolbar = CredentialsToolBar()
        layout.addWidget(self.toolbar)

        # Content area
        content = QWidget()
        content_layout = QHBoxLayout(content)
        content_layout.setContentsMargins(0, 0, 0, 0)

        # Group sidebar
        self.group_sidebar = GroupSidebar()
        self.group_sidebar.groupSelected.connect(self.filter_credentials)
        content_layout.addWidget(self.group_sidebar)

        # Credential list area
        cred_area = QWidget()
        cred_layout = QHBoxLayout(cred_area)
        cred_layout.setContentsMargins(20, 20, 0, 20)

        # Credential list
        self.cred_list = QVBoxLayout()
        self.cred_list.setSpacing(2)
        self.cred_list.setAlignment(Qt.AlignmentFlag.AlignTop)
        cred_layout.addLayout(self.cred_list)

        # Detail sidebar
        self.detail_sidebar = DetailSidebar()
        cred_layout.addWidget(self.detail_sidebar)

        content_layout.addWidget(cred_area)
        layout.addWidget(content)

    def load_credentials(self):
        """Load and display credentials"""
        # Clear existing credentials
        self.clear_credentials()
        
        # TODO: Load credentials from database
        # For now, add some sample credentials
        sample_creds = [
            ("Gmail", "user@gmail.com", "https://gmail.com"),
            ("GitHub", "username", "https://github.com"),
            ("Netflix", "user@email.com", "https://netflix.com")
        ]
        
        for title, username, url in sample_creds:
            cred_btn = CredentialButton(title)
            cred_btn.clicked.connect(
                lambda checked, t=title, u=username, l=url: 
                self.detail_sidebar.update_details(t, u, l)
            )
            self.cred_list.addWidget(cred_btn)

    def clear_credentials(self):
        """Clear all credentials from view"""
        while self.cred_list.count():
            item = self.cred_list.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
                
        # Reset sidebar
        self.detail_sidebar.show_placeholder()

    def filter_credentials(self, group_name):
        """Filter credentials by group"""
        # TODO: Implement filtering
        pass
