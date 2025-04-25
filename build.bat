@echo off
setlocal enabledelayedexpansion

echo Building StreamerOCR...

REM Check for Python
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Error: Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Check for virtual environment
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
    if %ERRORLEVEL% NEQ 0 (
        echo Error: Failed to create virtual environment
        pause
        exit /b 1
    )
)

REM Activate virtual environment
call venv\Scripts\activate
if %ERRORLEVEL% NEQ 0 (
    echo Error: Failed to activate virtual environment
    pause
    exit /b 1
)

REM Check for Tesseract OCR
where tesseract >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ⚠️ Warning: Tesseract OCR not found in PATH!
    echo Please install Tesseract OCR before using StreamerOCR.
    echo Download from: https://github.com/UB-Mannheim/tesseract/wiki
    echo.
    echo Press any key to continue building...
    pause >nul
)

REM Install build dependencies
echo Installing build dependencies...
pip install pyinstaller==6.13.0
if %ERRORLEVEL% NEQ 0 (
    echo Error: Failed to install PyInstaller
    pause
    exit /b 1
)

REM Create the executable
echo Creating executable...
pyinstaller --clean StreamerOCR.spec
if %ERRORLEVEL% NEQ 0 (
    echo Error: Failed to create executable
    pause
    exit /b 1
)

REM Create distribution package
echo Creating distribution package...
if not exist dist\StreamerOCR\docs mkdir dist\StreamerOCR\docs
copy docs\DOCS.html dist\StreamerOCR\docs\ >nul
copy docs\overview.html dist\StreamerOCR\docs\ >nul
copy README.md dist\StreamerOCR\ >nul

echo.
echo Build complete!
echo The executable and documentation can be found in the dist\StreamerOCR folder.
echo.
echo ⚠️ Remember: Users must install Tesseract OCR separately!
echo Download from: https://github.com/UB-Mannheim/tesseract/wiki
pause 