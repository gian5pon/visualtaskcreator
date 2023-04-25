from os import listdir
from experiment_flow import *
from exp_wizard_pyqt import *
from consent_form_pyqt import *
from demographics_pyqt import *
from functions import *


# This is the main file, containing the whole flow of the experiment.
# 1. The experimenter sets all the parameters up for the experiment
# 2. The participant inserts demographics
# 3. Then the experiment can start

# Initialise the experiment_wizard

app = QApplication(sys.argv)

Expwindow = ExperimentWizard()
Expwindow.show()
app.exec()


# Experimenter input
conditions_dictionary = Expwindow.conditions_dic


# Initialise the demographics window only if experimenter has set conditions up
# Participants FIRST INPUT == demographics data
if len(conditions_dictionary) != 0:

    n_trials = int(conditions_dictionary.pop('n_trials')) # Get the number of trials indicated
    keyboard_keys = conditions_dictionary.pop('keyboard_keys') # Get the keys chosen

    Demogwindow = DemographicsWindow()
    Demogwindow.show()
    app.exec()
    demogs_dic = Demogwindow.demogs_dic


# Create the .csv file with conditions to be set in the experiment, starting from here
if len(demogs_dic) != 0:
    Consentformwin = ConsentFormWindow()
    Consentformwin.show()
    app.exec()

if Consentformwin.consent == True:
    #demogs_dic = Demogwindow.demogs_dic
    # This creates a dictionary with conditions per single trial
    trials_dictionary = trials_generator(conditions_dictionary, n_trials)

    # This creates a conditions_file.csv with all the conditions' values per trial
    input_file_name = "conditions_input"
    csv_generator(trials_dictionary, input_file_name)


    # Create a folder for the .csv outputs of the experiment
    data_folder = "data_output"
    if data_folder not in listdir():
        os.makedirs(data_folder, exist_ok=True) # if it already exists doesn't execute

    output_list = listdir(data_folder)
    if len(output_list) > 0:
        exp_number = len(output_list)
    else:
        exp_number = 0
    output_file_name = f"exp{exp_number}.csv"
    # Create the .csv output file in the data folder
    data_output_path = os.path.join(data_folder, output_file_name)
    output_current = open(data_output_path, "a")

    # Writing the first lines of 'output_current' .csv file
    # Get the demographics
    lines_writer(data_output_path, demogs_dic)

# The experiment can start only if the output file has been successfully created
output_file_path = f'data_output/{output_file_name}'
if os.path.exists(output_file_path):
    experiment_flow(input_file_name, data_output_path, keyboard_keys)
else:
    print(f"The output file is not in {output_file_path}!")
#
#
# END




