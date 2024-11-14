import sys
import os
from PyQt6.QtWidgets import QApplication

# Unify all modules
from src.backend import app, user
from src.modules import auth, encryption, pw_gen
from src.frontend import base, login
import setup


# main.py
class Application:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setDesktopFileName("krypt")

        # Create single instances
        self.login = login.LoginScreen()
        self.main_window = base.MainWindow()

        # Connect signals
        self.login.login_success.connect(self.show_main_window)
        self.main_window.logout.connect(self.show_login)

    def show_login(self):
        self.main_window.hide()
        self.login.clear_fields()
        self.login.show()

    def show_main_window(self):
        self.login.hide()
        self.main_window.refresh_credentials()
        self.main_window.show()

    def run(self):
        self.show_login()
        return self.app.exec()


def Setup():
    if not os.path.exists("db"):
        setup.dirs()


if __name__ == "__main__":
    Setup()
    app = Application()
    sys.exit(app.run())
