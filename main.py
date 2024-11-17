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
        self.main_window = None
        self.login.login_success.connect(self.show_main_window)

    def show_login(self):
        if self.main_window:
            self.main_window.hide()
        self.login.clear_fields()
        self.login.show()

    def show_main_window(self):
        if not self.main_window:
            db_path = self.login.user_auth.db
            username = self.login.current_user
            self.main_window = base.MainWindow(db_path, username)
            self.main_window.logout.connect(self.show_login)

        self.login.hide()
        self.main_window.refresh_credentials()
        self.main_window.show()

    def run(self):
        self.show_login()
        return self.app.exec()


if __name__ == "__main__":
    app = Application()
    sys.exit(app.run())
