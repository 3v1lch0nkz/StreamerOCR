import sys
import json
import keyboard
import warnings
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QWidget, QVBoxLayout, QPushButton, QLabel, QStyle
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
        self.setup_hotkey()
        self.load_regions()
        
        # Setup processing timer
        self.process_timer = QTimer()
        self.process_timer.timeout.connect(self.check_hotkey)
        self.process_timer.start(100)  # Check every 100ms
        
        print("StreamerOCR initialized successfully")

    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle('StreamerOCR')
        self.setGeometry(100, 100, 300, 200)
        
        layout = QVBoxLayout()
        
        self.status_label = QLabel("No region selected")
        layout.addWidget(self.status_label)
        
        select_btn = QPushButton("Select Region")
        select_btn.clicked.connect(self.select_region)
        layout.addWidget(select_btn)
        
        self.setLayout(layout)
        
        # Setup system tray
        self.tray_icon = QSystemTrayIcon(self)
        self.setup_tray_icon()

    def setup_tray_icon(self):
        """Setup the system tray icon and menu."""
        try:
            self.tray_icon.setIcon(QIcon("resources/icon.png"))
        except:
            # If icon is not found, create a default system tray icon
            self.tray_icon.setIcon(self.style().standardIcon(QStyle.SP_ComputerIcon))
            
        tray_menu = QMenu()
        configure_action = tray_menu.addAction("Configure")
        configure_action.triggered.connect(self.show)
        quit_action = tray_menu.addAction("Quit")
        quit_action.triggered.connect(QApplication.quit)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

    def setup_hotkey(self):
        """Setup the global hotkey for OCR processing."""
        print("Setting up hotkey (Ctrl+Shift+O)...")

    def check_hotkey(self):
        """Check if the hotkey is pressed."""
        if not self.processing and keyboard.is_pressed('ctrl+shift+o'):
            self.process_current_region()

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

    def process_current_region(self):
        """Process the currently selected region with OCR and TTS."""
        if self.processing:
            return
            
        print("\nProcessing current region...")
        if not self.current_region:
            print("No region selected!")
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
        except Exception as e:
            print(f"Error processing region: {e}")
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
        except FileNotFoundError:
            pass

def main():
    # Create the QApplication instance
    if not QApplication.instance():
        app = QApplication(sys.argv)
    else:
        app = QApplication.instance()
        
    # Create and show the main window
    window = StreamerOCR()
    window.show()
    
    # Start the event loop
    sys.exit(app.exec_())

if __name__ == '__main__':
    main() 