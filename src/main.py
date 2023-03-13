from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from random import randint
from StudentWindow import StudentWindow

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(QMainWindow, self).__init__(parent)

        self.mainWidget = None
        self.mainLayout = None
        self.mainLayout2 = None

        self.headerHLayout = None
        self.headerFrame = None
        self.cohortComboBox = None
        self.filterComboBox = None
        self.searchStudentLineEdit = None
        self.searchCompleter = None
        self.importDataButton = None
        self.usernameLabel = None
        self.dashboardSplitter = None

        self.bodyFrame = None
        self.bodyGridLayout = None
        self.heatmapFrame = None
        self.heatmapLabel = None
        self.heatmapHBoxLayout = None
        self.heatmapVBoxLayout = None

        self.courseFrame = None
        self.courseLabel = None
        self.courseHBoxLayout = None
        self.courseVBoxLayout = None
        self.courseListWidget = None
        self.courseWidget = None
        self.courseWidgetLayout = None

        self.studentFrame = None
        self.studentHeaderLayout = None
        self.studentLabel = None
        self.studentRadioButton = None
        self.studentLineEdit = None
        self.studentHBoxLayout = None
        self.studentVBoxLayout = None
        self.studentListWidget = None

        self.students = ["12345678", "12341234", "11111111", "12121212", "87654321", "22446688", "11335577"]
        self.courses = []

        for i in range(25):
            self.courses.append("course_"+str(i+1))

        while len(self.students) < 50:
            id = str(randint(10**7, (10**8)-1))
            if id not in self.students:
                self.students.append(id)

        self.setupUI()

        self.studentListWidget.itemClicked.connect(self.studentClicked)
        self.searchStudentLineEdit.returnPressed.connect(self.studentEntered)
    
    def setupUI(self):
        self.mainWidget = QWidget()
        self.mainWidget.setMinimumSize(640,500)
        self.setWindowTitle("Early Interventions")

        self.cohortComboBox = QComboBox()
        self.cohortComboBox.addItems(["Cohort 2022", "Cohort 2021", "Cohort 2020"])
        self.cohortComboBox.setCurrentIndex(0)

        self.filterComboBox = QComboBox()
        self.filterComboBox.addItems(["Filter By", " ", " "])
        self.filterComboBox.setCurrentIndex(0)

        self.searchStudentLineEdit = QLineEdit()
        self.searchStudentLineEdit.setPlaceholderText("Search by StudentID")

        self.searchCompleter = QCompleter(self.students)
        self.searchCompleter.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)

        self.searchStudentLineEdit.setCompleter(self.searchCompleter)

        self.importDataButton = QPushButton("Import Data")
        
        self.usernameLabel = QLabel("user_123")

        self.dashboardSplitter = QSplitter(Qt.Orientation.Horizontal)

        self.headerHLayout = QHBoxLayout()
        self.headerHLayout.addWidget(self.cohortComboBox)
        self.headerHLayout.addWidget(self.filterComboBox)
        self.headerHLayout.addWidget(self.searchStudentLineEdit)
        self.headerHLayout.addStretch()
        self.headerHLayout.addWidget(self.importDataButton)
        self.headerHLayout.addWidget(self.usernameLabel)

        self.headerFrame = QFrame()
        self.headerFrame.setStyleSheet(".QFrame {border-width: 1; border-style: solid; border-color: rgb(0, 0, 0);}")
        self.headerFrame.setLayout(self.headerHLayout)

        self.bodyGridLayout = QGridLayout()

        self.heatmapFrame = QFrame()
        self.heatmapFrame.setStyleSheet(".QFrame {border-width: 1; border-style: solid; border-color: rgb(0, 0, 0);}")
        self.heatmapFrame.setMinimumSize(450, 300)

        self.heatmapLabel = QLabel("Cohort 2022 Heatmap")
        self.heatmapHBoxLayout = QHBoxLayout()
        self.heatmapHBoxLayout.addWidget(self.heatmapLabel)
        self.heatmapHBoxLayout.addStretch()
        self.heatmapVBoxLayout = QVBoxLayout()
        self.heatmapVBoxLayout.addLayout(self.heatmapHBoxLayout)
        self.heatmapVBoxLayout.addStretch()
        self.heatmapFrame.setLayout(self.heatmapVBoxLayout)

        self.dashboardSplitter.addWidget(self.heatmapFrame)

        self.courseFrame = QFrame()
        self.courseFrame.setStyleSheet(".QFrame {border-width: 1; border-style: solid; border-color: rgb(0, 0, 0);}")
        self.courseFrame.setMinimumSize(250, 300)

        self.courseLabel = QLabel("Most Significant Courses")
        self.courseLabel.setContentsMargins(0, 5, 0, 0)
        self.courseHBoxLayout = QHBoxLayout()
        self.courseHBoxLayout.addWidget(self.courseLabel)
        self.courseHBoxLayout.addStretch()
        self.courseVBoxLayout = QVBoxLayout()
        self.courseVBoxLayout.addLayout(self.courseHBoxLayout)

        self.courseListWidget = QListWidget()
        self.courseListWidget.setFrameShape(QFrame.Shape.NoFrame)
        self.courseListWidget.viewport().setAutoFillBackground(False)
        self.courseListWidget.setSpacing(2)
        for c in self.courses:
            self.courseListWidget.addItem(c)
        self.courseVBoxLayout.addWidget(self.courseListWidget, 1)
        self.courseVBoxLayout.setContentsMargins(5, 0, 0, 0)
        self.courseFrame.setLayout(self.courseVBoxLayout)

        self.dashboardSplitter.addWidget(self.courseFrame)

        self.studentFrame = QFrame()
        self.studentFrame.setStyleSheet(".QFrame {border-width: 1; border-style: solid; border-color: rgb(0, 0, 0);}")
        self.studentFrame.setMinimumSize(300, 300)

        self.studentLabel = QLabel("Students Performance")
        self.studentHBoxLayout = QHBoxLayout()
        self.studentHBoxLayout.addWidget(self.studentLabel)
        self.studentHBoxLayout.setContentsMargins(0, 5, 5, 0)
        self.studentRadioButton = QRadioButton()
        self.studentRadioButton.setText("Most Severe")
        self.studentHBoxLayout.addWidget(self.studentRadioButton)
        self.studentLineEdit = QLineEdit()
        self.studentLineEdit.setPlaceholderText("  Filter by Severity")
        self.studentHBoxLayout.addWidget(self.studentLineEdit)
        self.studentVBoxLayout = QVBoxLayout()
        self.studentVBoxLayout.addLayout(self.studentHBoxLayout)
        self.studentVBoxLayout.addStretch()

        self.studentListWidget = QListWidget()
        self.studentListWidget.setFrameShape(QFrame.Shape.NoFrame)
        self.studentListWidget.viewport().setAutoFillBackground(False)
        self.studentListWidget.setSpacing(2)
        for s in self.students:
            self.studentListWidget.addItem(s)
        self.studentVBoxLayout.addWidget(self.studentListWidget, 1)
        self.studentVBoxLayout.setContentsMargins(5, 0, 0, 0)
        self.studentFrame.setLayout(self.studentVBoxLayout)

        self.dashboardSplitter.addWidget(self.studentFrame)
        self.bodyGridLayout.addWidget(self.dashboardSplitter, 1, 0)
        self.bodyGridLayout.setRowStretch(1, 1)
        self.bodyGridLayout.setColumnStretch(0, 1)

        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.headerFrame)
        self.mainLayout.addLayout(self.bodyGridLayout)
        self.mainWidget.setLayout(self.mainLayout)

        self.setCentralWidget(self.mainWidget)

    def studentClicked(self, s_id):
        studentWindow = StudentWindow(self, s_id.text())
        studentWindow.show()
    
    def studentEntered(self):
        s_id = self.searchStudentLineEdit.text()
        if s_id in self.students:
            studentWindow = StudentWindow(self, s_id)
            studentWindow.show()


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    gallery = MainWindow()
    gallery.show()
    sys.exit(app.exec())
