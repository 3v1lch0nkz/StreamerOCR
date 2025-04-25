import pytesseract
from PIL import Image
import os

def test_tesseract_installation():
    """Test if Tesseract is properly installed and accessible."""
    print("Testing Tesseract installation...")
    try:
        version = pytesseract.get_tesseract_version()
        print(f"Tesseract version: {version}")
        return True
    except Exception as e:
        print(f"Tesseract test failed: {e}")
        # Try to find Tesseract in common locations
        common_paths = [
            r"C:\Program Files\Tesseract-OCR\tesseract.exe",
            r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"
        ]
        for path in common_paths:
            if os.path.exists(path):
                print(f"Found Tesseract at: {path}")
                pytesseract.pytesseract.tesseract_cmd = path
                try:
                    version = pytesseract.get_tesseract_version()
                    print(f"Tesseract version after path set: {version}")
                    return True
                except:
                    continue
        return False

def test_ocr_with_sample_text():
    """Test OCR with a simple image containing text."""
    # Create a simple test image with text
    from PIL import Image, ImageDraw, ImageFont
    
    # Create a new image with white background
    img = Image.new('RGB', (200, 50), color='white')
    d = ImageDraw.Draw(img)
    
    # Add text to the image
    d.text((10,10), "Hello World", fill='black')
    
    # Save temporary image
    img.save("test_ocr.png")
    
    print("Testing OCR with sample text...")
    try:
        # Perform OCR
        text = pytesseract.image_to_string(img)
        print(f"OCR Result: {text.strip()}")
        
        # Clean up
        os.remove("test_ocr.png")
        return "Hello World" in text
    except Exception as e:
        print(f"OCR test failed: {e}")
        return False

if __name__ == "__main__":
    print("=== OCR Component Tests ===")
    tesseract_ok = test_tesseract_installation()
    print(f"Tesseract installation test: {'PASSED' if tesseract_ok else 'FAILED'}")
    
    if tesseract_ok:
        ocr_ok = test_ocr_with_sample_text()
        print(f"OCR functionality test: {'PASSED' if ocr_ok else 'FAILED'}") 