import sys
import json
import keyboard
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

from gui.region_selector import RegionSelector
from ocr.processor import OCRProcessor
from tts.speaker import TTSSpeaker

class StreamerOCR(QWidget):
    def __init__(self):
        super().__init__()
        self.ocr = OCRProcessor()
        self.tts = TTSSpeaker()
        self.current_region = None
        self.init_ui()
        self.setup_hotkey()
        self.load_regions()

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
            # If icon is not found, the application will still work
            pass
            
        tray_menu = QMenu()
        configure_action = tray_menu.addAction("Configure")
        configure_action.triggered.connect(self.show)
        quit_action = tray_menu.addAction("Quit")
        quit_action.triggered.connect(QApplication.quit)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

    def setup_hotkey(self):
        """Setup the global hotkey for OCR processing."""
        keyboard.add_hotkey('ctrl+shift+o', self.process_current_region)

    def select_region(self):
        """Open the region selector."""
        self.selector = RegionSelector()
        self.selector.region_selected.connect(self.on_region_selected)

    def on_region_selected(self, region):
        """Handle the selected region."""
        self.current_region = region
        self.status_label.setText(f"Region selected: {region}")
        self.save_regions()

    def process_current_region(self):
        """Process the currently selected region with OCR and TTS."""
        if not self.current_region:
            return
            
        text = self.ocr.process_region(self.current_region)
        self.tts.speak(text)

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
    app = QApplication(sys.argv)
    window = StreamerOCR()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main() 