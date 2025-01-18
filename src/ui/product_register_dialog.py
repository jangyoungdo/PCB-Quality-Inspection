from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, 
                           QLineEdit, QPushButton, QLabel, QMessageBox,
                           QSpinBox, QFormLayout)
from PyQt5.QtCore import Qt
from datetime import datetime

class ProductRegisterDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("제품 등록")
        self.setModal(True)
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout()
        form_layout = QFormLayout()

        # 생산 일자 (자동 설정)
        self.production_date = QLabel(datetime.now().strftime("%Y-%m-%d"))
        form_layout.addRow("생산 일자:", self.production_date)

        # 생산품 ID
        self.product_id = QLineEdit()
        form_layout.addRow("생산품 ID:", self.product_id)

        # 장비 ID (콤보박스로 변경 가능)
        self.equipment_id = QLineEdit()
        form_layout.addRow("장비 ID:", self.equipment_id)

        # 생산품명
        self.product_name = QLineEdit()
        form_layout.addRow("생산품명:", self.product_name)

        # 생산개수
        self.production_count = QSpinBox()
        self.production_count.setRange(1, 9999)
        form_layout.addRow("생산개수:", self.production_count)

        # 불량개수
        self.defect_count = QSpinBox()
        self.defect_count.setRange(0, 9999)
        form_layout.addRow("불량개수:", self.defect_count)

        layout.addLayout(form_layout)

        # 버튼
        button_layout = QHBoxLayout()
        save_button = QPushButton("저장")
        cancel_button = QPushButton("취소")
        save_button.clicked.connect(self.save_product)
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def save_product(self):
        # 여기에 데이터베이스 저장 로직 구현
        product_data = {
            'production_date': datetime.now().date(),
            'product_id': self.product_id.text(),
            'equipment_id': self.equipment_id.text(),
            'product_name': self.product_name.text(),
            'production_count': self.production_count.value(),
            'defect_count': self.defect_count.value()
        }
        
        # TODO: 데이터베이스에 저장하는 코드 추가
        self.accept() 