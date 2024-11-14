# audit.py
from PyQt6.QtWidgets import (
    QGridLayout,
    QVBoxLayout,
    QLabel,
    QWidget,
    QFrame
)
from qfluentwidgets import TitleLabel, CardWidget, PushButton
from PyQt6.QtCore import Qt, QPoint

class LogDetailPopup(QFrame):
    def __init__(self, details, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.Popup)
        self.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 4px;
                padding: 12px;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel(details))

class AuditLogButton(PushButton):
    def __init__(self, log_id, time, action, details, parent=None):
        super().__init__(parent)
        self.log_id = log_id
        self.time = time
        self.action = action
        self.details = details
        self.popup = None
        self.popup_visible = False
        
        self.setText(f"{time} - {action} (ID: {log_id})")
        self.clicked.connect(self.toggle_popup)
        
        self.setStyleSheet("""
            PushButton {
                text-align: left;
                padding: 8px 20px;
                border: none;
                border-radius: 4px;
                margin: 2px 8px;
                background-color: transparent;
                font-size: 14px;
            }
            PushButton:hover {
                background-color: #f0f0f0;
            }
            PushButton:pressed {
                background-color: #e0e0e0;
            }
        """)

    def toggle_popup(self):
        if self.popup_visible:
            self.popup.hide()
            self.popup_visible = False
        else:
            if not self.popup:
                self.popup = LogDetailPopup(self.details, self)
            
            # Position popup below button
            pos = self.mapToGlobal(QPoint(0, self.height()))
            self.popup.move(pos)
            self.popup.show()
            self.popup_visible = True

# audit.py
class AuditLogCard(CardWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(600)
        self.setup_ui()

        self.setStyleSheet("""
            AuditLogCard {
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
            }
        """)

    def setup_ui(self):
        layout = QGridLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        # Title with proper spacing
        title = TitleLabel("Audit Log")
        layout.addWidget(title, 0, 0, 1, 2)

        # Container for log buttons in next row
        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setSpacing(2)
        container_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        container_layout.setContentsMargins(0, 0, 0, 0)

        for log_id, time, action, details in self.load_placeholder_data():
            log_btn = AuditLogButton(log_id, time, action, details)
            container_layout.addWidget(log_btn)

        layout.addWidget(container, 1, 0, 1, 2)

    def load_placeholder_data(self):
        return [
            (1, "2024-03-20 10:00", "Login", "Successful login from 192.168.1.100"),
            (2, "2024-03-20 09:45", "Password Change", "Password updated for user admin"),
            (3, "2024-03-19 16:30", "Logout", "User logged out normally"),
            (4, "2024-03-19 14:20", "Login", "Successful login from 192.168.1.101"),
            (5, "2024-03-19 11:00", "Failed Login", "Invalid credentials attempt from 192.168.1.102"),
        ]