@echo off
REM Gordon Secure Vault - Windows Build Script
REM Builds executable for Windows distribution

setlocal enabledelayedexpansion

echo.
echo ================================
echo Gordon Secure Vault - Windows Build
echo ================================
echo.

REM Check Python version
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Check for required directories
if not exist "desktop" (
    echo ERROR: desktop directory not found
    pause
    exit /b 1
)

REM Create build directories
echo Creating build directories...
if not exist "build" mkdir build
if not exist "dist" mkdir dist
if not exist ".github\workflows" mkdir ".github\workflows"

REM Install dependencies
echo.
echo Installing dependencies...
pip install -r requirements.txt

if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

REM Run tests
echo.
echo Running tests...
pytest tests/ -v --tb=short

if errorlevel 1 (
    echo WARNING: Some tests failed. Continue with build? (Y/N)
    set /p continue=">"
    if /i not "!continue!"=="Y" exit /b 1
)

REM Code quality checks
echo.
echo Running code quality checks...
flake8 core desktop --max-line-length=100 --ignore=E501,W503

REM Build executable with PyInstaller
echo.
echo Building executable...

set MAIN_PY=desktop\main.py
set OUTPUT_NAME=gordon-secure-vault
set ICON=assets\icons\logo.ico

if exist %ICON% (
    pyinstaller ^
        --name=%OUTPUT_NAME% ^
        --icon=%ICON% ^
        --windowed ^
        --onefile ^
        --add-data "core:core" ^
        --add-data "assets:assets" ^
        --collect-all customtkinter ^
        --distpath=dist ^
        --buildpath=build ^
        %MAIN_PY%
) else (
    pyinstaller ^
        --name=%OUTPUT_NAME% ^
        --windowed ^
        --onefile ^
        --add-data "core:core" ^
        --add-data "assets:assets" ^
        --collect-all customtkinter ^
        --distpath=dist ^
        --buildpath=build ^
        %MAIN_PY%
)

if errorlevel 1 (
    echo ERROR: PyInstaller build failed
    pause
    exit /b 1
)

REM Create version file
echo.
echo Creating version file...
set FILENAME=dist\VERSION.txt
(
    echo Application: Gordon Secure Vault
    echo Version: 1.0.0
    echo Build Date: %date% %time%
    echo Platform: Windows 10/11
    echo Python: 3.13+
) > %FILENAME%

REM Create README for distribution
echo.
echo Creating distribution README...
set DISTREADME=dist\README.txt
(
    echo Gordon Secure Vault v1.0.0
    echo.
    echo Installation:
    echo 1. Extract gordon-secure-vault.exe to desired location
    echo 2. Double-click gordon-secure-vault.exe to run
    echo.
    echo System Requirements:
    echo - Windows 10 (Build 1909) or later
    echo - Windows 11 recommended
    echo - 1GB RAM minimum
    echo - 500MB free disk space
    echo.
    echo First Run:
    echo 1. Application will create .gordon_secure_vault directory in your home folder
    echo 2. Create your first vault in the Vault Manager
    echo 3. Set a strong password
    echo.
    echo Documentation:
    echo See README.md for detailed usage instructions
) > %DISTREADME%

REM Calculate build time
echo.
echo.
echo ================================
echo Build completed successfully!
echo ================================
echo.
echo Output: dist\gordon-secure-vault.exe
echo Size: 
for %%A in (dist\gordon-secure-vault.exe) do echo %%~zA bytes
echo.
echo Next steps:
echo 1. Test the executable: dist\gordon-secure-vault.exe
echo 2. Create installer (optional): Use NSIS or WiX
echo 3. Distribute to users
echo.

pause
