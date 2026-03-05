#!/bin/bash
set -e

# Add logging
exec > >(tee build.log) 2>&1

# Set platform
if [[ "$OSTYPE" == "linux-gnu"* ]] || [[ "$OSTYPE" == "cygwin"* ]]; then
    PLATFORM="linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    PLATFORM="mac"
elif [[ "$OSTYPE" == "msys"* ]]; then
    PLATFORM="windows"
else
    echo "Unsupported platform: $OSTYPE"
    exit 1
fi

echo "Building for $OSTYPE..."
DIST_DIR="dist/$PLATFORM"

# Install uv if not available
if ! command -v uv &> /dev/null; then
    if [[ "$PLATFORM" == "windows" ]]; then
        winget install --id astral-sh.uv || true
    elif [[ "$PLATFORM" == "linux" ]]; then
        curl -LsSf https://astral.sh/uv/install.sh | sh
        source "$HOME/.local/bin/env"
    else
        brew install uv
    fi
fi

# Set uv python version to 3.10
uv python pin 3.10

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    uv venv
fi

# Activate virtual environment
if [[ "$PLATFORM" == "windows" ]]; then
    source .venv/Scripts/activate
else
    source .venv/bin/activate
fi

# Install platform-specific dependencies
if [[ "$PLATFORM" == "linux" ]]; then
    sudo apt-get install -y libsm6 libgl1 libgtk-3-0t64 libsdl2-2.0-0 libpcre2-32-0 upx
    uv pip install "https://extras.wxpython.org/wxPython4/extras/linux/gtk3/ubuntu-24.04/wxpython-4.2.5-cp310-cp310-linux_x86_64.whl"
elif [[ "$PLATFORM" == "mac" ]]; then
    brew install upx
elif [[ "$PLATFORM" == "windows" ]]; then
    winget install -e --id UPX.UPX || true
fi

uv pip install -r requirements.txt

# Remove old dist
rm -rf "$DIST_DIR"

# Choose icon file
if [[ "$PLATFORM" == "mac" ]]; then ICON="reacto.icns"; else ICON="reacto.ico"; fi

# Build executable with PyInstaller
uv run pyinstaller --distpath "$DIST_DIR" --onedir --clean --name reacto --icon "$ICON" \
    --hidden-import psychopy.visual.backends.pygletbackend \
    --hidden-import psychopy.visual.movies \
    --hidden-import psychopy.sound.backend_ptb \
    --hidden-import psychopy.sound \
    --exclude-module arabic-reshaper \
    --exclude-module astunparse \
    --exclude-module beautifulsoup4 \
    --exclude-module blosc2 \
    --exclude-module contourpy \
    --exclude-module cycler \
    --exclude-module decorator \
    --exclude-module elementpath \
    --exclude-module esprima \
    --exclude-module et-xmlfile \
    --exclude-module fonttools \
    --exclude-module freetype-py \
    --exclude-module gevent \
    --exclude-module gitdb \
    --exclude-module gitpython \
    --exclude-module greenlet \
    --exclude-module imageio \
    --exclude-module imageio_ffmpeg \
    --exclude-module jedi \
    --exclude-module json-tricks \
    --exclude-module json-tricks \
    --exclude-module kiwisolver \
    --exclude-module matplotlib \
    --exclude-module meshpy \
    --exclude-module moviepy \
    --exclude-module msgpack \
    --exclude-module msgpack-numpy \
    --exclude-module ndindex \
    --exclude-module numexpr \
    --exclude-module opencv-python \
    --exclude-module openpyxl \
    --exclude-module parso \
    --exclude-module pillow \
    --exclude-module proglog \
    --exclude-module psutil \
    --exclude-module psychtoolbox \
    --exclude-module py-cpuinfo \
    --exclude-module pyarrow \
    --exclude-module pyparallel \
    --exclude-module pypiwin32 \
    --exclude-module pyqt6 \
    --exclude-module pyqt6-qt6 \
    --exclude-module pyqt6-sip \
    --exclude-module pyserial \
    --exclude-module python-bidi \
    --exclude-module python-dotenv \
    --exclude-module python-gitlab \
    --exclude-module python-vlc \
    --exclude-module pywin32 \
    --exclude-module pywinhook \
    --exclude-module pyyaml \
    --exclude-module pyzmq \
    --exclude-module questplus \
    --exclude-module requests-toolbelt \
    --exclude-module smmap \
    --exclude-module soupsieve \
    --exclude-module tables \
    --exclude-module tqdm \
    --exclude-module ujson \
    --exclude-module wheel \
    --exclude-module wxpython \
    --exclude-module xarray \
    --exclude-module xmlschema \
    --exclude-module zope-event \
    --exclude-module zope-interface \
    main.py

# Copy assets if they exist
for dir in clips onboarding; do
    if [ -d "$dir" ]; then
        mkdir -p "$DIST_DIR/reacto/$dir"
        cp -r "$dir/"* "$DIST_DIR/reacto/$dir/"
    fi
done

if [ -f "example.configuration.ini" ]; then
    cp example.configuration.ini "$DIST_DIR/reacto/configuration.ini"
fi

if [ -f "README.md" ]; then
    cp README.md "$DIST_DIR/reacto/README.md"
fi