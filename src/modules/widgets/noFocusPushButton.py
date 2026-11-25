from PySide6.QtWidgets import QPushButton, QStyleOptionButton, QStylePainter, QStyle

from PySide6.QtCore import QProcess, QTimer, Qt
from PySide6.QtGui import QTextCursor


class NoFocusPushButton(QPushButton):
    def paintEvent(self, event):
        option = QStyleOptionButton()
        self.initStyleOption(option)
        option.state &= ~QStyle.State_HasFocus
        painter = QStylePainter(self)
        painter.drawControl(QStyle.CE_PushButton, option)
