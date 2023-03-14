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
        self.scoreLabel = None
        self.levelLabel = None
        self.confIntervalLabel = None
        self.studentScore = None
        self.tabWidget = None
        self.yearOneWidget = None
        self.yearOneVBox = None
        self.yearOneTopFive = None
        self.yearTwoWidget = None
        self.yearTwoVBox = None
        self.yearTwoTopFive = None
        self.yearThreeWidget = None
        self.yearThreeVBox = None
        self.yearThreeTopFive = None
        self.overallWidget = None
        self.overallVBox = None
        self.overallTopFive = None

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

        self.levelLabel = QLabel("Year in Program: 2")
        self.mainLayout.addWidget(self.levelLabel)

        self.scoreLabel = QLabel("Predicted Score: 300")
        self.mainLayout.addWidget(self.scoreLabel)

        self.confIntervalLabel = QLabel("Confidence Interval: 85%")
        self.mainLayout.addWidget(self.confIntervalLabel)


        self.tabWidget = QTabWidget()
        self.yearOneWidget = QWidget()
        self.yearTwoWidget = QWidget()
        self.yearThreeWidget = QWidget()
        self.overallWidget = QWidget()

        self.tabWidget.addTab(self.overallWidget, "Overall")
        self.tabWidget.addTab(self.yearOneWidget, "Year One")
        self.tabWidget.addTab(self.yearTwoWidget, "Year Two")
        self.tabWidget.addTab(self.yearThreeWidget, "Year Three")

        self.overallTopFive = QLabel("Top 5 Predicitive Classes - Overall")
        self.overallTopFive.setFont(font)
        self.yearOneTopFive = QLabel("Top 5 Predicitive Classes - Year One")
        self.yearOneTopFive.setFont(font)
        self.yearTwoTopFive = QLabel("Top 5 Predicitive Classes - Year Two")
        self.yearTwoTopFive.setFont(font)
        self.yearThreeTopFive = QLabel("Top 5 Predicitive Classes - Year Three")
        self.yearThreeTopFive.setFont(font)

        self.overallVBox = QVBoxLayout()
        self.yearOneVBox = QVBoxLayout()
        self.yearTwoVBox = QVBoxLayout()
        self.yearThreeVBox = QVBoxLayout()
        
        self.overallVBox.addWidget(self.overallTopFive)
        self.overallVBox.addStretch()
        self.overallWidget.setLayout(self.overallVBox)
        
        self.yearOneVBox.addWidget(self.yearOneTopFive)
        self.yearOneVBox.addStretch()
        self.yearOneWidget.setLayout(self.yearOneVBox)

        self.yearTwoVBox.addWidget(self.yearTwoTopFive)
        self.yearTwoVBox.addStretch()
        self.yearTwoWidget.setLayout(self.yearTwoVBox)

        self.yearThreeVBox.addWidget(self.yearThreeTopFive)
        self.yearThreeVBox.addStretch()
        self.yearThreeWidget.setLayout(self.yearThreeVBox)

        self.mainLayout.addWidget(self.tabWidget)
        self.mainWidget.setLayout(self.mainLayout)

        self.setCentralWidget(self.mainWidget)
