import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, radians, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)


# this function returns an array of randomly shuffled possible positions the stimuli can occupy
# within the experiment window. It takes the size of the stimulus as parameter to avoid overlappings
def random_positions(stimuli_size):
    positions_list = []
    for x in np.arange(-0.45, 0.5, stimuli_size + 0.05):
        for y in np.arange(-0.45, 0.5, stimuli_size + 0.05):
            positions_list.append((x, y))

    np.random.shuffle(positions_list)
    return positions_list

# this is the animation function which leverages psychopy '.pos' function for drawing the stimuli.
# It takes a list of stimuli, a list of directions' angles, and a 'speed' parameter as arguments
def animating_stimuli(stimuli_list, angles_list, speed):
    count = 0
    for stimulus in stimuli_list:
        # assign a random direction to each distractor
        count += 1
        direction_x = cos(angles_list[count])
        direction_y = sin(angles_list[count])

        # update the direction if the stimulus position is out of bounds
        if stimulus.pos[0] <= -0.5 or stimulus.pos[0] >= 0.5:
            angle = angles_list[count] + 180
            angles_list[count] = angle
            direction_x = cos(angle)

        if stimulus.pos[1] <= -0.5 or stimulus.pos[1] >= 0.5:
            angle = angles_list[count] + 180
            angles_list[count] = angle
            direction_y = sin(angle)

        # 'speed' indicates the range of the step per frame that the stimulus will make
        stimulus.pos += (direction_x * speed,
                           direction_y * speed)