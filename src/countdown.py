"""
Countdown Module

Functions for handling countdown logic in the reaction time test.
"""
import random
import math
from psychopy.visual import TextStim, Window
from psychopy.core import getTime
from psychopy.event import getKeys

class CountdownManager:
    """Manages countdown durations and display to avoid immediate repeats without external state."""

    def __init__(self, durations_list=None):
        self.durations_list = durations_list if durations_list else [3, 4, 5]
        self.last_duration = None

    def perform_countdown(self, win: Window, enable_countdown: bool):
        """Get a countdown duration and perform the countdown display, avoiding immediate repeats."""
        if not enable_countdown:
            return
        choice = random.choice(self.durations_list)
        # Avoid immediate repeat if possible
        while choice == self.last_duration and len(self.durations_list) > 1:
            choice = random.choice(self.durations_list)
        self.last_duration = choice
        duration = choice

        countdown_text = TextStim(win, text='', pos=(0, 0), color='white', height=0.5)
        countdown_start = getTime()
        while True:
            elapsed = getTime() - countdown_start
            if elapsed >= duration:
                break
            remaining = duration - elapsed
            display_num = math.ceil(remaining)
            if display_num <= 0:
                break
            countdown_text.setText(f'{display_num}')
            countdown_text.draw()
            win.flip()
            keys = getKeys(keyList=['escape'])
            if keys:
                break
