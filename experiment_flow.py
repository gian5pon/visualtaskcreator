from functions import *
from animation_stimuli import *
#import psychopy
from psychopy import visual, core
from psychopy.constants import (NOT_STARTED, STARTED, FINISHED)

from psychopy.hardware import keyboard


# This is the main function to be called to execute the experiment
# The arguments explicit the number of trials (and the parameters associated within every trial) in the form of either a
# dictionary 'trials_conditions', or a input file .csv, and the output file to use to write the output of the experiment
def experiment_flow(input, output_file, keyboard_input):

    experiment_output_list = [] # this is the main output of the experiment
    # It returns a list of dictionaries (one with key_resp and key_resp_rt per single trial) to be used to write
    # each row (per trial) of the output file

    # Extract conditions per each trial
    if isinstance(input, dict): # the argument passed is a dictionary
        trials_conditions = input
    else:  # if you want to read a .csv file instead, simply pass its name as a string without '.csv'
        trials_conditions = file_reader(input)

    endExpNow = False  # flag for 'escape' or other condition => quit the exp
    frameTolerance = 0.001  # how close to onset before 'same' frame


    # --- Setup the Window ---
    win = visual.Window(
        fullscr=True, screen=0,
        winType='pyglet', allowStencil=False,
        monitor='testMonitor', color=[0, 0, 0], colorSpace='rgb',
        blendMode='avg', useFBO=True,
        units='height')

    win.mouseVisible = False

    # set up a default keyboard for proceed after the instructions
    defaultKeyboard = keyboard.Keyboard()


    # Start Code -> code to be run after the window creation

    # --- Initialize components for Routine "instructions" ---
    # Present some instructions. The parameters (target and distractors specs) are taken from the dictionary
    # Retrieve conditions for the instructions:
    conditions_dic = trials_conditions["trial1"]
    keyboard_key1 = keyboard_input[0]
    keyboard_key2 = keyboard_input[-1]
    target_shape = str(conditions_dic["target_shape"]).upper()
    target_color = str(conditions_dic["target_color"]).upper()
    distractors_shape = conditions_dic["distractor_shape"]
    distractors_color = conditions_dic["distractor_color"]
    instructions_text = f"Hello participant! You are going to be presented with an array of objects, and your aim is to " \
                        f"individuate the target stimulus in the scene.\nThe target can be either present or absent." \
                        f"\nIn case it is present, you will press '{keyboard_key1}', while if it is not present " \
                        f"you will press '{keyboard_key2}'.\nIt is important that you press the key as fast as possible." \
                        f"\nIn this experiment, your target stimulus will be a {target_color} {target_shape}.\nYou will also " \
                        f"see a variety of 'distractor' objects.\nTheir shape will be {distractors_shape} and " \
                        f"their color will be {distractors_color}.\nPress any key whenever you are ready to START!"

    instructions_text = visual.TextStim(win=win, text=instructions_text, height=0.04, pos=[0, 0])

    instructions_text.draw()
    win.flip()
    key_press = defaultKeyboard.waitKeys()

    # to track time remaining of each routine
    routineTimer = core.Clock()

    # Extract a list containing the total number of trials to run in this experiment
    trials = trials_conditions.keys()


    # START THE TRIALS
    if key_press:

        # Looping over the list containing the number of trials to display
        for thisTrial in trials:

            # Extract the nested dictionary with conditions as keys, and parameters as values
            conditions_dic = trials_conditions[f"{thisTrial}"]

            # This returns a small dictionary with keys pressed (if any) and reaction times
            experiment_output_dic = {}

            # define target as a global variable, to be looked for in every subloop within the function
            global target


            # --- Prepare to start Routine "trial" ---
            continueRoutine = True
            routineForceEnded = False

            # update parameters for each repeat
            # --- Initialize components for Routine "trial" ---


            # Angles of moving direction to use in case ANIMATION is toggled for distractors
            angles_list = []

            stim_size = 0.1
            angle = uniform(0, 360)
            angles_list.append(angle)

            # POSITIONING of the stimuli
            positions_list = random_positions(stim_size)


            # TARGET
            target = visual.ShapeStim(
                win=win, name='target',
                size=(0.1, 0.1), vertices=conditions_dic['target_shape'],
                ori=0.0, pos=[0, 0], anchor='center',
                lineWidth=1.0, colorSpace='rgb', fillColor=conditions_dic['target_color'],
                opacity=None, depth=0.0, interpolate=True)

            target.pos = positions_list.pop()

            # FIXATION CROSS
            fixation = visual.ShapeStim(
                win=win, name='fixation', vertices='cross',
                size=(0.1, 0.1),
                ori=0.0, pos=(0, 0), anchor='center',
                lineWidth=1.0, colorSpace='rgb', lineColor='white', fillColor='white',
                opacity=None, depth=-3.0, interpolate=True)

            # Set up the Keyboard
            key_resp = keyboard.Keyboard()


            # Number of DISTRACTORS as defined by experimenter
            n_distractors = int(conditions_dic['n_distractors'])
            distractors_list = []
            shapes_list = ['triangle', 'rectangle', 'circle']
            color_list = ['red', 'blue']
            count = 0

            if conditions_dic['distractor_shape'] == 'random':
                distractors_shapes = equal_distribution(shapes_list, n_distractors)
            else:
                distractors_shapes = []
                for n in range(n_distractors):
                    distractors_shapes.append(conditions_dic['distractor_shape'])

            if conditions_dic['distractor_color'] == 'random':
                distractors_colors = equal_distribution(color_list, n_distractors)
            else:
                distractors_colors = []
                for n in range(n_distractors):
                    distractors_colors.append(conditions_dic['distractor_color'])


            for n in range(n_distractors):
                count += 1
                angle = uniform(0, 360)
                angles_list.append(angle)
                distractor = visual.ShapeStim(
                    win=win, name='distractor', vertices=distractors_shapes.pop(),
                    size=(0.1, 0.1),
                    ori=0.0, pos=positions_list.pop(), anchor='center',
                    lineWidth=1.0, colorSpace='rgb', fillColor=distractors_colors.pop(),
                    opacity=None, depth=-2.0, interpolate=True)

                distractors_list.append(distractor)

            # Create the distractors
            for distractor in distractors_list:
                distractor.setAutoDraw(True)


            # Lists for storing input
            key_resp.keys = []
            key_resp.rt = []
            _key_resp_allKeys = []


            # Keep track of which components have finished
            # This is a list of timed components of the routine. Add any here.
            # It is helpful e.g. if one wants to allow for mouse resp.
            # In this version of the program the only timed component is the fixation cross.
            trialComponents = [fixation]
            for thisComponent in trialComponents:
                thisComponent.tStart = None
                thisComponent.tStop = None
                thisComponent.tStartRefresh = None
                thisComponent.tStopRefresh = None
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED

            # reset timers
            t = 0
            _timeToFirstFrame = win.getFutureFlipTime(clock="now")
            frameN = -1

            # --- Run Routine "trial" ---
            while continueRoutine and routineTimer.getTime() < 5:
                # get current time
                t = routineTimer.getTime()
                tThisFlip = win.getFutureFlipTime(clock=routineTimer)
                tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)

                # update/draw components on each frame

                # TARGET updates
                if conditions_dic['target_presence'] == "1":
                    if target.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
                        # keep track of start time/frame for later
                        target.frameNStart = frameN
                        target.tStart = t
                        target.tStartRefresh = tThisFlipGlobal  # on global time
                        win.timeOnFlip(target, 'tStartRefresh')  # time at next scr refresh

                        target.setAutoDraw(True)

                # ANIMATION -> the experimenter can choose whether display moving distractors
                speed = 0.005


                if conditions_dic['movement'] == 'scatter': # if the experimenter has chosen the option, then...
                    animating_stimuli(distractors_list, angles_list, speed)


                # KEY_RESP updates
                waitOnFlip = False
                if key_resp.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
                    # keep track of start time/frame for later
                    key_resp.frameNStart = frameN
                    key_resp.tStart = t
                    key_resp.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(key_resp, 'tStartRefresh')  # time at next scr refresh
                    key_resp.status = STARTED
                    # keyboard checking is just starting
                    waitOnFlip = True
                    win.callOnFlip(key_resp.clock.reset)
                    win.callOnFlip(key_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip

                if key_resp.status == STARTED and not waitOnFlip:
                    theseKeys = key_resp.getKeys(keyList=keyboard_input, waitRelease=False)
                    _key_resp_allKeys.extend(theseKeys)
                    if len(_key_resp_allKeys):
                        key_resp.keys = _key_resp_allKeys[-1].name  # just the last key pressed
                        key_resp.rt = _key_resp_allKeys[-1].rt
                        # a response ends the routine
                        continueRoutine = False

                # FIXATION updates
                if fixation.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
                    # keep track of start time/frame for later
                    fixation.frameNStart = frameN  # exact frame index
                    fixation.tStart = t  # local t and not account for scr refresh
                    fixation.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(fixation, 'tStartRefresh')  # time at next scr refresh
                    fixation.setAutoDraw(True)
                if fixation.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > fixation.tStartRefresh + 1.0 - frameTolerance:
                        # keep track of stop time/frame for later
                        fixation.tStop = t  # not accounting for scr refresh
                        fixation.frameNStop = frameN  # exact frame index
                        fixation.setAutoDraw(False)

                # check for quit (typically the Esc key)
                if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                    core.quit()

                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    routineForceEnded = True
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in trialComponents:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished

                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()


            # --- Ending Routine "trial" ---

            # Eliminate stimuli from the screen
            for thisComponent in trialComponents:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)

            if conditions_dic["target_presence"] == "1":
                target.setAutoDraw(False)

            for distractor in distractors_list:
                distractor.setAutoDraw(False)


            # CHECK RESPONSES
            # populate the output dictionary with conditions_dic
            if key_resp.keys in ['', [], None]:  # No response was made
                key_resp.keys = "na"
                key_resp.rt = "na"
            experiment_output_dic["key_resp"] = key_resp.keys

            if key_resp.keys != ["na"]:  # we had a response
                experiment_output_dic["key_resp_time"] = f"{key_resp.rt}"


            # populate the list with all the responses per trial (1 entry = 1 trial)
            experiment_output_list.append(experiment_output_dic)

            # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
            if routineForceEnded:
                routineTimer.reset()
            else:
                routineTimer.addTime(-5.000000)

    ################################################
    # LOOP CLOSES -> completed 1 repeats of 'trials'
    ################################################

    # --- End experiment ---
    # Write the output_file .csv before closing

    # Retrieve the conditions_dic common for all trials
    conditions = trials_conditions["trial1"].keys()
    conditions_str = ",".join(conditions)
    # create the first line with conditions_dic and parameters labels
    first_line = f"{conditions_str},keyboard_keys,key_resp,key_resp_time\n"

    # Write the first row of the output_file
    output_csv = open(f"{output_file}", "a")
    output_csv.write(first_line)

    # Looping per trial in the trials dictionary
    trials = trials_conditions.keys()
    count = 0
    # append one row per trial
    for trial in trials:
        count += 1
        conditions_values = trials_conditions[f"{trial}"].values() # get the parameters for each played trial
        conditions_values_str = ",".join(conditions_values)
        output = experiment_output_list[count-1].values() # get the outputs (ordered list -> 1 element = 1 trial)
        output_str = ",".join(output)
        output_final = f"{conditions_values_str},[{keyboard_input}],{output_str}"
        output_csv.write(f"{output_final}\n")

    # QUIT functions
    output_csv.close()
    win.flip()
    win.close()
    core.quit()