# main.py
import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon

# Unify all modules
from src.backend import app, user
from src.modules import encryption, login, pw_gen
from src.frontend import base, log_reg

# main.py
class Application:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setDesktopFileName("krypt")
        
        # Create single instances
        self.login = log_reg.LoginScreen()
        self.main_window = base.MainWindow()
        
        # Connect signals
        self.login.login_success.connect(self.show_main_window)
        self.main_window.logout.connect(self.show_login)
        
    def show_login(self):
        self.main_window.hide()
        self.login.clear_fields()  # Add this method to LoginScreen
        self.login.show()
        
    def show_main_window(self):
        self.login.hide()
        self.main_window.show()
        
    def run(self):
        self.show_login()
        return self.app.exec()

if __name__ == "__main__":
    app = Application()
    sys.exit(app.run())