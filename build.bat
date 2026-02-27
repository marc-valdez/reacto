@echo off

if not exist ".uv_venv" (
    powershell -Command "& {Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process; Install-Module -Name UniversalDashboard -Force; Import-Module -Name UniversalDashboard; New-UDEnvironment -Name .uv_venv}""
)
call ".venv\Scripts\activate.bat"

uv pip install -r requirements.txt

rmdir /s /q dist 2>nul
rmdir /s /q build 2>nul

if exist clips (
    mkdir "dist\clips" 2>nul
    xcopy "clips\*" "dist\clips\" /E /I /Y >nul
)

if exist example.configuration.ini (
    copy example.configuration.ini dist\example.configuration.ini >nul
)

if exist README.md   (
    copy README.md dist\README.md >nul
)

python -m PyInstaller --onefile --clean --name reacto --icon reacto.ico ^
--hidden-import psychopy.visual.backends.pygletbackend ^
--hidden-import psychopy.visual.movies ^
--hidden-import psychopy.sound.backend_ptb ^
--hidden-import psychopy.sound ^
--exclude-module arabic-reshaper ^
--exclude-module astunparse ^
--exclude-module beautifulsoup4 ^
--exclude-module blosc2 ^
--exclude-module contourpy ^
--exclude-module cycler ^
--exclude-module decorator ^
--exclude-module elementpath ^
--exclude-module esprima ^
--exclude-module et-xmlfile ^
--exclude-module fonttools ^
--exclude-module freetype-py ^
--exclude-module gevent ^
--exclude-module gitdb ^
--exclude-module gitpython ^
--exclude-module greenlet ^
--exclude-module imageio ^
--exclude-module imageio_ffmpeg ^
--exclude-module jedi ^
--exclude-module json-tricks ^
--exclude-module json-tricks ^
--exclude-module kiwisolver ^
--exclude-module matplotlib ^
--exclude-module meshpy ^
--exclude-module moviepy ^
--exclude-module msgpack ^
--exclude-module msgpack-numpy ^
--exclude-module ndindex ^
--exclude-module numexpr ^
--exclude-module opencv-python ^
--exclude-module openpyxl ^
--exclude-module parso ^
--exclude-module pillow ^
--exclude-module proglog ^
--exclude-module psutil ^
--exclude-module psychtoolbox ^
--exclude-module py-cpuinfo ^
--exclude-module pyarrow ^
--exclude-module pyparallel ^
--exclude-module pypiwin32 ^
--exclude-module pyqt6 ^
--exclude-module pyqt6-qt6 ^
--exclude-module pyqt6-sip ^
--exclude-module pyserial ^
--exclude-module python-bidi ^
--exclude-module python-dotenv ^
--exclude-module python-gitlab ^
--exclude-module python-vlc ^
--exclude-module pywin32 ^
--exclude-module pywinhook ^
--exclude-module pyyaml ^
--exclude-module pyzmq ^
--exclude-module questplus ^
--exclude-module requests-toolbelt ^
--exclude-module smmap ^
--exclude-module soupsieve ^
--exclude-module tables ^
--exclude-module tqdm ^
--exclude-module ujson ^
--exclude-module wheel ^
--exclude-module wxpython ^
--exclude-module xarray ^
--exclude-module xmlschema ^
--exclude-module zope-event ^
--exclude-module zope-interface ^
main.py
 
pause
