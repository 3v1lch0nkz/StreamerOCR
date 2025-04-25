import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt, QTimer, QRect
from PyQt5.QtGui import QScreen, QPixmap
import time
import pyttsx3
import pytesseract
from PIL import Image
import os
import tempfile
import traceback

class TestWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.current_region = None
        self.tts_engine = pyttsx3.init()
        
    def initUI(self):
        self.setWindowTitle('Integration Test')
        self.setGeometry(100, 100, 400, 300)
        
        layout = QVBoxLayout()
        
        # Create a test area with known text
        self.test_text = QLabel("Hello World - OCR Test")
        self.test_text.setStyleSheet("""
            QLabel {
                font-size: 24px;
                padding: 20px;
                background-color: white;
                color: black;
                border: 1px solid black;
            }
        """)
        layout.addWidget(self.test_text)
        
        # Status label
        self.status_label = QLabel("Status: Ready")
        layout.addWidget(self.status_label)
        
        # Add test buttons
        test_region_btn = QPushButton('Test Region Selection')
        test_region_btn.clicked.connect(self.test_region_selection)
        layout.addWidget(test_region_btn)
        
        test_ocr_btn = QPushButton('Test OCR on Region')
        test_ocr_btn.clicked.connect(self.test_ocr)
        layout.addWidget(test_ocr_btn)
        
        test_tts_btn = QPushButton('Test TTS')
        test_tts_btn.clicked.connect(self.test_tts)
        layout.addWidget(test_tts_btn)
        
        test_all_btn = QPushButton('Test Full Integration')
        test_all_btn.clicked.connect(self.test_full_integration)
        layout.addWidget(test_all_btn)
        
        self.setLayout(layout)
    
    def update_status(self, message):
        self.status_label.setText(f"Status: {message}")
        print(message)
        QApplication.processEvents()  # Ensure UI updates
    
    def test_region_selection(self):
        """Test region selection functionality."""
        self.update_status("Select the test text area...")
        
        # Get the geometry of the test text label
        rect = self.test_text.geometry()
        global_pos = self.test_text.mapToGlobal(rect.topLeft())
        
        self.current_region = QRect(
            global_pos.x(),
            global_pos.y(),
            rect.width(),
            rect.height()
        )
        
        self.update_status(f"Region selected: {self.current_region}")
    
    def test_ocr(self):
        """Test OCR on the selected region."""
        if not self.current_region:
            self.update_status("Please select a region first")
            return
            
        try:
            self.update_status("Preparing to capture screen...")
            screen = QApplication.primaryScreen()
            
            # Capture the screen region
            self.update_status(f"Capturing region: {self.current_region}")
            pixmap = screen.grabWindow(
                0,
                self.current_region.x(),
                self.current_region.y(),
                self.current_region.width(),
                self.current_region.height()
            )
            
            if pixmap.isNull():
                raise Exception("Screen capture failed - null pixmap")
                
            # Save to temporary file
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
                temp_path = tmp_file.name
                pixmap.save(temp_path, "PNG")
                
            # Open with PIL and perform OCR
            self.update_status("Performing OCR...")
            img = Image.open(temp_path)
            text = pytesseract.image_to_string(img).strip()
            
            # Clean up temporary file
            os.unlink(temp_path)
            
            self.update_status(f"OCR Result: {text}")
            return text
            
        except Exception as e:
            self.update_status(f"OCR Error: {str(e)}")
            print("Full error:", traceback.format_exc())
            return None
    
    def test_tts(self):
        """Test TTS with a sample text."""
        try:
            text = "Testing text to speech integration"
            self.update_status(f"Speaking: {text}")
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
            self.update_status("TTS test completed")
        except Exception as e:
            self.update_status(f"TTS Error: {str(e)}")
    
    def test_full_integration(self):
        """Test the full integration of region selection, OCR, and TTS."""
        self.update_status("Starting full integration test...")
        self.test_region_selection()
        QTimer.singleShot(500, self._continue_integration_test)
    
    def _continue_integration_test(self):
        text = self.test_ocr()
        if text:
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
            self.update_status("Full integration test completed")
        else:
            self.update_status("Integration test failed at OCR stage")

def main():
    app = QApplication(sys.argv)
    window = TestWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main() 