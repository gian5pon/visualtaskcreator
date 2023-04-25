"""
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
import sys
"""

from packages import *


class DemographicsWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.Components()

        self.demogs_dic = {}  # the output

    def Components(self):

        central_widget = QWidget()

        # Create labels for the demographic fields
        name_label = QLabel("Name:")
        age_label = QLabel("Age:")
        gender_label = QLabel("Gender:")
        education_label = QLabel("Education:")

        # Create text fields for the demographic information
        self.name_field = QLineEdit()
        self.age_field = QSpinBox()

        # Create radio buttons for gender
        self.gender_male = QRadioButton("Male")
        self.gender_female = QRadioButton("Female")
        self.gender_other = QRadioButton("Other")

        # Create a combobox for education
        self.education_field = QComboBox()
        self.education_field.addItems(["", "High School", "Bachelor's", "Master's", "PhD"])

        # Create a submit button
        submit_button = QPushButton("Submit")
        submit_button.clicked.connect(self.submit)

        # Create a grid layout for the demographic fields
        grid = QGridLayout()
        grid.setSpacing(10)

        count = 0
        label_list = [name_label, age_label, gender_label, education_label]
        for label in label_list:
            count +=1
            if count <= 3:
                grid.addWidget(label, count, 0)
            else:
                grid.addWidget(label, 6, 0)

        count = 0
        widget_list = [self.name_field, self.age_field, self.gender_male, self.gender_female, self.gender_other,
                       self.education_field, submit_button]
        for widget in widget_list:
            count += 1
            grid.addWidget(widget, count, 1)


        layout = QVBoxLayout()
        layout.addLayout(grid)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        #self.setLayout(grid)

        self.setGeometry(800, 400, 350, 300)
        self.setWindowTitle("Demographics")
        self.show()

    def submit(self):

        # Check if any of the fields are empty
        if not self.name_field.text():
            self.showError("Please enter your name.")
        elif self.age_field.value() < 18:
            self.showError("Please enter a valid age")
        elif not self.gender_male.isChecked() and not self.gender_female.isChecked() and not self.gender_other.isChecked():
            self.showError("Please select your gender.")
        elif self.education_field.currentText() == "":
            self.showError("Please specify the last education achieved.")
        else:

            if self.gender_male.isChecked():
                gender = "Male"
            elif self.gender_female.isChecked():
                gender = "Female"
            elif self.gender_other.isChecked():
                gender = "Other"

            # Display a message box summarising the participant's input before closing
            message = "Name: {}\nAge: {}\nGender: {}\nEducation: {}".format(self.name_field.text(),
                                                                            self.age_field.text(), gender,
                                                                            self.education_field.currentText())

            QMessageBox.information(self, "Demographic Information", message)

            user_inputs_list = [self.name_field.text(), self.age_field.text(), gender,
                                self.education_field.currentText()]
            demogs_list = ["Name:", "Age:", "Gender:", "Education:"]

            # same method as for the experimenter's input window
            self.demogs_dic = dict(map(lambda i,j : (i,j) , demogs_list, user_inputs_list))

            self.close()


    # Message for the participant -> check again the responses!
    def showError(self, message):
        QMessageBox.warning(self, "Error", message)