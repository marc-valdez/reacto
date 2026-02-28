import sys
import os
from pathlib import Path
from config import config

def load_clips(dir: str):
    if hasattr(sys, 'frozen'):
        # Bundled (PyInstaller / Nuitka)
        base_path = Path(sys.executable).parent
    else:
        # Development
        base_path = Path(__file__).parent
    clips_dir = os.path.join(base_path, dir)
    return [f.name for f in Path(clips_dir).glob("*.mp4")]
