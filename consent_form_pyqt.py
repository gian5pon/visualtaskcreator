from packages import *



class ConsentFormWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        # Just a dummy variable which changes to 'True' if the participant agrees
        self.consent = False

        self.setWindowTitle("Terms of agreement")

        self.UiComponents()

        self.show()

    def UiComponents(self):

        self.central_widget = QWidget()

        # Consent form text
        self.consent_form_text = "This is a sample consent form. This is a sample consent form.\n\n" \
                                 "This is a sample consent form. This is a sample consent form.\n\n" \
                                 "This is a sample consent form. This is a sample consent form.\n\n" \
                                 "This is a sample consent form. This is a sample consent form.\n\n" \
                                 "This is a sample consent form. This is a sample consent form.\n\n" \
                                 "This is a sample consent form. This is a sample consent form.\n\n" \
                                 "This is a sample consent form. This is a sample consent form.\n\n" \
                                 "This is a sample consent form. This is a sample consent form.\n\n" \
                                 "This is a sample consent form. This is a sample consent form.\n\n" \
                                 "This is a sample consent form. This is a sample consent form.\n\n" \
                                 "This is a sample consent form. This is a sample consent form.\n\n" \
                                 "This is a sample consent form. This is a sample consent form.\n\n" \
                                 "This is a sample consent form. This is a sample consent form.\n\n " \
                                 "By clicking the checkbox and submitting, I agree to the terms and conditions of this " \
                                 "consent form."

        # Scroll area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area_widget = QWidget()
        self.scroll_area_layout = QVBoxLayout(self.scroll_area_widget)
        self.scroll_area_text = QLabel(self.consent_form_text)
        self.scroll_area_layout.addWidget(self.scroll_area_text)
        self.scroll_area.setWidget(self.scroll_area_widget)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        # Checkbox to proceed
        self.checkbox = QCheckBox("I have read and agree to the terms and conditions")
        self.checkbox.setEnabled(False)

        # Submit button
        self.submit_button = QPushButton("Submit")

        # Layout
        layout = QVBoxLayout()
        widgets = [self.scroll_area, self.checkbox, self.submit_button]
        for widget in widgets:
            layout.addWidget(widget)

        # Set layout
        self.central_widget.setLayout(layout)
        self.setCentralWidget(self.central_widget)

        # Connect signals
        self.scroll_area.verticalScrollBar().valueChanged.connect(self.enable_checkbox)
        self.submit_button.clicked.connect(self.submit)

    def enable_checkbox(self):
        maximum = self.scroll_area.verticalScrollBar().maximum()
        value = self.scroll_area.verticalScrollBar().value()
        if value == maximum:
            self.checkbox.setEnabled(True)

    def submit(self):
        if self.checkbox.isChecked():
            self.consent = True # The participant has agreed upon -> move on
            self.close()
        else:
            error_dialog = QMessageBox()
            error_dialog.setWindowTitle("Error")
            error_dialog.setText("Please scroll all the way down and check the checkbox to proceed.")
            error_dialog.exec_()
