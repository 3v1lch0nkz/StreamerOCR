import unittest
from src.ocr.processor import OCRProcessor

class TestOCRProcessor(unittest.TestCase):
    def setUp(self):
        self.processor = OCRProcessor()

    def test_capture_region(self):
        # Test region capture
        region = (0, 0, 100, 100)
        image = self.processor.capture_region(region)
        self.assertIsNotNone(image)
        self.assertEqual(image.size, (100, 100))

    def tearDown(self):
        del self.processor

if __name__ == '__main__':
    unittest.main() 