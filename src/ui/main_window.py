import cv2
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QAction, QMenuBar
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QScreen
from ui.roi_config_dialog import ROIConfigDialog
from ui.roi_stream_window import ROIStreamWindow
from config.settings import DEFAULT_ROI, CAMERA_FPS

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ROI Viewer UI")
        
        # 전체 화면으로 설정
        self.showMaximized()
        
        # 빈 중앙 위젯 설정
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # 메뉴바 설정
        self.menu_bar = QMenuBar(self)
        self.setMenuBar(self.menu_bar)
        
        # ROI 설정 초기화
        self.roi_rects = DEFAULT_ROI
        self.stream_windows = []
        
        self._setup_camera()
        self._setup_timer()
        self._setup_menu()

    def _setup_menu(self):
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
            self.update_streaming_windows()  # new_rois 매개변수 없이 호출

    def update_streaming_windows(self, new_rois=None):
        # 기존 스트리밍 창 닫기
        for window in self.stream_windows:
            window.close()
        self.stream_windows.clear()
        
        # ROI 업데이트
        if new_rois is not None:
            self.roi_rects = new_rois
        
        # 새로운 스트리밍 창 생성
        for i, rect in enumerate(self.roi_rects):
            stream_window = ROIStreamWindow(i, rect, self.get_color(i), self)
            stream_window.show()
            self.stream_windows.append(stream_window)

    def get_color(self, index):
        # HSV 색상환을 사용하여 다양한 색상 생성
        hue = (index * 137) % 360
        from PyQt5.QtGui import QColor
        color = QColor.fromHsv(hue, 255, 255)
        return color.name()

    def update_frame(self):
        ret, frame = self.camera.read()
        if ret:
            # 각 스트리밍 창 업데이트
            for window in self.stream_windows:
                window.update_stream(frame)

    def closeEvent(self, event):
        # 모든 스트리밍 창 닫기
        for window in self.stream_windows:
            window.close()
        self.camera.release()
        event.accept()