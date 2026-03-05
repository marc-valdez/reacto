"""
Reaction Time Test Script

This script runs a reaction time test using video clips from the 'clips' directory.
It displays videos, measures reaction times, and shows results.
"""

import sys
import time

from pathlib import Path
from psychopy.visual import Window
from psychopy.monitors import Monitor

from reaction_time import get_reaction_time
from results import display_result_screen, display_final_screen
from countdown import CountdownManager
from export import export_results
from config import Config
from auth import authenticate
from tutorial import run_tutorial, confirm_tutorial
from asset_loader import load_clips

# Global Base Path
if getattr(sys, 'frozen', False):
    base_path = Path(sys.executable).parent
else:
    base_path = Path(__file__).parent

# Configuration
config = Config(base_path)
enable_countdown = config.get_boolean('app', 'enable_countdown', True)
countdown_durations = config.get_int_list('app', 'countdown_durations', [3, 4, 5])
countdown_manager = CountdownManager(countdown_durations)
clips_dir = config.get_string('app', 'clips_directory', 'clips')

# Authentication
client, session = None, None
if config.get_boolean('auth', 'enable_supabase', False):
    print("Authenticating with Supabase...")
    client, session = authenticate(config)

# Initialize window
mon = Monitor(name='monitor', width=config.get_int('display', 'window_width', 1920))
win = Window(
    monitor=mon, checkTiming=False, color='black',
    size=(config.get_int('display', 'window_width', 1920), config.get_int('display', 'window_height', 1080)), 
    allowGUI=not config.get_boolean('display', 'borderless', False), 
    fullscr=config.get_boolean('display', 'fullscreen', False)
)

# Onboard participants with tutorial
enable_tutorial = confirm_tutorial(win)
if enable_tutorial: run_tutorial(win, base_path)

# Data storage
results = []
averages = {
    "default": [],
    "deuteranopia": [],
    "protanopia": [],
    "tritanopia": [],
}

# Load randomized clips
clips, movies, sounds = load_clips(win, base_path, clips_dir, randomize=True)

# Capture start time
start_time = time.time()

# Main experiment loop
while clips:
    clip = clips.pop(0)

    # Get clip information from filename
    filename = clip.split('.')[0].split('_')
    stimulus_frame = int(filename[0])
    color_mode = filename[1]
    game = filename[2]

    movie = movies[clip]
    sound = sounds[clip]

    # Countdown phase
    countdown_manager.perform_countdown(win, enable_countdown)

    # Measure reaction time
    rt_ms, verdict = get_reaction_time(win, movie, sound, stimulus_frame)
    print(f"[{clip}] Reaction Time: {rt_ms} ms, Verdict: {verdict}")

    # Update rolling average
    if verdict == 'pass':
        averages[color_mode].append(rt_ms)
        print(f"Rolling Average of {color_mode}: {sum(averages[color_mode]) / len(averages[color_mode])}\n")

    # Record reaction
    results.append({
        'filename': clip,
        'rt_ms': rt_ms, 
        'verdict': verdict,
        'stimulus_frame': stimulus_frame,
        'color_mode': color_mode,
        'game': game,
    })

    # Display result
    display_result_screen(win, rt_ms, verdict)

# Record end time and print total duration
end_time = time.time()
test_duration = end_time - start_time
print(f"Test took: {test_duration} seconds")

# Export results
export_results(results, test_duration, client)

# Display final results
display_final_screen(win, averages)

# Cleanup
win.close()
if session:
    response = client.table("participants").update({
        "test_duration": test_duration
    }).eq("id", session.user.id).execute()
    print("Signing out from Supabase...")
    client.auth.sign_out()
