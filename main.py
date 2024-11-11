# Import necessary modules
import sys
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication
from src.frontend.splash import Splash  # Import Splash class
from src.frontend.base import Window  # Import the main application window

# Unify all modules
from src.backend import app, user
from src.modules import encryption, login, pw_gen
from src.frontend import base, cred, log_reg, sidebar
from PyQt6.QtWidgets import QApplication

def runApp():
    app = QApplication(sys.argv)

    splash = Splash()
    splash.show()

    QTimer.singleShot(400, lambda: showMainWindow(splash))
    sys.exit(app.exec())

def showMainWindow(splash):
    splash.close()  # Close the splash screen
    mainWindow = Window()  # Initialize the main window
    mainWindow.show()  # Show the main application window

if __name__ == "__main__":
    runApp()
