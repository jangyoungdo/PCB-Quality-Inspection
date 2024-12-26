from PyQt5.QtWidgets import QMessageBox

def validate_roi_dimensions(roi_id, x, y, w, h, frame_width, frame_height, parent=None):
    """ROI 치수의 유효성을 검사합니다."""
    if w <= 0 or h <= 0:
        QMessageBox.warning(parent, "Invalid Dimensions", 
            f"ROI {roi_id}: Width and height must be greater than 0")
        return False
        
    if x < 0 or y < 0:
        QMessageBox.warning(parent, "Invalid Position", 
            f"ROI {roi_id}: Position cannot be negative")
        return False
        
    if x + w > frame_width or y + h > frame_height:
        QMessageBox.warning(parent, "ROI Out of Bounds", 
            f"ROI {roi_id}: Region extends beyond image boundaries")
        return False
        
    return True