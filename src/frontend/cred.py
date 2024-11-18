from PyQt6.QtWidgets import QWidget, QVBoxLayout, QDialog, QHBoxLayout, QLabel, QGridLayout, QFrame, QStackedWidget, QToolButton, QScrollArea, QMessageBox, QComboBox
from qfluentwidgets import PushButton, LineEdit, SubtitleLabel, TransparentPushButton
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon

from .sidebar import GroupSidebar
from src.backend.user import Credentials
from src.modules.contextmanager import db_connect


class CredentialButton(PushButton):
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.setText(title)
        self.setCheckable(True)
        self.setStyleSheet(
            """
            PushButton {
                text-align: left;
                padding: 8px 20px;
                border: none;
                border-radius: 4px;
                margin: 2px 8px;
                background-color: transparent;
                font-size: 14px;
                color: #000000;
            }
            PushButton:checked {
                background-color: #e6e6e6;
                color: #0078d4;
            }
            PushButton:hover {
                background-color: #f0f0f0;
            }
        """
        )


class DetailSidebar(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(350)
        self.setStyleSheet(
            """
            QFrame {
                background-color: #f5f5f5;
                border-left: 1px solid #e0e0e0;
            }
            QLabel {
                color: #202020;
                font-size: 14px;
            }
            .field-label {
                color: #666666;
                font-size: 14px;
                margin-bottom: 4px;
            }
            .field-value {
                color: #202020;
                font-size: 14px;
                padding: 8px 12px;
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 4px;
            }
            SubtitleLabel {
                font-size: 24px;
                font-weight: 700;
                color: #000000;
                margin-bottom: 20px;
            }
        """
        )

        # Create main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        # Create title
        self.detail_title = SubtitleLabel("")
        self.detail_title.setObjectName("detail_title")
        layout.addWidget(self.detail_title)

        # Create stack for switching between placeholder and details
        self.stack = QStackedWidget()

        # Create placeholder widget
        placeholder_widget = QWidget()
        placeholder_layout = QVBoxLayout(placeholder_widget)
        self.placeholder = QLabel("Select a credential to view details")
        self.placeholder.setStyleSheet("color: #666666; font-size: 14px;")
        self.placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        placeholder_layout.addStretch()
        placeholder_layout.addWidget(self.placeholder)
        placeholder_layout.addStretch()

        # Create details widget
        details_widget = QWidget()
        details_layout = QVBoxLayout(details_widget)

        # Create scroll area for content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setStyleSheet(
            """
            QScrollArea {
                border: none;
                background-color: #f5f5f5;
            }
            QWidget#scrollContent {
                background-color: #f5f5f5;
            }
        """
        )

        # Create content widget for scroll area
        content = QWidget()
        content.setObjectName("scrollContent")
        self.content_layout = QVBoxLayout(content)
        self.content_layout.setSpacing(10)
        scroll.setWidget(content)

        # Add scroll to details layout
        details_layout.addWidget(scroll)

        # Username section
        self.username_label = QLabel("Username")
        self.username_value = QLabel()
        self.username_value.setWordWrap(True)
        self.username_value.setProperty("class", "field-value")
        self.content_layout.addWidget(self.username_label)
        self.content_layout.addWidget(self.username_value)

        # Password section
        self.password_label = QLabel("Password")
        self.password_container = QWidget()
        password_layout = QHBoxLayout(self.password_container)
        password_layout.setContentsMargins(0, 0, 0, 0)
        self.password_value = QLabel()
        self.password_value.setWordWrap(True)
        self.password_value.setProperty("class", "field-value")
        self.toggle_password_btn = TransparentPushButton("Show")
        self.toggle_password_btn.setMaximumWidth(60)
        self.toggle_password_btn.clicked.connect(self.toggle_password_visibility)
        password_layout.addWidget(self.password_value)
        password_layout.addWidget(self.toggle_password_btn)
        self.content_layout.addWidget(self.password_label)
        self.content_layout.addWidget(self.password_container)

        # URL section
        self.url_label = QLabel("URL")
        self.url_value = QLabel()
        self.url_value.setWordWrap(True)
        self.url_value.setProperty("class", "field-value")
        self.content_layout.addWidget(self.url_label)
        self.content_layout.addWidget(self.url_value)

        # Notes section
        self.notes_label = QLabel("Notes")
        self.notes_value = QLabel()
        self.notes_value.setWordWrap(True)
        self.notes_value.setProperty("class", "field-value")
        self.content_layout.addWidget(self.notes_label)
        self.content_layout.addWidget(self.notes_value)

        # Add stretch to push content up
        self.content_layout.addStretch()

        # Add edit button at bottom
        self.edit_btn = PushButton("Edit")
        details_layout.addWidget(self.edit_btn)

        # Add widgets to stack
        self.stack.addWidget(placeholder_widget)
        self.stack.addWidget(details_widget)

        # Add stack to main layout
        layout.addWidget(self.stack)

        # Initialize password toggle state
        self._password = ""
        self._password_hidden = True

    def update_details(self, title, username, password, url="", notes=""):
        """Update sidebar with credential details"""
        self.detail_title.setText(title)
        self.username_value.setText(username)
        self._password = password
        self.password_value.setText("•" * len(password))
        self.url_value.setText(url)
        self.notes_value.setText(notes)
        self.stack.setCurrentIndex(1)
        self._password_hidden = True
        self.toggle_password_btn.setText("Show")

    def toggle_password_visibility(self):
        """Toggle password visibility"""
        if self._password_hidden:
            self.password_value.setText(self._password)
            self.toggle_password_btn.setText("Hide")
        else:
            self.password_value.setText("•" * len(self._password))
            self.toggle_password_btn.setText("Show")
        self._password_hidden = not self._password_hidden

    def show_placeholder(self):
        """Show placeholder when no credential selected"""
        self.stack.setCurrentIndex(0)


class CredentialDialog(QDialog):
    def __init__(self, parent=None, title="", username="", url="", db_path=None):
        super().__init__(parent)
        self.db_path = db_path
        self.setWindowTitle("Edit Credential" if title else "Add Credential")
        self.setFixedWidth(400)
        self.setStyleSheet(
            """
            QDialog {
                background-color: white;
            }
            QLabel {
                color: #202020;
                font-size: 14px;
            }
            LineEdit {
                padding: 8px 12px;
                border: 1px solid #e0e0e0;
                border-radius: 4px;
                background-color: white;
                font-size: 14px;
                color: #202020;
            }
            LineEdit:focus {
                border: 1px solid #0078d4;
            }
            PushButton {
                padding: 8px 16px;
                border: none;
                border-radius: 4px;
                background-color: #0078d4;
                color: white;
                font-size: 14px;
            }
            PushButton:hover {
                background-color: #106ebe;
            }
            PushButton:pressed {
                background-color: #005a9e;
            }
        """
        )

        layout = QGridLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        # Create fields with consistent styling
        self.title_label = QLabel("Title:")
        self.title_input = LineEdit(self)
        self.title_input.setText(title)

        self.username_label = QLabel("Username:")
        self.username_input = LineEdit(self)
        self.username_input.setText(username)

        self.password_label = QLabel("Password:")
        self.password_input = LineEdit(self)
        self.password_input.setEchoMode(LineEdit.EchoMode.Password)

        self.url_label = QLabel("URL:")
        self.url_input = LineEdit(self)
        self.url_input.setText(url)

        self.notes_label = QLabel("Notes:")
        self.notes_input = LineEdit(self)

        # Add group selection
        self.group_label = QLabel("Group:")
        self.group_combo = QComboBox(self)
        self.load_groups()

        self.save_button = PushButton("Save")
        self.save_button.clicked.connect(self.accept)

        # Layout fields
        layout.addWidget(self.title_label, 0, 0)
        layout.addWidget(self.title_input, 0, 1)
        layout.addWidget(self.username_label, 1, 0)
        layout.addWidget(self.username_input, 1, 1)
        layout.addWidget(self.password_label, 2, 0)
        layout.addWidget(self.password_input, 2, 1)
        layout.addWidget(self.url_label, 3, 0)
        layout.addWidget(self.url_input, 3, 1)
        layout.addWidget(self.notes_label, 4, 0)
        layout.addWidget(self.notes_input, 4, 1)
        layout.addWidget(self.group_label, 5, 0)
        layout.addWidget(self.group_combo, 5, 1)
        layout.addWidget(self.save_button, 6, 0, 1, 2)

    def load_groups(self):
        """Load groups into combo box"""
        self.group_combo.addItem("No Group", -1)
        if self.db_path:
            with db_connect(self.db_path) as cur:
                cur.execute("SELECT group_id, title FROM groups")
                groups = cur.fetchall()
                for group_id, title in groups:
                    self.group_combo.addItem(title, group_id)

    def get_data(self):
        return (
            self.title_input.text(),
            self.username_input.text(),
            self.password_input.text(),
            self.url_input.text(),
            self.notes_input.text(),
            self.group_combo.currentData()
        )


class CredentialsToolBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(
            """
            QWidget {
                background-color: #f8f8f8;
                border-bottom: 1px solid #e0e0e0;
            }
            QToolButton {
                border: none;
                border-radius: 4px;
                padding: 6px;
                background-color: transparent;
            }
            QToolButton:hover {
                background-color: #e8e8e8;
            }
            QToolButton:pressed {
                background-color: #e0e0e0;
            }
        """
        )

        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 4, 8, 4)
        layout.setSpacing(4)

        # Create buttons
        self.add_btn = self._create_tool_button("Add Entry", "assets/add.svg")
        self.edit_btn = self._create_tool_button("Edit Entry", "assets/edit.svg")
        self.delete_btn = self._create_tool_button("Delete Entry", "assets/delete.svg")

        # Add buttons to layout
        layout.addWidget(self.add_btn)
        layout.addWidget(self.edit_btn)
        layout.addWidget(self.delete_btn)
        layout.addStretch()

    def _create_tool_button(self, tooltip, icon_path):
        button = QToolButton()
        button.setIcon(QIcon(icon_path))
        button.setToolTip(tooltip)
        button.setIconSize(QSize(20, 20))
        return button


class CredentialsView(QWidget):
    def __init__(self, parent=None, db_path=None):
        super().__init__(parent)
        self.db_path = db_path
        self.cred_manager = Credentials(db_path) if db_path else None
        self.current_button = None

        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Content area
        content = QWidget()
        content_layout = QHBoxLayout(content)
        content_layout.setContentsMargins(0, 0, 0, 0)

        # Create DetailSidebar first
        self.detail_sidebar = DetailSidebar()

        # Group sidebar
        self.group_sidebar = GroupSidebar(db_path=db_path)
        self.group_sidebar.groupSelected.connect(self.filter_credentials)
        content_layout.addWidget(self.group_sidebar)

        # Credential list area
        cred_area = QWidget()
        cred_layout = QVBoxLayout(cred_area)
        cred_layout.setContentsMargins(5, 5, 5, 5)
        cred_layout.setSpacing(10)
        cred_area.setStyleSheet(
            """
            QWidget {
                background-color: white;
            }
            """
        )

        # Action buttons toolbar
        buttons_widget = QWidget()
        buttons_widget.setStyleSheet(
            """
            QWidget {
                border-bottom: 1px solid #e0e0e0;
            }
            """
        )
        buttons_layout = QHBoxLayout(buttons_widget)
        buttons_layout.setContentsMargins(10, 10, 10, 10)
        buttons_layout.setSpacing(4)

        # Create buttons
        self.add_btn = self._create_tool_button("Add Entry", "assets/add.svg")
        self.delete_btn = self._create_tool_button("Delete Entry", "assets/delete.svg")

        # Add buttons to layout
        buttons_layout.addWidget(self.add_btn)
        buttons_layout.addWidget(self.delete_btn)
        buttons_layout.addStretch()

        # Connect button signals
        self.add_btn.clicked.connect(self.add_credential)
        self.delete_btn.clicked.connect(self.delete_credential)
        self.detail_sidebar.edit_btn.clicked.connect(self.edit_credential)

        cred_layout.addWidget(buttons_widget, 0, Qt.AlignmentFlag.AlignTop)

        # Scrollable credentials list
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setStyleSheet(
            """
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QWidget {
                background-color: white;
            }
        """
        )

        # Container for credentials
        self.list_container = QWidget()
        self.cred_list = QVBoxLayout(self.list_container)
        self.cred_list.setSpacing(2)
        self.cred_list.setAlignment(Qt.AlignmentFlag.AlignTop)

        scroll.setWidget(self.list_container)
        cred_layout.addWidget(scroll)

        content_layout.addWidget(cred_area)
        content_layout.addWidget(self.detail_sidebar)

        layout.addWidget(content)
        self.load_credentials()

    def _create_tool_button(self, tooltip, icon_path):
        button = QToolButton()
        button.setIcon(QIcon(icon_path))
        button.setToolTip(tooltip)
        button.setIconSize(QSize(20, 20))
        button.setStyleSheet(
            """
            QToolButton {
                border: none;
                border-radius: 4px;
                padding: 6px;
                background-color: transparent;
            }
            QToolButton:hover {
                background-color: #e8e8e8;
            }
            QToolButton:pressed {
                background-color: #e0e0e0;
            }
        """
        )
        return button

    def load_credentials(self, group_id=None):
        """Load and display credentials from database"""
        self.clear_credentials()

        if not self.cred_manager:
            return

        with db_connect(self.db_path) as cur:
            if group_id is None or group_id == -1:
                query = """SELECT title, username, password, url, notes 
                          FROM credentials"""
                params = ()
            else:
                query = """SELECT title, username, password, url, notes 
                          FROM credentials WHERE group_id = ?"""
                params = (group_id,)
                
            cur.execute(query, params)
            credentials = cur.fetchall()

        for cred in credentials:
            title, username, password, url, notes = cred
            cred_btn = CredentialButton(title)
            cred_btn.clicked.connect(
                lambda checked, btn=cred_btn, t=title, u=username, p=password, l=url, n=notes: 
                self._handle_credential_click(btn, t, u, p, l, n)
            )
            self.cred_list.addWidget(cred_btn)

    def _handle_credential_click(self, button, title, username, password, url, notes):
        """Handle credential button click"""
        if self.current_button == button and button.isChecked():
            button.setChecked(False)
            self.current_button = None
            self.detail_sidebar.show_placeholder()
            return

        if self.current_button:
            self.current_button.setChecked(False)

        self.current_button = button
        button.setChecked(True)
        self.detail_sidebar.update_details(title, username, password, url, notes)

    def clear_credentials(self):
        """Clear all credentials from view"""
        while self.cred_list.count():
            item = self.cred_list.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        self.current_button = None
        self.detail_sidebar.show_placeholder()

    def filter_credentials(self, group_id):
        """Filter credentials by group"""
        self.load_credentials(group_id)

    def add_credential(self):
        """Add new credential"""
        dialog = CredentialDialog(self, db_path=self.db_path)
        if dialog.exec():
            title, username, password, url, notes, group_id = dialog.get_data()

            try:
                self.cred_manager.add_cred(
                    title=title,
                    username=username,
                    password=password,
                    url=url,
                    notes=notes,
                    tags="",
                    expiration="",
                    group_id=group_id if group_id != -1 else None
                )
                self.load_credentials()
            except Exception as e:
                QMessageBox.critical(
                    self, "Error", f"Failed to add credential: {str(e)}"
                )

    def delete_credential(self):
        """Delete selected credential"""
        if not self.current_button:
            return

        title = self.current_button.text()
        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            f"Are you sure you want to delete credential '{title}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )

        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.cred_manager.remove_cred(title)
                self.load_credentials()
            except Exception as e:
                QMessageBox.critical(
                    self, "Error", f"Failed to delete credential: {str(e)}"
                )

    def edit_credential(self):
        """Edit selected credential"""
        if not self.current_button:
            return

        title = self.current_button.text()
        with db_connect(self.db_path) as cur:
            cur.execute(
                """SELECT title, username, password, url, notes, group_id 
                   FROM credentials WHERE title = ?""",
                (title,)
            )
            cred = cur.fetchone()
        if not cred:
            return

        title, username, password, url, notes, group_id = cred
        dialog = CredentialDialog(self, title, username, url, self.db_path)
        dialog.password_input.setText(password)
        dialog.notes_input.setText(notes)
        if group_id:
            index = dialog.group_combo.findData(group_id)
            if index >= 0:
                dialog.group_combo.setCurrentIndex(index)

        if dialog.exec():
            new_title, new_username, new_password, new_url, new_notes, new_group_id = (
                dialog.get_data()
            )
            try:
                self.cred_manager.modify_cred(
                    new_title=new_title,
                    username=new_username,
                    password=new_password if new_password else password,
                    url=new_url,
                    notes=new_notes,
                    tags="",
                    expiration="",
                    group_id=new_group_id if new_group_id != -1 else None,
                    title=title,
                )
                if new_title != title:
                    self.current_button.setText(new_title)
                self.load_credentials()
            except Exception as e:
                QMessageBox.critical(
                    self, "Error", f"Failed to update credential: {str(e)}"
                )