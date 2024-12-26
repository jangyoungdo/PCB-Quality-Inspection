from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from ui.roi_stream_window import ROIStreamWindow
from utils.image_processing import create_roi_pixmap
from config.settings import COLOR_ANGLE

class ROIWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_layout = QVBoxLayout(self)
        self.grid_layout = QGridLayout()
        self.main_layout.addLayout(self.grid_layout)
        self.roi_labels = []
        self.roi_rects = []
        self.stream_windows = []

    def calculate_grid_dimensions(self, n):
        cols = max(1, min(3, n))
        rows = (n + cols - 1) // cols
        return rows, cols

    def get_color(self, index):
        hue = (index * COLOR_ANGLE) % 360
        color = QColor.fromHsv(hue, 255, 255)
        return color.name()

    def set_roi_rects(self, rects):
        for window in self.stream_windows:
            window.close()
        self.stream_windows.clear()
        
        self.roi_rects = rects
        
        for i, rect in enumerate(rects):
            stream_window = ROIStreamWindow(i, rect, self.get_color(i), self.parent())
            stream_window.show()
            self.stream_windows.append(stream_window)
            
        self.display_roi()

    def display_roi(self):
        for label in self.roi_labels:
            label.deleteLater()
        self.roi_labels.clear()

        rows, cols = self.calculate_grid_dimensions(len(self.roi_rects))

        for i in range(len(self.roi_rects)):
            label = QLabel(f"ROI {i + 1}")
            size = min(570 // cols, 570 // rows)
            label.setFixedSize(size, size)
            label.setStyleSheet(
                f"border: 3px solid {self.get_color(i)}; "
                "background-color: lightgray; font-size: 24px; text-align: center;"
            )
            label.setAlignment(Qt.AlignCenter)
            self.grid_layout.addWidget(label, i // cols, i % cols, Qt.AlignCenter)
            self.roi_labels.append(label)

    def update_roi_images(self, frame):
        for i, (rect, label) in enumerate(zip(self.roi_rects, self.roi_labels)):
            x, y, w, h = rect
            if y+h <= frame.shape[0] and x+w <= frame.shape[1]:
                roi_frame = frame[y:y+h, x:x+w]
                label_width = label.width() - 6
                label_height = label.height() - 6
                
                pixmap = create_roi_pixmap(roi_frame, label_width, label_height)
                label.setPixmap(pixmap)
        
        for window in self.stream_windows:
            window.update_stream(frame)