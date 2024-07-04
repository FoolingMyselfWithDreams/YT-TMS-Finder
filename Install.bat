@echo off
cd /d "%~dp0"

net session >nul 2>&1
if %ERRORLEVEL% == 0 (
	echo "Admin detected"
) else (
	echo, & echo, & echo "Error: Open Install.bat with admin permissions (right click -> Run as Administrator)" & echo, & echo,
	cmd /k
)

python --version 2>NUL

:Check to see if Python is in PATH, if not, install Python:
if %ERRORLEVEL% == 9009 (
	@"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command "iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))" && SET "PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin"
	RefreshEnv.cmd
	choco install python3 -y
	RefreshEnv.cmd
        pip install -r requirements.txt
	choco install chromedriver -y
	choco install ffmpeg -y
        cmd /k
) else (
	@"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command "iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))" && SET "PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin"
        RefreshEnv.cmd
	pip install -r requirements.txt
	choco install chromedriver -y
	choco install ffmpeg -y
        cmd /k
)