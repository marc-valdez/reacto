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
- Python 3.10 or higher
- Video clips in MP4 format and corresponding audio files in MP3 format placed in a `clips` directory next to the executable
- Clip filenames must follow the format `{stimulus_frame}_{color_mode}_{game}.{extension}`, where:
  - `stimulus_frame` is the frame number (starting from 0) where the reaction stimulus appears
  - `color_mode` specifies the color mode (e.g., default, deuteranopia, protanopia, tritanopia)
  - `game` indicates the game or context of the clip
  - `extension` can be `.mp3` or `.mp4`

## Configuration

The app uses `configuration.ini` for settings. Edit this file to customize:

- Countdown settings
- Display resolution and fullscreen mode
- File paths for clips and auth codes
- Authentication with Supabase (optional, configurable in `configuration.ini`)

## Usage

1. Place the `reacto.exe` and `clips` directory in the same folder
2. Run `reacto.exe`
3. Follow the on-screen instructions to complete the reaction time tests

## Building from Source

To build the executable yourself:

1. Install Python and dependencies: `pip install -r requirements.txt`
2. Run `build.bat` to generate `reacto.exe` inside `dist` directory

## Credits and Thanks

This project utilizes the following open-source software:

- **PsychoPy**: For visual and audio stimulus presentation
- **PyInstaller**: For packaging the application into a standalone executable
- **Python**: The programming language
- **Supabase**: For optional authentication and result storage

Special thanks to the developers and communities behind these projects for making scientific computing and multimedia applications accessible.

## License

See LICENSE file for details.
