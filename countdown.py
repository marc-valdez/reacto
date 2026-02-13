"""
Countdown Module

Functions for handling countdown logic in the reaction time test.
"""

import random

def get_countdown_duration(enable_countdown, last_duration):
    """Determine the countdown duration for the next trial."""
    if enable_countdown and last_duration is not None:
        possible = [3, 4, 5]
        possible.remove(last_duration)
        return random.choice(possible)
    elif enable_countdown:
        return random.choice([3, 4, 5])
    else:
        return None