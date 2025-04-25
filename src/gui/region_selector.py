from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtCore import Qt, pyqtSignal, QPoint, QRect
from PyQt5.QtGui import QPainter, QColor, QPen, QScreen

class RegionSelector(QWidget):
    """Widget for selecting a screen region."""
    
    region_selected = pyqtSignal(tuple)

    def __init__(self):
        super().__init__()
        self.init_ui()
        self.start_point = None
        self.end_point = None
        self.is_selecting = False
        
    def init_ui(self):
        """Initialize the UI components."""
        # Set window flags for a fullscreen overlay
        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setCursor(Qt.CrossCursor)
        
        # Get the primary screen
        screen = QApplication.primaryScreen()
        if screen:
            geometry = screen.geometry()
            self.setGeometry(geometry)
        
        # Make the window fullscreen
        self.showFullScreen()

    def paintEvent(self, event):
        """Draw the selection overlay."""
        painter = QPainter(self)
        
        # Draw semi-transparent dark overlay
        painter.fillRect(self.rect(), QColor(0, 0, 0, 128))
        
        if self.start_point and self.end_point:
            # Calculate selection rectangle
            selection = self.get_selection_rect()
            
            # Clear the selected area
            painter.eraseRect(selection)
            
            # Draw red border around selection
            painter.setPen(QPen(QColor(255, 0, 0), 2))
            painter.drawRect(selection)

    def get_selection_rect(self):
        """Get the rectangle of the current selection."""
        if not self.start_point or not self.end_point:
            return QRect()
            
        return QRect(
            min(self.start_point.x(), self.end_point.x()),
            min(self.start_point.y(), self.end_point.y()),
            abs(self.start_point.x() - self.end_point.x()),
            abs(self.start_point.y() - self.end_point.y())
        )

    def mousePressEvent(self, event):
        """Handle mouse press to start selection."""
        if event.button() == Qt.LeftButton:
            self.start_point = event.pos()
            self.end_point = self.start_point
            self.is_selecting = True
            self.update()

    def mouseMoveEvent(self, event):
        """Handle mouse movement to update selection."""
        if self.is_selecting:
            self.end_point = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        """Handle mouse release to complete selection."""
        if event.button() == Qt.LeftButton and self.is_selecting:
            self.is_selecting = False
            selection = self.get_selection_rect()
            
            # Only emit if selection is large enough
            if selection.width() > 10 and selection.height() > 10:
                self.region_selected.emit((
                    selection.x(),
                    selection.y(),
                    selection.width(),
                    selection.height()
                ))
            self.close()

    def keyPressEvent(self, event):
        """Handle escape key to cancel selection."""
        if event.key() == Qt.Key_Escape:
            self.close() 