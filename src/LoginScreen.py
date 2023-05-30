from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox

from PyQt6.QtCore import pyqtSignal
from ldap import LDAP


class LoginScreen(QWidget):
    login_regular_user = pyqtSignal()
    show_main_window = pyqtSignal()
    set_username = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()

        # Set window title and size
        self.setWindowTitle('Login Screen')
        self.setFixedSize(300, 150)

        # Create username and password labels and input fields
        self.username_label = QLabel('Username:')
        self.username_input = QLineEdit()
        self.password_label = QLabel('Password:')
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        # Create login button
        self.login_button = QPushButton('Login')
        self.login_button.clicked.connect(self.handle_login)

        # Create layout and add widgets
        layout = QVBoxLayout()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)

        # Set layout for the widget
        self.setLayout(layout)

    def handle_login(self):
        # Retrieve username and password from input fields
        # Test account username: Drextest
        # Test account password: Salus2023!
        username = self.username_input.text()
        password = self.password_input.text()
        user = LDAP(username, password)

        print("Is Authenticated:", user.isAuthenticated())
        print("Is Admin:", user.isAdmin())
        print("Is Standard User:", user.isStandardUser())

        if user.isAuthenticated():
            if user.isAdmin():
                self.show_main_window.emit()
                self.set_username.emit(username)
            elif user.isStandardUser():
                self.login_regular_user.emit()
                self.show_main_window.emit()
                self.set_username.emit(username)
            else:
                error_message = "This Salus faculty member does not have access to the application. Please contact Salus IT: glenn@salus.edu"
                self.show_error_message(error_message)
        else:
            error_message = "Invalid username or password"
            self.show_error_message(error_message)

    def show_error_message(self, message):
        error_box = QMessageBox()
        error_box.setIcon(QMessageBox.Icon.Critical)
        error_box.setWindowTitle("Error")
        error_box.setText(message)
        error_box.exec()