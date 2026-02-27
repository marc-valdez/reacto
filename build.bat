@echo off

if not exist ".venv" python -m venv .venv
call ".venv\Scripts\activate.bat"

python -m pip install --upgrade pip
python -m pip install -r requirements.txt

rmdir /s /q dist 2>nul
REM rmdir /s /q build 2>nul

if exist clips (
    mkdir "dist\clips" 2>nul
    xcopy "clips\*" "dist\clips\" /E /I /Y >nul
)

python -m PyInstaller --onefile --clean --name reacto --icon reacto.ico ^
--hidden-import psychopy.visual.backends.pygletbackend ^
--hidden-import psychopy.visual.movies ^
--hidden-import psychopy.sound.backend_ptb ^
--hidden-import psychopy.sound ^
--exclude-module wx ^
--exclude-module pyqt6 ^
--exclude-module matplotlib ^
--exclude-module psutil ^
--exclude-module openpyxl ^
--exclude-module imageio ^
--exclude-module imageio_ffmpeg ^
--exclude-module python_vlc ^
--exclude-module ujson ^
--exclude-module pyyaml ^
--exclude-module msgpack ^
--exclude-module zope_interface ^
--exclude-module cryptography ^
--exclude-module zeroconf ^
--exclude-module python_xlib ^
main.py

pause
