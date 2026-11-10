# main.py 电磁场校准演示界面
import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                               QComboBox, QLabel, QGroupBox, QLineEdit, QPushButton, QTextEdit)

class EmCalibWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("电磁场校准系统 演示界面")
        self.resize(900, 650)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # 顶部：选择校准类型 + 设备状态
        top_layout = QHBoxLayout()
        self.combo_type = QComboBox()
        self.combo_type.addItems([
            "TEM室校准(10kHz‑300MHz)",
            "GTEM室校准(10MHz‑1GHz)",
            "暗室射频校准",
            "工频磁场校准"
        ])
        self.label_status = QLabel("设备状态：未连接")
        top_layout.addWidget(self.combo_type)
        top_layout.addWidget(self.label_status)
        main_layout.addLayout(top_layout)

        # 参数区域
        param_group = QGroupBox("校准参数设置")
        param_layout = QVBoxLayout(param_group)
        self.edit_freq = QLineEdit("100000000")
        self.edit_amp = QLineEdit("0.5")
        self.edit_time = QLineEdit("2")
        param_layout.addWidget(QLabel("频率(Hz)"))
        param_layout.addWidget(self.edit_freq)
        param_layout.addWidget(QLabel("幅值"))
        param_layout.addWidget(self.edit_amp)
        param_layout.addWidget(QLabel("稳定时间(s)"))
        param_layout.addWidget(self.edit_time)
        main_layout.addWidget(param_group)

        # 按钮区
        btn_layout = QHBoxLayout()
        self.btn_connect = QPushButton("设备自检连接")
        self.btn_start = QPushButton("开始校准")
        self.btn_pause = QPushButton("暂停")
        self.btn_stop = QPushButton("中止")
        self.btn_export = QPushButton("导出CSV报告")
        btn_layout.addWidget(self.btn_connect)
        btn_layout.addWidget(self.btn_start)
        btn_layout.addWidget(self.btn_pause)
        btn_layout.addWidget(self.btn_stop)
        btn_layout.addWidget(self.btn_export)
        main_layout.addLayout(btn_layout)

        # 日志框
        main_layout.addWidget(QLabel("运行日志"))
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        main_layout.addWidget(self.log_text)

        # 绑定按钮
        self.btn_connect.clicked.connect(self.on_connect)

    def on_connect(self):
        self.label_status.setText("设备状态：自检完成")
        self.log_text.append("【信息】开始自检\n【信息】通信正常，可以启动校准")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = EmCalibWindow()
    win.show()
    sys.exit(app.exec())