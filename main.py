from psychopy import prefs
prefs.hardware['audioLib'] = ['sounddevice']

from psychopy import visual, core, event
from psychopy.monitors import Monitor

mon = Monitor('myMonitor')
mon.setSizePix((2560, 1440))
win = visual.Window(monitor=mon, fullscr=True, checkTiming=False)

frame_text = visual.TextStim(win, text='Frame: 0', pos=(0.8, 0.9), color='white', height=0.05)
movie = visual.MovieStim(win, filename='clips/130_valorant.mp4', size=win.size)
clock = core.Clock()

fps = 60
stimulus_time = 130 / fps
frame_counter = 0

clock.reset()
mouse = event.Mouse()
mouse.clickReset(buttons=[0])
left_pressed_prev = False

while not movie.isFinished:
    frame_counter += 1
    movie.draw()
    frame_text.setText(f'Frame: {frame_counter}')
    frame_text.draw()
    win.flip()

    keys = event.getKeys(keyList=['escape'], timeStamped=clock)
    pressed, times = mouse.getPressed(getTime=True)
    left_pressed = pressed[0]

    if keys or (left_pressed and not left_pressed_prev):
        if keys:
            if keys[0][0] == 'escape':
                break
        elif left_pressed and not left_pressed_prev:
            reaction_time = movie.movieTime
            if reaction_time < stimulus_time:
                reaction_type = 'too-early'
            else:
                reaction_type = 'pass'
            rt_ms = (reaction_time - stimulus_time) * 1000
            break

    left_pressed_prev = left_pressed

win.close()

if not 'reaction_type' in locals():
    reaction_type = 'too_late'
    rt_ms = (movie.duration - stimulus_time) * 1000

print(f"Reaction Time: {rt_ms:.2f} ms, Type: {reaction_type}")
