# Reacto - Reaction Time Test

Reacto is a reaction time testing application built with Python and PsychoPy. It displays video clips and measures user reaction times to stimuli within the videos, providing a fun and scientific way to test reflexes.

## Features

- Displays video clips from the `clips` directory
- Measures reaction time to specific frames in videos
- Supports countdown timers before each test
- Records and displays results
- Built as a standalone executable for easy distribution

## Requirements

- Windows (built with PyInstaller)
- Video clips in MP4 format and corresponding audio files in MP3 format placed in a `clips` directory next to the executable
- Clip filenames must follow the format `{stimulus_frame}_{name}.mp4` and `{stimulus_frame}_{name}.mp3`, where `stimulus_frame` is the frame number (starting from 0) where the reaction stimulus appears

## Usage

1. Place the `reacto.exe` and `clips` directory in the same folder
2. Run `reacto.exe`
3. Follow the on-screen instructions to complete the reaction time tests

## Building from Source

To build the executable yourself:

1. Install Python and dependencies: `pip install -r requirements.txt`
2. Run `build.bat` to generate `reacto.exe`

## Credits and Thanks

This project utilizes the following open-source software:

- **PsychoPy**: For visual and audio stimulus presentation
- **PyInstaller**: For packaging the application into a standalone executable
- **Python**: The programming language
- **FFmpeg**: For video decoding (bundled via PsychoPy dependencies)
- **SoundDevice**: For audio handling
- **OpenCV**: For video processing

Special thanks to the developers and communities behind these projects for making scientific computing and multimedia applications accessible.

## License

See LICENSE file for details.