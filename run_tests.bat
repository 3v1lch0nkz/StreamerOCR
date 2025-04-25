@echo off
echo Running component tests...

if exist venv (
    echo Using existing virtual environment
) else (
    echo Creating virtual environment...
    python -m venv venv
)

call venv\Scripts\activate.bat

echo Installing requirements...
pip install -r requirements.txt
pip install pyttsx3
pip install Pillow
pip install pytesseract
pip install PyQt5
pip install pywin32==306

echo.
echo Running basic tests...
python tests/test_basic.py

echo.
echo Running TTS tests...
python tests/test_tts.py

echo.
echo Running OCR tests...
python tests/test_ocr.py

echo.
echo Running region tests...
python tests/test_region.py

pause 