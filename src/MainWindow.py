import matplotlib
matplotlib.use('Qt5Agg')

import numpy as np
import pandas as pd
import pyodbc

from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar2QT
from matplotlib.lines import Line2D
from matplotlib.figure import Figure
from random import randint
from StudentWindow import StudentWindow
from Student import Student
from ImportData import ImportData

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
        self.heatmapFig = None
        self.heatmapToolbar = None
        self.clicked = False

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

        self.students = {}
        self.course_weight = {}
        self.courses = []
        self.allPredicted = []
        self.allActual = []
        self.allRaw = []

        self.getData()
        self.setupUI()

        self.studentListWidget.itemClicked.connect(self.studentClicked)
        self.searchStudentLineEdit.returnPressed.connect(self.studentEntered)
        self.filterComboBox.currentTextChanged.connect(self.filterCourses)
        self.cohortComboBox.currentTextChanged.connect(self.updateHeatmap)
        self.heatmapFig.mpl_connect("motion_notify_event", self.displayAnnotation)
        self.heatmapFig.mpl_connect("pick_event", self.on_click)
    
    def setupUI(self):
        self.mainWidget = QWidget()
        self.mainWidget.setMinimumSize(640,500)
        self.setWindowTitle("Early Interventions")

        self.cohortComboBox = QComboBox()
        self.cohortComboBox.addItems(["All Cohorts", "Cohort 2023"])
        self.cohortComboBox.setCurrentIndex(0)

        self.filterComboBox = QComboBox()
        self.filterComboBox.addItems(["Filter By Year", "Year 1", "Year 2", "Year 3"])
        self.filterComboBox.setCurrentIndex(0)

        self.searchStudentLineEdit = QLineEdit()
        self.searchStudentLineEdit.setPlaceholderText("Search by StudentID")

        self.searchCompleter = QCompleter(self.students.keys())
        self.searchCompleter.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)

        self.searchStudentLineEdit.setCompleter(self.searchCompleter)
        
        self.importDataButton = QPushButton("Import Data")
        self.importDataButton.clicked.connect(self.show_import_data_widget)
        
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

        self.heatmapFig = HeatMap(self, width=5, height=4, dpi=100)
        self.heatmapLabel.setText(self.cohortComboBox.currentText() + " Logistic Regression")
        graphDict = {}
        for key in self.students:
                graphDict[key] = self.students[key].getRawPredict()
        c = ["red", "lightcoral", "orange", "palegreen", "green"]
        v = [0, 0.25, 0.5, 0.75, 1.0]
        l = list(zip(v,c))
        custom_cmap = matplotlib.colors.LinearSegmentedColormap.from_list('rg', l, N=256)
        self.heatmapFig.axes.cla()
        self.scatter = self.heatmapFig.axes.scatter(range(len(graphDict.keys())), sorted(graphDict.values()), c=sorted(graphDict.values()), cmap=custom_cmap, marker=".", picker=5)
        self.annotation = self.heatmapFig.axes.annotate(text="", xy=(0,0), xytext=(15, 15), textcoords="offset points", bbox={"boxstyle": "round", "fc": "w"}, arrowprops={"arrowstyle": "->"})
        self.annotation.set_bbox(dict(boxstyle='round' , facecolor='white', alpha=0.5))
        self.annotation.set_visible(False)
        self.heatmapFig.axes.set_xlabel("All Students")
        self.heatmapFig.axes.set_ylabel("Chance to Pass")

        self.heatmapToolbar = NavigationToolbar(self.heatmapFig, self)
        self.heatmapVBoxLayout.addWidget(self.heatmapToolbar)
        self.heatmapVBoxLayout.addWidget(self.heatmapFig, 1)

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
        #self.courseListWidget.addItems(self.courses)
        for c in self.course_weight.keys():
            self.courseListWidget.addItem(c + ":\t" + str(self.course_weight[c]))
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
        self.studentRadioButton.hide() # temporary
        self.studentHBoxLayout.addWidget(self.studentRadioButton)
        self.studentLineEdit = QLineEdit()
        self.studentLineEdit.setPlaceholderText("  Filter by Severity")
        self.studentLineEdit.hide() # temporary
        self.studentHBoxLayout.addWidget(self.studentLineEdit)
        self.studentVBoxLayout = QVBoxLayout()
        self.studentVBoxLayout.addLayout(self.studentHBoxLayout)
        self.studentVBoxLayout.addStretch()

        self.studentListWidget = QListWidget()
        self.studentListWidget.setFrameShape(QFrame.Shape.NoFrame)
        self.studentListWidget.viewport().setAutoFillBackground(False)
        self.studentListWidget.setSpacing(2)
        #for s in self.students.keys():
        #    text = "%s: \t%.7f" % (s, self.students[s].getRawPredict())
        #    self.studentListWidget.addItem(text)
        sortedStudents = sorted(self.students.items(), key=lambda x:x[1].getRawPredict())
        sortedStudents.reverse()
        for k, v in sortedStudents:
            text = "%s: \t%.7f" % (k, v.getRawPredict())
            self.studentListWidget.addItem(text)
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
        key = s_id.text().split(':')[0]
        graphDict = {}
        x = 0
        y = self.students[key].getRawPredict()
        for k in self.students:
            graphDict[k] = self.students[k].getRawPredict()
        for v in sorted(graphDict.values()):
            if v == y:
                self.annotation.xy = (x, y)
                self.annotation.set_text("Student %s: \nPredicted Score: %f \nConfidence Interval: %.2f%%" % (key, y, 84.865))
                self.annotation.set_visible(True)
                self.heatmapFig.fig.canvas.draw_idle()
                break
            else:
                x += 1
        if not self.clicked:
            self.on_click(None)
    
    def studentEntered(self):
        s_id = self.searchStudentLineEdit.text()
        if s_id in self.students.keys():
            studentWindow = StudentWindow(self, s_id)
            studentWindow.show()
    
    def updateHeatmap(self):
        if self.sender() == self.cohortComboBox:
            currentCohort = self.cohortComboBox.currentText()
            graphDict = {}
            for key in self.students:
                if self.students[key].getCohort() == currentCohort.split()[1]:
                    graphDict[key] = self.students[key].getRawPredict()
                else:
                    graphDict[key] = self.students[key].getRawPredict()
            self.heatmapLabel.setText(currentCohort + " Logistic Regression")
            c = ["red", "lightcoral", "orange", "palegreen", "green"]
            v = [0, 0.25, 0.5, 0.75, 1.0]
            l = list(zip(v,c))
            custom_cmap = matplotlib.colors.LinearSegmentedColormap.from_list('rg', l, N=256)
            self.heatmapFig.axes.cla()
            self.scatter = self.heatmapFig.axes.scatter(range(len(graphDict.keys())), sorted(graphDict.values()), c=sorted(graphDict.values()), cmap=custom_cmap, marker=".")
            self.annotation = self.heatmapFig.axes.annotate(text="", xy=(0,0), xytext=(15, 15), textcoords="offset points", bbox={"boxstyle": "round", "fc": "w"}, arrowprops={"arrowstyle": "->"})
            self.annotation.set_visible(False)
            self.heatmapFig.axes.set_xlabel("%s Students" % currentCohort)
            self.heatmapFig.axes.set_ylabel("Chance to Pass")
        self.heatmapFig.fig.canvas.draw()

    def getData(self):

        conn = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};Server=EDREXEI\EI;Database=testjawn;"                  "uid=Drexel;pwd=$4hEs@7F")
        df = pd.read_sql_query('SELECT * FROM feature_importance \
            WHERE created_at = ( SELECT MAX( created_at ) FROM feature_importance);', conn)
        df = pd.read_sql_query('SELECT course_name, importance, created_at FROM feature_importance WHERE created_at = ( SELECT MAX( created_at ) FROM feature_importance);', conn)
        for index, row in df.iterrows():
            self.courses.append(row['course_name'])
            self.course_weight[row['course_name']] = row['importance']
        #for c in df["feature"]:
        #    self.courses.append(c)
        
        #get logistic regression from db
        df = pd.read_sql_query('SELECT ID, Year, Predicted, Probability FROM model_results WHERE created_at = ( SELECT MAX( created_at ) FROM model_results);', conn)
        #self.allActual = df['Actual']
        self.allPredicted = df['Predicted']
        self.allRaw = pd.to_numeric(df['Probability'])
        for index, row in df.iterrows():
            s = Student(row['ID'])
            s.setCohort(str(row['Year']))
            #s.setActualScore(row['Actual'])
            s.setPredictedScore(row['Predicted'])
            s.setRawPredict(float(row['Probability']))
            self.students[s.getID()] = s
    
    def on_click(self, event):
        if not self.clicked:
            self.clicked = True
        elif self.clicked:
            self.clicked = False

    def displayAnnotation(self, event):
        if event.inaxes == self.heatmapFig.axes:
            is_contained, annot_idx = self.scatter.contains(event)
            if is_contained and not self.clicked:
                data_point_location = self.scatter.get_offsets()[annot_idx["ind"][0]]
                self.annotation.xy = data_point_location
                for key, value in self.students.items():
                    if value.getRawPredict() == data_point_location[1]:
                        self.annotation.set_text("Student %s: \nCohort: %s \nChance to Pass: %f \nConfidence Interval: %.2f%%" \
                                                  % (key, self.students[key].getCohort(), data_point_location[1], 84.865))
                        break
                self.annotation.set_visible(True)
                self.heatmapFig.fig.canvas.draw_idle()
            else:
                if self.annotation.get_visible() and not self.clicked:
                    self.annotation.set_visible(False)
                    self.heatmapFig.fig.canvas.draw_idle()

    def closeEvent(self, event):
        QApplication.quit()

    def filterCourses(self):
        currentIndex = self.filterComboBox.currentIndex()
        if currentIndex == 0:
            for i in range(self.courseListWidget.count()):
                self.courseListWidget.item(i).setHidden(False)
        elif currentIndex == 1:
            for i in range(self.courseListWidget.count()):
                text = self.courseListWidget.item(i).text()
                if int(text.split(":")[0][-1]) == 1:
                    self.courseListWidget.item(i).setHidden(False)
                else:
                    self.courseListWidget.item(i).setHidden(True)
        elif currentIndex == 2:
            for i in range(self.courseListWidget.count()):
                text = self.courseListWidget.item(i).text()
                if int(text.split(":")[0][-1]) == 2:
                    self.courseListWidget.item(i).setHidden(False)
                else:
                    self.courseListWidget.item(i).setHidden(True)
        elif currentIndex == 3:
            for i in range(self.courseListWidget.count()):
                text = self.courseListWidget.item(i).text()
                if int(text.split(":")[0][-1]) == 3:
                    self.courseListWidget.item(i).setHidden(False)
                else:
                    self.courseListWidget.item(i).setHidden(True)


    def show_import_data_widget(self):
        self.importDataWidget = ImportData()  # Replace ImportData with the actual widget class name
        self.importDataWidget.show()

    def update_username_label(self, username):
        self.usernameLabel.setText(username)


def sigmoid(z):
        return 1 / (1 + np.exp(-z+16))

class HeatMap(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        super(HeatMap, self).__init__(self.fig)


class NavigationToolbar(NavigationToolbar2QT):
    # only display the buttons we need
    NavigationToolbar2QT.toolitems = (
        ('Home', 'Reset original view', 'home', 'home'),
        ('Back', 'Back to previous view', 'back', 'back'),
        ('Forward', 'Forward to next view', 'forward', 'forward'),
        (None, None, None, None),
        ('Pan', 'Pan axes with left mouse, zoom with right', 'move', 'pan'),
        ('Zoom', 'Zoom to rectangle', 'zoom_to_rect', 'zoom'),
        # ('Subplots', 'Configure subplots', 'subplots', 'configure_subplots'),
        (None, None, None, None),
        ('Save', 'Save the figure', 'filesave', 'save_figure'),
    )
