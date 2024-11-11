import sys

from qfluentwidgets import SplashScreen
from qframelesswindow import FramelessWindow, StandardTitleBar
from PyQt6.QtCore import QEventLoop, QTimer, QSize
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication


class Splash(FramelessWindow):
    def __init__(self):
        super().__init__()
        self.resize(1000, 700)
        self.setWindowTitle("Krypt")
        self.setWindowIcon(QIcon("assets/splash.png"))

        # 1. Create a splash screen
        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.splashScreen.setIconSize(QSize(102, 102))

        titleBar = StandardTitleBar(self.splashScreen)
        titleBar.setIcon(self.windowIcon())
        titleBar.setTitle(self.windowTitle())
        self.splashScreen.setTitleBar(titleBar)

        # 2. Show the main interface before creating other sub-interfaces
        self.show()

        # 3. Create sub-interfaces
        self.createSubInterface()

        # 4. Hide the splash screen
        self.splashScreen.finish()

    def createSubInterface(self):
        loop = QEventLoop(self)
        QTimer.singleShot(3000, loop.quit)  # 3 seconds to load other stuff
        loop.exec()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Splash()
    w.show()
    app.exec()
