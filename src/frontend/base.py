# base.py
import sys
from qfluentwidgets import NavigationItemPosition, FluentWindow, SubtitleLabel, setFont
from qfluentwidgets import FluentIcon as FIF
from PyQt6.QtWidgets import QApplication, QFrame, QHBoxLayout
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
from .splash import Splash
from .cred import CredentialsView

class Widget(QFrame):
    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.label = SubtitleLabel(text, self)
        self.hBoxLayout = QHBoxLayout(self)

        setFont(self.label, 24)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.hBoxLayout.addWidget(self.label, 1, Qt.AlignmentFlag.AlignCenter)
        self.setObjectName(text.replace(" ", "-"))


class Window(FluentWindow):
    """Main Interface"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Krypt")
        self.setWindowIcon(QIcon("assets/splash.png"))
        self.resize(1000, 700)

        # Initialize interfaces with unique names
        self.homeInterface = Widget("Home Interface", self)
        self.musicInterface = Widget("Music Interface", self)
        self.videoInterface = Widget("Video Interface", self)
        self.settingInterface = Widget("Setting Interface", self)
        
        # Initialize credentials interface and set a unique object name
        self.credentialsView = Widget("Credentials View", self)
        self.credentialsView.setObjectName("CredentialsView")

        self.initNavigation()
        self.show()
    
    def initNavigation(self):
        self.addSubInterface(self.homeInterface, FIF.HOME, "Home")
        self.addSubInterface(self.musicInterface, FIF.MUSIC, "Music library")
        self.addSubInterface(self.videoInterface, FIF.VIDEO, "Video library")
        self.addSubInterface(self.credentialsView, FIF.LINK, "Credentials")
        self.addSubInterface(
            self.settingInterface,
            FIF.SETTING,
            "Settings",
            NavigationItemPosition.BOTTOM,
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    splash = Splash()  # Initialize and show splash screen
    splash.show()
    w = Window()
    w.show()
    app.exec()
