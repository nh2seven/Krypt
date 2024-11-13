# main.py
import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon

# Unify all modules
from src.backend import app, user
from src.modules import encryption, login, pw_gen
from src.frontend import base, log_reg

# Get icon path
ICON_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "assets", "splash.png"))

class Application:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setWindowIcon(QIcon(ICON_PATH))
        self.app.setDesktopFileName("krypt")
        
        # Initialize windows
        self.login = None
        self.main_window = None
        
    def show_login(self):
        self.login = log_reg.LoginScreen()
        self.login.login_success.connect(self.show_main_window)
        self.login.show()
        
    def show_main_window(self):
        self.login.close()
        self.main_window = base.MainWindow()
        self.main_window.show()
        
    def run(self):
        self.show_login()
        return self.app.exec()

if __name__ == "__main__":
    app = Application()
    sys.exit(app.run())