import cv2
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QApplication, QSizePolicy, QAction, QMenuBar, QPushButton, QFrame)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont, QColor
from ui.roi_config_dialog import ROIConfigDialog
from ui.roi_stream_window import ROIStreamWindow
from config.settings import DEFAULT_ROI, CAMERA_FPS
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VISION CONTROL")
        self.setGeometry(100, 100, 800, 400)

        # Streaming state
        self.streaming = True

        # Central widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout()
        self.central_widget.setLayout(self.main_layout)

        # Left layout (1:3 ratio)
        self.left_layout = QVBoxLayout()
        self._setup_left_panel()
        self.main_layout.addLayout(self.left_layout, 1)

        # Right layout (2:3 ratio)
        self.right_layout = QVBoxLayout()
        self._setup_right_panel()
        self.main_layout.addLayout(self.right_layout, 4)

        # Camera and timer setup
        self._setup_camera()
        self._setup_timer()

        # Menu bar setup
        self._setup_menu()

        # ROI settings
        self.roi_rects = DEFAULT_ROI
        self.stream_windows = []

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

        roi_menu = self.menu_bar.addMenu("ROI")
        configure_action = QAction("Configure ROI", self)
        configure_action.triggered.connect(self.open_roi_config)
        roi_menu.addAction(configure_action)

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
        if not self.streaming:
            return  # 스트리밍이 중지된 경우 업데이트하지 않음

        ret, frame = self.camera.read()
        if ret:
            # 각 스트리밍 창 업데이트
            for window in self.stream_windows:
                window.update_stream(frame)

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
        # 모든 스트리밍 창 닫기
        for window in self.stream_windows:
            window.close()
        self.camera.release()
        event.accept()

