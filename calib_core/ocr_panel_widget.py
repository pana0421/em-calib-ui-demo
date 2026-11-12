from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFrame
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QColor, QFont

class OcrPanelWidget(QWidget):
    """模拟仪器摄像头画面 + OCR识别读数、置信度、人工复核按钮"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(180)
        self.read_val = "0.00"
        self.confidence = 0.0

        layout = QVBoxLayout()
        layout.setSpacing(6)

        self.frame = QFrame()
        self.frame.setStyleSheet("border:1px solid #888; background-color:#222;")
        self.frame.setMinimumHeight(110)
        frame_layout = QVBoxLayout(self.frame)
        self.cam_label = QLabel("模拟仪器取景画面")
        self.cam_label.setAlignment(Qt.AlignCenter)
        self.cam_label.setStyleSheet("color:#aaa;")
        frame_layout.addWidget(self.cam_label)
        layout.addWidget(self.frame)

        info_layout = QVBoxLayout()
        self.label_ocr = QLabel(f"OCR读数：{self.read_val}")
        self.label_conf = QLabel(f"置信度：{self.confidence:.2f}")
        info_layout.addWidget(self.label_ocr)
        info_layout.addWidget(self.label_conf)
        layout.addLayout(info_layout)

        self.btn_review = QPushButton("人工复核确认")
        self.btn_review.clicked.connect(self.on_review)
        layout.addWidget(self.btn_review)
        self.setLayout(layout)

    def update_data(self, val:str, conf:float):
        self.read_val = val
        self.confidence = conf
        self.label_ocr.setText(f"OCR读数：{self.read_val}")
        self.label_conf.setText(f"置信度：{self.confidence:.2f}")

    def on_review(self):
        self.label_ocr.setText(self.label_ocr.text() + " ✅已复核")