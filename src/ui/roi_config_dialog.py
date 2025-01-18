from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
<<<<<<< HEAD
                             QTableWidget, QTableWidgetItem, QSpinBox, QLabel, 
                             QMessageBox, QGroupBox, QFormLayout)
from PyQt5.QtGui import QColor, QPen, QPainter
from PyQt5.QtCore import Qt
=======
                             QTableWidget, QTableWidgetItem, QLabel, QMessageBox, QGroupBox, QFormLayout)
from PyQt5.QtGui import QColor, QPen, QPainter
from PyQt5.QtCore import Qt, QRect
>>>>>>> 79017c7 (2025-01-18)
from utils.image_processing import frame_to_pixmap
from config.settings import MAX_WIDTH, MAX_HEIGHT, COLOR_ANGLE

class ROIConfigDialog(QDialog):
    def __init__(self, parent=None, frame=None, roi_rects=None):
        super().__init__(parent)
        self.setWindowTitle("ROI Configuration")
        self.setGeometry(200, 200, 1500, 450)

        self.frame = frame
<<<<<<< HEAD
        self.roi_spinners = []
        self.colors = []
        self.selected_roi_idx = None  # 현재 선택된 ROI 인덱스
        self._init_ui()
        self.initialize_rois(roi_rects if roi_rects else [(50, 50, 100, 100)])
=======
        self.roi_rects = roi_rects if roi_rects else [(50, 50, 100, 100)]
        self.colors = []
        self.selected_roi_idx = None  # 현재 선택된 ROI 인덱스
        self.roi_counter = 0  # 고유한 ROI 이름을 위한 카운터

        # 드래그 상태
        self.drawing = False
        self.start_point = None
        self.end_point = None

        self._init_ui()
        self.initialize_rois()
>>>>>>> 79017c7 (2025-01-18)

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
        self.roi_table.setSelectionBehavior(QTableWidget.SelectRows)  # 행 선택 모드
        self.roi_table.setSelectionMode(QTableWidget.SingleSelection)  # 단일 선택 모드
<<<<<<< HEAD
        self.roi_table.itemSelectionChanged.connect(self.update_range_info)
=======
>>>>>>> 79017c7 (2025-01-18)
        left_panel.addWidget(self.roi_table)

        # Apply 버튼
        self.apply_button = QPushButton("Apply ROI Changes")
        self.apply_button.clicked.connect(self.apply_changes)
        left_panel.addWidget(self.apply_button)

        layout.addLayout(left_panel)

<<<<<<< HEAD
        # Range 정보 표시
        self.range_group = QGroupBox("ROI Input Range")
        range_layout = QFormLayout()
        self.x_range_label = QLabel("N/A")
        self.y_range_label = QLabel("N/A")
        range_layout.addRow("x range:", self.x_range_label)
        range_layout.addRow("y range:", self.y_range_label)
        self.range_group.setLayout(range_layout)
        layout.addWidget(self.range_group)

=======
>>>>>>> 79017c7 (2025-01-18)
        # 프리뷰 이미지
        self.image_label = QLabel()
        self.image_label.setFixedSize(640, 480)
        self.image_label.setStyleSheet("border: 1px solid black;")
        layout.addWidget(self.image_label)

        self.setLayout(layout)

<<<<<<< HEAD
    def initialize_rois(self, roi_rects):
        self.roi_table.setRowCount(len(roi_rects))
        self.roi_spinners.clear()
        self.colors.clear()

        for i, rect in enumerate(roi_rects):
=======
    def initialize_rois(self):
        self.roi_table.setRowCount(len(self.roi_rects))
        self.colors.clear()

        for i, rect in enumerate(self.roi_rects):
>>>>>>> 79017c7 (2025-01-18)
            self.add_roi_row(i, rect)

        self.update_display()

    def add_roi_row(self, row_idx, rect=(50, 50, 100, 100)):
<<<<<<< HEAD
        roi_item = QTableWidgetItem(f"ROI{row_idx+1}")
        roi_item.setFlags(Qt.ItemIsEnabled)
        self.roi_table.setItem(row_idx, 0, roi_item)

        spinners = []
        max_values = [self.image_label.width(), self.image_label.height(), self.image_label.width(), self.image_label.height()]

        for col, (value, max_val) in enumerate(zip(rect, max_values), 1):
            spin = QSpinBox()
            spin.setRange(0, max_val)
            spin.setValue(value)

            def validate_and_update():
                x = self.roi_spinners[row_idx][0].value()
                y = self.roi_spinners[row_idx][1].value()
                w = self.roi_spinners[row_idx][2].value()
                h = self.roi_spinners[row_idx][3].value()

                if w <= 0 or h <= 0 or x + w > self.image_label.width() or y + h > self.image_label.height():
                    self._restore_and_warn(
                        row_idx,
                        rect,
                        "Invalid ROI",
                        f"ROI {row_idx + 1}: Region extends beyond image boundaries."
                    )

                self.update_display()
                self.update_range_info()

            spin.valueChanged.connect(validate_and_update)
            self.roi_table.setCellWidget(row_idx, col, spin)
            spinners.append(spin)

        self.roi_spinners.append(tuple(spinners))

        # ROI 색상 설정
        hue = (row_idx * COLOR_ANGLE) % 360
        color = QColor.fromHsv(hue, 255, 255)
        self.colors.append(color)

    def update_range_info(self):
        """현재 선택된 ROI의 x, y 범위 업데이트"""
        selected_row = self.roi_table.currentRow()  # 선택된 행 가져오기
        if selected_row < 0 or selected_row >= len(self.roi_spinners):
            # 선택된 행이 없거나 유효하지 않을 경우
            self.x_range_label.setText("N/A")
            self.y_range_label.setText("N/A")
            print("No valid ROI selected.")  # 디버깅 로그
            return

        # 선택된 ROI의 w, h 값 가져오기
        self.selected_roi_idx = selected_row
        spins = self.roi_spinners[self.selected_roi_idx]
        w = spins[2].value()
        h = spins[3].value()
        print(f"Selected ROI dimensions: w={w}, h={h}")  # 디버깅 로그

        # x, y 범위 계산
        x_max = self.image_label.width() - w
        y_max = self.image_label.height() - h

        # 범위 표시
        self.x_range_label.setText(f"0 ~ {x_max}")
        self.y_range_label.setText(f"0 ~ {y_max}")
        print(f"x range: 0 ~ {x_max}, y range: 0 ~ {y_max}")  # 디버깅 로그

    def _restore_and_warn(self, row_idx, previous_values, title, message):
        """값 복구와 에러 메시지 표시"""
        for i, spin in enumerate(self.roi_spinners[row_idx]):
            spin.blockSignals(True)
            spin.setValue(previous_values[i])
            spin.blockSignals(False)
        self.update_display()  # 복구된 값 화면에 반영

        # 비동기 메시지 창 표시
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.show()  # 비동기 방식으로 창 표시

    def add_roi(self):
        """새로운 ROI를 추가하는 메서드"""
        current_row = self.roi_table.rowCount()
        self.roi_table.setRowCount(current_row + 1)
        self.add_roi_row(current_row)
        self.update_display()

    def remove_roi(self):
        """ROI를 제거하는 메서드"""
        current_row = self.roi_table.rowCount()
        if current_row > 1:
            self.roi_table.setRowCount(current_row - 1)
            self.roi_spinners.pop()
            self.colors.pop()
            self.update_display()
        else:
            QMessageBox.warning(self, "Cannot Remove", 
                                "At least one ROI must remain.")

    def apply_changes(self):
        """현재 설정된 ROI 값을 적용하는 메서드"""
        valid_rois = []
        for i, spins in enumerate(self.roi_spinners):
            x, y, w, h = [spin.value() for spin in spins]
            # ROI 유효성 검사
            if w <= 0 or h <= 0:
                QMessageBox.warning(self, "Invalid Dimensions", 
                                    f"ROI {i + 1}: Width and height must be greater than 0")
                return
            if x + w > self.image_label.width() or y + h > self.image_label.height():
                QMessageBox.warning(self, "ROI Out of Bounds", 
                                    f"ROI {i + 1}: Region extends beyond image boundaries")
                return

=======
        roi_name_item = QTableWidgetItem(f"ROI {self.roi_counter + 1}")
        roi_name_item.setFlags(Qt.ItemIsEnabled)
        self.roi_table.setItem(row_idx, 0, roi_name_item)

        for col, value in enumerate(rect, start=1):
            item = QTableWidgetItem(str(value))
            self.roi_table.setItem(row_idx, col, item)

        # ROI 색상 설정
        hue = (self.roi_counter * COLOR_ANGLE) % 360
        color = QColor.fromHsv(hue, 255, 255)
        self.colors.append(color)

        self.roi_counter += 1

    def add_roi(self):
        """새로운 ROI를 추가하는 메서드"""
        row_idx = self.roi_table.rowCount()
        self.roi_table.setRowCount(row_idx + 1)
        self.add_roi_row(row_idx)
        self.update_display()

    def _convert_to_image_coords(self, widget_x, widget_y):
        """QWidget 좌표를 이미지 좌표로 변환"""
        img_width = self.image_label.width()
        img_height = self.image_label.height()
        frame_height, frame_width = self.frame.shape[:2]

        x = int(widget_x * frame_width / img_width) - 850  # x 오프셋 제거
        y = int(widget_y * frame_height / img_height)

        return max(0, x), max(0, y)  # 음수 값 방지

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.start_point = self._convert_to_image_coords(event.x(), event.y())
            self.end_point = self.start_point

    def mouseMoveEvent(self, event):
        if self.drawing:
            self.end_point = self._convert_to_image_coords(event.x(), event.y())
            self.update_display()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = False
            if self.start_point and self.end_point:
                x1, y1 = self.start_point
                x2, y2 = self.end_point
                rect = (min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1))
                self.add_roi_from_drag(rect)

    def add_roi_from_drag(self, rect):
        # 이미지 크기 가져오기
        frame_height, frame_width = self.frame.shape[:2]
        
        # 좌표 보정
        x, y, w, h = rect
        
        # x, y 좌표가 음수인 경우 0으로 조정
        x = max(0, x)
        y = max(0, y)
        
        # 너비와 높이가 이미지 범위를 벗어나지 않도록 조정
        w = min(w, frame_width - x)
        h = min(h, frame_height - y)
        
        # 너비나 높이가 0 이하인 경우 ROI 추가하지 않음
        if w <= 0 or h <= 0:
            return
            
        # 보정된 좌표로 ROI 추가
        row_idx = self.roi_table.rowCount()
        self.roi_table.setRowCount(row_idx + 1)
        self.add_roi_row(row_idx, (x, y, w, h))
        self.update_display()

    def remove_roi(self):
        current_row = self.roi_table.currentRow()
        if current_row >= 0:
            self.roi_table.removeRow(current_row)
            self.colors.pop(current_row)
            self.update_display()

    def get_roi_values(self):
        """현재 설정된 모든 ROI 값을 반환"""
        return [
            (
                int(self.roi_table.item(row, 1).text()),  # x
                int(self.roi_table.item(row, 2).text()),  # y
                int(self.roi_table.item(row, 3).text()),  # w
                int(self.roi_table.item(row, 4).text())   # h
            )
            for row in range(self.roi_table.rowCount())
        ]

    def apply_changes(self):
        valid_rois = []
        for row in range(self.roi_table.rowCount()):
            x = int(self.roi_table.item(row, 1).text())
            y = int(self.roi_table.item(row, 2).text())
            w = int(self.roi_table.item(row, 3).text())
            h = int(self.roi_table.item(row, 4).text())
>>>>>>> 79017c7 (2025-01-18)
            valid_rois.append((x, y, w, h))

        # 부모 객체로 ROI 값을 전달하여 업데이트
        if hasattr(self.parent(), 'update_streaming_windows'):
            self.parent().update_streaming_windows(valid_rois)

        self.accept()  # 대화상자 닫기

    def update_display(self):
<<<<<<< HEAD
        """ROI를 현재 설정에 맞게 업데이트"""
=======
>>>>>>> 79017c7 (2025-01-18)
        if self.frame is None:
            return

        try:
            display_frame = self.frame.copy()
            painter = QPainter()
            pixmap = frame_to_pixmap(display_frame, 
                                    self.image_label.width(), 
                                    self.image_label.height())

            painter.begin(pixmap)
<<<<<<< HEAD
            for i, spins in enumerate(self.roi_spinners):
                x, y, w, h = [spin.value() for spin in spins]
                pen = QPen(self.colors[i], 2)
                painter.setPen(pen)
                painter.drawRect(x, y, w, h)
=======
            for i in range(self.roi_table.rowCount()):
                x = int(self.roi_table.item(i, 1).text())
                y = int(self.roi_table.item(i, 2).text())
                w = int(self.roi_table.item(i, 3).text())
                h = int(self.roi_table.item(i, 4).text())
                pen = QPen(self.colors[i], 2)
                painter.setPen(pen)
                painter.drawRect(x, y, w, h)

            # 드래그 중인 사각형 그리기
            if self.drawing and self.start_point and self.end_point:
                x1, y1 = self.start_point
                x2, y2 = self.end_point
                pen = QPen(Qt.DashLine)
                pen.setColor(Qt.red)
                painter.setPen(pen)
                painter.drawRect(min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1))

>>>>>>> 79017c7 (2025-01-18)
            painter.end()

            self.image_label.setPixmap(pixmap)

        except Exception as e:
            QMessageBox.critical(self, "Error", 
                                f"Error updating display: {str(e)}")

<<<<<<< HEAD
    def get_roi_values(self):
        """현재 설정된 모든 ROI 값을 반환"""
        return [(spins[0].value(), spins[1].value(), spins[2].value(), spins[3].value())
                for spins in self.roi_spinners]
=======
>>>>>>> 79017c7 (2025-01-18)
