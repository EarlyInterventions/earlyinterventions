#!/usr/bin/python

import sys
from PyQt6.QtWidgets import QApplication
from MainWindow import MainWindow
from LoginScreen import LoginScreen

if __name__ == "__main__":
    app = QApplication(sys.argv)

    login_screen = LoginScreen()
    main_window = MainWindow()

    login_screen.login_regular_user.connect(lambda: main_window.importDataButton.hide())
    login_screen.show_main_window.connect(lambda: main_window.show())
    login_screen.set_username.connect(main_window.update_username_label)

    login_screen.show()

    sys.exit(app.exec())