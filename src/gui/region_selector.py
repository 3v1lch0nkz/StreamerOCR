from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtCore import Qt, pyqtSignal, QPoint, QRect
from PyQt5.QtGui import QPainter, QColor, QPen, QScreen

class RegionSelector(QWidget):
    """Widget for selecting a screen region."""
    
    region_selected = pyqtSignal(tuple)

    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Set geometry to match the selected screen
        screen_geometry = screen.geometry()
        self.setGeometry(screen_geometry)
        
        # Selection properties
        self.selection_start = None
        self.selection_end = None
        self.selection_rect = None
        self.selection_color = QColor(255, 0, 0, 128)  # Semi-transparent red
        self.selection_border_color = QColor(255, 0, 0)  # Solid red
        self.selection_border_width = 2
        
        # Show the selector
        self.showFullScreen()
        self.setCursor(Qt.CrossCursor)

    def paintEvent(self, event):
        """Draw the selection overlay."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Draw semi-transparent overlay
        painter.fillRect(self.rect(), QColor(0, 0, 0, 128))
        
        # Draw selection rectangle if there is one
        if self.selection_rect:
            # Clear the selected area
            painter.eraseRect(self.selection_rect)
            
            # Draw border around selection
            painter.setPen(QPen(self.selection_border_color, self.selection_border_width))
            painter.drawRect(self.selection_rect)
            
            # Draw semi-transparent fill
            painter.fillRect(self.selection_rect, self.selection_color)

    def mousePressEvent(self, event):
        """Handle mouse press to start selection."""
        if event.button() == Qt.LeftButton:
            self.selection_start = event.pos()
            self.selection_end = self.selection_start
            self.update()

    def mouseMoveEvent(self, event):
        """Handle mouse movement to update selection."""
        if self.selection_start:
            self.selection_end = event.pos()
            self.selection_rect = QRect(
                min(self.selection_start.x(), self.selection_end.x()),
                min(self.selection_start.y(), self.selection_end.y()),
                abs(self.selection_start.x() - self.selection_end.x()),
                abs(self.selection_start.y() - self.selection_end.y())
            )
            self.update()

    def mouseReleaseEvent(self, event):
        """Handle mouse release to complete selection."""
        if event.button() == Qt.LeftButton and self.selection_rect:
            if self.selection_rect.width() > 10 and self.selection_rect.height() > 10:
                # Convert coordinates to screen-relative
                screen_pos = self.screen.geometry().topLeft()
                region = (
                    self.selection_rect.x() + screen_pos.x(),
                    self.selection_rect.y() + screen_pos.y(),
                    self.selection_rect.width(),
                    self.selection_rect.height()
                )
                self.region_selected.emit(region)
                self.close()

    def keyPressEvent(self, event):
        """Handle escape key to cancel selection."""
        if event.key() == Qt.Key_Escape:
            self.close() 