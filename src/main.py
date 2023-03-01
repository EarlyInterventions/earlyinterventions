from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from random import randint

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
        self.courseScrollArea = None
        self.courseWidget = None
        self.courseWidgetLayout = None

        self.studentFrame = None
        self.studentHeaderLayout = None
        self.studentLabel = None
        self.studentRadioButton = None
        self.studentLineEdit = None
        self.studentHBoxLayout = None
        self.studentVBoxLayout = None
        self.studentScrollArea = None
        self.studentWidget = None
        self.studentWidgetLayout = None

        self.students = ["12345678", "12341234", "11111111", "12121212", "87654321", "22446688", "11335577"]
        self.courses = []

        for i in range(25):
            self.courses.append("course_"+str(i+1))

        while len(self.students) < 50:
            id = str(randint(10**7, (10**8)-1))
            if id not in self.students:
                self.students.append(id)


        self.setupUI()
    
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

        self.bodyGridLayout.addWidget(self.heatmapFrame, 0, 0)

        self.courseFrame = QFrame()
        self.courseFrame.setStyleSheet(".QFrame {border-width: 1; border-style: solid; border-color: rgb(0, 0, 0);}")
        self.courseFrame.setMinimumSize(250, 300)

        self.courseLabel = QLabel("Most Significant Courses")
        self.courseHBoxLayout = QHBoxLayout()
        self.courseHBoxLayout.addWidget(self.courseLabel)
        self.courseHBoxLayout.addStretch()
        self.courseVBoxLayout = QVBoxLayout()
        self.courseVBoxLayout.addLayout(self.courseHBoxLayout)
        self.courseScrollArea = QScrollArea()
        self.courseScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.courseScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.courseScrollArea.setFrameShape(QFrame.Shape.NoFrame)
        self.courseWidget = QWidget()
        self.courseWidgetLayout = QVBoxLayout()
        self.courseWidgetLayout.setContentsMargins(1, 1, 1, 1)
        for c in self.courses:
            self.courseWidgetLayout.addWidget(QLabel(c))
        self.courseWidget.setLayout(self.courseWidgetLayout)
        self.courseScrollArea.setWidget(self.courseWidget)
        self.courseVBoxLayout.addWidget(self.courseScrollArea)
        self.courseVBoxLayout.setContentsMargins(5, 5, 0, 5)
        self.courseFrame.setLayout(self.courseVBoxLayout)

        self.bodyGridLayout.addWidget(self.courseFrame, 0, 1)

        self.studentFrame = QFrame()
        self.studentFrame.setStyleSheet(".QFrame {border-width: 1; border-style: solid; border-color: rgb(0, 0, 0);}")
        self.studentFrame.setMinimumSize(300, 300)

        self.studentLabel = QLabel("Students Performance")
        self.studentHBoxLayout = QHBoxLayout()
        self.studentHBoxLayout.addWidget(self.studentLabel)
        self.studentHBoxLayout.setContentsMargins(0, 0, 5, 0)
        self.studentRadioButton = QRadioButton()
        self.studentRadioButton.setText("Most Severe")
        self.studentHBoxLayout.addWidget(self.studentRadioButton)
        self.studentLineEdit = QLineEdit()
        self.studentLineEdit.setPlaceholderText("  Filter by Severity")
        self.studentHBoxLayout.addWidget(self.studentLineEdit)
        self.studentVBoxLayout = QVBoxLayout()
        self.studentVBoxLayout.addLayout(self.studentHBoxLayout)
        self.studentVBoxLayout.addStretch()

        self.studentScrollArea = QScrollArea()
        self.studentScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.studentScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.studentScrollArea.setFrameShape(QFrame.Shape.NoFrame)
        self.studentWidget = QWidget()
        self.studentWidgetLayout = QVBoxLayout()
        self.studentWidgetLayout.setContentsMargins(1, 1, 1, 1)
        for s in self.students:
            self.studentWidgetLayout.addWidget(QLabel(s))
        self.studentWidget.setLayout(self.studentWidgetLayout)
        self.studentScrollArea.setWidget(self.studentWidget)
        self.studentVBoxLayout.addWidget(self.studentScrollArea, 1)
        self.studentVBoxLayout.setContentsMargins(5, 5, 0, 5)
        self.studentFrame.setLayout(self.studentVBoxLayout)

        self.bodyGridLayout.addWidget(self.studentFrame, 0, 2)
        
        #self.bodyFrame = QFrame()
        #self.bodyFrame.setLayout(self.bodyGridLayout)

        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.headerFrame)
        self.mainLayout.addLayout(self.bodyGridLayout)
        self.mainWidget.setLayout(self.mainLayout)

        self.setCentralWidget(self.mainWidget)



if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    gallery = MainWindow()
    gallery.show()
    sys.exit(app.exec())
