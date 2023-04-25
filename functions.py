from packages import *


def lines_writer(file_name, data):
    # It writes rows according to the type of data is being fed.
    # 1. In case of a dictionary, it writes all the keys as a row, and all the values as second row.
    # 2. In case of a list, it just writes the elements
    with open(f"{file_name}", 'a', newline='') as file:
        writer = csv.writer(file)
        if isinstance(data, dict):
            writer.writerow(data.keys())
            writer.writerow(data.values())
        elif isinstance(data, list):
            writer.writerow(data)

        file.close()


# Opens the conditions_file file and produces a dictionary with trials as keys and unique values per trial as values
def file_reader(file_name):
    conditions_dic = {}  # this is the output

    trials_conditions = open(f"{file_name}.csv", "r")
    all_lines = trials_conditions.readlines()
    conditions_list = all_lines[0].split(",")  # the first line is just conditions labels
    trials_conditions.close()

    for n in range(len(all_lines)):
        if n >= 1:  # skips the first line with conditions label
            values_str = all_lines[n][:-1]
            values_list = values_str.split(",")
            conditions_dic[f"trial{n}"] = dict(zip(conditions_list, values_list))

    return conditions_dic


# gets a list of elements and produces a list of equally distributed elements of lenght n
def equal_distribution(elements_list, length):
    # Create a copy of the list not to modify the original
    elements_copy = elements_list[:]
    # Create an empty result list
    result = []
    # Repeat until the result list has the desired length
    while len(result) < length:
        # Choose a random element from the elements list
        element = randchoice(elements_copy)
        # Add the item to the result list
        result.append(element)
        # Remove the item from the elements list so it's not chosen again
        elements_copy.remove(element)
        # If all elements have been chosen, start over with the full list
        if not elements_copy:
            elements_copy = elements_list[:]
    return result


def trials_generator(conditions_dic, n_trials):
    # It creates a dictionary with 'trial#' as keys, and dictionaries of conditions' parameters as values
    # It takes a dictionary with conditions labels as keys, and all the possible values their parameter can take
    # across trials.

    trials_dic = {}  # final output
    conditions_trials_dic = {} # store randomly (but equally) distributed values per condition per trial
    conditions = conditions_dic.keys()


   # Extract the values per condition
    for condition in conditions:
        values_str = conditions_dic[f"{condition}"].replace(" ", "")
        if condition == "keyboard_keys":
            values_list = [f"{values_str}"]
        else:
            values_list = values_str.split(",")

        if condition == "target_presence":
        # this distributes uniformly random the presence of target across trials as established by the experimenter
            target_presence = int(conditions_dic["target_presence"])
            rand_values = []
            count = 0
            for i in range(n_trials):
                if count < target_presence:
                    rand_values.append("1")
                    count += 1
                else:
                    rand_values.append("0")
            np.random.shuffle(rand_values)
        else:
            rand_values = equal_distribution(
            values_list, n_trials)  # distributes randomly but equally the conditions' values per n_trials

        conditions_trials_dic[f"{condition}"] = rand_values

    count = 0
    for t in range(n_trials):
        trials_conditions_dic = {}  # a dictionary of conditions as keys and condition values as values
        count += 1

        for condition in conditions:
            values_str = conditions_trials_dic[f"{condition}"]  # get the randomly distributed values per condition
            trial_value = values_str[
                count - 1]  # gets the single value per single trial from the list of randomly distributed values
            trials_conditions_dic[f"{condition}"] = trial_value

        # populate the final output
        trials_dic[f"trial{count}"] = trials_conditions_dic

    return trials_dic


#trials_dic = trials_generator(conditions_dic, n_trials)
#print(trials_dic)

def csv_generator(trials_dictionary, name_file):
    # It takes a dictionary with all the trials as argument
    # The csv_generator generates 'conditions_file.csv' which is then use for setting up the experiment

    # Create the output file
    conditions_file = open(f"{name_file}.csv", "w")

    # Access the conditions' keys
    conditions_keys = trials_dictionary["trial1"].keys()

    # Write the first row (with conditions names)
    count = 0
    for condition in conditions_keys:
        count += 1
        conditions_file.write(f"{condition},")

        if count == len(conditions_keys):
            conditions_file.write(f"{condition}\n")

    # Loop over the dictionary of trials to retrieve the conditions' dictionaries
    trials_keys = trials_dictionary.keys()
    for trial in trials_keys:
        conditions_dic = trials_dictionary[f"{trial}"]  # access the conditions' dictionary
        conditions_keys = conditions_dic.keys()
        values_str = ""

        # Extract the conditions per trial
        for condition in conditions_keys:
            value = conditions_dic[f"{condition}"]  # access value per condition
            values_str = values_str + f"{value},"

        conditions_file.write(f"{values_str[:-1]}\n")  # write one row per trial

    conditions_file.close()


#csv_generator(trials_dic)