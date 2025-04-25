import pytesseract
from PIL import Image
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QScreen
import tempfile

class OCRProcessor:
    """Handles OCR processing of screen regions."""

    def __init__(self):
        print("Initializing OCR processor...")
        
        # Check Tesseract installation
        try:
            tesseract_path = pytesseract.get_tesseract_version()
            print(f"Tesseract version: {tesseract_path}")
        except Exception as e:
            print(f"Warning: Tesseract not found. Please ensure Tesseract is installed and in PATH. Error: {e}")
            # Try to find Tesseract in common locations
            common_paths = [
                r"C:\Program Files\Tesseract-OCR\tesseract.exe",
                r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"
            ]
            for path in common_paths:
                if os.path.exists(path):
                    print(f"Found Tesseract at: {path}")
                    pytesseract.pytesseract.tesseract_cmd = path
                    break

    def capture_region(self, region):
        """Capture a specific region of the screen using PyQt5."""
        print(f"Capturing region: {region}")
        try:
            x, y, width, height = region
            screen = QApplication.primaryScreen()
            if not screen:
                print("Error: Could not get primary screen")
                return None
                
            # Capture the region
            pixmap = screen.grabWindow(0, x, y, width, height)
            if pixmap.isNull():
                print("Error: Screen capture failed - null pixmap")
                return None
                
            # Save to temporary file
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
                temp_path = tmp_file.name
                pixmap.save(temp_path, "PNG")
                
            # Load with PIL
            img = Image.open(temp_path)
            
            # Clean up temporary file
            os.unlink(temp_path)
            
            print("Screenshot captured successfully")
            return img
            
        except Exception as e:
            print(f"Error capturing screenshot: {e}")
            return None

    def process_image(self, image):
        """Process an image with OCR and return the text."""
        if image is None:
            return ""
        try:
            text = pytesseract.image_to_string(image)
            print(f"OCR processed successfully, found text: {text}")
            return text
        except Exception as e:
            print(f"Error during OCR processing: {e}")
            return ""

    def process_region(self, region):
        """Capture and process a screen region."""
        image = self.capture_region(region)
        return self.process_image(image)

    def __del__(self):
        """Clean up resources."""
        if hasattr(self, 'd3d'):
            self.d3d.stop() 