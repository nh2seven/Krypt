from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLabel, QHBoxLayout
from qfluentwidgets import PushButton, LineEdit, InfoBar, InfoBarPosition, TitleLabel, CardWidget
from PyQt6.QtCore import Qt
from .audit import AuditLogCard
from src.backend.auth import User


class PasswordChangeCard(CardWidget):
    def __init__(self, db_path, username, parent=None):
        super().__init__(parent)
        self.db_path = db_path
        self.username = username
        self.user = User(db_path, username, None)
        self.setFixedWidth(350)
        self.setup_ui()
        self.setFixedWidth(350)
        self.setStyleSheet(
            """
            PasswordChangeCard {
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
            }
        """
        )

    def setup_ui(self):
        layout = QGridLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        title = TitleLabel("Change Password")
        layout.addWidget(title, 0, 0, 1, 2)

        self.current_pw_label = QLabel("Current Password:")
        self.current_pw_input = LineEdit()
        self.current_pw_input.setEchoMode(LineEdit.EchoMode.Password)
        layout.addWidget(self.current_pw_label, 1, 0)
        layout.addWidget(self.current_pw_input, 1, 1)

        self.new_pw_label = QLabel("New Password:")
        self.new_pw_input = LineEdit()
        self.new_pw_input.setEchoMode(LineEdit.EchoMode.Password)
        layout.addWidget(self.new_pw_label, 2, 0)
        layout.addWidget(self.new_pw_input, 2, 1)

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

        if not all([current_pw, new_pw, confirm_pw]):
            self.show_error("All fields are required")
            return

        if new_pw != confirm_pw:
            self.show_error("New passwords do not match")
            return

        if self.user.change_password(current_pw, new_pw):
            self.show_success("Password changed successfully!")
            self.clear_fields()
        else:
            self.show_error("Current password is incorrect.")

    def show_error(self, message):
        InfoBar.error(
            title="Error",
            content=message,
            orient=Qt.Orientation.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=3000,
            parent=self,
        )

    def show_success(self, message):
        InfoBar.success(
            title="Success",
            content=message,
            orient=Qt.Orientation.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=3000,
            parent=self,
        )

    def clear_fields(self):
        self.current_pw_input.clear()
        self.new_pw_input.clear()
        self.confirm_pw_input.clear()


class SettingsView(QWidget):
    def __init__(self, db_path, username, parent=None):
        super().__init__(parent)
        self.db_path = db_path
        self.username = username
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(20)

        self.pw_change_card = PasswordChangeCard(self.db_path, self.username)
        self.pw_change_card.setFixedWidth(300)
        cards_layout.addWidget(self.pw_change_card, 1)

        self.audit_log_card = AuditLogCard(db_path=self.db_path)
        self.audit_log_card.setFixedWidth(600)
        cards_layout.addWidget(self.audit_log_card, 2)

        layout.addLayout(cards_layout)
        layout.addStretch()
