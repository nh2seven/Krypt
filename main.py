import sys
from PyQt6.QtWidgets import QApplication
from src.frontend import base, login
import setup


class Application:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setDesktopFileName("krypt")

        setup.dirs()

        self.login = login.LoginScreen()
        self.main_window = base.MainWindow()
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


if __name__ == "__main__":
    app = Application()
    sys.exit(app.run())
