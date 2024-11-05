import sys

from qfluentwidgets import NavigationItemPosition, FluentWindow, SubtitleLabel, setFont
from qfluentwidgets import FluentIcon as FIF
from PyQt6.QtWidgets import QApplication, QFrame, QHBoxLayout
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt


# https://qfluentwidgets.com/pages/components/fluentwindow/
class Widget(QFrame):

    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.label = SubtitleLabel(text, self)
        self.hBoxLayout = QHBoxLayout(self)

        setFont(self.label, 24)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.hBoxLayout.addWidget(self.label, 1, Qt.AlignmentFlag.AlignCenter)

        # Must set a globally unique object name for the sub-interface
        self.setObjectName(text.replace(" ", "-"))


class Window(FluentWindow):
    """Main Interface"""

    def __init__(self):
        super().__init__()

        # Create sub-interfaces, when actually using, replace Widget with your own sub-interface
        self.homeInterface = Widget("Home Interface", self)
        self.musicInterface = Widget("Music Interface", self)
        self.videoInterface = Widget("Video Interface", self)
        self.settingInterface = Widget("Setting Interface", self)
        self.albumInterface = Widget("Album Interface", self)
        self.albumInterface1 = Widget("Album Interface 1", self)

        self.initNavigation()
        self.initWindow()

    def initNavigation(self):
        self.addSubInterface(self.homeInterface, FIF.HOME, "Home")
        self.addSubInterface(self.musicInterface, FIF.MUSIC, "Music library")
        self.addSubInterface(self.videoInterface, FIF.VIDEO, "Video library")
        self.addSubInterface(
            self.settingInterface,
            FIF.SETTING,
            "Settings",
            NavigationItemPosition.BOTTOM,
        )

    def initWindow(self):
        self.resize(1000, 700)
        self.setWindowIcon(QIcon("assets/splash.png"))
        self.setWindowTitle("Krypt")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    app.exec()
