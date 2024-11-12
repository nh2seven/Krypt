# Import necessary modules
import sys
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication

# Unify all modules
from src.backend import app, user
from src.modules import encryption, login, pw_gen
from src.frontend import base, log_reg, splash


def showMainWindow(login):
    login.close()
    mainWindow = base.Window()
    mainWindow.show()

def showLoginScreen(splash):
    splash.close()
    login = log_reg.LoginScreen()
    login.login_success.connect(lambda: showMainWindow(login))
    login.show()

def runApp():
    app = QApplication(sys.argv)
    
    spl = splash.Splash()
    spl.show()

    QTimer.singleShot(400, lambda: showLoginScreen(spl))
    
    sys.exit(app.exec())

if __name__ == "__main__":
    runApp()
