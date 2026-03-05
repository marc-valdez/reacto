import os
import random
from pathlib import Path

from psychopy.visual import Window, TextStim, ImageStim
from psychopy.visual.movie import MovieStim
from psychopy.sound import Sound

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


def load_clips(win: Window, base_path: Path, dir: Path, randomize: bool = False):
    clips_dir = base_path / dir

    movies = {}
    sounds = {}
    clips = [f.name for f in clips_dir.glob("*.mp4")]

    loading_text = TextStim(win, color="white", height=0.05)
    for clip in clips:
        video_path = clips_dir / clip
        audio_path = clips_dir / clip.replace(".mp4", ".mp3")

        print(f"Loading... {clip}")
        loading_text.setText(f"Loading... {clip}")
        loading_text.draw()
        win.flip()

        if os.path.exists(audio_path):
            sounds[clip] = Sound(audio_path)
        else:
            sounds[clip] = None
        movies[clip] = MovieStim(
            win, filename=video_path, size=win.size, autoStart=False
        )

    # Randomize clips
    if randomize:
        random.shuffle(clips)
    return clips, movies, sounds


def load_images(win: Window, base_path: Path, dir: Path):
    images_dir = base_path / dir
    images = [f for f in images_dir.glob("*.jpg")]
    images.sort()
    return [ImageStim(win, image=f, units="pix", size=win.size) for f in images]


if __name__ == "__main__":
    win = Window()
    clips = load_clips(win, Path("clips"))
    images = load_images(win, Path("onboarding"))
