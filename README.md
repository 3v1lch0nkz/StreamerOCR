# StreamerOCR

A lightweight desktop utility for streamers and gamers to capture and process text from specific screen regions using OCR technology.

## Features

- Region selection similar to snipping tool
- OCR text recognition using Tesseract
- Text-to-Speech output
- System tray application
- Configurable keyboard shortcuts
- Region profile management

## Prerequisites

1. Python 3.11 or higher
2. Tesseract OCR installed on your system
   - Download from: https://github.com/UB-Mannheim/tesseract/wiki
   - Make sure to add Tesseract to your system PATH

## Installation

1. Clone this repository
2. Install required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```bash
   python streamer_ocr.py
   ```

2. The application will start in the system tray
3. Right-click the tray icon and select "Configure"
4. Click "Select Region" to define the area you want to capture
5. Use the configured hotkey to capture and process the region

## Configuration

- Regions are automatically saved in `regions.json`
- You can configure multiple regions and switch between them
- The application remembers your last used region

## Troubleshooting

If you encounter issues with Tesseract OCR:
1. Verify Tesseract is installed correctly
2. Check if Tesseract is in your system PATH
3. Restart the application after making changes

## License

MIT License 