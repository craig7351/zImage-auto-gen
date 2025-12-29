@echo off
chcp 65001 > nul
cd /d "%~dp0"

REM Check for virtual environment and activate if exists
if exist venv\Scripts\activate.bat (
    echo Activating venv...
    call venv\Scripts\activate.bat
) else if exist .venv\Scripts\activate.bat (
    echo Activating .venv...
    call .venv\Scripts\activate.bat
) else (
    echo No venv found, using system python...
)

echo Starting Photo Album App...
python main.py

pause
