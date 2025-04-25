import os
import sys

def test_environment():
    """Test Python environment."""
    print("=== Environment Test ===")
    print(f"Python version: {sys.version}")
    print(f"Python executable: {sys.executable}")
    print(f"Working directory: {os.getcwd()}")

def test_imports():
    """Test importing each required package."""
    print("\n=== Import Tests ===")
    
    # Test pyttsx3
    print("\nTesting pyttsx3 import...")
    try:
        import pyttsx3
        print("pyttsx3 imported successfully")
        print(f"Version: {getattr(pyttsx3, '__version__', 'version not available')}")
    except ImportError as e:
        print(f"Failed to import pyttsx3: {e}")
    
    # Test PIL
    print("\nTesting PIL import...")
    try:
        from PIL import Image, ImageDraw
        print("PIL imported successfully")
        print(f"Version: {Image.__version__}")
    except ImportError as e:
        print(f"Failed to import PIL: {e}")
    
    # Test pytesseract
    print("\nTesting pytesseract import...")
    try:
        import pytesseract
        print("pytesseract imported successfully")
        try:
            version = pytesseract.get_tesseract_version()
            print(f"Tesseract version: {version}")
        except Exception as e:
            print(f"Tesseract not properly configured: {e}")
    except ImportError as e:
        print(f"Failed to import pytesseract: {e}")

def test_tts_basic():
    """Basic TTS test."""
    print("\n=== Basic TTS Test ===")
    try:
        import pyttsx3
        engine = pyttsx3.init()
        print("TTS engine initialized successfully")
        
        # Get available voices
        voices = engine.getProperty('voices')
        print(f"Available voices: {len(voices)}")
        
        # Test properties
        rate = engine.getProperty('rate')
        volume = engine.getProperty('volume')
        print(f"Rate: {rate}")
        print(f"Volume: {volume}")
        
        engine.stop()
        return True
    except Exception as e:
        print(f"TTS test failed: {e}")
        return False

def test_ocr_basic():
    """Basic OCR test with a simple image."""
    print("\n=== Basic OCR Test ===")
    try:
        import pytesseract
        from PIL import Image, ImageDraw
        
        # Create a simple test image
        img = Image.new('RGB', (100, 30), color='white')
        d = ImageDraw.Draw(img)
        d.text((10, 10), "Test", fill='black')
        
        # Save the test image
        img.save("test_ocr.png")
        print("Created test image: test_ocr.png")
        
        # Try OCR
        text = pytesseract.image_to_string(img)
        print(f"OCR result: {text.strip()}")
        
        # Clean up
        os.remove("test_ocr.png")
        return True
    except Exception as e:
        print(f"OCR test failed: {e}")
        print("If this is a Tesseract error, make sure Tesseract is installed and in your PATH")
        return False

if __name__ == "__main__":
    test_environment()
    test_imports()
    
    print("\nRunning component tests...")
    tts_ok = test_tts_basic()
    print(f"Basic TTS test: {'PASSED' if tts_ok else 'FAILED'}")
    
    ocr_ok = test_ocr_basic()
    print(f"Basic OCR test: {'PASSED' if ocr_ok else 'FAILED'}") 