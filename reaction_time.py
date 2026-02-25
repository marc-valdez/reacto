"""
Reaction Time Measurement Module

This module contains functions for measuring reaction times in response to video stimuli.
"""

from psychopy.visual import TextStim
from psychopy.event import Mouse

def get_reaction_time(win, movie, sound, stimulus_frame, framerate=60):
    """
    Measure reaction time to a stimulus in a video.

    Args:
        win: PsychoPy window object.
        movie: Pre-loaded MovieStim object.
        sound: Pre-loaded Sound object.
        stimulus_frame (int): Frame number where the stimulus appears.
        framerate: Video framerate as fallback/override.

    Returns:
        tuple: (reaction_time_ms, reaction_type) where reaction_type is 'pass', 'too-early', or 'too_late'.
    """

    frame_text = TextStim(win, text='Frame: 0', pos=(0.8, 0.9), color='white', height=0.05)
    
    # Line 1298 of psychopy\visual\movies\__init__.py
    # has a bug that makes movie.frameRate not work
    # replace `return self._player.metadata.frameRate`
    # with `return self._player._metadata.frameRate`
    framerate = (movie.frameRate if (movie.frameRate is not None) else framerate)
    stimulus_time = stimulus_frame / framerate

    print(f"frame@{stimulus_frame}, framerate@{movie.frameRate}")

    # Reset mouse for reaction measurement
    mouse = Mouse()
    mouse.clickReset(buttons=[0])

    # Main video playback loop
    movie.replay()
    sound.play()
    while not movie.isFinished:
        # Display movie
        movie.draw()
        frame = movie.movieTime * framerate
        frame_text.setText(f'Frame: {frame:.0f}')
        frame_text.draw()
        win.flip()

        # Check for input events
        pressed = mouse.getPressed()
        left_pressed = pressed[0]

        if left_pressed:
            reaction_time = movie.movieTime
            if reaction_time < stimulus_time:
                movie.pause()
                sound.stop()
                reaction_type = 'too-early'
            else:
                movie.unload() # Unload player from memory since we won't need it anymore.
                sound.stop()
                reaction_type = 'pass'
            delta = reaction_time - stimulus_time
            rt_ms = delta * 1000
            print(f"paused@{reaction_time} - stimulus@{stimulus_time} = delta@{delta}")
            break

    # If no reaction detected, mark as too late
    if 'reaction_type' not in locals():
        movie.pause()
        sound.stop()
        reaction_type = 'too_late'
        rt_ms = 0.0

    return rt_ms, reaction_type
