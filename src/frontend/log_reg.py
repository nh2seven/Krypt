# login_screen.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtCore import Qt

class LoginScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Login")
        
        layout = QVBoxLayout(self)
        
        # Username label and input
        self.username_label = QLabel("Username")
        self.username_input = QLineEdit()
        
        # Password label and input
        self.password_label = QLabel("Password")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

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

        if username == "admin" and password == "password":  # Example check
            QMessageBox.information(self, "Login Success", "Welcome back!")
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid credentials")
