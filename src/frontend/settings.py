# settings.py
from PyQt6.QtWidgets import (
    QWidget, 
    QVBoxLayout,
    QGridLayout,
    QLabel,
    QHBoxLayout
)
from qfluentwidgets import (
    PushButton,
    LineEdit,
    InfoBar,
    InfoBarPosition,
    TitleLabel,
    CardWidget
)
from PyQt6.QtCore import Qt
from .audit import AuditLogCard

class PasswordChangeCard(CardWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(350)
        self.setup_ui()

        self.setStyleSheet("""
            PasswordChangeCard {
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
            }
        """)

    def setup_ui(self):
        layout = QGridLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        # Title
        title = TitleLabel("Change Password")
        layout.addWidget(title, 0, 0, 1, 2)

        # Current password
        self.current_pw_label = QLabel("Current Password:")
        self.current_pw_input = LineEdit()
        self.current_pw_input.setEchoMode(LineEdit.EchoMode.Password)
        layout.addWidget(self.current_pw_label, 1, 0)
        layout.addWidget(self.current_pw_input, 1, 1)

        # New password
        self.new_pw_label = QLabel("New Password:")
        self.new_pw_input = LineEdit()
        self.new_pw_input.setEchoMode(LineEdit.EchoMode.Password)
        layout.addWidget(self.new_pw_label, 2, 0)
        layout.addWidget(self.new_pw_input, 2, 1)

        # Confirm password
        self.confirm_pw_label = QLabel("Confirm Password:")
        self.confirm_pw_input = LineEdit()
        self.confirm_pw_input.setEchoMode(LineEdit.EchoMode.Password)
        layout.addWidget(self.confirm_pw_label, 3, 0)
        layout.addWidget(self.confirm_pw_input, 3, 1)

        # Save button
        self.save_button = PushButton("Change Password")
        self.save_button.clicked.connect(self.change_password)
        layout.addWidget(self.save_button, 4, 0, 1, 2)

    def change_password(self):
        current_pw = self.current_pw_input.text()
        new_pw = self.new_pw_input.text()
        confirm_pw = self.confirm_pw_input.text()

        # Basic validation
        if not all([current_pw, new_pw, confirm_pw]):
            self.show_error("All fields are required")
            return

        if new_pw != confirm_pw:
            self.show_error("New passwords do not match")
            return

        # TODO: Add actual password change logic here
        self.show_success("Password changed successfully")
        self.clear_fields()

    def show_error(self, message):
        InfoBar.error(
            title="Error",
            content=message,
            orient=Qt.Orientation.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=3000,
            parent=self
        )

    def show_success(self, message):
        InfoBar.success(
            title="Success",
            content=message,
            orient=Qt.Orientation.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=3000,
            parent=self
        )

    def clear_fields(self):
        self.current_pw_input.clear()
        self.new_pw_input.clear()
        self.confirm_pw_input.clear()

# settings.py
class SettingsView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        # Main vertical layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)

        # Horizontal container for cards
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(20)
        
        # Add password change card
        self.pw_change_card = PasswordChangeCard()
        self.pw_change_card.setFixedWidth(300)
        cards_layout.addWidget(self.pw_change_card, 1)
        
        # Add audit log card
        self.audit_log_card = AuditLogCard()
        self.audit_log_card.setFixedWidth(600)
        cards_layout.addWidget(self.audit_log_card, 2)
        
        # Add the cards layout to main layout
        layout.addLayout(cards_layout)
        layout.addStretch()