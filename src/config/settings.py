# Default window settings
MAIN_WINDOW_WIDTH = 1920
MAIN_WINDOW_HEIGHT = 1080
ROI_WIDGET_SIZE = 1200

# Camera settings
CAMERA_FPS = 30

# ROI default settings
DEFAULT_ROI = [(50, 50, 100, 100)]
MAX_WIDTH = 1920
MAX_HEIGHT = 1080

# Stream window settings
STREAM_WINDOW_MIN_SIZE = 200
STREAM_WINDOW_DEFAULT_SIZE = 400
STREAM_WINDOW_OFFSET = 50

# Color settings
<<<<<<< HEAD
COLOR_ANGLE = 137  # Golden angle for color distribution
=======
COLOR_ANGLE = 60  # ROI 색상 간격 (색상환에서의 각도)

# 사용 가능한 모델 목록
AVAILABLE_MODELS = {
    'RGB': 'RGB 검사',
    'SIMILARITY': '유사도 검사',
    'DEEP_LEARNING': '딥러닝 검사'
}

# 모델별 기본 설정값
MODEL_DEFAULT_SETTINGS = {
    'RGB': {
        'tolerance': 30  # RGB 허용 오차 기본값
    },
    'SIMILARITY': {
        # 유사도 검사 관련 기본 설정들
    },
    'DEEP_LEARNING': {
        # 딥러닝 검사 관련 기본 설정들
    }
}
>>>>>>> 79017c7 (2025-01-18)
