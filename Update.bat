@echo off
cd /d "%~dp0"
net session >nul 2>&1
if %ERRORLEVEL% == 0 (
	echo "Admin detected"
) else (
	echo, & echo, & echo "Error: Open Update.bat with admin permissions (right click -> Run as Administrator)" & echo, & echo,
	cmd /k
)
pip install -r requirements.txt --upgrade
choco upgrade chromedriver -y
choco upgrade ffmpeg -y
cmd /k