@echo off
set Location=C:%HOMEPATH%\AppData\Local\Programs\Python\

:Check to see if the Python directory exists, if not, display error message:
IF EXIST "%Location%" ( 
    python reset-database.py
    cmd /k
) ELSE (
    echo This program uses Python, which is not installed on your system. Please double-click Install.bat or download and install Python at https://www.python.org/downloads/. & pause
)
