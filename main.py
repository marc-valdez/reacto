"""
Reaction Time Test Script

This script runs a reaction time test using video clips from the 'clips' directory.
It displays videos, measures reaction times, and shows results.
"""

import os
import sys
import random
from psychopy.visual import Window, MovieStim, TextStim
from psychopy.monitors import Monitor
from reaction_time import get_reaction_time
from results import display_result_screen, display_final_screen
from countdown import CountdownManager

# Initialize window
mon = Monitor(name='monitor', width=1440)
win = Window(monitor=mon, size=(2560, 1440), allowGUI=False, fullscr=False, checkTiming=False, color='black')

# Configuration
enable_countdown = True                    # Set to False to disable countdown
countdown_durations = list(range(3, 5))    # Adjustable list of possible countdown durations (default from 3 to 5 seconds)
countdown_manager = CountdownManager(countdown_durations)

# Data storage
valid_rt = []

# Load video clips
if getattr(sys, 'frozen', False):
    # Running as bundled executable
    clips_dir = os.path.join(os.path.dirname(sys.executable), 'clips')
else:
    # Running in development
    clips_dir = 'clips'
clips = [clip for clip in os.listdir(clips_dir) if clip.endswith('.mp4')]
random.shuffle(clips)

# Preload movies
loading_text = TextStim(win, color='white', height=0.05)
movies = {}
for clip in clips:
    video_path = os.path.join(clips_dir, clip)
    try:
        print(f"Loading...{clip}")
        loading_text.setText(f"Loading...{clip}")
        loading_text.draw()
        movies[clip] = MovieStim(win, filename=video_path, size=win.size, autoStart=False)
        win.flip()
    except RuntimeError as e:
        print(f"Failed to load {clip}: {e}")
        exit(1)

# Main experiment loop
while clips:
    clip = clips.pop(0)
    video_path = os.path.join(clips_dir, clip)
    stimulus_frame = int(os.path.basename(video_path).split('_')[0])
    movie = movies[clip]

    # Countdown phase
    countdown_manager.perform_countdown(win, enable_countdown)

    # Measure reaction time
    rt_ms, reaction_type = get_reaction_time(movie, win, stimulus_frame)
    print(f"\n[{clip}] Reaction Time: {rt_ms} ms, Type: {reaction_type}")

    # Record valid reactions
    if reaction_type == 'pass':
        valid_rt.append(rt_ms)
    else:
        # Re-queue the clip for retry
        clips.append(clip)

    # Display result
    display_result_screen(win, rt_ms, reaction_type)

# Display final results
display_final_screen(win, valid_rt)

# Cleanup
win.close()
