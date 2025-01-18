class RGBInspector:
    def __init__(self):
        self.settings = {}
        
    def set_settings(self, roi_settings):
        """ROI별 RGB 설정 업데이트"""
        self.settings = roi_settings
        
    def inspect(self, frame, roi_rect, roi_index):
        """RGB 검사 수행
        
        Args:
            frame: 검사할 프레임 (numpy array)
            roi_rect: (x, y, w, h) 형태의 ROI 좌표
            roi_index: ROI 인덱스 (설정값 참조용)
            
        Returns:
            (bool, str): (검사 통과 여부, 메시지)
        """
        if roi_index not in self.settings:
            return False, "설정되지 않은 ROI"
            
        x, y, w, h = roi_rect
        roi = frame[y:y+h, x:x+w]
        
        # 여기에 외부 개발자의 RGB 검사 코드를 넣을 수 있습니다
        # 예시:
        # result = external_rgb_check(roi, 
        #     self.settings[roi_index]['rgb_controls']['R'],
        #     self.settings[roi_index]['rgb_controls']['G'],
        #     self.settings[roi_index]['rgb_controls']['B'])
        
        return True, "검사 통과"  # 임시 반환값 