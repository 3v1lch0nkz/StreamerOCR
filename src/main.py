import sys
import os
import json
import keyboard
import warnings

# Add the project root directory to Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QStyle, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QTimer

# Filter out the deprecation warning
warnings.filterwarnings("ignore", category=DeprecationWarning)

from src.gui.region_selector import RegionSelector
from src.ocr.processor import OCRProcessor
from src.tts.speaker import TTSSpeaker

class StreamerOCR(QWidget):
    def __init__(self):
        super().__init__()
        print("Initializing StreamerOCR...")
        
        self.ocr = OCRProcessor()
        self.tts = TTSSpeaker()
        self.current_region = None
        self.selector = None
        self.processing = False
        self.init_ui()
        self.setup_hotkeys()
        self.load_regions()
        
        # Setup processing timer
        self.process_timer = QTimer()
        self.process_timer.timeout.connect(self.check_hotkeys)
        self.process_timer.start(100)  # Check every 100ms
        
        print("StreamerOCR initialized successfully")
        print("Hotkeys:")
        print("- Alt+Shift+Space: Process selected region")
        print("- Alt+Shift+M: Select new region")
        print("- Alt+Shift+N: Exit application")

    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle('StreamerOCR')
        self.setGeometry(100, 100, 300, 200)
        
        layout = QVBoxLayout()
        
        # Add hotkey information
        hotkey_label = QLabel(
            "Hotkeys:\n"
            "Alt+Shift+Space: Process region\n"
            "Alt+Shift+M: Select region\n"
            "Alt+Shift+N: Exit"
        )
        layout.addWidget(hotkey_label)
        
        self.status_label = QLabel("No region selected")
        layout.addWidget(self.status_label)
        
        select_btn = QPushButton("Select Region")
        select_btn.clicked.connect(self.select_region)
        layout.addWidget(select_btn)
        
        self.setLayout(layout)

    def setup_hotkeys(self):
        """Setup the global hotkeys."""
        print("Setting up hotkeys...")
        print("- Alt+Shift+Space: Process selected region")
        print("- Alt+Shift+M: Select new region")
        print("- Alt+Shift+N: Exit application")

    def check_hotkeys(self):
        """Check if hotkeys are pressed."""
        if not self.processing and keyboard.is_pressed('alt+shift+space'):
            self.process_current_region()
        elif keyboard.is_pressed('alt+shift+m'):
            self.select_region()
        elif keyboard.is_pressed('alt+shift+n'):
            self.quit_application()

    def quit_application(self):
        """Quit the application with confirmation."""
        reply = QMessageBox.question(
            self, 'Exit StreamerOCR',
            "Are you sure you want to exit?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            print("Exiting StreamerOCR...")
            QApplication.quit()

    def select_region(self):
        """Open the region selector."""
        if self.selector is None or not self.selector.isVisible():
            self.hide()  # Hide the main window while selecting
            self.selector = RegionSelector()
            self.selector.region_selected.connect(self.on_region_selected)
            # Connect the close event to show the main window again
            self.selector.destroyed.connect(self.show)

    def on_region_selected(self, region):
        """Handle the selected region."""
        self.current_region = region
        self.status_label.setText(f"Region selected: {region}")
        self.save_regions()
        print(f"Region selected and saved: {region}")

    def process_current_region(self):
        """Process the currently selected region with OCR and TTS."""
        if self.processing:
            return
            
        print("\nProcessing current region...")
        if not self.current_region:
            print("No region selected!")
            QMessageBox.warning(
                self,
                "StreamerOCR",
                "No region selected! Please select a region first.",
                QMessageBox.Ok
            )
            return

        self.processing = True
        print(f"Capturing region: {self.current_region}")
        
        try:
            text = self.ocr.process_region(self.current_region)
            print(f"OCR Result: {text}")
            
            if text and text.strip():
                print("Text found, converting to speech...")
                self.tts.speak(text)
            else:
                print("No text found in the region")
                QMessageBox.information(
                    self,
                    "StreamerOCR",
                    "No text found in the selected region.",
                    QMessageBox.Ok
                )
        except Exception as e:
            print(f"Error processing region: {e}")
            QMessageBox.critical(
                self,
                "StreamerOCR",
                f"Error processing region: {str(e)}",
                QMessageBox.Ok
            )
        finally:
            self.processing = False

    def save_regions(self):
        """Save the current region configuration."""
        with open('regions.json', 'w') as f:
            json.dump({'current_region': self.current_region}, f)

    def load_regions(self):
        """Load the saved region configuration."""
        try:
            with open('regions.json', 'r') as f:
                data = json.load(f)
                self.current_region = data.get('current_region')
                if self.current_region:
                    self.status_label.setText(f"Region loaded: {self.current_region}")
                    print(f"Loaded saved region: {self.current_region}")
        except FileNotFoundError:
            print("No saved regions found")
            pass

def main():
    print("\n=== Starting StreamerOCR ===")
    
    # Create the QApplication instance
    if not QApplication.instance():
        app = QApplication(sys.argv)
    else:
        app = QApplication.instance()
    
    print("QApplication instance created")
    
    # Create and show the main window
    window = StreamerOCR()
    window.show()
    
    print("Application window displayed")
    print("Press Alt+Shift+Space to process the selected region")
    print("Press Alt+Shift+M to select a new region")
    print("Press Alt+Shift+N to exit the application")
    
    # Start the event loop
    return_code = app.exec_()
    print("Application closed")
    sys.exit(return_code)

if __name__ == '__main__':
    main() 