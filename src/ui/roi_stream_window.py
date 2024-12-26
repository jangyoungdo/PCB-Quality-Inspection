from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QSizePolicy, QMessageBox
from PyQt5.QtCore import Qt
from utils.image_processing import create_roi_pixmap
from utils.validators import validate_roi_dimensions
from config.settings import STREAM_WINDOW_MIN_SIZE, STREAM_WINDOW_DEFAULT_SIZE, STREAM_WINDOW_OFFSET

class ROIStreamWindow(QDialog):
    def __init__(self, roi_id, roi_rect, color, parent=None):
        super().__init__(parent)
        self.roi_id = roi_id
        self.roi_rect = roi_rect
        self.color = color
        
        self.setWindowTitle(f"ROI {roi_id + 1} Stream")
        self.setGeometry(
            STREAM_WINDOW_OFFSET + roi_id * STREAM_WINDOW_OFFSET, 
            STREAM_WINDOW_OFFSET + roi_id * STREAM_WINDOW_OFFSET, 
            STREAM_WINDOW_DEFAULT_SIZE, 
            STREAM_WINDOW_DEFAULT_SIZE
        )
        
        self.setMinimumSize(STREAM_WINDOW_MIN_SIZE, STREAM_WINDOW_MIN_SIZE)
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout()
        self.stream_label = QLabel()
        self.stream_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.stream_label.setStyleSheet(f"border: 3px solid {self.color}; background-color: black;")
        self.stream_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.stream_label)
        self.setLayout(layout)

    def update_stream(self, frame):
        if not validate_roi_dimensions(
            self.roi_id + 1, 
            *self.roi_rect, 
            frame.shape[1], 
            frame.shape[0], 
            self
        ):
            return
            
        try:
            x, y, w, h = self.roi_rect
            roi_frame = frame[y:y+h, x:x+w]
            display_w = self.stream_label.width() - 6
            display_h = self.stream_label.height() - 6
            
            if display_w <= 0 or display_h <= 0:
                return
                
            pixmap = create_roi_pixmap(roi_frame, display_w, display_h)
            self.stream_label.setPixmap(pixmap)
            
        except Exception as e:
            QMessageBox.warning(self, "ROI Error", 
                f"Error processing ROI {self.roi_id + 1}: {str(e)}")

    def update_roi_rect(self, new_rect):
        self.roi_rect = new_rect

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if hasattr(self.parent(), 'update_frame'):
            self.parent().update_frame()

    def closeEvent(self, event):
        event.accept()