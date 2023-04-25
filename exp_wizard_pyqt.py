from packages import *


class ExperimentWizard(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Experiment set up Wizard")

        self.UiComponents()

        self.show()

        self.conditions_dic = {} # this is the output of the dialog window

    def UiComponents(self):
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)


        # first layout - conditions
        self.conditions_layout = QGridLayout()
        self.conditions_label = QLabel("Conditions:")

        ######################
        # CONDITIONS TYPES #
        ######################

        self.conditions_distractor_layout = QHBoxLayout()
        self.n_distractor_label = QLabel("Number of Distractors (use comma to separate values):")
        self.conditions_distractor_layout.addWidget(self.n_distractor_label)

        self.n_distractors_textbox = QLineEdit()
        self.n_distractors_textbox.setText("4, 8, 12, 32")
        self.n_distractors_textbox.setFixedSize(280, 40)
        self.conditions_distractor_layout.addWidget(self.n_distractors_textbox)

        self.conditions_movement_layout = QHBoxLayout()
        self.stimuli_fixed_radio = QRadioButton("Fixed stimuli")
        self.stimuli_scatter_radio = QRadioButton("Moving stimuli")
        self.conditions_movement_layout.addWidget(self.stimuli_fixed_radio)
        self.conditions_movement_layout.addWidget(self.stimuli_scatter_radio)

        self.conditions_layout.addWidget(self.conditions_label, 0, 0)
        self.conditions_layout.addLayout(self.conditions_distractor_layout, 1, 0)
        self.conditions_layout.addLayout(self.conditions_movement_layout, 2, 0)




        # second layout: stimuli characteristics
        self.stimuli_char_layout = QGridLayout()
        self.stimuli_char_label = QLabel("Stimuli Characteristics:")
        self.stimuli_char_layout.addWidget(self.stimuli_char_label, 0, 0)

        self.target_form = QHBoxLayout()
        self.distractor_form = QHBoxLayout()

        self.target_shape_combo = QComboBox(self)
        self.target_shape_combo.addItems(["", "triangle", "rectangle", "circle"])
        self.target_shape_combo.setFixedSize(280, 40)

        self.distractor_shape_combo = QComboBox(self)
        self.distractor_shape_combo.addItems(["", "triangle", "rectangle", "circle", "random"])
        self.distractor_shape_combo.setFixedSize(280, 40)

        self.target_color_combo = QComboBox(self)
        self.target_color_combo.addItems(["", "red", "blue"])
        self.target_color_combo.setFixedSize(280, 40)

        self.distractor_color_combo = QComboBox(self)
        self.distractor_color_combo.addItems(["", "red", "blue", "random"])
        self.distractor_color_combo.setFixedSize(280, 40)

        self.target_label = QLabel("Target")
        self.target_color_label = QLabel("Color")

        self.distractor_label = QLabel("Distractor(s)")
        self.distractor_color_label = QLabel("Color")

        target_form_list = [self.target_label, self.target_shape_combo, self.target_color_label, self.target_color_combo]

        for target_form_element in target_form_list:
            self.target_form.addWidget(target_form_element)

        distractor_form_list = [self.distractor_label, self.distractor_shape_combo, self.distractor_color_label
                                , self.distractor_color_combo]

        for distractor_form_element in distractor_form_list:
            self.distractor_form.addWidget(distractor_form_element)


        self.stimuli_char_layout.addLayout(self.target_form, 1, 0)
        self.stimuli_char_layout.addLayout(self.distractor_form, 2, 0)


        # third layout - trials specs
        self.loops_layout = QHBoxLayout(self)

        self.loops_label = QLabel("Trials' specifications:")
        self.trials_label = QLabel("Number of trials")
        self.target_presence = QLabel("Target's presence")

        self.trials_spinbox = QSpinBox(self)
        self.trials_spinbox.setFixedSize(80, 40)

        self.target_presence_spinbox = QSpinBox(self)
        self.target_presence_spinbox.setFixedSize(80, 40)

        # ADDING WIDGETS
        loops_layout_widgets = [self.loops_label, self.trials_label, self.trials_spinbox, self.target_presence,
                                self.target_presence_spinbox]

        for loops_layout_element in loops_layout_widgets:
            self.loops_layout.addWidget(loops_layout_element)


        # forth layout: input type
        self.input_layout = QVBoxLayout(self)
        self.input_label = QLabel("Keyboard keys (use comma to separate values)")
        self.input_layout.addWidget(self.input_label)

        self.keyboard_keys = QLineEdit()
        self.keyboard_keys.setText("y,n")
        self.keyboard_keys.setFixedSize(280, 40)
        self.input_layout.addWidget(self.keyboard_keys)


        self.submit_push = QPushButton("Submit")




        # main layout
        self.main_layout = QVBoxLayout(self.central_widget)

        self.layouts_list = [self.conditions_layout, self.stimuli_char_layout, self.loops_layout,
                        self.input_layout]
        for layout in self.layouts_list:
            self.main_layout.addLayout(layout)

        self.main_layout.addWidget(self.submit_push)
        self.central_widget.setLayout(self.main_layout)

        # Set some lists to be retrieved as output of the dialog window
        self.count = 0
        self.conditions_list = []
        self.children_list = []

        # Actions
        self.trials_spinbox.valueChanged.connect(self.update_max_value) # bound the value of 'target presence' to trials
        self.submit_push.clicked.connect(self.conditions_check)




    def update_max_value(self):
        value = self.trials_spinbox.value()
        self.target_presence_spinbox.setMaximum(value)



    def conditions_check(self):

        self.conditions_dic = {}

        if self.n_distractors_textbox.text() == "":
            self.displayError("Please insert the number of distractors")

        elif self.stimuli_fixed_radio.isChecked() == False and self.stimuli_scatter_radio.isChecked() == False:
            self.displayError("Please choose the movement of distractors")

        elif self.target_shape_combo.currentText() == "":
            self.displayError("Please choose a target's shape")

        elif self.target_color_combo.currentText() == "":
            self.displayError("Please choose the target's color")

        elif self.distractor_shape_combo.currentText() == "":
            self.displayError("Please choose the shape of distractors")

        elif self.distractor_color_combo.currentText() == "":
            self.displayError("Please choose the color of distractors")

        elif self.target_presence_spinbox.value() == 0:
            self.displayError("Please allow for the presentation of the target at least 1 time")

        elif self.trials_spinbox.value() == 0:
            self.displayError("Please choose the number of trials")

        elif self.keyboard_keys.text() == "":
            self.displayError("Please type some keyboard keys (e.g. 'y,n' "
                              "for 'yes' and 'no' respectively.")

        else:

            if self.stimuli_scatter_radio.isChecked():
                movement = "scatter"
            elif self.stimuli_fixed_radio.isChecked():
                movement = "fixed"

            # Display a message box summarising the conditions
            message = "Distractors number: {}\nStimuli's movement: {}\nTarget's shape: {}" \
                      "\nTarget's color: {}\nDistractors shape: {}\nDistractor's color: {}" \
                      "\nNumber of trials: {}\nof which the target is present: {}\n" \
                      "Keyboard's input keys: {}".format(self.n_distractors_textbox.text(),
                                                         movement, self.target_shape_combo.currentText(),
                                                         self.target_shape_combo.currentText(),
                                                         self.target_color_combo.currentText(),
                                                         self.distractor_shape_combo.currentText(),
                                                         self.distractor_color_combo.currentText(),
                                                         self.target_presence_spinbox.value(),
                                                         self.keyboard_keys.text())

            QMessageBox.information(self, "Experiment's Information", message)


            # POPULATE THE DICTIONARY -> OUTPUT OF THE WINDOW
            conditions_list = ["n_distractors", "movement", "target_shape", "target_color", "distractor_shape",
                               "distractor_color", "n_trials", "target_presence", "keyboard_keys"]

            values_list = [self.n_distractors_textbox.text(), movement, self.target_shape_combo.currentText(),
                          self.target_color_combo.currentText(), self.distractor_shape_combo.currentText(),
                          self.distractor_color_combo.currentText(), self.trials_spinbox.value(),
                          str(self.target_presence_spinbox.value()), self.keyboard_keys.text()]

            # the dict() method creates a dictionary, the lambda map function crosses the values within the two lists
            self.conditions_dic = dict(map(lambda i,j : (i,j) , conditions_list, values_list))

            self.close()

    # Small error window to be displayed if one of the conditions is not specified
    def displayError(self, message):
        error_dialog = QMessageBox()
        error_dialog.setIcon(QMessageBox.Warning)
        error_dialog.setText(message)
        error_dialog.setWindowTitle("Error")
        error_dialog.exec_()
