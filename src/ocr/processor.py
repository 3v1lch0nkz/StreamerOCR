import pytesseract
from PIL import Image
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QScreen
from PyQt5.QtCore import QBuffer, QByteArray
import io
import mss
import numpy as np

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

        # Initialize the screen capture tool
        self.sct = mss.mss()

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
                
            # Convert QPixmap to PIL Image using memory buffer
            buffer = QBuffer()
            buffer.open(QBuffer.ReadWrite)
            pixmap.save(buffer, "PNG")
            
            # Convert QBuffer to PIL Image
            pil_img = Image.open(io.BytesIO(buffer.data()))
            buffer.close()
            
            print("Screenshot captured successfully")
            return pil_img
            
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

    def process_region(self, region, monitor_index=0):
        """
        Process a region of the screen with OCR.
        
        Args:
            region (tuple): (x, y, width, height) of the region to capture
            monitor_index (int): Index of the monitor to capture from (0-based)
            
        Returns:
            str: Extracted text from the region
        """
        try:
            # Get the monitor geometry
            monitor = self.sct.monitors[monitor_index + 1]  # monitors[0] is all monitors
            
            # Adjust region coordinates relative to the monitor
            x = region[0] - monitor['left']
            y = region[1] - monitor['top']
            width = region[2]
            height = region[3]
            
            # Capture the region
            screenshot = self.sct.grab({
                'left': x,
                'top': y,
                'width': width,
                'height': height,
                'mon': monitor_index + 1  # Specify which monitor to capture
            })
            
            # Convert to PIL Image
            img = Image.frombytes('RGB', screenshot.size, screenshot.rgb)
            
            # Convert to grayscale for better OCR
            img = img.convert('L')
            
            # Perform OCR
            text = pytesseract.image_to_string(img)
            
            return text.strip()
            
        except Exception as e:
            print(f"Error in OCR processing: {str(e)}")
            return ""

    def __del__(self):
        """Clean up resources."""
        if hasattr(self, 'd3d'):
            self.d3d.stop()
        self.sct.close() 