# credentials_view.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QDialog,
    QHBoxLayout, QLineEdit, QLabel, QGridLayout
)
from PyQt6.QtCore import Qt

class CredentialsView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Credentials Manager")

        # Main layout for the credentials view
        layout = QVBoxLayout(self)
        
        # Create the table to display credentials
        self.credentials_table = QTableWidget(0, 4)  # Assuming columns: Title, Username, URL, Actions
        self.credentials_table.setHorizontalHeaderLabels(["Title", "Username", "URL", "Actions"])
        self.credentials_table.horizontalHeader().setStretchLastSection(True)
        
        # Load credentials initially
        self.load_credentials()

        # Button for adding a new credential
        self.add_button = QPushButton("Add Credential")
        self.add_button.clicked.connect(self.show_add_credential_dialog)
        
        layout.addWidget(self.credentials_table)
        layout.addWidget(self.add_button)

    def load_credentials(self):
        # Simulated data - Replace with actual database call
        credentials_data = [
            ("Email", "user@example.com", "https://example.com"),
            ("Social Media", "user123", "https://social.com"),
            ("Work", "employee@company.com", "https://company.com")
        ]

        self.credentials_table.setRowCount(len(credentials_data))
        for row, (title, username, url) in enumerate(credentials_data):
            self.credentials_table.setItem(row, 0, QTableWidgetItem(title))
            self.credentials_table.setItem(row, 1, QTableWidgetItem(username))
            self.credentials_table.setItem(row, 2, QTableWidgetItem(url))

            # Edit button
            edit_button = QPushButton("Edit")
            edit_button.clicked.connect(lambda _, r=row: self.show_edit_credential_dialog(r))
            self.credentials_table.setCellWidget(row, 3, edit_button)

    def show_add_credential_dialog(self):
        dialog = CredentialDialog(self)
        if dialog.exec():
            title, username, password, url, notes = dialog.get_data()
            print(f"Added: {title}, {username}, {password}, {url}, {notes}")  # Replace with DB insertion

    def show_edit_credential_dialog(self, row):
        title = self.credentials_table.item(row, 0).text()
        username = self.credentials_table.item(row, 1).text()
        url = self.credentials_table.item(row, 2).text()

        dialog = CredentialDialog(self, title, username, url)
        if dialog.exec():
            title, username, password, url, notes = dialog.get_data()
            print(f"Updated: {title}, {username}, {password}, {url}, {notes}")  # Replace with DB update


class CredentialDialog(QDialog):
    def __init__(self, parent=None, title="", username="", url=""):
        super().__init__(parent)
        self.setWindowTitle("Edit Credential" if title else "Add Credential")

        layout = QGridLayout(self)
        
        # Title input
        self.title_label = QLabel("Title:")
        self.title_input = QLineEdit(title)
        
        # Username input
        self.username_label = QLabel("Username:")
        self.username_input = QLineEdit(username)
        
        # Password input
        self.password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        # URL input
        self.url_label = QLabel("URL:")
        self.url_input = QLineEdit(url)

        # Notes input
        self.notes_label = QLabel("Notes:")
        self.notes_input = QLineEdit()

        # Save button
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.accept)

        # Add widgets to layout
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
            self.notes_input.text()
        )
