import sys
import json
import keyboard
import pytesseract
import pyttsx3
from PyQt5.QtWidgets import (QApplication, QSystemTrayIcon, QMenu, 
                           QWidget, QVBoxLayout, QPushButton, QLabel)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, QRect
from PIL import ImageGrab
import mss
import mss.tools

class RegionSelector(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setGeometry(0, 0, 0, 0)
        self.start_point = None
        self.end_point = None
        self.region = None
        self.show()

    def mousePressEvent(self, event):
        self.start_point = event.pos()
        self.setGeometry(0, 0, 0, 0)

    def mouseMoveEvent(self, event):
        if self.start_point:
            self.end_point = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if self.start_point and self.end_point:
            x = min(self.start_point.x(), self.end_point.x())
            y = min(self.start_point.y(), self.end_point.y())
            width = abs(self.start_point.x() - self.end_point.x())
            height = abs(self.start_point.y() - self.end_point.y())
            self.region = (x, y, width, height)
            self.close()

class StreamerOCR(QWidget):
    def __init__(self):
        super().__init__()
        self.regions = {}
        self.current_region = None
        self.engine = pyttsx3.init()
        self.init_ui()
        self.load_regions()

    def init_ui(self):
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
        self.tray_icon.setIcon(QIcon("icon.png"))
        self.tray_icon.show()
        
        # Create tray menu
        tray_menu = QMenu()
        configure_action = tray_menu.addAction("Configure")
        configure_action.triggered.connect(self.show)
        quit_action = tray_menu.addAction("Quit")
        quit_action.triggered.connect(QApplication.quit)
        self.tray_icon.setContextMenu(tray_menu)

    def select_region(self):
        self.selector = RegionSelector()
        self.selector.show()
        self.selector.region_selected.connect(self.on_region_selected)

    def on_region_selected(self, region):
        self.current_region = region
        self.status_label.setText(f"Region selected: {region}")
        self.save_regions()

    def capture_and_process(self):
        if not self.current_region:
            return
        
        with mss.mss() as sct:
            screenshot = sct.grab(self.current_region)
            image = Image.frombytes('RGB', screenshot.size, screenshot.rgb)
            
            # Perform OCR
            text = pytesseract.image_to_string(image)
            
            # Convert to speech
            self.engine.say(text)
            self.engine.runAndWait()

    def save_regions(self):
        with open('regions.json', 'w') as f:
            json.dump(self.regions, f)

    def load_regions(self):
        try:
            with open('regions.json', 'r') as f:
                self.regions = json.load(f)
        except FileNotFoundError:
            self.regions = {}

def main():
    app = QApplication(sys.argv)
    window = StreamerOCR()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main() 