"""
Reaction Time Measurement Module

This module contains functions for measuring reaction times in response to video stimuli.
"""

import math
import random
from psychopy import prefs
prefs.hardware['audioLib'] = ['sounddevice']

from psychopy import visual, core, event

def get_reaction_time(movie, win, stimulus_frame):
    """
    Measure reaction time to a stimulus in a video.

    Args:
        movie: Pre-loaded MovieStim object.
        win: PsychoPy window object.
        stimulus_frame (int): Frame number where the stimulus appears.

    Returns:
        tuple: (reaction_time_ms, reaction_type) where reaction_type is 'pass', 'too-early', or 'too_late'.
    """
    # Initialize stimuli and clock
    frame_text = visual.TextStim(win, text='Frame: 0', pos=(0.8, 0.9), color='white', height=0.05)
    clock = core.Clock()

    try:
        stimulus_time = stimulus_frame / movie.frameRate
    except AttributeError:
        stimulus_time = 0  # Fallback if frameRate is not available
    frame_counter = 0

    # Reset clock and mouse for reaction measurement
    clock.reset()
    mouse = event.Mouse()
    mouse.clickReset(buttons=[0])
    left_pressed_prev = False

    # Main video playback loop
    while not movie.isFinished:
        frame_counter += 1
        movie.draw()
        frame_text.setText(f'Frame: {frame_counter}')
        frame_text.draw()
        win.flip()

        # Check for input events
        keys = event.getKeys(keyList=['escape'], timeStamped=clock)
        pressed, times = mouse.getPressed(getTime=True)
        left_pressed = pressed[0]

        # Detect reaction
        if keys or (left_pressed and not left_pressed_prev):
            if keys:
                if keys[0][0] == 'escape':
                    break
            elif left_pressed and not left_pressed_prev:
                reaction_time = movie.movieTime
                if reaction_time < stimulus_time:
                    reaction_type = 'too-early'
                else:
                    reaction_type = 'pass'
                rt_ms = (reaction_time - stimulus_time) * 1000
                break

        left_pressed_prev = left_pressed

    # If no reaction detected, mark as too late
    if 'reaction_type' not in locals():
        reaction_type = 'too_late'
        rt_ms = (movie.duration - stimulus_time) * 1000

    # Cleanup
    movie.stop()
    return rt_ms, reaction_type
