@echo off
REM Glitch SQL Injector Launcher
REM Ethical SQL Injection Testing Tool

setlocal

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in PATH.
    echo Please install Python 3.6 or higher and try again.
    pause
    exit /b 1
)

REM Check if required Python packages are installed
python -c "import requests" >nul 2>&1
if errorlevel 1 (
    echo Installing required Python packages...
    python -m pip install requests >nul 2>&1
    if errorlevel 1 (
        echo Failed to install required packages.
        pause
        exit /b 1
    )
)

REM Display Glitch SQL Injector header with animation
echo.
echo ############################################################################
echo.
echo                    GGGGGG  LL      IIIIII  TTTTTT  CCCCCC  HH    HH
echo                   GG    GG LL       II    TT  TT CC    CC HH    HH
echo                   GG       LL       II      TT   CC       HH    HH
echo                   GG  GGGG LL       II      TT   CC       HHHHHHHH
echo                   GG    GG LL       II      TT   CC       HH    HH
echo                   GG    GG LL       II      TT   CC    CC HH    HH
echo                    GGGGGG  LLLLLL  IIIIII   TT    CCCCCC  HH    HH
echo.
echo ############################################################################
echo.
echo                 GLITCH SQL INJECTOR - ETHICAL TESTING TOOL
echo.
echo ############################################################################
echo.

REM Show help if no arguments provided
if "%1"=="" (
    echo Usage: %0 ^<target_url^>
    echo Example: %0 "http://example.com/page.php?id=1"
    echo.
    echo WARNING: This tool is for educational purposes only.
    echo Only use on systems you own or have explicit permission to test.
    echo Unauthorized use may violate local, state, and federal laws.
    echo.
    goto :end
)

REM Run the Python script with provided arguments
echo Running Glitch SQL Injector on: %1
echo.
python glitch_sql_injector.py %*

:end
pause