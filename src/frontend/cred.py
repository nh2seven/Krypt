# src/frontend/cred.py
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QDialog,
    QHBoxLayout,
    QLabel,
    QGridLayout,
    QFrame,
    QStackedWidget,
)
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve
from qfluentwidgets import (
    TableWidget,
    PushButton,
    LineEdit,
    CardWidget,
    InfoBar,
    InfoBarPosition,
    SubtitleLabel,
)


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


# src/frontend/cred.py

class DetailSidebar(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(300)
        self.setStyleSheet("""
            QFrame {
                background-color: #f5f5f5;
                border-left: 1px solid #e0e0e0;
            }
        """)
        
        # Create layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Header
        self.title = SubtitleLabel("Credentials")
        layout.addWidget(self.title)
        
        # Placeholder content
        self.placeholder = QLabel("Select a credential to view details")
        self.placeholder.setStyleSheet("""
            QLabel {
                color: #666666;
                font-size: 14px;
            }
        """)
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


class CredentialsView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Left content area
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(20, 20, 20, 20)
        
        self.cred_list = QVBoxLayout()
        self.cred_list.setSpacing(2)
        self.cred_list.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        self.add_button = PushButton("Add Credential")
        self.add_button.clicked.connect(self.show_add_credential_dialog)
        
        content_layout.addLayout(self.cred_list)
        content_layout.addWidget(self.add_button)
        
        self.detail_sidebar = DetailSidebar()
        
        layout.addWidget(content)
        layout.addWidget(self.detail_sidebar)
        
        # Initialize credentials
        self.load_credentials()

    def load_credentials(self):
        """Load credentials into list"""
        # Clear existing buttons
        while self.cred_list.count():
            item = self.cred_list.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Dummy data for testing
        test_data = [
            ("Email", "user@example.com", "mail.example.com"),
            ("Social", "username123", "social.example.com"),
            ("Work", "worker", "work.example.com")
        ]
        
        # Add credential buttons
        for title, username, url in test_data:
            btn = CredentialButton(title)
            btn.clicked.connect(
                lambda checked, t=title, u=username, url=url: 
                self.show_credential_details(t, u, url)
            )
            self.cred_list.addWidget(btn)

    def show_credential_details(self, title, username, url, notes=""):
    # Update and show details
        self.detail_sidebar.update_details(title, username, url, notes)
    
    # Uncheck other buttons 
        for i in range(self.cred_list.count()):
            btn = self.cred_list.itemAt(i).widget()
            if isinstance(btn, CredentialButton):
                # Only check matching button
                btn.setChecked(btn.text() == title)

    def show_add_credential_dialog(self):
        dialog = CredentialDialog(self)
        if dialog.exec():
            title, username, password, url, notes = dialog.get_data()
            print(f"Adding: {title}, {username}, {url}")  # Replace with DB call
            self.load_credentials()  # Reload to show new credential