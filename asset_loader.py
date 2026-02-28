import sys
import os
from pathlib import Path

def load_clips(dir: str):
    if hasattr(sys, 'frozen'):
        base_path = Path(sys.executable).parent
    else:
        base_path = Path(__file__).parent
    clips_dir = os.path.join(base_path, dir)
    return [f.name for f in Path(clips_dir).glob("*.mp4")]

def load_images(dir: str):
    if hasattr(sys, 'frozen'):
        base_path = Path(sys.executable).parent
    else:
        base_path = Path(__file__).parent
    images_dir = os.path.join(base_path, dir)
    return {f.stem: f for f in Path(images_dir).glob("*.png")}
