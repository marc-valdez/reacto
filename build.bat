@echo off
call .venv\Scripts\activate.bat
rmdir /s /q dist 2>nul
rmdir /s /q build 2>nul
pyinstaller --onefile --name reacto --icon reacto.ico --hidden-import psychopy.visual.backends.pygletbackend --hidden-import psychopy.visual.backends._base --hidden-import psychopy.visual.backends.gamma --hidden-import psychopy.visual.movies main.py
xcopy clips dist\clips /E /I
pause
