from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

class StudentWindow(QMainWindow):
    def __init__(self, parent=None, studentID=None):
        super(QMainWindow, self).__init__(parent)

        self.mainWidget = None
        self.mainLayout = None
        self.studentID = studentID
        self.studentLabel = None
        self.studentScore = None
        self.tabWidget = None
        self.yearOneWidget = None
        self.yearTwoWidget = None
        self.yearThreeWidget = None
        self.overallWidget = None

        self.setupUI()
    
    def setupUI(self):
        self.mainWidget = QWidget()
        self.mainWidget.setMinimumSize(500,500)
        self.setWindowTitle("Student View - " + str(self.studentID))

        self.mainLayout = QVBoxLayout()

        self.studentLabel = QLabel("Student " + self.studentID)
        font = QFont()
        font = self.studentLabel.font()
        font.setBold(True)
        font.setPointSize(16)
        self.studentLabel.setFont(font)

        self.mainLayout.addWidget(self.studentLabel)

        self.tabWidget = QTabWidget()
        self.yearOneWidget = QWidget()
        self.yearTwoWidget = QWidget()
        self.yearThreeWidget = QWidget()
        self.overallWidget = QWidget()

        self.tabWidget.addTab(self.overallWidget, "Overall")
        self.tabWidget.addTab(self.yearOneWidget, "Year One")
        self.tabWidget.addTab(self.yearTwoWidget, "Year Two")
        self.tabWidget.addTab(self.yearThreeWidget, "Year Three")

        self.mainLayout.addWidget(self.tabWidget)
        self.mainWidget.setLayout(self.mainLayout)

        self.setCentralWidget(self.mainWidget)
