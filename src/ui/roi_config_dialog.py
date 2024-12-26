from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
                           QTableWidget, QTableWidgetItem, QSpinBox, QLabel, 
                           QMessageBox)
from PyQt5.QtGui import QColor, QPen, QPainter
from PyQt5.QtCore import Qt
from utils.image_processing import frame_to_pixmap
from config.settings import MAX_WIDTH, MAX_HEIGHT, COLOR_ANGLE

class ROIConfigDialog(QDialog):
    def __init__(self, parent=None, frame=None, roi_rects=None):
        super().__init__(parent)
        self.setWindowTitle("ROI Configuration")
        self.setGeometry(200, 200, 1500, 450)

        self.frame = frame
        self.roi_spinners = []
        self.colors = []
        self._init_ui()
        self.initialize_rois(roi_rects if roi_rects else [(50, 50, 100, 100)])

    def _init_ui(self):
        layout = QHBoxLayout()
        
        # Left Panel
        left_panel = QVBoxLayout()
        
        # ROI 관리 버튼들
        button_layout = QHBoxLayout()
        self.add_roi_button = QPushButton("Add ROI")
        self.remove_roi_button = QPushButton("Remove ROI")
        self.add_roi_button.clicked.connect(self.add_roi)
        self.remove_roi_button.clicked.connect(self.remove_roi)
        button_layout.addWidget(self.add_roi_button)
        button_layout.addWidget(self.remove_roi_button)
        left_panel.addLayout(button_layout)

        # ROI 테이블
        self.roi_table = QTableWidget()
        self.roi_table.setColumnCount(5)
        self.roi_table.setHorizontalHeaderLabels(["ROI", "x", "y", "w", "h"])
        self.roi_table.verticalHeader().setVisible(False)
        left_panel.addWidget(self.roi_table)

        # Apply 버튼
        self.apply_button = QPushButton("Apply ROI Changes")
        self.apply_button.clicked.connect(self.apply_changes)
        left_panel.addWidget(self.apply_button)

        layout.addLayout(left_panel)

        # 프리뷰 이미지
        self.image_label = QLabel()
        self.image_label.setFixedSize(640, 480)
        self.image_label.setStyleSheet("border: 1px solid black;")
        layout.addWidget(self.image_label)

        self.setLayout(layout)

    def initialize_rois(self, roi_rects):
        self.roi_table.setRowCount(len(roi_rects))
        self.roi_spinners.clear()
        self.colors.clear()

        for i, rect in enumerate(roi_rects):
            self.add_roi_row(i, rect)
        
        self.update_display()

    def add_roi_row(self, row_idx, rect=(50, 50, 100, 100)):
        roi_item = QTableWidgetItem(f"ROI{row_idx+1}")
        roi_item.setFlags(Qt.ItemIsEnabled)
        self.roi_table.setItem(row_idx, 0, roi_item)

        spinners = []
        max_values = [MAX_WIDTH, MAX_HEIGHT, MAX_WIDTH, MAX_HEIGHT]
        
        for col, (value, max_val) in enumerate(zip(rect, max_values), 1):
            spin = QSpinBox()
            spin.setRange(0, max_val)
            spin.setValue(value)
            
            # SpinBox 값이 변경될 때의 검증
            def validate_and_update():
                x = self.roi_spinners[row_idx][0].value()
                y = self.roi_spinners[row_idx][1].value()
                w = self.roi_spinners[row_idx][2].value()
                h = self.roi_spinners[row_idx][3].value()
                
                if w <= 0 or h <= 0:
                    QMessageBox.warning(self, "Invalid Dimensions", 
                        f"ROI {row_idx + 1}: Width and height must be greater than 0")
                elif x + w > MAX_WIDTH or y + h > MAX_HEIGHT:
                    QMessageBox.warning(self, "ROI Out of Bounds", 
                        f"ROI {row_idx + 1} extends beyond image boundaries")
                else:
                    self.update_display()
            
            spin.valueChanged.connect(validate_and_update)
            self.roi_table.setCellWidget(row_idx, col, spin)
            spinners.append(spin)

        self.roi_spinners.append(tuple(spinners))
        
        # ROI 색상 설정
        hue = (row_idx * COLOR_ANGLE) % 360
        color = QColor.fromHsv(hue, 255, 255)
        self.colors.append(color)

    def add_roi(self):
        current_row = self.roi_table.rowCount()
        self.roi_table.setRowCount(current_row + 1)
        self.add_roi_row(current_row)
        self.update_display()

    def remove_roi(self):
        current_row = self.roi_table.rowCount()
        if current_row > 1:
            self.roi_table.setRowCount(current_row - 1)
            self.roi_spinners.pop()
            self.colors.pop()
            self.update_display()
        else:
            QMessageBox.warning(self, "Cannot Remove", 
                "At least one ROI must remain.")

    def update_display(self):
        if self.frame is None:
            return

        try:
            display_frame = self.frame.copy()
            painter = QPainter()
            pixmap = frame_to_pixmap(display_frame, 
                                    self.image_label.width(), 
                                    self.image_label.height())

            painter.begin(pixmap)
            for i, spins in enumerate(self.roi_spinners):
                x, y, w, h = [spin.value() for spin in spins]
                pen = QPen(self.colors[i], 2)
                painter.setPen(pen)
                painter.drawRect(x, y, w, h)
            painter.end()

            self.image_label.setPixmap(pixmap)
            
            # 부모 객체의 스트리밍 윈도우 업데이트
            if hasattr(self.parent(), 'update_streaming_windows'):
                new_rois = self.get_roi_values()
                self.parent().update_streaming_windows(new_rois)
                
        except Exception as e:
            QMessageBox.critical(self, "Error", 
                f"Error updating display: {str(e)}")

    def get_roi_values(self):
        return [(spins[0].value(), spins[1].value(), 
                 spins[2].value(), spins[3].value()) 
                for spins in self.roi_spinners]

    def apply_changes(self):
        # ROI 값들의 유효성 검사
        for i, spins in enumerate(self.roi_spinners):
            x, y, w, h = [spin.value() for spin in spins]
            if w <= 0 or h <= 0:
                QMessageBox.warning(self, "Invalid Dimensions", 
                    f"ROI {i + 1}: Width and height must be greater than 0")
                return
            if x + w > MAX_WIDTH or y + h > MAX_HEIGHT:
                QMessageBox.warning(self, "ROI Out of Bounds", 
                    f"ROI {i + 1} extends beyond image boundaries")
                return
        
        self.accept()