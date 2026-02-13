from psychopy import prefs
prefs.hardware['audioLib'] = ['sounddevice']

from psychopy import visual
import os
import random
from reaction_time import get_reaction_time

win = visual.Window(size=(2560, 1440), fullscr=True, checkTiming=False, color='black')

enable_countdown = True  # Set to False to disable countdown

last_duration = None
clips_dir = 'clips'
for clip in os.listdir(clips_dir):
    if clip.endswith('.mp4'):
        video_path = os.path.join(clips_dir, clip)
        stimulus_frame = int(os.path.basename(video_path).split('_')[0])
        if enable_countdown and last_duration is not None:
            possible = [3, 4, 5]
            possible.remove(last_duration)
            countdown_duration = random.choice(possible)
        elif enable_countdown:
            countdown_duration = random.choice([3, 4, 5])
        else:
            countdown_duration = None
        last_duration = countdown_duration
        rt_ms, reaction_type = get_reaction_time(video_path, win, stimulus_frame, enable_countdown, countdown_duration)
        print(f"{clip}: Reaction Time: {rt_ms:.2f} ms, Type: {reaction_type}")

win.close()
