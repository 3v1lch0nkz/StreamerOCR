import sys
import os
import json
import keyboard
import warnings

# Add the project root directory to Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, 
                           QLabel, QStyle, QMessageBox, QListWidget, QInputDialog,
                           QHBoxLayout, QListWidgetItem, QComboBox)
from PyQt5.QtGui import QIcon, QPainter, QColor, QFont
from PyQt5.QtCore import Qt, QTimer, QRect

# Filter out the deprecation warning
warnings.filterwarnings("ignore", category=DeprecationWarning)

from src.gui.region_selector import RegionSelector
from src.ocr.processor import OCRProcessor
from src.tts.speaker import TTSSpeaker

class OverlayWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(
            Qt.FramelessWindowHint | 
            Qt.WindowStaysOnTopHint | 
            Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.text = ""
        self.font_size = 20
        self.text_color = QColor(255, 255, 255)  # White text
        self.bg_color = QColor(0, 0, 0, 180)  # Semi-transparent black background
        self.padding = 10
        self.show()

    def set_text(self, text):
        self.text = text
        self.update_geometry()
        self.update()

    def update_geometry(self):
        if not self.text:
            return
            
        # Create a temporary painter to measure text
        painter = QPainter()
        font = QFont()
        font.setPointSize(self.font_size)
        painter.setFont(font)
        
        # Calculate text dimensions
        text_rect = painter.boundingRect(
            QRect(0, 0, 1000, 1000),
            Qt.TextWordWrap,
            self.text
        )
        
        # Set window size with padding
        width = text_rect.width() + (2 * self.padding)
        height = text_rect.height() + (2 * self.padding)
        
        # Position in top-right corner of primary screen
        screen_geometry = QApplication.primaryScreen().geometry()
        x = screen_geometry.width() - width - 20  # 20px from right edge
        y = 20  # 20px from top
        
        self.setGeometry(x, y, width, height)

    def paintEvent(self, event):
        if not self.text:
            return
            
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Draw background
        painter.fillRect(self.rect(), self.bg_color)
        
        # Draw text
        painter.setPen(self.text_color)
        font = QFont()
        font.setPointSize(self.font_size)
        painter.setFont(font)
        
        painter.drawText(
            self.rect().adjusted(self.padding, self.padding, -self.padding, -self.padding),
            Qt.TextWordWrap,
            self.text
        )

class StreamerOCR(QWidget):
    def __init__(self):
        super().__init__()
        print("Initializing StreamerOCR...")
        
        self.ocr = OCRProcessor()
        self.tts = TTSSpeaker()
        self.regions = {}  # Dictionary to store named regions
        self.current_region_name = None
        self.selector = None
        self.processing = False
        self.overlay = OverlayWindow()
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
        self.setGeometry(100, 100, 400, 400)  # Increased window size
        
        layout = QVBoxLayout()
        
        # Add hotkey information
        hotkey_label = QLabel(
            "Hotkeys:\n"
            "Alt+Shift+Space: Process region\n"
            "Alt+Shift+M: Select region\n"
            "Alt+Shift+N: Exit"
        )
        layout.addWidget(hotkey_label)
        
        # Monitor selection
        monitor_layout = QHBoxLayout()
        monitor_layout.addWidget(QLabel("Monitor:"))
        self.monitor_combo = QComboBox()
        self.update_monitor_list()
        monitor_layout.addWidget(self.monitor_combo)
        layout.addLayout(monitor_layout)
        
        # Region list
        self.region_list = QListWidget()
        self.region_list.itemClicked.connect(self.on_region_selected)
        layout.addWidget(QLabel("Saved Regions:"))
        layout.addWidget(self.region_list)
        
        # Buttons layout
        buttons_layout = QHBoxLayout()
        
        select_btn = QPushButton("Select Region")
        select_btn.clicked.connect(self.select_region)
        buttons_layout.addWidget(select_btn)
        
        rename_btn = QPushButton("Rename")
        rename_btn.clicked.connect(self.rename_region)
        buttons_layout.addWidget(rename_btn)
        
        delete_btn = QPushButton("Delete")
        delete_btn.clicked.connect(self.delete_region)
        buttons_layout.addWidget(delete_btn)
        
        layout.addLayout(buttons_layout)
        
        self.status_label = QLabel("No region selected")
        layout.addWidget(self.status_label)
        
        self.setLayout(layout)
        self.update_region_list()

    def update_monitor_list(self):
        """Update the monitor selection combo box."""
        self.monitor_combo.clear()
        screens = QApplication.screens()
        for i, screen in enumerate(screens, 1):
            self.monitor_combo.addItem(f"Monitor {i} ({screen.size().width()}x{screen.size().height()})", i-1)

    def update_region_list(self):
        """Update the region list widget with current regions."""
        self.region_list.clear()
        for name in self.regions:
            monitor_index = self.regions[name]['monitor']
            item = QListWidgetItem(f"{name} (Monitor {monitor_index + 1})")
            self.region_list.addItem(item)
            if name == self.current_region_name:
                item.setSelected(True)

    def get_selected_screen(self):
        """Get the currently selected screen."""
        screen_index = self.monitor_combo.currentData()
        return QApplication.screens()[screen_index]

    def select_region(self):
        """Open the region selector."""
        if self.selector is None or not self.selector.isVisible():
            selected_screen = self.get_selected_screen()
            self.selector = RegionSelector(selected_screen)
            self.selector.region_selected.connect(self.on_region_selected)
            self.selector.show()

    def on_region_selected(self, region):
        """Handle the selected region."""
        if region:
            # Ask for region name
            name, ok = QInputDialog.getText(
                self, 'Region Name',
                'Enter a name for this region:',
                text='Region ' + str(len(self.regions) + 1)
            )
            
            if ok and name:
                # Store region with monitor information
                screen_index = self.monitor_combo.currentData()
                self.regions[name] = {
                    'region': region,
                    'monitor': screen_index
                }
                self.current_region_name = name
                self.status_label.setText(f"Region selected: {name} (Monitor {screen_index + 1})")
                self.save_regions()
                self.update_region_list()
                print(f"Region '{name}' selected and saved: {region} on Monitor {screen_index + 1}")
                
                # Close the selector
                if self.selector:
                    self.selector.close()
                    self.selector = None

    def rename_region(self):
        """Rename the currently selected region."""
        current_item = self.region_list.currentItem()
        if current_item:
            old_name = current_item.text()
            new_name, ok = QInputDialog.getText(
                self, 'Rename Region',
                'Enter new name:',
                text=old_name
            )
            
            if ok and new_name and new_name != old_name:
                if new_name in self.regions:
                    QMessageBox.warning(
                        self, 'Error',
                        'A region with this name already exists.',
                        QMessageBox.Ok
                    )
                    return
                
                self.regions[new_name] = self.regions.pop(old_name)
                if self.current_region_name == old_name:
                    self.current_region_name = new_name
                self.save_regions()
                self.update_region_list()

    def delete_region(self):
        """Delete the currently selected region."""
        current_item = self.region_list.currentItem()
        if current_item:
            name = current_item.text().split(" (Monitor")[0]  # Extract just the region name
            reply = QMessageBox.question(
                self, 'Delete Region',
                f'Are you sure you want to delete "{name}"?',
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                try:
                    # Remove the region from the dictionary
                    if name in self.regions:
                        del self.regions[name]
                        
                        # Update current region if needed
                        if self.current_region_name == name:
                            self.current_region_name = None
                            self.status_label.setText("No region selected")
                        
                        # Save the updated regions
                        self.save_regions()
                        
                        # Update the UI
                        self.update_region_list()
                        
                        print(f"Region '{name}' deleted successfully")
                    else:
                        print(f"Region '{name}' not found in regions dictionary")
                except Exception as e:
                    print(f"Error deleting region: {e}")
                    QMessageBox.critical(
                        self,
                        "Error",
                        f"Failed to delete region: {str(e)}",
                        QMessageBox.Ok
                    )

    def save_regions(self):
        """Save the regions configuration."""
        try:
            # Create a copy of regions with serializable data
            save_data = {
                'regions': self.regions,
                'current_region_name': self.current_region_name
            }
            
            # Save to file
            with open('regions.json', 'w') as f:
                json.dump(save_data, f, indent=4)
            print("Regions saved successfully")
        except Exception as e:
            print(f"Error saving regions: {e}")
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to save regions: {str(e)}",
                QMessageBox.Ok
            )

    def load_regions(self):
        """Load the saved regions configuration."""
        try:
            if os.path.exists('regions.json'):
                with open('regions.json', 'r') as f:
                    data = json.load(f)
                    self.regions = data.get('regions', {})
                    self.current_region_name = data.get('current_region_name')
                    if self.current_region_name:
                        self.status_label.setText(f"Region loaded: {self.current_region_name}")
                        print(f"Loaded saved region: {self.current_region_name}")
                    print(f"Loaded {len(self.regions)} regions")
            else:
                print("No saved regions found")
                self.regions = {}
                self.current_region_name = None
        except Exception as e:
            print(f"Error loading regions: {e}")
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to load regions: {str(e)}",
                QMessageBox.Ok
            )
            self.regions = {}
            self.current_region_name = None

    def process_current_region(self):
        """Process the currently selected region with OCR and TTS."""
        if self.processing:
            return
            
        print("\nProcessing current region...")
        if not self.current_region_name or self.current_region_name not in self.regions:
            print("No region selected!")
            QMessageBox.warning(
                self,
                "StreamerOCR",
                "No region selected! Please select a region first.",
                QMessageBox.Ok
            )
            return

        self.processing = True
        region_data = self.regions[self.current_region_name]
        region = region_data['region']
        monitor_index = region_data['monitor']
        
        print(f"Capturing region: {region} from Monitor {monitor_index + 1}")
        
        try:
            text = self.ocr.process_region(region, monitor_index)
            print(f"OCR Result: {text}")
            
            if text and text.strip():
                print("Text found, converting to speech...")
                self.tts.speak(text)
                # Update overlay with the text
                self.overlay.set_text(text)
            else:
                print("No text found in the region")
                self.overlay.set_text("")  # Clear overlay
                QMessageBox.information(
                    self,
                    "StreamerOCR",
                    "No text found in the selected region.",
                    QMessageBox.Ok
                )
        except Exception as e:
            print(f"Error processing region: {e}")
            self.overlay.set_text("")  # Clear overlay
            QMessageBox.critical(
                self,
                "StreamerOCR",
                f"Error processing region: {str(e)}",
                QMessageBox.Ok
            )
        finally:
            self.processing = False

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