# base.py
import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, 
                           QVBoxLayout, QHBoxLayout,
                           QStackedWidget, QLabel)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, pyqtSignal

from .sidebar import Sidebar
from .topbar import TopToolBar
from .cred import CredentialsView


class MainWindow(QMainWindow):
    logout = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Krypt")
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

        # Connect logout signal
        self.sidebar.logoutClicked.connect(self.handle_logout)

    def refresh_credentials(self):
        """Refresh credentials list"""
        if hasattr(self, 'credentials_view'):
            self.credentials_view.load_credentials()

    def _setup_pages(self):
        """Setup all application pages"""
        # Home page
        home_page = QWidget()
        home_layout = QVBoxLayout(home_page)
        home_layout.addWidget(QLabel("Home Interface"))
        self.stack.addWidget(home_page)
        
        # Passwords page
        self.credentials_view = CredentialsView()
        self.stack.addWidget(self.credentials_view)
        
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

    def handle_logout(self):
        """Clean up and return to login screen"""
        # Reset sensitive UI elements
        self.credentials_view.clear_credentials()
        self.stack.setCurrentIndex(0)
        self.sidebar.set_active_page(0)
        
        # Emit logout signal
        self.logout.emit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setDesktopFileName("Krypt")  # Match with .desktop file name
    window = MainWindow()
    window.show()
    sys.exit(app.exec())