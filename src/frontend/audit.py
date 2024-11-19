from PyQt6.QtWidgets import (
    QGridLayout, 
    QVBoxLayout,
    QLabel,
    QWidget,
    QFrame,
    QScrollArea
)
from qfluentwidgets import TitleLabel, CardWidget, PushButton, TransparentPushButton
from PyQt6.QtCore import Qt, QPoint
from src.modules.contextmanager import db_connect

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

class AuditLogButton(TransparentPushButton):
    def __init__(self, log_id, time, action_type, details, parent=None):
        super().__init__(parent)
        self.log_id = log_id
        self.time = time 
        self.action_type = action_type
        self.details = details
        self.popup = None
        self.popup_visible = False
        
        self.setText(f"{time} - {action_type}")
        self.clicked.connect(self.toggle_popup)
        
        self.setStyleSheet("""
            TransparentPushButton {
                text-align: left;
                padding: 8px 16px;
                border: none;
                border-radius: 4px;
                margin: 2px 8px;
                background-color: transparent;
                color: #202020;
                font-size: 14px;
            }
            TransparentPushButton:hover {
                background-color: #f0f0f0;
            }
            TransparentPushButton:pressed {
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
            pos = self.mapToGlobal(QPoint(0, self.height()))
            self.popup.move(pos)
            self.popup.show()
            self.popup_visible = True

class AuditLogCard(CardWidget):
    def __init__(self, db_path, parent=None):
        super().__init__(parent)
        self.db_path = db_path
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
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        title = TitleLabel("Audit Log")
        layout.addWidget(title)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea { 
                border: none; 
                background-color: white;
            }
            QWidget#container {
                background-color: white;
            }
        """)

        self.container = QWidget()
        self.container.setObjectName("container")
        self.container_layout = QVBoxLayout(self.container)
        self.container_layout.setSpacing(2)
        self.container_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.container_layout.setContentsMargins(0, 0, 0, 0)

        self.refresh_logs()
        scroll.setWidget(self.container)
        layout.addWidget(scroll)

    def load_audit_logs(self):
        try:
            with db_connect(self.db_path) as cur:
                query = """
                SELECT log_id, action_type, action_time, details 
                FROM auditlog 
                ORDER BY action_time DESC 
                LIMIT 50
                """
                cur.execute(query)
                return cur.fetchall()
        except Exception as e:
            print(f"Error loading audit logs: {e}")
            return []

    def refresh_logs(self):
        """Refresh the audit log display"""
        while self.container_layout.count():
            item = self.container_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            
        for log in self.load_audit_logs():
            log_btn = AuditLogButton(
                log[0],  # log_id
                log[2],  # action_time
                log[1],  # action_type
                log[3]   # details
            )
            self.container_layout.addWidget(log_btn)