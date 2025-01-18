from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, 
                           QLineEdit, QPushButton, QLabel, QMessageBox,
                           QFormLayout)
from PyQt5.QtCore import Qt
from datetime import datetime

class EquipmentRegisterDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("장비 등록")
        self.setModal(True)
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout()
        form_layout = QFormLayout()

        # 장비 ID
        self.equipment_id = QLineEdit()
        form_layout.addRow("장비 ID:", self.equipment_id)

        # 장비 이름
        self.equipment_name = QLineEdit()
        form_layout.addRow("장비 이름:", self.equipment_name)

        # 관리자
        self.manager = QLineEdit()
        form_layout.addRow("관리자:", self.manager)

        layout.addLayout(form_layout)

        # 버튼
        button_layout = QHBoxLayout()
        save_button = QPushButton("저장")
        cancel_button = QPushButton("취소")
        save_button.clicked.connect(self.save_equipment)
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def save_equipment(self):
        # 여기에 데이터베이스 저장 로직 구현
        equipment_data = {
            'equipment_id': self.equipment_id.text(),
            'reg_date': datetime.now().date(),
            'equipment_name': self.equipment_name.text(),
            'manager': self.manager.text(),
            'last_update': datetime.now()
        }
        
        # TODO: 데이터베이스에 저장하는 코드 추가
        self.accept() 