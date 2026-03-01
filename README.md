# Reacto - Reaction Time Test

Reacto is a reaction time testing application built with Python and PsychoPy. It displays video clips and measures user reaction times to stimuli within the videos, providing a fun and scientific way to test reflexes.

## Features

- Displays video clips from the `clips` directory
- Measures reaction time against pre-determined stimulus frames in videos
- Supports countdown timers before each test
- **Interactive tutorial** with visual examples and mini-test trials
- Records and displays results with per-color-mode averages
- Exports results to JSON and optionally to Supabase
- Built as a standalone executable for easy distribution

### Directory Structure

The following directories must be placed next to the executable:

- **`clips/`** - Video clips in MP4 format (and optional MP3 audio files)
- **`onboarding/`** - Tutorial assets including images and practice clips (auto-copied during build)

### Clip Naming Convention

Clip filenames must follow the format `{stimulus_frame}_{color_mode}_{game}.{extension}`:

| Component | Description |
|-----------|-------------|
| `stimulus_frame` | Frame number (starting from 0) where the reaction stimulus appears |
| `color_mode` | Color mode: `default`, `deuteranopia`, `protanopia`, or `tritanopia` |
| `game` | Game or context identifier (e.g., `valorant`) |
| `extension` | `.mp4` for video, `.mp3` for audio (optional) |

**Example:** `43_default_valorant.mp4`

## Configuration

The app uses `configuration.ini` for settings. Copy `example.configuration.ini` to `configuration.ini` and edit to customize:

### `[app]` Section

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `enable_countdown` | Boolean | `True` | Enable countdown before each clip |
| `countdown_durations` | List | `3,4,5` | Randomized countdown durations (seconds) |
| `clips_directory` | String | `clips` | Directory containing video clips |

### `[display]` Section

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `window_width` | Integer | `1920` | Window width in pixels |
| `window_height` | Integer | `1080` | Window height in pixels |
| `fullscreen` | Boolean | `True` | Run in fullscreen mode |
| `borderless` | Boolean | `False` | Remove window borders (when not fullscreen) |

### `[auth]` Section

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `enable_supabase` | Boolean | `False` | Enable Supabase authentication |
| `SUPABASE_URL` | String | - | Your Supabase project URL |
| `SUPABASE_KEY` | String | - | Your Supabase publishable key |

## Usage

1. Place `reacto.exe`, `clips/`, and `onboarding/` directories in the same folder
2. Ensure `configuration.ini` is present (copied from `example.configuration.ini`)
3. Run `reacto.exe`
4. Choose whether to complete the interactive tutorial
5. React to stimuli in video clips by clicking the left mouse button
6. View your results at the end of the test

---

## Building from Source

To build the executable yourself, run `build.sh` using Git Bash (on Windows) or any Bash terminal (on Mac/Linux):
   ```bash
   ./build.sh
   ```

What `build.sh` does:
- Detects your platform (Windows, Mac, Linux) and sets up platform-specific build steps
- Installs the `uv` package manager if not already available
- Pins Python to version 3.10 for consistent builds
- Creates a virtual environment using `uv venv` if one does not exist
- Installs platform-specific dependencies (e.g., system libraries, UPX, wxPython)
- Installs all Python dependencies from `requirements.txt` using `uv pip`
- Copies the `clips/` and `onboarding/` directories (if present) into a platform-specific `dist/` folder
- Copies `example.configuration.ini` as `configuration.ini` and `README.md` into the `dist/` folder
- Selects the correct icon format for your platform
- Runs PyInstaller with many hidden imports and excluded modules to generate a standalone executable in the appropriate `dist/` subfolder

GitHub Actions workflows are also available in the [`.github/workflows/`](.github/workflows/:1) directory for CI and build automation.

## Credits and Thanks

This project utilizes the following open-source software:

- **PsychoPy**: For visual and audio stimulus presentation
- **PyInstaller**: For packaging the application into a standalone executable
- **Python**: The programming language
- **Supabase**: For optional authentication and result storage

Special thanks to the developers and communities behind these projects for making scientific computing and multimedia applications accessible.

## Privacy

When Supabase authentication is enabled, the application collects your **email address** for authentication purposes.  
The release builds include my public Reacto database keys and is enabled by default.

## License

This project is licensed under the [MIT License](LICENSE).
