# base.py
import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, 
                           QVBoxLayout, QHBoxLayout,
                           QStackedWidget, QLabel)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt

from .sidebar import Sidebar
from .topbar import TopToolBar

# Get absolute path to icon
ICON_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "assets", "splash.png"))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Krypt")
        self.setWindowIcon(QIcon(ICON_PATH))
        self.resize(1000, 700)

        # Style
        self.setStyleSheet("""
            QMainWindow {
                background-color: #ffffff;
            }
            QLabel {
                color: #202020;
            }
            QStackedWidget {
                background-color: #ffffff;
            }
        """)

        # Add top toolbar
        self.toolbar = TopToolBar(self)
        self.addToolBar(self.toolbar)
        
        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create sidebar
        self.sidebar = Sidebar()
        
        # Create stacked widget for content
        self.stack = QStackedWidget()
        
        # Add pages
        self._setup_pages()
        
        # Connect sidebar signals
        self.sidebar.pageChanged.connect(self.stack.setCurrentIndex)
        
        # Add widgets to main layout
        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.stack)
    
    def _setup_pages(self):
        """Setup all application pages"""
        # Home page
        home_page = QWidget()
        home_layout = QVBoxLayout(home_page)
        home_layout.addWidget(QLabel("Home Interface"))
        self.stack.addWidget(home_page)
        
        # Passwords page
        passwords_page = QWidget()
        passwords_layout = QVBoxLayout(passwords_page)
        passwords_layout.addWidget(QLabel("Password Manager"))
        self.stack.addWidget(passwords_page)
        
        # Generator page
        generator_page = QWidget()
        generator_layout = QVBoxLayout(generator_page)
        generator_layout.addWidget(QLabel("Password Generator"))
        self.stack.addWidget(generator_page)
        
        # Settings page
        settings_page = QWidget()
        settings_layout = QVBoxLayout(settings_page)
        settings_layout.addWidget(QLabel("Settings"))
        self.stack.addWidget(settings_page)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(ICON_PATH))  # Set app-wide icon
    app.setDesktopFileName("Krypt")  # Match with .desktop file name
    window = MainWindow()
    window.show()
    sys.exit(app.exec())