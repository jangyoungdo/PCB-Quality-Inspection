<<<<<<< HEAD
import cv2
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QApplication, QSizePolicy, QAction, QMenuBar, QPushButton, QFrame)
=======
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                           QLabel, QApplication, QSizePolicy, QAction, QMenuBar)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap  # QImage와 QPixmap 추가
import cv2
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QApplication, QSizePolicy, QAction, QMenuBar, QPushButton, QFrame, QGroupBox, QFormLayout, QDialog, QToolBar)
>>>>>>> 79017c7 (2025-01-18)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont, QColor
from ui.roi_config_dialog import ROIConfigDialog
from ui.roi_stream_window import ROIStreamWindow
<<<<<<< HEAD
from config.settings import DEFAULT_ROI, CAMERA_FPS
=======
from ui.model_config_dialog import ModelConfigDialog
from config.settings import DEFAULT_ROI, CAMERA_FPS
from ui.equipment_register_dialog import EquipmentRegisterDialog
from ui.product_register_dialog import ProductRegisterDialog
>>>>>>> 79017c7 (2025-01-18)
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VISION CONTROL")
<<<<<<< HEAD
        self.setGeometry(100, 100, 800, 400)

        # Streaming state
        self.streaming = True
=======
        self.setGeometry(100, 100, 1200, 600)

        # 등록 정보를 저장할 변수들
        self.current_equipment = None
        self.current_product = None

        # 메뉴바 설정
        self._setup_menu()
        
        # 정보 툴바 설정
        self._setup_info_toolbar()
>>>>>>> 79017c7 (2025-01-18)

        # Central widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout()
        self.central_widget.setLayout(self.main_layout)

<<<<<<< HEAD
        # Left layout (1:3 ratio)
        self.left_layout = QVBoxLayout()
        self._setup_left_panel()
        self.main_layout.addLayout(self.left_layout, 1)
=======
        # 카메라 설정 - 초기화를 더 앞으로 이동
        self.camera = cv2.VideoCapture(0)
        self.timer = QTimer(self)  # parent 설정
        self.timer.timeout.connect(self.update_frame)

        # 왼쪽 패널 설정
        left_panel = self._setup_left_panel()
        self.main_layout.addWidget(left_panel)

        # 타이머 시작
        self.timer.start(30)

        # Streaming state
        self.streaming = True
>>>>>>> 79017c7 (2025-01-18)

        # Right layout (2:3 ratio)
        self.right_layout = QVBoxLayout()
        self._setup_right_panel()
<<<<<<< HEAD
        self.main_layout.addLayout(self.right_layout, 4)
=======
        self.main_layout.addLayout(self.right_layout, 3)
>>>>>>> 79017c7 (2025-01-18)

        # Camera and timer setup
        self._setup_camera()
        self._setup_timer()

        # Menu bar setup
<<<<<<< HEAD
        self._setup_menu()
=======
        self.menu_bar = QMenuBar(self)
        self.setMenuBar(self.menu_bar)

        # ROI 메뉴
        roi_menu = self.menu_bar.addMenu("ROI")
        configure_action = QAction("Configure ROI", self)
        configure_action.triggered.connect(self.open_roi_config)
        roi_menu.addAction(configure_action)

        # 설정 메뉴
        settings_menu = self.menu_bar.addMenu("설정")
        model_config_action = QAction("모델 설정", self)
        model_config_action.triggered.connect(self.open_model_config)
        settings_menu.addAction(model_config_action)

        # 등록 메뉴 추가
        register_menu = self.menu_bar.addMenu("등록")
        
        # 장비 등록 액션
        equipment_action = QAction("장비 등록", self)
        equipment_action.triggered.connect(self.open_equipment_register)
        register_menu.addAction(equipment_action)
        
        # 제품 등록 액션
        product_action = QAction("제품 등록", self)
        product_action.triggered.connect(self.open_product_register)
        register_menu.addAction(product_action)
>>>>>>> 79017c7 (2025-01-18)

        # ROI settings
        self.roi_rects = DEFAULT_ROI
        self.stream_windows = []
<<<<<<< HEAD

    def _setup_left_panel(self):
        # 검사 결과 (박스 포함)
        result_box = QFrame()
        result_box.setFrameShape(QFrame.Box)
        result_box.setLineWidth(2)
        result_layout = QVBoxLayout()

        result_label = QLabel("검사 결과")
        result_label.setAlignment(Qt.AlignCenter)
        result_label.setFont(QFont("Arial", 14))

        # 불통과 (빨간색 텍스트)
        self.fail_label = QLabel("불통과")
        self.fail_label.setAlignment(Qt.AlignCenter)
        self.fail_label.setFont(QFont("Arial", 24, QFont.Bold))
        self.fail_label.setStyleSheet("color: red;")

        result_layout.addWidget(result_label)
        result_layout.addWidget(self.fail_label)
        result_box.setLayout(result_layout)

        # 현재 상태 (박스 포함)
        status_box = QFrame()
        status_box.setFrameShape(QFrame.Box)
        status_box.setLineWidth(2)
        status_layout = QVBoxLayout()

        status_label = QLabel("현재 상태")
        status_label.setAlignment(Qt.AlignCenter)
        status_label.setFont(QFont("Arial", 14))

        # 대기중/구동중 버튼 (상태 전환)
        self.status_button = QPushButton("구동중")
        self.status_button.setFont(QFont("Arial", 20, QFont.Bold))
        self.status_button.setStyleSheet("background-color: lightgray; color: blue;")
        self.status_button.clicked.connect(self.toggle_streaming)

        status_layout.addWidget(status_label)
        status_layout.addWidget(self.status_button)
        status_box.setLayout(status_layout)

        # Add widgets to the left layout
        self.left_layout.addWidget(result_box)
        self.left_layout.addWidget(status_box)
        self.left_layout.setStretch(0, 3)
        self.left_layout.setStretch(1, 2)
=======
        self.model_settings = {}  # 모델 설정을 저장할 딕셔너리 추가
        self.selected_models = set()  # 선택된 모델들을 저장할 set 추가

        # 레이아웃 비율 설정
        self.main_layout.setStretch(0, 10)  # 왼쪽 패널 (스트리밍)
        self.main_layout.setStretch(1, 20)  # 오른쪽 패널 비율 증가 (10 -> 15)

    def _setup_left_panel(self):
        left_panel = QWidget()
        left_layout = QVBoxLayout()
        left_panel.setLayout(left_layout)

        # 카메라 레이블 초기화
        self.camera_label = QLabel(left_panel)
        self.camera_label.setMinimumSize(510, 340)  # 1.7배 크기 증가
        self.camera_label.setStyleSheet("""
            QLabel {
                background-color: transparent;
                min-height: 510px;
            }
        """)
        
        # 불통과 레이블
        fail_label = QLabel("불통과", left_panel)
        fail_label.setStyleSheet("color: red;")

        # 현재 상태 레이블
        status_label = QLabel("현재 상태", left_panel)

        # 구동중 상태 표시 위젯
        status_widget = QWidget(left_panel)
        status_widget.setStyleSheet("background-color: #cccccc;")
        status_layout = QHBoxLayout()
        status_layout.addWidget(QLabel("구동중", status_widget))
        status_widget.setLayout(status_layout)

        # 레이아웃에 위젯 추가
        left_layout.addWidget(self.camera_label)
        left_layout.addWidget(fail_label)
        left_layout.addWidget(status_label)
        left_layout.addWidget(status_widget)
        left_layout.addStretch()

        return left_panel
>>>>>>> 79017c7 (2025-01-18)

    def _setup_right_panel(self):
        # Placeholder for right content
        right_placeholder = QLabel("")
        right_placeholder.setAlignment(Qt.AlignCenter)
        right_placeholder.setFont(QFont("Arial", 16))
        right_placeholder.setStyleSheet("border: 1px solid black;")
        self.right_layout.addWidget(right_placeholder)

    def _setup_menu(self):
        self.menu_bar = QMenuBar(self)
        self.setMenuBar(self.menu_bar)

<<<<<<< HEAD
=======
        # ROI 메뉴
>>>>>>> 79017c7 (2025-01-18)
        roi_menu = self.menu_bar.addMenu("ROI")
        configure_action = QAction("Configure ROI", self)
        configure_action.triggered.connect(self.open_roi_config)
        roi_menu.addAction(configure_action)

<<<<<<< HEAD
=======
        # 설정 메뉴
        settings_menu = self.menu_bar.addMenu("설정")
        model_config_action = QAction("모델 설정", self)
        model_config_action.triggered.connect(self.open_model_config)
        settings_menu.addAction(model_config_action)

        # 등록 메뉴 추가
        register_menu = self.menu_bar.addMenu("등록")
        
        # 장비 등록 액션
        equipment_action = QAction("장비 등록", self)
        equipment_action.triggered.connect(self.open_equipment_register)
        register_menu.addAction(equipment_action)
        
        # 제품 등록 액션
        product_action = QAction("제품 등록", self)
        product_action.triggered.connect(self.open_product_register)
        register_menu.addAction(product_action)

>>>>>>> 79017c7 (2025-01-18)
    def _setup_camera(self):
        self.camera = cv2.VideoCapture(0)
        if not self.camera.isOpened():
            raise RuntimeError("Error: Cannot open camera.")

    def _setup_timer(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(1000 // CAMERA_FPS)

    def open_roi_config(self):
        ret, frame = self.camera.read()
        if not ret:
            return
        dialog = ROIConfigDialog(self, frame=frame, roi_rects=self.roi_rects)
        if dialog.exec_():
            self.roi_rects = dialog.get_roi_values()
            self.update_streaming_windows()

    def update_streaming_windows(self, new_rois=None):
        # 기존 스트리밍 창 닫기
        for window in self.stream_windows:
            window.close()
        self.stream_windows.clear()

        # ROI 업데이트
        if new_rois is not None:
            self.roi_rects = new_rois
        elif not hasattr(self, 'roi_rects') or not self.roi_rects:
            print("No ROI to update")
            return

        # 새로운 스트리밍 창 생성
        for i, rect in enumerate(self.roi_rects):
            print(f"Creating stream window for ROI {i}: {rect}")
            stream_window = ROIStreamWindow(i, rect, self.get_color(i), self)
            stream_window.show()
            self.stream_windows.append(stream_window)

    def get_color(self, index):
        # HSV 색상환을 사용하여 다양한 색상 생성
        hue = (index * 137) % 360
        color = QColor.fromHsv(hue, 255, 255)
        return color.name()

    def update_frame(self):
<<<<<<< HEAD
        if not self.streaming:
            return  # 스트리밍이 중지된 경우 업데이트하지 않음

        ret, frame = self.camera.read()
        if ret:
            # 각 스트리밍 창 업데이트
            for window in self.stream_windows:
                window.update_stream(frame)
=======
        if hasattr(self, 'camera_label') and self.camera_label is not None:
            ret, frame = self.camera.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                height, width, channel = frame.shape
                bytes_per_line = 3 * width
                q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(q_image)
                
                # 레이블 크기에 맞춰 비율 유지하며 스케일링
                if self.camera_label.width() > 0 and self.camera_label.height() > 0:
                    scaled_pixmap = pixmap.scaled(
                        self.camera_label.width(), 
                        self.camera_label.height(), 
                        Qt.KeepAspectRatio
                    )
                    # 중앙 정렬을 위한 여백 계산
                    x = (self.camera_label.width() - scaled_pixmap.width()) // 2
                    y = (self.camera_label.height() - scaled_pixmap.height()) // 2
                    self.camera_label.setPixmap(scaled_pixmap)
                    self.camera_label.setContentsMargins(x, y, x, y)
>>>>>>> 79017c7 (2025-01-18)

    def toggle_streaming(self):
        if self.streaming:
            self.streaming = False
            self.status_button.setText("대기중")
            self.status_button.setStyleSheet("background-color: lightblue; color: green;")
        else:
            self.streaming = True
            self.status_button.setText("구동중")
            self.status_button.setStyleSheet("background-color: lightgray; color: blue;")

    def closeEvent(self, event):
<<<<<<< HEAD
        # 모든 스트리밍 창 닫기
        for window in self.stream_windows:
            window.close()
        self.camera.release()
        event.accept()

=======
        if hasattr(self, 'camera'):
            self.camera.release()
        event.accept()

    def open_model_config(self):
        ret, frame = self.camera.read()
        if not ret:
            return
            
        dialog = ModelConfigDialog(self)
        dialog.set_frame(frame)
        if hasattr(self, 'roi_rects'):
            dialog.set_roi_data(self.roi_rects)
            
        # 이전 설정 확인
        print("이전 설정:", self.model_settings.get('RGB'))
            
        # 이전 설정이 있다면 복원
        if 'RGB' in self.model_settings:
            print("RGB 설정 복원 시도")
            dialog.rgb_page.restore_settings(self.model_settings['RGB'])
            
        if dialog.exec_():
            self.selected_models = dialog.selected_models
            # RGB 설정 저장 - 선택 여부와 관계없이 항상 저장
            self.model_settings['RGB'] = dialog.rgb_page.get_settings()
            print("새로운 RGB 설정 저장:", self.model_settings['RGB'])

    def open_equipment_register(self):
        dialog = EquipmentRegisterDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            # 장비 정보 업데이트
            self.current_equipment = {
                'id': dialog.equipment_id.text(),
                'name': dialog.equipment_name.text(),
                'manager': dialog.manager.text()
            }
            # 레이블 업데이트
            self.equipment_id_label.setText(self.current_equipment['id'])
            self.equipment_name_label.setText(self.current_equipment['name'])
            self.manager_label.setText(self.current_equipment['manager'])

    def open_product_register(self):
        dialog = ProductRegisterDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            # 제품 정보 업데이트
            self.current_product = {
                'id': dialog.product_id.text(),
                'name': dialog.product_name.text()
            }
            # 레이블 업데이트
            self.product_id_label.setText(self.current_product['id'])
            self.product_name_label.setText(self.current_product['name'])

    def _setup_info_toolbar(self):
        info_toolbar = QToolBar()
        self.addToolBar(info_toolbar)
        
        # 기본 라벨 스타일
        label_style = "QLabel { font-size: 12pt; font-weight: bold; }"
        # 값 라벨 스타일
        value_style = """
            QLabel { 
                font-size: 12pt; 
                color: #333;
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 3px;
                padding: 2px 8px;
                min-width: 120px;
            }
        """
        
        # 장비 정보
        equipment_label = QLabel("장비 ID:")
        equipment_label.setStyleSheet(label_style)
        info_toolbar.addWidget(equipment_label)
        
        self.equipment_id_label = QLabel("미등록")
        self.equipment_id_label.setStyleSheet(value_style)
        info_toolbar.addWidget(self.equipment_id_label)
        
        info_toolbar.addSeparator()
        
        name_label = QLabel("장비 이름:")
        name_label.setStyleSheet(label_style)
        info_toolbar.addWidget(name_label)
        
        self.equipment_name_label = QLabel("미등록")
        self.equipment_name_label.setStyleSheet(value_style)
        info_toolbar.addWidget(self.equipment_name_label)
        
        info_toolbar.addSeparator()
        
        manager_label = QLabel("관리자:")
        manager_label.setStyleSheet(label_style)
        info_toolbar.addWidget(manager_label)
        
        self.manager_label = QLabel("미등록")
        self.manager_label.setStyleSheet(value_style)
        info_toolbar.addWidget(self.manager_label)
        
        info_toolbar.addSeparator()
        
        # 제품 정보
        product_id_label = QLabel("제품 ID:")
        product_id_label.setStyleSheet(label_style)
        info_toolbar.addWidget(product_id_label)
        
        self.product_id_label = QLabel("미등록")
        self.product_id_label.setStyleSheet(value_style)
        info_toolbar.addWidget(self.product_id_label)
        
        info_toolbar.addSeparator()
        
        product_name_label = QLabel("제품 이름:")
        product_name_label.setStyleSheet(label_style)
        info_toolbar.addWidget(product_name_label)
        
        self.product_name_label = QLabel("미등록")
        self.product_name_label.setStyleSheet(value_style)
        info_toolbar.addWidget(self.product_name_label)

        # 툴바 자체 스타일
        info_toolbar.setStyleSheet("""
            QToolBar {
                spacing: 10px;
                padding: 5px;
                background-color: #f0f0f0;
            }
            QToolBar::separator {
                width: 2px;
                background-color: #ccc;
                margin: 0 10px;
            }
        """)

>>>>>>> 79017c7 (2025-01-18)
