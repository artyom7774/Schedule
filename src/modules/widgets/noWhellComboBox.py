from PyQt5.QtWidgets import QComboBox
from PyQt5.QtCore import Qt


class NoWhellComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setFocusPolicy(Qt.StrongFocus)

    def wheelEvent(self, event):
        event.ignore()
