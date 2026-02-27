"""
Reaction Time Test Script

This script runs a reaction time test using video clips from the 'clips' directory.
It displays videos, measures reaction times, and shows results.
"""

import os
import sys
import random
from psychopy.visual import Window, MovieStim, TextStim
from psychopy.sound import Sound
from psychopy.monitors import Monitor
from reaction_time import get_reaction_time
from results import display_result_screen, display_final_screen
from countdown import CountdownManager
from export import export_results
import auth
from config import config

# Authenticate user
auth_code = auth.authenticate()

# Initialize window
mon = Monitor(name='monitor', width=config.get_int('display', 'monitor_width', 1080))
win = Window(monitor=mon, size=(config.get_int('display', 'window_width', 1920), config.get_int('display', 'window_height', 1080)), allowGUI=False, fullscr=config.get_boolean('display', 'fullscreen', False), checkTiming=False, color='black')

# Configuration
enable_countdown = config.get_boolean('app', 'enable_countdown', True)
countdown_durations = config.get_int_list('app', 'countdown_durations', [3, 4, 5])
countdown_manager = CountdownManager(countdown_durations)

# Data storage (dict: clip_name -> {'rt_ms': float, 'type': str})
results = {}

# Load video clips
if getattr(sys, 'frozen', False):
    # Running as bundled executable
    clips_dir = os.path.join(os.path.dirname(sys.executable), config.get_string('app', 'clips_directory', 'clips'))
else:
    # Running in development
    clips_dir = config.get_string('app', 'clips_directory', 'clips')
clips = [clip for clip in os.listdir(clips_dir) if clip.endswith('.mp4')]

# Preload movies and sounds
"""Add to .venv\Lib\site-packages\psychopy\sound\backend_ptb.py
after Line 264 to fix issues on audio devices with channels > 2
```
    # pad channels if needed
    if clip.samples.shape[1] < self.speaker.channels:
        padding = np.zeros((clip.samples.shape[0], int(self.speaker.channels - clip.samples.shape[1])))
        clip.samples = np.hstack((clip.samples, padding))
```
"""
loading_text = TextStim(win, color='white', height=0.05)
movies = {}
sounds = {}
for clip in clips:
    video_path = os.path.join(clips_dir, clip)
    wav_path = os.path.join(clips_dir, clip.replace('.mp4', '.mp3'))
    try:
        print(f"Loading... {clip}")
        loading_text.setText(f"Loading... {clip}")
        loading_text.draw()
        win.flip()

        if os.path.exists(wav_path):
            sounds[clip] = Sound(wav_path)
        else:
            sounds[clip] = None
        movies[clip] = MovieStim(win, filename=video_path, size=win.size, autoStart=False)
    except RuntimeError as e:
        print(f"Failed to load {clip}: {e}")
        exit(1)

# Randomize clips
random.shuffle(clips)

# Main experiment loop
while clips:
    clip = clips.pop(0)
    video_path = os.path.join(clips_dir, clip)
    stimulus_frame = int(os.path.basename(video_path).split('_')[0])
    movie = movies[clip]
    sound = sounds[clip]

    # Countdown phase
    countdown_manager.perform_countdown(win, enable_countdown)

    # Measure reaction time
    rt_ms, verdict = get_reaction_time(win, movie, sound, stimulus_frame)
    print(f"\n[{clip}] Reaction Time: {rt_ms} ms, Type: {verdict}\n")

    # Record reaction
    clip_name = clip.replace('.mp4', '')  # Remove extension for key
    results[clip_name] = {'rt_ms': rt_ms, 'type': verdict}

    # Display result
    display_result_screen(win, rt_ms, verdict)

# Export results
export_results(results, auth_code)

# Display final results
display_final_screen(win, results)

# Cleanup
win.close()
