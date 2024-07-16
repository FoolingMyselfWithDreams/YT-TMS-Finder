@echo off
python check_python.py

:Check to see if the Python directory exists, if not, display error message:
IF %ERRORLEVEL% == 10 (
    echo This program uses Python 3.8 or newer, which is not installed on your system. Please double-click Install.bat or download and install Python at https://www.python.org/downloads/. & pause
) ELSE (
    python collect-fingerprints.py
    cmd /k
)
