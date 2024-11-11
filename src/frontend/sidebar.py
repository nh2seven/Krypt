# sidebar.py
from PyQt6.QtWidgets import QFrame, QVBoxLayout
from qfluentwidgets import NavigationWidget, NavigationItemPosition, FluentIcon as FIF

class Sidebar(NavigationWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Define navigation items
        self.addItem("Home", FIF.HOME, position=NavigationItemPosition.TOP)
        self.addItem("Passwords", FIF.LOCK, position=NavigationItemPosition.TOP)
        self.addItem("Groups", FIF.GROUP, position=NavigationItemPosition.TOP)
        self.addItem("Settings", FIF.SETTING, position=NavigationItemPosition.BOTTOM)
        
        # Connect the items to methods or signals
        self.itemClicked.connect(self.handle_navigation_click)

    def handle_navigation_click(self, item):
        print(f"Navigation item clicked: {item.text()}")
