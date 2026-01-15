from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QLineEdit, QPushButton, QMessageBox, QGroupBox,
                               QFormLayout, QComboBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from pydantic import ValidationError

from data_validation_auth import UserLogin, User
from services.auth_service import AuthService
from PySide6.QtCore import Signal



class LoginPage(QWidget):
    login_success = Signal(dict)   # emits user_data

    def __init__(self, auth_service: AuthService):
        super().__init__()
        self.auth_service = auth_service
        self.setup_ui()
        self.user_data = None

    def setup_ui(self):
        """Setup login page UI"""
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(50, 50, 50, 50)

        # Title
        title = QLabel("Patient Management System")
        title_font = QFont()
        title_font.setPointSize(24)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)

        subtitle = QLabel("Login")
        subtitle_font = QFont()
        subtitle_font.setPointSize(14)
        subtitle.setFont(subtitle_font)
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(subtitle)

        # Login Form Group
        form_group = QGroupBox("User Login")
        form_layout = QFormLayout()

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter your username")
        form_layout.addRow("Username:", self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        form_layout.addRow("Password:", self.password_input)

        form_group.setLayout(form_layout)
        main_layout.addWidget(form_group)

        # Buttons layout
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)

        login_btn = QPushButton("Login")
        login_btn.setMinimumHeight(40)
        login_btn.setMinimumWidth(100)
        login_btn.clicked.connect(self.login)
        buttons_layout.addWidget(login_btn)

        register_btn = QPushButton("Register New User")
        register_btn.setMinimumHeight(40)
        register_btn.setMinimumWidth(100)
        register_btn.clicked.connect(self.show_register_dialog)
        buttons_layout.addWidget(register_btn)

        main_layout.addLayout(buttons_layout)
        main_layout.addStretch()

        self.setLayout(main_layout)
        self.setWindowTitle("Patient Management System - Login")

    def login(self)->bool:
        """Handle login"""
        username = self.username_input.text().strip()
        password = self.password_input.text()

        if not username or not password:
            QMessageBox.warning(self, "Validation Error", "Username and password are required!")
            return False

        try:
            login_data = UserLogin(username=username, password=password)
        except ValidationError as e:
            QMessageBox.warning(self, "Validation Error", str(e))
            return False

        result = self.auth_service.login_user(login_data)

        if result['success']:
            self.user_data = {
                'user_id': result['user_id'],
                'username': result['username'],
                'role': result['role'],
                'email': result['email']
            }
            QMessageBox.information(self, "Success", result['message'])
            self.login_success.emit(self.user_data)
            self.close()

        else:
            QMessageBox.warning(self, "Login Failed", result['message'])
            return False
        
    def show_register_dialog(self):
        """Show registration dialog"""
        dialog = RegisterDialog(self.auth_service)
        if dialog.exec():
            QMessageBox.information(self, "Success", "User registered successfully! Please login.")


class RegisterDialog(QWidget):
    def __init__(self, auth_service: AuthService):
        super().__init__()
        self.auth_service = auth_service
        self.dialog_accepted = False
        self.setup_ui()

    def setup_ui(self):
        """Setup registration dialog UI"""
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)

        title = QLabel("Register New User")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)

        # Form
        form_layout = QFormLayout()

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Min 3 characters")
        form_layout.addRow("Username:", self.username_input)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Valid email address")
        form_layout.addRow("Email:", self.email_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Min 6 characters")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        form_layout.addRow("Password:", self.password_input)

        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setPlaceholderText("Confirm password")
        self.confirm_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        form_layout.addRow("Confirm Password:", self.confirm_password_input)

        self.role_combo = QComboBox()
        self.role_combo.addItems(['staff', 'doctor', 'admin'])
        form_layout.addRow("Role:", self.role_combo)

        main_layout.addLayout(form_layout)

        # Buttons
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)

        register_btn = QPushButton("Register")
        register_btn.setMinimumHeight(35)
        register_btn.clicked.connect(self.register)
        buttons_layout.addWidget(register_btn)

        cancel_btn = QPushButton("Cancel")
        cancel_btn.setMinimumHeight(35)
        cancel_btn.clicked.connect(self.close)
        buttons_layout.addWidget(cancel_btn)

        main_layout.addLayout(buttons_layout)

        self.setLayout(main_layout)
        self.setWindowTitle("Register New User")
        self.setMinimumWidth(400)

    def register(self):
        """Handle user registration"""
        username = self.username_input.text().strip()
        email = self.email_input.text().strip()
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()
        role = self.role_combo.currentText()

        # Validate inputs
        if not all([username, email, password, confirm_password]):
            QMessageBox.warning(self, "Validation Error", "All fields are required!")
            return

        if password != confirm_password:
            QMessageBox.warning(self, "Validation Error", "Passwords do not match!")
            return

        try:
            user = User(username=username, email=email, password=password, role=role)
        except ValidationError as e:
            QMessageBox.warning(self, "Validation Error", str(e))
            return

        result = self.auth_service.register_user(user)

        if result['success']:
            self.dialog_accepted = True
            self.close()
        else:
            QMessageBox.warning(self, "Registration Failed", result['message'])

    def exec(self):
        """Show dialog and return if registration was successful"""
        self.show()
        from PySide6.QtWidgets import QApplication
        while self.isVisible():
            QApplication.processEvents()
        return self.dialog_accepted

    def closeEvent(self, event):
        """Handle close event"""
        super().closeEvent(event)
