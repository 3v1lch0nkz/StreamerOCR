# StreamerOCR

A lightweight desktop application that performs real-time OCR on selected screen regions and converts text to speech.

## Features

- Screen region selection with visual feedback
- Real-time OCR processing using Tesseract
- Text-to-Speech conversion
- Global hotkeys for quick access
- Region persistence between sessions

## Installation

1. Download the latest release from the releases page
2. Extract the ZIP file to your desired location
3. Run `StreamerOCR.exe`

## Usage

1. Launch StreamerOCR
2. Click the "Select Region" button or press `Alt + Shift + R` to select a screen region
3. Click and drag to select the desired area
4. Press `Alt + Shift + Space` to process the selected region
5. The application will read aloud any text found in the region

## Keyboard Shortcuts

- `Alt + Shift + Space` - Process the selected region
- `Alt + Shift + R` - Select a new region
- `Alt + Shift + Q` - Exit application

## Development Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   python src/main.py
   ```

## Building from Source

1. Install PyInstaller:
   ```bash
   pip install pyinstaller
   ```
2. Build the executable:
   ```bash
   pyinstaller streamer_ocr.spec
   ```
3. The executable will be created in the `dist` directory

## Requirements

- Windows 10 or later
- Tesseract OCR engine (included in the installation)
- Python 3.8 or later (if running from source)

## License

This project is licensed under the MIT License - see the LICENSE file for details. 