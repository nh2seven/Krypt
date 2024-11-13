from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QHBoxLayout,
    QScrollArea,
    QFrame,
)
from PyQt6.QtCore import pyqtSignal, Qt
from qfluentwidgets import (
    CardWidget,
    ScrollArea,
    PushButton,
    InfoBar,
    LineEdit,
    TitleLabel,
    SubtitleLabel,
    InfoBarPosition,
)
from qfluentwidgets.common.style_sheet import FluentStyleSheet


class UserCard(CardWidget):
    userClicked = pyqtSignal(str)  # Create new signal for username

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
            self.userClicked.emit(self.username)  # Emit username with new signal


class LoginScreen(QWidget):
    login_success = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setFixedSize(1000, 700)
        self.current_user = None
        self.initUI()

    def initUI(self):
        # Main layout
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Left panel (User list)
        left_panel = QFrame()
        left_panel.setStyleSheet("background-color: #f5f5f5;")
        left_panel.setFixedWidth(400)
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(20, 20, 20, 20)

        # Action buttons
        buttons_layout = QHBoxLayout()
        add_user_btn = PushButton("New User")
        add_user_btn.clicked.connect(self.add_user)
        delete_user_btn = PushButton("Delete User")
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

        # Add sample users
        self.add_sample_users()

    def add_sample_users(self):
        # Add some sample users
        sample_users = ["admin", "user1", "user2"]
        for username in sample_users:
            self.add_user_card(username)

    def add_user_card(self, username):
        card = UserCard(username)
        card.userClicked.connect(self.select_user)  # Connect to new signal
        self.cards_layout.addWidget(card)

    def select_user(self, username):
        self.current_user = username
        self.user_label.setText(f"Welcome back, {username}")
        self.password_input.setFocus()

    def add_user(self):
        # TODO: Implement user creation
        pass

    def delete_user(self):
        # TODO: Implement user deletion
        pass

    def handle_login(self):
        if not self.current_user:
            InfoBar.error(
                title="Error",
                content="Please select a user first",
                orient=Qt.Orientation.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=2000,
                parent=self,
            )
            return

        password = self.password_input.text()

        # Sample authentication
        if self.current_user == "admin" and password == "password":
            InfoBar.success(
                title="Success",
                content="Login successful",
                orient=Qt.Orientation.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=1000,
                parent=self,
            )
            self.login_success.emit()
        else:
            InfoBar.error(
                title="Error",
                content="Invalid credentials",
                orient=Qt.Orientation.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=2000,
                parent=self,
            )

    def clear_fields(self):
        """Reset login form state"""
        # Reset user selection
        self.current_user = None
        self.user_label.setText("Select a user to login")
        
        # Clear password
        self.password_input.clear()
        self.password_input.setPlaceholderText("Enter password")

        # Optional: Reset focus
        self.password_input.clearFocus()
