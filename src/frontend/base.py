import sys
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QStackedWidget,
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, pyqtSignal

# Remove sidebar import
from .topbar import TopToolBar
from .cred import CredentialsView
from .settings import SettingsView
from .generator import PasswordGeneratorDialog


class MainWindow(QMainWindow):
    logout = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Krypt")
        self.setFixedSize(1000, 700)
        self.setWindowFlags(
            Qt.WindowType.Window |
            Qt.WindowType.CustomizeWindowHint |
            Qt.WindowType.WindowCloseButtonHint |
            Qt.WindowType.WindowMinimizeButtonHint
        )

        # Style
        self.setStyleSheet(
            """
            QMainWindow {
                background-color: #ffffff;
            }
            QLabel {
                color: #202020;
            }
            QStackedWidget {
                background-color: #ffffff;
            }
        """
        )

        self.last_active_tab = 0

        # Add top toolbar
        self.toolbar = TopToolBar(self)
        self.addToolBar(self.toolbar)

        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Connect toolbar signals
        self.toolbar.pageChanged.connect(self.handle_page_change)
        self.toolbar.logoutClicked.connect(self.handle_logout)

        # Create stacked widget for content
        self.stack = QStackedWidget()

        # Add pages
        self._setup_pages()

        # Connect toolbar signals
        self.toolbar.pageChanged.connect(self.stack.setCurrentIndex)
        self.toolbar.logoutClicked.connect(self.handle_logout)

        # Add widgets to main layout
        main_layout.addWidget(self.stack)

    def _setup_pages(self):
        """Setup all application pages"""
        # Passwords page (index 0)
        self.credentials_view = CredentialsView()
        self.stack.addWidget(self.credentials_view)
        
        # Settings page (index 1)
        self.settings_view = SettingsView()
        self.stack.addWidget(self.settings_view)

    def show_generator_dialog(self):
        """Show password generator dialog"""
        dialog = PasswordGeneratorDialog(self)
        dialog.exec()

    def handle_page_change(self, index):
        """Handle page change from toolbar"""
        if index == 1:
            self.show_generator_dialog()
            # Revert to last active tab
            self.toolbar.set_active_tab(self.last_active_tab)
        else:
            self.last_active_tab = index  # Update last active tab
            self.stack.setCurrentIndex(index)

    def handle_logout(self):
        """Clean up and return to login screen"""
        # Reset UI state
        self.credentials_view.clear_credentials()
        self.stack.setCurrentIndex(0)
        
        # Emit logout signal
        self.logout.emit()

    def refresh_credentials(self):
        """Refresh credentials list"""
        if hasattr(self, 'credentials_view'):
            self.credentials_view.load_credentials()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setDesktopFileName("Krypt")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
