import os
import sys
from pathlib import Path
from psychopy import event
from psychopy.visual import Window, TextStim
from psychopy.visual.movie import MovieStim

from countdown import CountdownManager
from results import display_result_screen, display_final_screen
from reaction_time import get_reaction_time
from asset_loader import load_clips

def press_space_to_continue(win: Window):
    footer_message = TextStim(win, text="Press SPACE to continue...", height=0.05, pos=(0, -0.9))
    footer_message.draw()
    win.flip()
    event.waitKeys(keyList=['space'])

def explain_reacto(win: Window):
    # Display the welcome text in a larger font size
    welcome_message = TextStim(win, text="Welcome to Reacto!", height=0.1, pos=(0, 0.2))
    welcome_message.draw()

    # Display the explanation text in a normal font size
    explanation_message = TextStim(win, text=(
        "This is a reaction time test designed to measure how quickly you can respond to visual stimuli.\n\n"
        "You will see a countdown, followed by a stimulus. Your goal is to react as quickly as possible."
    ), height=0.05, pos=(0, -0.2))
    explanation_message.draw()

    # Add the footer message
    press_space_to_continue(win)

def show_image_stim_examples(win: Window):
    examples = [
        ("Example 1: Too Early", "Reacting before the stimulus appears is too early."),
        ("Example 2: Too Late", "Reacting after the stimulus disappears is too late."),
        ("Example 3: Just Right", "Reacting within the optimal window is just right.")
    ]

    for title, description in examples:
        message = TextStim(win, text=f"{title}\n\n{description}", height=0.05)
        message.draw()
        press_space_to_continue(win)

def explain_countdown(win: Window):
    message = TextStim(win, text=(
        "The countdown helps you prepare.\n\n"
        "When it reaches zero, the stimulus will appear.\n"
        "Focus during the countdown and be ready to react."
    ), height=0.05)
    message.draw()
    press_space_to_continue(win)

def mini_test(win: Window, clips: list[str]):
    countdown_manager = CountdownManager()

    message = TextStim(win, text="Mini-Test: React to the stimulus in three trials.", height=0.05)
    message.draw()
    press_space_to_continue(win)

    for i, clip in enumerate(clips):
        countdown_manager.perform_countdown(win, enable_countdown=True)

        # Load the video clip and measure reaction time
        stimulus_frame = int(clip.split('_')[0])
        video_path = os.path.join('onboarding', clip)

        movie = MovieStim(win, filename=video_path, size=win.size, autoStart=False)
        rt_ms, verdict = get_reaction_time(win, movie, None, stimulus_frame)

        display_result_screen(win, rt_ms=rt_ms, verdict=verdict)

def transition_to_test(win: Window):
    message = TextStim(win, text=(
        "You have completed the tutorial.\n\n"
        "Press 'R' to repeat the tutorial or 'P' to proceed to the test."
    ), height=0.05)
    message.draw()
    win.flip()

    while True:
        keys = event.waitKeys(keyList=['r', 'p'])
        if 'r' in keys:
            run_tutorial(win)
            break
        elif 'p' in keys:
            message = TextStim(win, text="Proceeding to the test...", height=0.05)
            message.draw()
            win.flip()
            break

def confirm_tutorial():
    while True:
        user_input = input("Would you like to run the tutorial? Y/N: ")
        if user_input.lower() in ['y', 'yes']:
            return True
        elif user_input.lower() in ['n', 'no']:
            print("Skipping tutorial...")
            return False
        else:
            print("Invalid input. Please enter Y or N.")

def run_tutorial(win: Window):
    clips = load_clips('onboarding')

    explain_reacto(win)
    show_image_stim_examples(win)
    explain_countdown(win)
    mini_test(win, clips)
    transition_to_test(win)

if __name__ == "__main__":
    win = Window(fullscr=True, color="black")
    run_tutorial(win)
    win.close()
