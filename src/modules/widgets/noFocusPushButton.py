from PyQt5.QtWidgets import QPushButton, QStyleOptionButton, QStylePainter, QStyle

from PyQt5.QtCore import QProcess, QTimer, Qt
from PyQt5.QtGui import QTextCursor


class NoFocusPushButton(QPushButton):
    def paintEvent(self, event):
        option = QStyleOptionButton()
        self.initStyleOption(option)
        option.state &= ~QStyle.State_HasFocus
        painter = QStylePainter(self)
        painter.drawControl(QStyle.CE_PushButton, option)
