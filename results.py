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

def display_final_screen(win, results):
    """Display the final screen with total average and per color mode averages."""
    if not results:
        main_text = "No Data"
        main_color = 'white'
        bottom_text = "No valid reactions"
    else:
        # Group results by color mode
        color_groups = {}
        all_rts = []
        for clip_name, data in results.items():
            rt = data['rt_ms']
            reaction_type = data['type']
            if reaction_type == 'pass':
                parts = clip_name.split('_')
                if len(parts) >= 2:
                    color_mode = parts[1]
                    if color_mode not in color_groups:
                        color_groups[color_mode] = []
                    color_groups[color_mode].append(rt)
                    all_rts.append(rt)
        
        # Total average
        total_avg = sum(all_rts) / len(all_rts) if all_rts else 0
        main_text = f"{total_avg:.1f} ms"
        main_color = 'green'
        
        # Bottom text: averages per color mode
        bottom_lines = []
        for color in ['default', 'deuteranopia', 'protanopia', 'tritanopia']:
            if color in color_groups:
                rt_list = color_groups[color]
                avg = sum(rt_list) / len(rt_list)
                bottom_lines.append(f"{color.capitalize()}: {avg:.1f} ms")
            else:
                bottom_lines.append(f"{color.capitalize()}: No data")
        bottom_text = "\n".join(bottom_lines)

    main_stim = TextStim(win, text=main_text, pos=(0, 0.3), color=main_color, height=0.25)
    subtitle_stim = TextStim(win, text="Average Reaction Time", pos=(0, 0.1), color='white', height=0.05)
    detail_stim = TextStim(win, text=bottom_text, pos=(0, -0.1), color='white', height=0.05)
    continue_stim = TextStim(win, text="Press SPACE to exit", pos=(0, -0.3), color='white', height=0.05)
    main_stim.draw()
    subtitle_stim.draw()
    detail_stim.draw()
    continue_stim.draw()
    win.flip()
    waitKeys(keyList=['space'])