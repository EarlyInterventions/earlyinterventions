from PyQt6.QtWidgets import *

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(QMainWindow, self).__init__(parent)

        mainWidget = QWidget()
        mainWidget.setMinimumSize(500,500)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(QLabel("Welcome to Early Interventions!"))
        mainLayout2 = QHBoxLayout()
        mainLayout2.addStretch()
        mainLayout2.addLayout(mainLayout)
        mainLayout2.addStretch()
        mainWidget.setLayout(mainLayout2)

        self.setCentralWidget(mainWidget)

if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    gallery = MainWindow()
    gallery.show()
    sys.exit(app.exec())
