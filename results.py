"""
Results Display Module

Functions for displaying result screens in the reaction time test.
"""

from psychopy.visual import TextStim
from psychopy.event import waitKeys

def display_result_screen(win, rt_ms, reaction_type):
    """Display the result screen after each reaction time measurement."""
    if reaction_type == 'pass':
        main_text = f"{rt_ms:.1f} ms"
        main_color = 'green'
        subtitle_text = "Reaction Time"
    elif reaction_type == 'too-early':
        main_text = "Too Early"
        main_color = 'red'
        subtitle_text = "Miss"
    else:
        main_text = "Too Late"
        main_color = 'grey'
        subtitle_text = "Miss"

    main_stim = TextStim(win, text=main_text, pos=(0, 0.3), color=main_color, height=0.2)
    subtitle_stim = TextStim(win, text=subtitle_text, pos=(0, 0.1), color='white', height=0.05)
    next_stim = TextStim(win, text="Press SPACE to continue", pos=(0, -0.2), color='white', height=0.05)
    main_stim.draw()
    subtitle_stim.draw()
    next_stim.draw()
    win.flip()
    waitKeys(keyList=['space'])

def display_final_screen(win, valid_rt):
    """Display the final screen with average reaction time or no data message."""
    if valid_rt:
        final_average = sum(valid_rt) / len(valid_rt)
        main_text = f"{final_average:.1f} ms"
        main_color = 'green'
        subtitle_text = "Average Reaction Time"
    else:
        main_text = "No Data"
        main_color = 'white'
        subtitle_text = "No valid reactions"

    main_stim = TextStim(win, text=main_text, pos=(0, 0.3), color=main_color, height=0.2)
    subtitle_stim = TextStim(win, text=subtitle_text, pos=(0, 0.1), color='white', height=0.05)
    continue_stim = TextStim(win, text="Press SPACE to exit", pos=(0, -0.2), color='white', height=0.05)
    main_stim.draw()
    subtitle_stim.draw()
    continue_stim.draw()
    win.flip()
    waitKeys(keyList=['space'])