# Import necessary modules
import sys

# Unify all modules
from src.backend import app, user
from src.modules import encryption, login, pw_gen
from src.frontend import base, cred, log_reg, sidebar, view
from PyQt6.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = base.Window()
    window.show()
    app.exec()
