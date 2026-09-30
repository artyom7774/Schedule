from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QColor, QBrush, QPen


class CircleButton(QPushButton):
    def __init__(self, color=QColor(255, 0, 0), sz=60, parent=None):
        super().__init__(parent)
        self.color = color
        self.sz = sz

        self.setFixedSize(sz, sz)

        self.setCursor(Qt.PointingHandCursor)

        self.setStyleSheet("background-color: transparent; border: none;")

    def set_color(self, color):
        self.color = color

        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.setBrush(QBrush(self.color))
        painter.setPen(QPen(self.color, 1))
        painter.drawEllipse(2, 2, self.sz - 4, self.sz - 4)
