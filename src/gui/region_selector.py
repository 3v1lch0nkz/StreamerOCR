from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, pyqtSignal

class RegionSelector(QWidget):
    """Widget for selecting a screen region."""
    
    region_selected = pyqtSignal(tuple)

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
            self.region_selected.emit(self.region)
            self.close() 