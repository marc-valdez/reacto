from psychopy import prefs
prefs.hardware['audioLib'] = ['sounddevice']

from psychopy import visual, core, event
from psychopy.monitors import Monitor

mon = Monitor('myMonitor')
mon.setSizePix((2560, 1440))

win = visual.Window(monitor=mon, fullscr=True, checkTiming=False)
movie = visual.MovieStim(win, filename='clips/133_foxy.mp4', size=win.size)
clock = core.Clock()

fps = 30
stimulus_frame = 133  # pre-annotated enemy appearance
frame_counter = 0

clock.reset()

while not movie.isFinished:
    movie.draw()
    win.flip()

    frame_counter += 1

    # only check for responses after stimulus appears
    current_movie_frame = movie.movieTime * fps
    if current_movie_frame >= stimulus_frame:
        keys = event.getKeys(keyList=['space', 'escape'], timeStamped=clock)
        mouse = event.Mouse()

        if keys:
            key, time = keys[0]
            reaction_movie_time = movie.movieTime
            reaction_frame = reaction_movie_time * fps
            break

win.close()

# compute perceptual RT
delta_frames = reaction_frame - stimulus_frame
true_rt_ms = (delta_frames / fps) * 1000

print("Reaction Time:", true_rt_ms, "ms")
