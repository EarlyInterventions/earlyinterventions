import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QMessageBox, QListWidget, QListWidgetItem, QAbstractItemView
from init import get_years, get_unique_values, filter_training_dataframe, create_test_dataframe, create_model, fit_model, predict_results, get_feature_importance

class ImportData(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Upload Data")
        self.setFixedSize(800, 400)

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.layout)

        self.file_label = QLabel("No file selected")
        self.layout.addWidget(self.file_label)

        self.browse_button = QPushButton("Browse")
        self.browse_button.clicked.connect(self.open_file_dialog)
        self.layout.addWidget(self.browse_button)

        self.upload_button = QPushButton("Submit")
        self.upload_button.clicked.connect(self.upload_data)
        self.layout.addWidget(self.upload_button)

    def open_file_dialog(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)

        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                file_path = selected_files[0]
                self.file_label.setText(f"Selected file: {file_path}")

    def upload_data(self):
        file_path = self.file_label.text().replace("Selected file: ", "")

        if file_path.endswith(".csv"):
            # Process the CSV file here
            # This is where calls to the database/server should go
            QMessageBox.information(self, "Success", "File uploaded successfully!")
            
            self.browse_button.hide()
            self.upload_button.hide()
            
            year_values, clean_cohort_df = get_years(file_path)
            
            self.list_widget = QListWidget()
            self.list_widget.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)  # Allow multiple selections

            for value in year_values:
                item = QListWidgetItem(str(value))
                self.list_widget.addItem(item) 
            
            self.submit_courses_button = QPushButton("Submit")
            self.submit_courses_button.clicked.connect(lambda: self.submit_courses(clean_cohort_df))

            self.layout.addWidget(self.list_widget)
            self.layout.addWidget(self.submit_courses_button)
            self.layout.addSpacing(40)

        else:
            QMessageBox.critical(self, "Error", "Invalid file format. Please select a CSV file.")

    def submit_courses(self, clean_cohort_df):
    
        # Find the QListWidget in the parent widget
        list_widget = self.findChild(QListWidget)

        if list_widget:
            selected_items = list_widget.selectedItems()
            selected_values = [item.text() for item in selected_items]
            
            unique_courses = get_unique_values(clean_cohort_df, selected_values)

            self.list_widget.hide()
            self.submit_courses_button.hide()
            
            self.list_widget = QListWidget()
            self.list_widget.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)  # Allow multiple selections

            self.submit_training_button = QPushButton("Submit")
            self.submit_training_button.clicked.connect(lambda: self.upload_new_data(clean_cohort_df, selected_values, self.list_widget.selectedItems()))

            self.select_all_button = QPushButton("Select All")
            self.select_all_button.clicked.connect(lambda: self.select_all_items())
            
            for value in unique_courses:
                item = QListWidgetItem(str(value))
                self.list_widget.addItem(item)

            self.layout.addWidget(self.list_widget)
            self.layout.addWidget(self.submit_training_button)
            self.layout.addWidget(self.select_all_button)
            self.layout.addSpacing(40) 
    
    def select_all_items(self):
        for index in range(self.list_widget.count()):
            item = self.list_widget.item(index)
            item.setSelected(True)

    def upload_new_data(self, clean_cohort_df, selected_cohorts, selected_courses):
        selected_courses = [item.text() for item in selected_courses]

        
        training_df = filter_training_dataframe(clean_cohort_df, selected_cohorts, selected_courses)
        testing_df = create_test_dataframe(clean_cohort_df, selected_courses)

        X_train, y_train, X_test, ID_df, feature_names = create_model(training_df, testing_df)
        fitted_model = fit_model(X_train, y_train)
        logresults = predict_results(fitted_model, X_test, ID_df)

        feature_importance_df = get_feature_importance(fitted_model, feature_names)

        QMessageBox.information(self, "Success", "Data uploated to database! This screen will now close.")

        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    upload_data = ImportData()
    upload_data.show()

    sys.exit(app.exec())