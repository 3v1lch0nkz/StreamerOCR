import sys
import os

# Add the project root directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel
from PyQt5.QtCore import Qt, QTimer
from src.gui.region_selector import RegionSelector

class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        print("Test window initialized")
        
    def initUI(self):
        self.setWindowTitle('Region Selector Test')
        self.setGeometry(100, 100, 400, 300)
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Add a test area
        self.test_area = QLabel("Test Area - Try selecting this!")
        self.test_area.setStyleSheet("""
            QLabel {
                font-size: 24px;
                padding: 20px;
                background-color: white;
                color: black;
                border: 1px solid black;
            }
        """)
        layout.addWidget(self.test_area)
        
        # Add status label
        self.status_label = QLabel("No region selected")
        layout.addWidget(self.status_label)
        
        # Add button to trigger region selection
        select_btn = QPushButton('Select Region')
        select_btn.clicked.connect(self.start_selection)
        layout.addWidget(select_btn)
        
        print("UI setup complete")
        
    def start_selection(self):
        """Start the region selection process."""
        print("Starting region selection...")
        self.hide()  # Hide the main window during selection
        self.selector = RegionSelector()
        self.selector.region_selected.connect(self.on_region_selected)
        self.selector.destroyed.connect(self.show)  # Show main window when selector is closed
        
    def on_region_selected(self, region):
        """Handle the selected region."""
        x, y, w, h = region
        print(f"Region selected: x={x}, y={y}, width={w}, height={h}")
        self.status_label.setText(f"Selected Region: x={x}, y={y}, width={w}, height={h}")
        
        # Schedule application to quit after showing the result
        QTimer.singleShot(1000, self.close_application)
        
    def close_application(self):
        """Clean up and close the application."""
        print("Test completed. Closing application...")
        QApplication.quit()

def main():
    print("\n=== Starting Region Selector Test ===")
    
    # Create the QApplication instance
    if not QApplication.instance():
        app = QApplication(sys.argv)
    else:
        app = QApplication.instance()
    
    print("QApplication instance created")
    
    # Create and show the main window
    window = TestWindow()
    window.show()
    
    print("Main window displayed. Please select a region using the button.")
    
    # Start the event loop
    return_code = app.exec_()
    print("Application event loop ended")
    sys.exit(return_code)

if __name__ == '__main__':
    main() 