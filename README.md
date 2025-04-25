# StreamerOCR

A powerful screen text recognition tool designed for streamers and content creators.

## ⚠️ Important Prerequisite

**Tesseract OCR must be installed separately before using StreamerOCR:**

1. Download Tesseract OCR from: [UB-Mannheim Tesseract Installer](https://github.com/UB-Mannheim/tesseract/wiki)
2. Run the installer
3. Add Tesseract to your system PATH (default: `C:\Program Files\Tesseract-OCR`)
4. Restart your computer after installation

## Features

- Multi-monitor support
- Real-time OCR processing
- Text-to-Speech conversion
- Global hotkeys
- Region persistence
- Multiple saved regions
- Easy region management

## Installation

### Prerequisites

- Windows 10 or later
- Tesseract OCR (see above)
- Python 3.8 or later (if running from source)

### Standalone Installation

1. Download the latest release
2. Extract the package to your desired location
3. Run `StreamerOCR.exe`

### Source Installation

```bash
# Clone the repository
git clone [repository-url]
cd StreamerOCR

# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Run the application
python src/main.py
```

## Usage

1. Launch StreamerOCR
2. Select your target monitor from the dropdown
3. Click "Select Region" or press `Alt + Shift + M`
4. Click and drag to select the desired area
5. Name your region when prompted
6. Press `Alt + Shift + Space` to process the region

### Hotkeys

- `Alt + Shift + Space`: Process selected region
- `Alt + Shift + M`: Select new region
- `Alt + Shift + N`: Exit application

## Documentation

For detailed documentation, please see:
- [Quick Start Guide](docs/overview.html)
- [Full Documentation](docs/DOCS.html)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. 