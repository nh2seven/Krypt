import os
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QHBoxLayout, QFrame, QInputDialog, QMessageBox
from qfluentwidgets import CardWidget, ScrollArea, PushButton, InfoBar, LineEdit, TitleLabel, SubtitleLabel, InfoBarPosition
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QIcon
from src.backend.auth import User


class UserCard(CardWidget):
    userClicked = pyqtSignal(str)

    def __init__(self, username):
        super().__init__()
        self.username = username

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 15, 20, 15)

        name_label = SubtitleLabel(username)
        name_label.setStyleSheet(
            """
            QLabel {
                color: #202020;
                background: transparent;
            }
        """
        )
        layout.addWidget(name_label)

        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFixedHeight(70)
        self.setStyleSheet(
            """
            CardWidget {
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 6px;
            }
            CardWidget:hover {
                background-color: #f5f5f5;
                border: 1px solid #d0d0d0;
            }
        """
        )

    def mouseReleaseEvent(self, e):
        super().mouseReleaseEvent(e)
        if e.button() == Qt.MouseButton.LeftButton:
            self.userClicked.emit(self.username)


class LoginScreen(QWidget):
    login_success = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setFixedSize(700, 500)
        self.setWindowFlags(
            Qt.WindowType.Window
            | Qt.WindowType.CustomizeWindowHint
            | Qt.WindowType.WindowCloseButtonHint
            | Qt.WindowType.WindowMinimizeButtonHint
        )
        self.current_user = None
        self.user_auth = None
        self.initUI()
        self.load_users()

    def initUI(self):
        # Main layout
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Left panel (User list)
        left_panel = QFrame()
        left_panel.setStyleSheet("background-color: #f5f5f5;")
        left_panel.setFixedWidth(350)
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(20, 20, 20, 20)

        # Action buttons
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)
        add_user_btn = PushButton("New User")
        add_user_btn.setIcon(QIcon("assets/add.svg"))
        add_user_btn.setFixedWidth(135)
        add_user_btn.clicked.connect(self.add_user)
        delete_user_btn = PushButton("Delete User")
        delete_user_btn.setIcon(QIcon("assets/delete.svg"))
        delete_user_btn.setFixedWidth(135)
        delete_user_btn.clicked.connect(self.delete_user)
        buttons_layout.addWidget(add_user_btn)
        buttons_layout.addWidget(delete_user_btn)
        left_layout.addLayout(buttons_layout)

        # Scrollable user list
        scroll = ScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setStyleSheet(
            "QScrollArea{border: none; background-color: transparent;}"
        )

        # Container for user cards
        scroll_content = QWidget()
        self.cards_layout = QVBoxLayout(scroll_content)
        self.cards_layout.setSpacing(10)
        self.cards_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        scroll.setWidget(scroll_content)
        left_layout.addWidget(scroll)

        # Right panel (Login form)
        right_panel = QFrame()
        right_panel.setStyleSheet("background-color: white;")
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(40, 40, 40, 40)
        right_layout.setSpacing(20)

        # App title
        title = TitleLabel("Krypt")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        right_layout.addWidget(title)

        # Selected user
        self.user_label = SubtitleLabel("Select a user to login")
        self.user_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        right_layout.addWidget(self.user_label)

        # Password input
        self.password_input = LineEdit()
        self.password_input.setPlaceholderText("Enter password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.returnPressed.connect(self.handle_login)
        right_layout.addWidget(self.password_input)

        # Login button
        login_btn = PushButton("Login")
        login_btn.clicked.connect(self.handle_login)
        right_layout.addWidget(login_btn)
        right_layout.addStretch()

        # Add panels to main layout
        layout.addWidget(left_panel)
        layout.addWidget(right_panel)

    def load_users(self):
        """Load existing users from users directory"""
        os.makedirs("db/users", exist_ok=True)
        for file in os.listdir("db/users"):
            if file.endswith(".db"):
                username = os.path.splitext(file)[0]
                self.add_user_card(username)

    def add_user_card(self, username):
        card = UserCard(username)
        card.userClicked.connect(self.select_user)
        self.cards_layout.addWidget(card)

    def select_user(self, username):
        self.current_user = username
        self.user_label.setText(f"Welcome back, {username}")
        self.password_input.setFocus()

    def handle_login(self):
        if not self.current_user:
            InfoBar.error(
                title="Error",
                content="Please select a user first",
                position=InfoBarPosition.TOP,
                duration=2000,
                parent=self,
            )
            return

        password = self.password_input.text()

        # Create auth instance for selected user
        user_db = f"db/users/{self.current_user}.db"  # Adjust path as needed
        self.user_auth = User(user_db, self.current_user, password)

        # Attempt login
        if self.user_auth.login():
            InfoBar.success(
                title="Success",
                content="Login successful",
                position=InfoBarPosition.TOP,
                duration=1000,
                parent=self,
            )
            self.login_success.emit()
        else:
            InfoBar.error(
                title="Error",
                content="Invalid credentials",
                position=InfoBarPosition.TOP,
                duration=2000,
                parent=self,
            )

    def refresh_users(self):
        """Clear and reload user cards"""
        while self.cards_layout.count():
            item = self.cards_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        self.load_users()

    def add_user(self):
        """Create a new user with password"""
        username, ok = QInputDialog.getText(self, "New User", "Enter username:")
        if not ok or not username:
            return

        password, ok = QInputDialog.getText(
            self, "New User", "Enter password:", QLineEdit.EchoMode.Password
        )
        if not ok or not password:
            return

        db_path = f"db/users/{username}.db"
        if os.path.exists(db_path):
            InfoBar.error(
                title="Error",
                content="User already exists",
                position=InfoBarPosition.TOP,
                duration=2000,
                parent=self,
            )
            return

        user = User(db_path, username, password)
        user.create(password)
        self.add_user_card(username)

        InfoBar.success(
            title="Success",
            content="User created successfully",
            position=InfoBarPosition.TOP,
            duration=2000,
            parent=self,
        )

    def delete_user(self):
        """Delete selected user"""
        if not self.current_user:
            InfoBar.error(
                title="Error",
                content="Please select a user first",
                position=InfoBarPosition.TOP,
                duration=2000,
                parent=self,
            )
            return

        reply = QMessageBox.question(
            self,
            "Confirm Deletion",
            f"Are you sure you want to delete user {self.current_user}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )

        if reply == QMessageBox.StandardButton.No:
            return

        db_path = f"db/users/{self.current_user}.db"
        if os.path.exists(db_path):
            os.remove(db_path)
            self.clear_fields()
            self.refresh_users()

            InfoBar.success(
                title="Success",
                content="User deleted successfully",
                position=InfoBarPosition.TOP,
                duration=2000,
                parent=self,
            )

    def clear_fields(self):
        """Reset login form state"""
        self.current_user = None
        self.user_label.setText("Select a user to login")
        self.password_input.clear()
        self.password_input.setPlaceholderText("Enter password")
        self.password_input.clearFocus()
