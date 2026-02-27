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

def display_final_screen(win, averages):
    """Display the final screen with total average and per color mode averages."""
    if not averages:
        main_text = "No Data"
        main_color = 'white'
        detail_text = "No valid reactions"
    else:
        # Total average
        total_avg = sum([sum(times) / len(times) for times in averages.values() if times]) / len(averages) if averages else 0
        main_text = f"{total_avg:.1f} ms"
        main_color = 'green'
        
        # Averages per color mode
        detail_lines = [] 
        for color, times in averages.items():
            avg = sum(times) / len(times) if times else 0
            detail_lines.append(f"{color.capitalize()}: {avg:.1f} ms")
        detail_text = "\n".join(detail_lines)

    main_stim = TextStim(win, text=main_text, pos=(0, 0.3), color=main_color, height=0.25)
    subtitle_stim = TextStim(win, text="Average Reaction Time", pos=(0, 0.1), color='white', height=0.05)
    detail_stim = TextStim(win, text=detail_text, pos=(0, -0.1), color='white', height=0.05)
    exit_stim = TextStim(win, text="Press SPACE to exit", pos=(0, -0.3), color='white', height=0.05)
    
    main_stim.draw()
    subtitle_stim.draw()
    detail_stim.draw()
    exit_stim.draw()

    win.flip()
    waitKeys(keyList=['space'])
