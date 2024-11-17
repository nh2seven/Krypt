from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QSlider
from qfluentwidgets import PrimaryPushButton, TransparentPushButton, LineEdit, TitleLabel
from PyQt6.QtCore import Qt
from src.modules import pw_gen


class PasswordGeneratorDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Password Generator")
        self.setFixedWidth(400)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # Title
        title = TitleLabel("Password Generator")
        layout.addWidget(title)

        # Password display
        password_layout = QHBoxLayout()
        self.password_field = LineEdit()
        self.password_field.setText("Generated password will appear here")
        self.password_field.setReadOnly(True)
        self.password_field.setEchoMode(LineEdit.EchoMode.Password)

        self.toggle_btn = TransparentPushButton("Show")
        self.toggle_btn.clicked.connect(self.toggle_password_visibility)

        password_layout.addWidget(self.password_field)
        password_layout.addWidget(self.toggle_btn)
        layout.addLayout(password_layout)

        # Length slider
        length_layout = QHBoxLayout()
        length_label = QLabel("Length:")
        self.length_slider = QSlider(Qt.Orientation.Horizontal)
        self.length_slider.setMinimum(8)
        self.length_slider.setMaximum(32)
        self.length_slider.setValue(20)
        self.length_value = QLabel("20")
        self.length_slider.valueChanged.connect(
            lambda v: self.length_value.setText(str(v))
        )

        length_layout.addWidget(length_label)
        length_layout.addWidget(self.length_slider)
        length_layout.addWidget(self.length_value)
        layout.addLayout(length_layout)

        # Generate button
        generate_btn = PrimaryPushButton("Generate")
        generate_btn.clicked.connect(self.generate_password)
        layout.addWidget(generate_btn)

        layout.addStretch()

        # Done button
        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch()
        done_btn = PrimaryPushButton("Done")
        done_btn.clicked.connect(self.accept)
        bottom_layout.addWidget(done_btn)
        layout.addLayout(bottom_layout)

        self.setStyleSheet(
            """
            QDialog {
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
            }
            QLabel {
                color: #202020;
                font-size: 14px;
            }
            QSlider {
                height: 24px;
            }
            QSlider::groove:horizontal {
                height: 4px;
                background: #e0e0e0;
                margin: 0 10px;
            }
            QSlider::handle:horizontal {
                background: #0078d4;
                width: 16px;
                height: 16px;
                margin: -6px -8px;
                border-radius: 8px;
            }
        """
        )

    def toggle_password_visibility(self):
        if self.password_field.echoMode() == LineEdit.EchoMode.Password:
            self.password_field.setEchoMode(LineEdit.EchoMode.Normal)
            self.toggle_btn.setText("Hide")
        else:
            self.password_field.setEchoMode(LineEdit.EchoMode.Password)
            self.toggle_btn.setText("Show")

    def generate_password(self):
        length = self.length_slider.value()
        password = pw_gen.generate_strong_password(length)
        self.password_field.setText(password)
