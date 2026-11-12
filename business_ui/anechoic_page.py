from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QDoubleSpinBox,
                               QPushButton, QTableWidget, QTableWidgetItem, QTextEdit, QHeaderView)
from PySide6.QtCore import QTimer
import csv
import os
import random
from calib_core.chart_widget import CurveChartWidget
from calib_core.ocr_panel_widget import OcrPanelWidget

class AnechoicCalPage(QWidget):
    def __init__(self):
        super().__init__()
        self.task_running = False
        self.timer = QTimer()
        self.timer.timeout.connect(self.add_row)
        self.counter = 0
        self.start_val = 0.0
        self.end_val = 0.0
        self.step = 0.0

        main_layout = QVBoxLayout()

        dev_layout = QHBoxLayout()
        self.dev_label1 = QLabel("🔴 信号源")
        self.dev_label2 = QLabel("🔴 接收天线")
        self.dev_label3 = QLabel("🔴 频谱仪")
        self.btn_connect = QPushButton("全部设备自检连接")
        self.btn_connect.clicked.connect(self.on_connect)
        dev_layout.addWidget(self.dev_label1)
        dev_layout.addWidget(self.dev_label2)
        dev_layout.addWidget(self.dev_label3)
        dev_layout.addStretch()
        dev_layout.addWidget(self.btn_connect)
        main_layout.addLayout(dev_layout)

        param_layout = QHBoxLayout()
        param_layout.addWidget(QLabel("起始频率(Hz)"))
        self.sp_start = QDoubleSpinBox()
        self.sp_start.setRange(0, 1000000000)
        self.sp_start.setValue(1000000.0)
        param_layout.addWidget(self.sp_start)

        param_layout.addWidget(QLabel("结束频率(Hz)"))
        self.sp_end = QDoubleSpinBox()
        self.sp_end.setRange(0, 1000000000)
        self.sp_end.setValue(10000000.0)
        param_layout.addWidget(self.sp_end)

        param_layout.addWidget(QLabel("步长(Hz)"))
        self.sp_step = QDoubleSpinBox()
        self.sp_step.setRange(0.1, 1000000)
        self.sp_step.setValue(1000000.0)
        param_layout.addWidget(self.sp_step)

        param_layout.addWidget(QLabel("设定幅值"))
        self.sp_amp = QDoubleSpinBox()
        self.sp_amp.setRange(0,20)
        self.sp_amp.setValue(1.0)
        param_layout.addWidget(self.sp_amp)
        main_layout.addLayout(param_layout)

        chart_ocr_layout = QHBoxLayout()
        self.chart = CurveChartWidget()
        self.chart.set_axis_names("频率(Hz)", "接收幅值")
        self.ocr_panel = OcrPanelWidget()
        chart_ocr_layout.addWidget(self.chart, stretch=3)
        chart_ocr_layout.addWidget(self.ocr_panel, stretch=1)
        main_layout.addLayout(chart_ocr_layout)

        btn_layout = QHBoxLayout()
        self.btn_start = QPushButton("开始任务")
        self.btn_start.clicked.connect(self.start_task)
        self.btn_pause = QPushButton("暂停")
        self.btn_pause.clicked.connect(self.pause_task)
        self.btn_stop = QPushButton("中止任务")
        self.btn_stop.clicked.connect(self.stop_task)
        self.btn_export = QPushButton("导出CSV")
        self.btn_export.clicked.connect(self.export_csv)
        btn_layout.addWidget(self.btn_start)
        btn_layout.addWidget(self.btn_pause)
        btn_layout.addWidget(self.btn_stop)
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_export)
        main_layout.addLayout(btn_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(["point_id", "频率(Hz)", "设定幅值", "接收读数", "EUT-OCR读数", "标准值", "偏差", "状态"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        main_layout.addWidget(self.table)

        self.log_box = QTextEdit()
        self.log_box.setReadOnly(True)
        main_layout.addWidget(self.log_box)

        self.setLayout(main_layout)

    def on_connect(self):
        self.dev_label1.setText("🟢 信号源")
        self.dev_label2.setText("🟢 接收天线")
        self.dev_label3.setText("🟢 频谱仪")
        self.log("✅ 暗室射频设备自检完成")

    def start_task(self):
        if self.task_running:
            return
        self.start_val = self.sp_start.value()
        self.end_val = self.sp_end.value()
        self.step = self.sp_step.value()
        self.counter = 0
        self.task_running = True
        self.chart.clear()
        self.timer.start(300)
        self.log("▶ 暗室射频校准任务开始")

    def pause_task(self):
        self.timer.stop()
        self.log("⏸ 任务暂停")

    def stop_task(self):
        self.timer.stop()
        self.task_running = False
        self.log("⏹ 任务中止")

    def add_row(self):
        freq = self.start_val + self.counter * self.step
        if freq > self.end_val:
            self.timer.stop()
            self.task_running = False
            self.log("✅ 全部扫描完成")
            return
        set_amp = self.sp_amp.value()
        ocr_read = set_amp + random.uniform(-0.08, 0.08)
        conf = random.uniform(0.88, 0.99)
        recv_val = set_amp * random.uniform(0.97, 1.03)
        std_val = set_amp * 1.2
        dev = ocr_read - std_val

        self.ocr_panel.update_data(f"{ocr_read:.3f}", conf)
        self.chart.add_point(f"{freq:.0f}", set_amp, ocr_read)

        row = self.table.rowCount()
        self.table.insertRow(row)
        self.table.setItem(row, 0, QTableWidgetItem(str(row+1)))
        self.table.setItem(row, 1, QTableWidgetItem(f"{freq:.2f}"))
        self.table.setItem(row, 2, QTableWidgetItem(f"{set_amp:.2f}"))
        self.table.setItem(row, 3, QTableWidgetItem(f"{recv_val:.3f}"))
        self.table.setItem(row, 4, QTableWidgetItem(f"{ocr_read:.3f}"))
        self.table.setItem(row, 5, QTableWidgetItem(f"{std_val:.2f}"))
        self.table.setItem(row, 6, QTableWidgetItem(f"{dev:.3f}"))
        self.table.setItem(row, 7, QTableWidgetItem("正常"))
        self.counter += 1

    def export_csv(self):
        path = "anechoic_result.csv"
        with open(path, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            headers = ["point_id", "频率(Hz)", "设定幅值", "接收读数", "EUT-OCR读数", "标准值", "偏差", "状态"]
            writer.writerow(headers)
            for r in range(self.table.rowCount()):
                line = []
                for c in range(8):
                    item = self.table.item(r,c)
                    line.append(item.text() if item else "")
                writer.writerow(line)
        self.log(f"📤 导出成功：{os.path.abspath(path)}")

    def log(self, msg):
        self.log_box.append(msg)