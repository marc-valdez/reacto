"""
Reaction Time Test Script

This script runs a reaction time test using video clips from the 'clips' directory.
It displays videos, measures reaction times, and shows results.
"""

from psychopy import prefs
prefs.hardware['audioLib'] = ['sounddevice']

from psychopy import visual
import os
from reaction_time import get_reaction_time
from results import display_result_screen, display_final_screen
from countdown import get_countdown_duration

# Initialize window
win = visual.Window(size=(2560, 1440), fullscr=True, checkTiming=False, color='black')

# Configuration
enable_countdown = True  # Set to False to disable countdown

# Data storage
valid_rt = []
last_duration = None

# Load video clips
clips_dir = 'clips'
clips = [clip for clip in os.listdir(clips_dir) if clip.endswith('.mp4')]

# Load movie stimuli
movies = {}
for clip in clips:
    video_path = os.path.join(clips_dir, clip)
    movies[clip] = visual.MovieStim(win, filename=video_path, size=(None, None))

# Main experiment loop
for clip in clips:
    video_path = os.path.join(clips_dir, clip)
    stimulus_frame = int(os.path.basename(video_path).split('_')[0])
    movie = movies[clip]

    # Determine countdown duration
    countdown_duration = get_countdown_duration(enable_countdown, last_duration)
    last_duration = countdown_duration

    # Measure reaction time
    rt_ms, reaction_type = get_reaction_time(video_path, win, stimulus_frame, enable_countdown, countdown_duration, movie=movie)
    print(f"{clip}: Reaction Time: {rt_ms:.2f} ms, Type: {reaction_type}")

    # Record valid reactions
    if reaction_type == 'pass':
        valid_rt.append(rt_ms)

    # Display result
    display_result_screen(win, rt_ms, reaction_type)

# Display final results
display_final_screen(win, valid_rt)

# Cleanup
win.close()
