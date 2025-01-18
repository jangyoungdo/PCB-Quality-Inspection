from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
                           QTableWidget, QTableWidgetItem, QLabel, QMessageBox,
                           QSpinBox, QGroupBox, QFormLayout, QToolButton,
                           QCheckBox, QStackedWidget, QWidget)
from PyQt5.QtGui import QColor, QPen, QPainter, QFont, QIcon
from PyQt5.QtCore import Qt, QRect
from utils.image_processing import frame_to_pixmap
from config.settings import COLOR_ANGLE, AVAILABLE_MODELS, MODEL_DEFAULT_SETTINGS
import cv2
import numpy as np

class RGBSettingsPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.frame = None
        self.roi_rects = []
        self.colors = []
        self.is_eyedropper_active = False
        self.current_rgb = None
        self._init_ui()

    def _init_ui(self):
        layout = QHBoxLayout()

        # Left Panel (ROI 테이블)
        left_panel = QVBoxLayout()
        self._setup_roi_table(left_panel)
        layout.addLayout(left_panel)

        # Middle Panel (이미지 표시)
        middle_panel = QVBoxLayout()
        self._setup_image_display(middle_panel)
        layout.addLayout(middle_panel)

        # Right Panel (RGB 설정)
        right_panel = QVBoxLayout()
        self._setup_rgb_controls(right_panel)
        layout.addLayout(right_panel)

        self.setLayout(layout)

    def _setup_roi_table(self, layout):
        self.roi_table = QTableWidget()
        self.roi_table.setColumnCount(6)
        self.roi_table.setHorizontalHeaderLabels(["ROI", "x", "y", "w", "h", "RGB"])
        self.roi_table.verticalHeader().setVisible(False)
        self.roi_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.roi_table.setSelectionMode(QTableWidget.SingleSelection)
        self.roi_table.itemSelectionChanged.connect(self._on_roi_selection_changed)
        layout.addWidget(self.roi_table)

    def _setup_image_display(self, layout):
        self.image_label = QLabel()
        self.image_label.setFixedSize(640, 480)
        self.image_label.setStyleSheet("border: 1px solid black;")
        self.image_label.setMouseTracking(True)
        self.image_label.mousePressEvent = self.on_image_click
        self.image_label.mouseMoveEvent = self.on_mouse_move
        layout.addWidget(self.image_label)
        layout.setAlignment(self.image_label, Qt.AlignCenter)

    def _setup_rgb_controls(self, layout):
        rgb_group = QGroupBox("RGB 설정")
        rgb_layout = QFormLayout()

        # 스포이드 버튼
        self.eyedropper_button = QToolButton()
        self.eyedropper_button.setText("스포이드")
        self.eyedropper_button.setCheckable(True)
        self.eyedropper_button.clicked.connect(self.toggle_eyedropper)
        rgb_layout.addRow("색상 선택:", self.eyedropper_button)

        # 허용 오차 설정
        self.tolerance_spin = QSpinBox()
        self.tolerance_spin.setRange(0, 255)
        self.tolerance_spin.setValue(MODEL_DEFAULT_SETTINGS['RGB']['tolerance'])
        rgb_layout.addRow("허용 오차:", self.tolerance_spin)

        # RGB 범위 설정
        self.rgb_controls = {}
        for color in ['R', 'G', 'B']:
            group = QGroupBox(f"{color} 범위")
            group_layout = QFormLayout()
            
            min_spin = QSpinBox()
            max_spin = QSpinBox()
            min_spin.setRange(0, 255)
            max_spin.setRange(0, 255)
            min_spin.setValue(0)
            max_spin.setValue(255)
            
            group_layout.addRow("최소값:", min_spin)
            group_layout.addRow("최대값:", max_spin)
            
            self.rgb_controls[color] = {
                'min': min_spin,
                'max': max_spin
            }
            
            group.setLayout(group_layout)
            rgb_layout.addRow(group)

        rgb_group.setLayout(rgb_layout)
        layout.addWidget(rgb_group)

    def toggle_eyedropper(self):
        """스포이드 모드 토글"""
        self.is_eyedropper_active = self.eyedropper_button.isChecked()
        if self.is_eyedropper_active:
            self.image_label.setCursor(Qt.CrossCursor)  # 십자 커서로 변경
        else:
            self.image_label.setCursor(Qt.ArrowCursor)  # 기본 커서로 복귀

    def on_image_click(self, event):
        """이미지 클릭 이벤트 처리"""
        if self.frame is None:
            return

        # 이미지 내 실제 좌표 계산
        frame_height, frame_width = self.frame.shape[:2]
        label_width = self.image_label.width()
        label_height = self.image_label.height()
        
        x = int(event.x() * frame_width / label_width)
        y = int(event.y() * frame_height / label_height)

        if self.is_eyedropper_active:
            # 스포이드 모드일 때의 처리
            if 0 <= x < frame_width and 0 <= y < frame_height:
                b, g, r = self.frame[y, x]
                self.current_rgb = (r, g, b)
                
                current_row = self.roi_table.currentRow()
                if current_row >= 0:
                    tolerance = self.tolerance_spin.value()
                    rgb_text = f"R:{r}±{tolerance}, G:{g}±{tolerance}, B:{b}±{tolerance}"
                    
                    if self.roi_table.item(current_row, 5) is None:
                        self.roi_table.setItem(current_row, 5, QTableWidgetItem())
                    
                    self.roi_table.item(current_row, 5).setText(rgb_text)
                    
                    for color, value in zip(['R', 'G', 'B'], [r, g, b]):
                        min_val = max(0, value - tolerance)
                        max_val = min(255, value + tolerance)
                        self.rgb_controls[color]['min'].setValue(min_val)
                        self.rgb_controls[color]['max'].setValue(max_val)
                
                self.eyedropper_button.setChecked(False)
                self.toggle_eyedropper()
        else:
            # ROI 선택 모드일 때의 처리
            for i in range(self.roi_table.rowCount()):
                try:
                    roi_x = int(self.roi_table.item(i, 1).text())
                    roi_y = int(self.roi_table.item(i, 2).text())
                    roi_w = int(self.roi_table.item(i, 3).text())
                    roi_h = int(self.roi_table.item(i, 4).text())
                    
                    # 클릭 좌표가 ROI 영역 내에 있는지 확인
                    if (roi_x <= x <= roi_x + roi_w) and (roi_y <= y <= roi_y + roi_h):
                        self.roi_table.selectRow(i)
                        break
                except (ValueError, AttributeError):
                    continue

    def on_mouse_move(self, event):
        """마우스 이동 이벤트 처리"""
        if self.is_eyedropper_active:
            self.image_label.setCursor(Qt.CrossCursor)
        else:
            self.image_label.setCursor(Qt.ArrowCursor)

    def _on_roi_selection_changed(self):
        current_row = self.roi_table.currentRow()
        if current_row >= 0:
            try:
                rgb_item = self.roi_table.item(current_row, 5)
                if rgb_item is None or rgb_item.text() == "미설정":
                    for color in ['R', 'G', 'B']:
                        self.rgb_controls[color]['min'].setValue(0)
                        self.rgb_controls[color]['max'].setValue(255)
                    return

                rgb_text = rgb_item.text()
                rgb_parts = rgb_text.split(', ')
                for part in rgb_parts:
                    color, values = part.split(':')
                    value, tolerance = map(int, values.split('±'))
                    
                    self.rgb_controls[color]['min'].setValue(max(0, value - tolerance))
                    self.rgb_controls[color]['max'].setValue(min(255, value + tolerance))
                    
                self.tolerance_spin.setValue(tolerance)
                
            except (ValueError, KeyError, AttributeError) as e:
                print(f"Error processing RGB values: {str(e)}")
                for color in ['R', 'G', 'B']:
                    self.rgb_controls[color]['min'].setValue(0)
                    self.rgb_controls[color]['max'].setValue(255)

    def update_display(self):
        if self.frame is None:
            return

        try:
            display_frame = self.frame.copy()
            pixmap = frame_to_pixmap(display_frame, 
                                   self.image_label.width(), 
                                   self.image_label.height())

            painter = QPainter(pixmap)
            for i in range(self.roi_table.rowCount()):
                x = int(self.roi_table.item(i, 1).text())
                y = int(self.roi_table.item(i, 2).text())
                w = int(self.roi_table.item(i, 3).text())
                h = int(self.roi_table.item(i, 4).text())
                
                pen = QPen(self.colors[i], 2)
                painter.setPen(pen)
                painter.drawRect(x, y, w, h)
                
                painter.setFont(QFont("Arial", 10, QFont.Bold))
                text = f"ROI {i + 1}"
                painter.drawText(QRect(x, y, 50, 20), Qt.AlignLeft, text)

            painter.end()
            self.image_label.setPixmap(pixmap)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error updating display: {str(e)}")

    def set_frame(self, frame):
        self.frame = frame
        self.update_display()

    def set_roi_data(self, roi_data):
        self.roi_rects = roi_data
        self.initialize_rois()

    def initialize_rois(self):
        if not self.roi_rects:
            return
            
        self.roi_table.setRowCount(len(self.roi_rects))
        self.colors.clear()

        for i, rect in enumerate(self.roi_rects):
            roi_name_item = QTableWidgetItem(f"ROI {i + 1}")
            roi_name_item.setFlags(Qt.ItemIsEnabled)
            self.roi_table.setItem(i, 0, roi_name_item)

            for col, value in enumerate(rect, start=1):
                item = QTableWidgetItem(str(value))
                item.setFlags(Qt.ItemIsEnabled)
                self.roi_table.setItem(i, col, item)

            rgb_item = QTableWidgetItem("미설정")
            rgb_item.setFlags(Qt.ItemIsEnabled)
            self.roi_table.setItem(i, 5, rgb_item)

            hue = (i * COLOR_ANGLE) % 360
            color = QColor.fromHsv(hue, 255, 255)
            self.colors.append(color)

        self.update_display()

    def get_settings(self):
        """현재 설정값들을 딕셔너리로 반환"""
        settings = {
            'roi_settings': {}
        }
        
        # ROI별 RGB 설정 저장
        for i in range(self.roi_table.rowCount()):
            rgb_item = self.roi_table.item(i, 5)
            if rgb_item and rgb_item.text() != "미설정":
                settings['roi_settings'][i] = {
                    'rgb_text': rgb_item.text(),
                    'tolerance': self.tolerance_spin.value(),
                    'rgb_controls': {
                        color: {
                            'min': self.rgb_controls[color]['min'].value(),
                            'max': self.rgb_controls[color]['max'].value()
                        }
                        for color in ['R', 'G', 'B']
                    }
                }
        print("설정 저장:", settings)
        return settings
        
    def restore_settings(self, settings):
        """저장된 설정값들을 복원"""
        print("설정 복원 시도:", settings)
        if not settings:
            return
            
        roi_settings = settings.get('roi_settings', {})
        for roi_idx, roi_setting in roi_settings.items():
            if roi_idx >= self.roi_table.rowCount():
                continue
                
            # RGB 텍스트 복원
            if self.roi_table.item(roi_idx, 5) is None:
                self.roi_table.setItem(roi_idx, 5, QTableWidgetItem())
            self.roi_table.item(roi_idx, 5).setText(roi_setting['rgb_text'])
            
            # 허용 오차 복원
            self.tolerance_spin.setValue(roi_setting['tolerance'])
            
            # RGB 컨트롤 값 복원
            for color in ['R', 'G', 'B']:
                self.rgb_controls[color]['min'].setValue(
                    roi_setting['rgb_controls'][color]['min'])
                self.rgb_controls[color]['max'].setValue(
                    roi_setting['rgb_controls'][color]['max'])

class SimilaritySettingsPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel("유사도 검사 설정 (개발 중)"))
        self.setLayout(layout)

class DeepLearningSettingsPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel("딥러닝 검사 설정 (개발 중)"))
        self.setLayout(layout)

class ModelConfigDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("모델 설정")
        self.setGeometry(200, 200, 1800, 600)
        
        self.selected_models = parent.selected_models if hasattr(parent, 'selected_models') else set()
        self._init_ui()
        
        # 이전 선택 모델 체크 상태 복원
        for model_id in self.selected_models:
            if model_id in self.model_checkboxes:
                self.model_checkboxes[model_id].setChecked(True)

    def _init_ui(self):
        main_layout = QVBoxLayout()
        
        # 모델 선택 영역
        model_selection = QGroupBox("검사 모델 선택")
        model_layout = QVBoxLayout()
        
        self.model_checkboxes = {}
        for model_id, model_name in AVAILABLE_MODELS.items():
            checkbox = QCheckBox(model_name)
            checkbox.stateChanged.connect(self._on_model_selection_changed)
            self.model_checkboxes[model_id] = checkbox
            model_layout.addWidget(checkbox)
        
        model_selection.setLayout(model_layout)
        main_layout.addWidget(model_selection)
        
        # 설정 화면 스택
        self.settings_stack = QStackedWidget()
        
        # RGB 설정 페이지
        self.rgb_page = RGBSettingsPage(self)
        self.settings_stack.addWidget(self.rgb_page)
        
        # 유사도 설정 페이지
        self.similarity_page = SimilaritySettingsPage(self)
        self.settings_stack.addWidget(self.similarity_page)
        
        # 딥러닝 설정 페이지
        self.deep_learning_page = DeepLearningSettingsPage(self)
        self.settings_stack.addWidget(self.deep_learning_page)
        
        main_layout.addWidget(self.settings_stack)
        
        # 확인/취소 버튼
        button_layout = QHBoxLayout()
        ok_button = QPushButton("확인")
        cancel_button = QPushButton("취소")
        ok_button.clicked.connect(self.accept)
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)
        main_layout.addLayout(button_layout)
        
        self.setLayout(main_layout)

    def _on_model_selection_changed(self):
        sender = self.sender()
        for model_id, checkbox in self.model_checkboxes.items():
            if checkbox == sender:
                if checkbox.isChecked():
                    self.selected_models.add(model_id)
                    if model_id == 'RGB':
                        self.settings_stack.setCurrentWidget(self.rgb_page)
                    elif model_id == 'SIMILARITY':
                        self.settings_stack.setCurrentWidget(self.similarity_page)
                    elif model_id == 'DEEP_LEARNING':
                        self.settings_stack.setCurrentWidget(self.deep_learning_page)
                else:
                    self.selected_models.remove(model_id)

    def set_frame(self, frame):
        self.rgb_page.set_frame(frame)

    def set_roi_data(self, roi_data):
        self.rgb_page.set_roi_data(roi_data)

