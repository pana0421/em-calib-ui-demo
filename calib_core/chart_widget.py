from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QColor, QPen


class CurveChartWidget(QWidget):
    """实时双曲线图：设定值(蓝) / 实测值(红)，纯 QPainter 自绘，不依赖 matplotlib。"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(220)
        self.x_labels = []      # 横轴标签（频率/电流等）
        self.set_values = []    # 设定值序列
        self.meas_values = []   # 实测值序列
        self.x_axis_name = "频率"
        self.y_axis_name = "数值"

    def set_axis_names(self, x_name: str, y_name: str):
        self.x_axis_name = x_name
        self.y_axis_name = y_name

    def add_point(self, x_label: str, set_val: float, meas_val: float):
        self.x_labels.append(x_label)
        self.set_values.append(set_val)
        self.meas_values.append(meas_val)
        self.update()

    def clear(self):
        self.x_labels.clear()
        self.set_values.clear()
        self.meas_values.clear()
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        w, h = self.width(), self.height()
        margin_l, margin_r, margin_t, margin_b = 50, 20, 20, 30
        plot_w = w - margin_l - margin_r
        plot_h = h - margin_t - margin_b

        # 背景
        painter.fillRect(self.rect(), QColor(255, 255, 255))

        # 计算纵轴范围
        all_vals = self.set_values + self.meas_values
        if len(all_vals) == 0:
            painter.setPen(QColor(120, 120, 120))
            painter.drawText(self.rect(), Qt.AlignCenter, "暂无曲线数据")
            painter.end()
            return

        vmin, vmax = min(all_vals), max(all_vals)
        if abs(vmax - vmin) < 1e-9:
            vmin -= 1
            vmax += 1
        pad = (vmax - vmin) * 0.1
        vmin -= pad
        vmax += pad

        n = len(self.set_values)

        def to_x(i):
            if n == 1:
                return margin_l + plot_w / 2
            return margin_l + plot_w * i / (n - 1)

        def to_y(v):
            return margin_t + plot_h * (1 - (v - vmin) / (vmax - vmin))

        # 网格 + 坐标轴
        painter.setPen(QPen(QColor(220, 220, 220), 1))
        for k in range(5):
            y = margin_t + plot_h * k / 4
            painter.drawLine(margin_l, int(y), w - margin_r, int(y))
        painter.setPen(QPen(QColor(120, 120, 120), 1))
        painter.drawLine(margin_l, margin_t, margin_l, margin_t + plot_h)
        painter.drawLine(margin_l, margin_t + plot_h, w - margin_r, margin_t + plot_h)

        # 纵轴刻度文字
        painter.setPen(QColor(80, 80, 80))
        for k in range(5):
            v = vmax - (vmax - vmin) * k / 4
            y = margin_t + plot_h * k / 4
            painter.drawText(0, int(y) - 8, margin_l - 5, 16,
                             Qt.AlignRight, f"{v:.2f}")

        # 横轴标签（最多显示6个）
        tick = max(1, n // 6)
        for i, label in enumerate(self.x_labels):
            if i % tick != 0 and i != n - 1:
                continue
            painter.drawText(int(to_x(i)) - 30, margin_t + plot_h + 8,
                             60, 16, Qt.AlignCenter, str(label))

        # 画设定值曲线（蓝）
        if n >= 2:
            painter.setPen(QPen(QColor(30, 100, 220), 2))
            for i in range(1, n):
                painter.drawLine(int(to_x(i - 1)), int(to_y(self.set_values[i - 1])),
                                 int(to_x(i)), int(to_y(self.set_values[i])))
            # 实测值曲线（红）
            painter.setPen(QPen(QColor(220, 60, 60), 2))
            for i in range(1, n):
                painter.drawLine(int(to_x(i - 1)), int(to_y(self.meas_values[i - 1])),
                                 int(to_x(i)), int(to_y(self.meas_values[i])))
        elif n == 1:
            painter.setPen(QPen(QColor(30, 100, 220), 2))
            painter.drawPoint(int(to_x(0)), int(to_y(self.set_values[0])))
            painter.setPen(QPen(QColor(220, 60, 60), 2))
            painter.drawPoint(int(to_x(0)), int(to_y(self.meas_values[0])))

        # 图例
        painter.setPen(QColor(30, 100, 220))
        painter.drawText(margin_l, 4, 120, 16, Qt.AlignLeft, "— 设定值")
        painter.setPen(QColor(220, 60, 60))
        painter.drawText(margin_l + 90, 4, 120, 16, Qt.AlignLeft, "— 实测值")

        # 坐标轴名称
        painter.setPen(QColor(80, 80, 80))
        painter.drawText(0, 0, margin_l - 5, h, Qt.AlignRight | Qt.AlignVCenter, self.y_axis_name)
        painter.drawText(margin_l, h - 18, plot_w, 16, Qt.AlignCenter, self.x_axis_name)

        painter.end()