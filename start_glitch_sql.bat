@echo off
REM Glitch SQL Injector Launcher
REM Starts both the API server and opens the web interface

setlocal

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in PATH.
    echo Please install Python 3.6 or higher and try again.
    pause
    exit /b 1
)

echo Starting Glitch SQL Injector...
echo.

REM Start the API server in a new window
start "Glitch SQL API Server" cmd /c "python api_server.py"

REM Wait a moment for the server to start
timeout /t 3 /nobreak >nul

REM Open the web interface
start http://localhost:8080

echo Glitch SQL Injector is now running!
echo API Server: http://localhost:8080
echo Web Interface will open automatically.
echo.
echo WARNING: This tool is for educational purposes only.
echo Only use on systems you own or have explicit permission to test.
echo Unauthorized use may violate local, state, and federal laws.
echo.
echo Press any key to exit...
pause >nul