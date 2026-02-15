"""
Reaction Time Measurement Module

This module contains functions for measuring reaction times in response to video stimuli.
"""

from psychopy.visual import TextStim, MovieStim
from psychopy.core import Clock
from psychopy.event import Mouse, getKeys

def get_reaction_time(movie, win, stimulus_frame, framerate=60):
    """
    Measure reaction time to a stimulus in a video.

    Args:
        movie: Pre-loaded MovieStim object.
        win: PsychoPy window object.
        stimulus_frame (int): Frame number where the stimulus appears.
        framerate: Video framerate as fallback/override.

    Returns:
        tuple: (reaction_time_ms, reaction_type) where reaction_type is 'pass', 'too-early', or 'too_late'.
    """
    # Initialize stimuli and clock
    frame_text = TextStim(win, text='Frame: 0', pos=(0.8, 0.9), color='white', height=0.05)
    clock = Clock()

    # Line 1298 of psychopy\visual\movies\__init__.py
    # has a bug that makes movie.frameRate not work
    # replace `return self._player.metadata.frameRate`
    # with `return self._player._metadata.frameRate`
    stimulus_time = stimulus_frame / (movie.frameRate if (movie.frameRate is not None) else framerate)
    frame_counter = 0

    # Reset clock and mouse for reaction measurement
    clock.reset()
    mouse = Mouse()
    mouse.clickReset(buttons=[0])

    # Main video playback loop
    movie.replay()
    while not movie.isFinished:
        # Frame display logic
        frame_counter += 1
        frame_text.setText(f'Frame: {frame_counter}')
        frame_text.draw()
        
        # Display movie
        movie.draw()
        win.flip()

        # Check for input events
        keys = getKeys(keyList=['escape'], timeStamped=clock)
        pressed, times = mouse.getPressed(getTime=True)
        left_pressed = pressed[0]

        # Detect reaction
        if keys and keys[0][0] == 'escape':
            movie.pause() # Only pause but don't unload the player from memory.
            break
        elif left_pressed:
            reaction_time = movie.movieTime
            if reaction_time < stimulus_time:
                movie.pause()
                reaction_type = 'too-early'
            else:
                movie.unload() # Unload player from memory since we won't need it anymore.
                reaction_type = 'pass'
            rt_ms = (reaction_time - stimulus_time) * 1000
            break

    # If no reaction detected, mark as too late
    if 'reaction_type' not in locals():
        movie.pause()
        reaction_type = 'too_late'
        rt_ms = (movie.duration - stimulus_time) * 1000

    return rt_ms, reaction_type
