import sys
import os
import json
import keyboard
import warnings

# Add the project root directory to Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QWidget, QVBoxLayout, QPushButton, QLabel, QStyle, QMessageBox
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
        
        # Check if system supports tray icons
        if not QSystemTrayIcon.isSystemTrayAvailable():
            QMessageBox.critical(None, "StreamerOCR",
                               "System tray is not available on this system")
            sys.exit(1)
            
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
        print("- Ctrl+Shift+O: Process selected region")
        print("- Ctrl+Shift+K: Show/restore window")
        print("- Ctrl+Shift+M: Exit application")

    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle('StreamerOCR')
        self.setGeometry(100, 100, 300, 200)
        
        layout = QVBoxLayout()
        
        # Add hotkey information
        hotkey_label = QLabel(
            "Hotkeys:\n"
            "Ctrl+Shift+O: Process region\n"
            "Ctrl+Shift+K: Show window\n"
            "Ctrl+Shift+M: Exit"
        )
        layout.addWidget(hotkey_label)
        
        self.status_label = QLabel("No region selected")
        layout.addWidget(self.status_label)
        
        select_btn = QPushButton("Select Region")
        select_btn.clicked.connect(self.select_region)
        layout.addWidget(select_btn)
        
        self.setLayout(layout)
        
        # Setup system tray
        self.create_tray_icon()
        
    def create_tray_icon(self):
        """Create and setup the system tray icon."""
        self.tray_icon = QSystemTrayIcon(self)
        
        # Try to load custom icon, fall back to system icon if needed
        try:
            icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "resources", "icon.png")
            if os.path.exists(icon_path):
                self.tray_icon.setIcon(QIcon(icon_path))
            else:
                self.tray_icon.setIcon(self.style().standardIcon(QStyle.SP_ComputerIcon))
        except:
            self.tray_icon.setIcon(self.style().standardIcon(QStyle.SP_ComputerIcon))
        
        # Create tray menu
        self.tray_menu = QMenu()
        
        # Add show/hide action
        self.toggle_window_action = self.tray_menu.addAction("Hide Window")
        self.toggle_window_action.triggered.connect(self.toggle_window)
        
        # Add select region action
        select_action = self.tray_menu.addAction("Select Region")
        select_action.triggered.connect(self.select_region)
        
        self.tray_menu.addSeparator()
        
        # Add quit action
        quit_action = self.tray_menu.addAction("Quit")
        quit_action.triggered.connect(self.quit_application)
        
        # Set the menu and enable tray icon
        self.tray_icon.setContextMenu(self.tray_menu)
        self.tray_icon.activated.connect(self.tray_icon_activated)
        
        # Set tooltip with all hotkeys
        self.tray_icon.setToolTip(
            "StreamerOCR\n"
            "Ctrl+Shift+O: Process region\n"
            "Ctrl+Shift+K: Show window\n"
            "Ctrl+Shift+M: Exit"
        )
        
        # Show the tray icon
        self.tray_icon.show()

    def tray_icon_activated(self, reason):
        """Handle tray icon activation."""
        if reason == QSystemTrayIcon.DoubleClick:
            self.toggle_window()

    def toggle_window(self):
        """Toggle the window visibility."""
        if self.isVisible():
            self.hide()
            self.toggle_window_action.setText("Show Window")
        else:
            self.show()
            self.toggle_window_action.setText("Hide Window")
            self.activateWindow()  # Bring window to front

    def closeEvent(self, event):
        """Handle the window close event."""
        event.ignore()  # Prevent the window from being destroyed
        self.hide()
        self.toggle_window_action.setText("Show Window")
        self.tray_icon.showMessage(
            "StreamerOCR",
            "Application minimized to tray.\nPress Ctrl+Shift+K or double-click tray icon to restore.",
            QSystemTrayIcon.Information,
            2000
        )

    def setup_hotkeys(self):
        """Setup the global hotkeys."""
        print("Setting up hotkeys...")
        print("- Ctrl+Shift+O: Process selected region")
        print("- Ctrl+Shift+K: Show/restore window")
        print("- Ctrl+Shift+M: Exit application")

    def check_hotkeys(self):
        """Check if hotkeys are pressed."""
        if not self.processing and keyboard.is_pressed('ctrl+shift+o'):
            self.process_current_region()
        elif keyboard.is_pressed('ctrl+shift+k'):
            self.show_window()
        elif keyboard.is_pressed('ctrl+shift+m'):
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
        
        # Show notification
        self.tray_icon.showMessage(
            "StreamerOCR",
            "Region selected successfully. Press Ctrl+Shift+O to process.",
            QSystemTrayIcon.Information,
            2000
        )

    def process_current_region(self):
        """Process the currently selected region with OCR and TTS."""
        if self.processing:
            return
            
        print("\nProcessing current region...")
        if not self.current_region:
            print("No region selected!")
            self.tray_icon.showMessage(
                "StreamerOCR",
                "No region selected! Please select a region first.",
                QSystemTrayIcon.Warning,
                2000
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
                self.tray_icon.showMessage(
                    "StreamerOCR",
                    "No text found in the selected region.",
                    QSystemTrayIcon.Information,
                    2000
                )
        except Exception as e:
            print(f"Error processing region: {e}")
            self.tray_icon.showMessage(
                "StreamerOCR",
                f"Error processing region: {str(e)}",
                QSystemTrayIcon.Critical,
                2000
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

    def show_window(self):
        """Show and activate the window."""
        if not self.isVisible():
            self.show()
            self.activateWindow()  # Bring window to front
            self.toggle_window_action.setText("Hide Window")
            print("Window restored")

def main():
    print("\n=== Starting StreamerOCR ===")
    
    # Create the QApplication instance
    if not QApplication.instance():
        app = QApplication(sys.argv)
    else:
        app = QApplication.instance()
    
    # Enable system tray if available
    if not QSystemTrayIcon.isSystemTrayAvailable():
        QMessageBox.critical(None, "StreamerOCR",
                           "System tray is not available on this system")
        sys.exit(1)
    
    QApplication.setQuitOnLastWindowClosed(False)  # Prevent app from quitting when window is closed
    
    print("QApplication instance created")
    
    # Create and show the main window
    window = StreamerOCR()
    window.show()
    
    print("Application window displayed")
    print("Press Ctrl+Shift+O to process the selected region")
    print("Press Ctrl+Shift+M to exit the application")
    
    # Start the event loop
    return_code = app.exec_()
    print("Application closed")
    sys.exit(return_code)

if __name__ == '__main__':
    main() 