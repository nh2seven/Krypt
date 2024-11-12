from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtCore import pyqtSignal

class LoginScreen(QWidget):
    login_success = pyqtSignal()  # Signal to indicate successful login

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setFixedSize(1000, 700)
        self.initUI()
    
    def initUI(self):
        # Main layout
        layout = QVBoxLayout(self)

        # Username label and input
        self.username_label = QLabel("Username:")
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter your username")

        # Password label and input
        self.password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText("Enter your password")

        # Login button
        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.handle_login)

        # Add widgets to layout
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)

    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if username == "admin" and password == "password":  # Sample credentials
            QMessageBox.information(self, "Login Success", "Welcome back!")
            self.login_success.emit()  # Emit success signal
            self.close()  # Close login screen on success
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid credentials")
