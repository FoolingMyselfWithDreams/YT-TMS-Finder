@echo off
cd /d "%~dp0"

net session >nul 2>&1
if %ERRORLEVEL% == 0 (
	echo "Admin detected"
) else (
	echo, & echo, & echo "Error: Open Install.bat with admin permissions (right click -> Run as Administrator)" & echo, & echo,
	cmd /k
)

@"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command "iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))" && SET "PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin"
call RefreshEnv.cmd

python check_python.py

:Check to see if Python version is sufficient, if not, install Python:
if %ERRORLEVEL% == 10 (
	choco upgrade python3 -y
	call RefreshEnv.cmd
)
if %ERRORLEVEL% == 9009 (
	choco install python3 -y
	call RefreshEnv.cmd
)

pip install -r requirements.txt
choco install chromedriver -y
choco install ffmpeg -y
cmd /k
