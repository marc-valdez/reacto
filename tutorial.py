import random
from psychopy import visual, core, event

from countdown import CountdownManager
from results import display_result_screen, display_final_screen

def press_space_to_continue(win):
    footer_message = visual.TextStim(win, text="Press SPACE to continue...", height=0.05, pos=(0, -0.9))
    footer_message.draw()
    win.flip()
    event.waitKeys(keyList=['space'])

def explain_reacto(win):
    # Display the welcome text in a larger font size
    welcome_message = visual.TextStim(win, text="Welcome to Reacto!", height=0.1, pos=(0, 0.2))
    welcome_message.draw()

    # Display the explanation text in a normal font size
    explanation_message = visual.TextStim(win, text=(
        "This is a reaction time test designed to measure how quickly you can respond to visual stimuli.\n\n"
        "You will see a countdown, followed by a stimulus. Your goal is to react as quickly as possible."
    ), height=0.05, pos=(0, -0.2))
    explanation_message.draw()

    # Add the footer message
    press_space_to_continue(win)

def show_image_stim_examples(win):
    examples = [
        ("Example 1: Too Early", "Reacting before the stimulus appears is too early."),
        ("Example 2: Too Late", "Reacting after the stimulus disappears is too late."),
        ("Example 3: Just Right", "Reacting within the optimal window is just right.")
    ]

    for title, description in examples:
        message = visual.TextStim(win, text=f"{title}\n\n{description}", height=0.05)
        message.draw()
        press_space_to_continue(win)

def explain_countdown(win):
    message = visual.TextStim(win, text=(
        "The countdown helps you prepare.\n\n"
        "When it reaches zero, the stimulus will appear.\n"
        "Focus during the countdown and be ready to react."
    ), height=0.05)
    message.draw()
    press_space_to_continue(win)

def mini_test(win):
    countdown_manager = CountdownManager()

    message = visual.TextStim(win, text="Mini-Test: React to the stimulus in three trials.", height=0.05)
    message.draw()
    press_space_to_continue(win)

    reaction_times = []

    for i in range(3):
        message = visual.TextStim(win, text=f"Trial {i + 1}:\nGet ready...", height=0.05)
        message.draw()
        win.flip()
        core.wait(2)

        countdown_manager.perform_countdown(win, enable_countdown=True)

        core.wait(random.uniform(1, 3))
        stimulus = visual.TextStim(win, text="Stimulus! Press SPACE now!", height=0.1)
        stimulus.draw()
        win.flip()

        start_time = core.getTime()
        keys = event.waitKeys(keyList=['space'], timeStamped=True)
        reaction_time = keys[0][1] - start_time
        reaction_times.append(reaction_time)

        if reaction_time < 0.2:
            verdict = 'too-early'
        elif reaction_time > 0.6:
            verdict = 'too-late'
        else:
            verdict = 'pass'

        display_result_screen(win, rt_ms=reaction_time * 1000, verdict=verdict)

    averages = {"mini-test": reaction_times}
    display_final_screen(win, averages)

def transition_to_test(win):
    message = visual.TextStim(win, text=(
        "You have completed the tutorial.\n\n"
        "Press 'R' to repeat the tutorial or 'P' to proceed to the test."
    ), height=0.05)
    message.draw()
    press_space_to_continue(win)

    while True:
        keys = event.waitKeys(keyList=['r', 'p'])
        if 'r' in keys:
            run_tutorial(win)
            break
        elif 'p' in keys:
            message = visual.TextStim(win, text="Proceeding to the test...", height=0.05)
            message.draw()
            win.flip()
            core.wait(2)
            break

def run_tutorial(win):
    explain_reacto(win)
    show_image_stim_examples(win)
    explain_countdown(win)
    mini_test(win)
    transition_to_test(win)

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

if __name__ == "__main__":
    win = visual.Window(fullscr=True, color="black")
    run_tutorial(win)
    win.close()
    core.quit()