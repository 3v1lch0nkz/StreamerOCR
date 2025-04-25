from PIL import Image, ImageGrab
import d3dshot
import numpy as np
import time

def test_region_capture_pillow(region):
    """Test region capture using PIL."""
    print("\nTesting PIL region capture...")
    try:
        x, y, width, height = region
        bbox = (x, y, x + width, y + height)
        
        # Capture using PIL
        screenshot = ImageGrab.grab(bbox=bbox)
        
        # Save for verification
        screenshot.save("test_region_pil.png")
        print(f"Region captured and saved as 'test_region_pil.png'")
        print(f"Image size: {screenshot.size}")
        return True
    except Exception as e:
        print(f"PIL region capture failed: {e}")
        return False

def test_region_capture_d3d(region):
    """Test region capture using d3dshot."""
    print("\nTesting d3dshot region capture...")
    try:
        d3d = d3dshot.create(capture_output="numpy")
        x, y, width, height = region
        
        # Capture using d3dshot
        screenshot = d3d.screenshot(region=(x, y, x + width, y + height))
        
        if screenshot is not None:
            # Convert to PIL and save
            img = Image.fromarray(screenshot)
            img.save("test_region_d3d.png")
            print(f"Region captured and saved as 'test_region_d3d.png'")
            print(f"Image size: {img.size}")
            return True
        else:
            print("d3dshot capture returned None")
            return False
    except Exception as e:
        print(f"d3dshot region capture failed: {e}")
        return False

def test_region_to_text(region):
    """Test converting a captured region to text using OCR."""
    print("\nTesting region to text conversion...")
    try:
        import pytesseract
        
        # Try both capture methods
        methods = [
            ("PIL", test_region_capture_pillow),
            ("d3dshot", test_region_capture_d3d)
        ]
        
        for method_name, capture_func in methods:
            print(f"\nTrying {method_name}...")
            if capture_func(region):
                # Load the captured image
                img_path = f"test_region_{method_name.lower()}.png"
                img = Image.open(img_path)
                
                # Perform OCR
                text = pytesseract.image_to_string(img)
                print(f"OCR Result from {method_name}: {text.strip()}")
        
        return True
    except Exception as e:
        print(f"Region to text conversion failed: {e}")
        return False

if __name__ == "__main__":
    print("=== Region Capture Tests ===")
    
    # Test region (x, y, width, height)
    test_region = (100, 100, 400, 100)  # Adjust these coordinates as needed
    
    print(f"Testing with region: {test_region}")
    time.sleep(2)  # Give time to prepare the screen
    
    pil_ok = test_region_capture_pillow(test_region)
    print(f"PIL region capture test: {'PASSED' if pil_ok else 'FAILED'}")
    
    d3d_ok = test_region_capture_d3d(test_region)
    print(f"d3dshot region capture test: {'PASSED' if d3d_ok else 'FAILED'}")
    
    if pil_ok or d3d_ok:
        ocr_ok = test_region_to_text(test_region)
        print(f"Region to text test: {'PASSED' if ocr_ok else 'FAILED'}") 