import cv2
from PyQt5.QtGui import QImage, QPixmap, QPainter
from PyQt5.QtCore import Qt

def extract_roi(frame, roi_rect):
    """프레임에서 ROI 영역을 추출합니다."""
    x, y, w, h = roi_rect
    return frame[y:y+h, x:x+w]

def resize_with_aspect_ratio(image, target_width, target_height):
    """종횡비를 유지하면서 이미지 크기를 조정합니다."""
    h, w = image.shape[:2]
    aspect_ratio = w / h
    
    if aspect_ratio > 1:
        new_width = target_width
        new_height = int(target_width / aspect_ratio)
    else:
        new_height = target_height
        new_width = int(target_height * aspect_ratio)
        
    return cv2.resize(image, (new_width, new_height))

def frame_to_pixmap(frame, width, height):
    """OpenCV 프레임을 Qt Pixmap으로 변환합니다."""
    # BGR에서 RGB로 변환
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # 이 부분이 중요
    h, w, ch = rgb_frame.shape
    bytes_per_line = ch * w
    
    q_img = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
    return QPixmap.fromImage(q_img).scaled(width, height, Qt.KeepAspectRatio)

def create_roi_pixmap(roi_frame, display_w, display_h):
    """ROI 프레임을 표시용 Pixmap으로 변환합니다."""
    roi_frame = resize_with_aspect_ratio(roi_frame, display_w, display_h)
    roi_frame = cv2.cvtColor(roi_frame, cv2.COLOR_BGR2RGB)
    
    h, w, ch = roi_frame.shape
    bytes_per_line = ch * w
    q_img = QImage(roi_frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
    pixmap = QPixmap(q_img)
    
    final_pixmap = QPixmap(display_w, display_h)
    final_pixmap.fill(Qt.black)
    
    painter = QPainter(final_pixmap)
    x_offset = (display_w - w) // 2
    y_offset = (display_h - h) // 2
    painter.drawPixmap(x_offset, y_offset, pixmap)
    painter.end()
    
    return final_pixmap