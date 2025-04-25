import pytesseract
from PIL import Image
import mss

class OCRProcessor:
    """Handles OCR processing of screen regions."""

    def __init__(self):
        self.screen_capture = mss.mss()

    def capture_region(self, region):
        """Capture a specific region of the screen."""
        x, y, width, height = region
        bbox = {'top': y, 'left': x, 'width': width, 'height': height}
        screenshot = self.screen_capture.grab(bbox)
        return Image.frombytes('RGB', screenshot.size, screenshot.rgb)

    def process_image(self, image):
        """Process an image with OCR and return the text."""
        return pytesseract.image_to_string(image)

    def process_region(self, region):
        """Capture and process a screen region."""
        image = self.capture_region(region)
        return self.process_image(image)

    def __del__(self):
        """Clean up screen capture resources."""
        self.screen_capture.close() 