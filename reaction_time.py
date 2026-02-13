"""
Reaction Time Measurement Module

This module contains functions for measuring reaction times in response to video stimuli.
"""

import math
import random
from psychopy import prefs
prefs.hardware['audioLib'] = ['sounddevice']

from psychopy import visual, core, event

def get_reaction_time(video_path, win, stimulus_frame, enable_countdown=True, countdown_duration=None, movie=None):
    """
    Measure reaction time to a stimulus in a video.

    Args:
        video_path (str): Path to the video file.
        win: PsychoPy window object.
        stimulus_frame (int): Frame number where the stimulus appears.
        enable_countdown (bool): Whether to show a countdown before the video.
        countdown_duration (float): Duration of the countdown in seconds.
        movie: Pre-loaded MovieStim object (optional).

    Returns:
        tuple: (reaction_time_ms, reaction_type) where reaction_type is 'pass', 'too-early', or 'too_late'.
    """
    # Initialize stimuli and clock
    frame_text = visual.TextStim(win, text='Frame: 0', pos=(0.8, 0.9), color='white', height=0.05)
    if movie is None:
        movie = visual.MovieStim(win, filename=video_path, size=(None, None))
    clock = core.Clock()

    stimulus_time = stimulus_frame / movie.frameRate
    frame_counter = 0

    # Countdown phase
    if enable_countdown:
        countdown_text = visual.TextStim(win, text='', pos=(0, 0), color='white', height=0.5)
        countdown_duration = countdown_duration if countdown_duration is not None else random.uniform(3, 5)
        countdown_start = clock.getTime()
        while True:
            elapsed = clock.getTime() - countdown_start
            if elapsed >= countdown_duration:
                break
            remaining = countdown_duration - elapsed
            display_num = math.ceil(remaining)
            if display_num <= 0:
                break
            countdown_text.setText(f'{display_num}')
            countdown_text.draw()
            win.flip()
            keys = event.getKeys(keyList=['escape'])
            if keys:
                break

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
    movie.unload()
    return rt_ms, reaction_type
