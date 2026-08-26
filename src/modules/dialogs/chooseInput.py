from PyQt5.QtWidgets import QLabel, QPushButton, QDialog, QLineEdit, QComboBox
from PyQt5.QtCore import Qt

from src.variables import *


class ChooseInputDialog(QDialog):
    def __init__(self, parent, chooses, title, label, accept, function):
        super().__init__(parent)

        self.setWindowTitle(title)
        self.setFixedSize(600, 400)

        self.empty = QPushButton(parent=self)
        self.empty.setGeometry(0, 0, 0, 0)

        self.label = QLabel(label, parent=self)
        self.label.setGeometry(10, 10, 200, 28)
        self.label.setFont(FONT)
        self.label.show()

        self.edit = QComboBox(parent=self)
        self.edit.addItems(chooses)
        self.edit.setGeometry(250, 10, 300, 28)
        self.edit.setFont(FONT)
        self.edit.show()

        self.log = QLabel("", parent=self)
        self.log.setStyleSheet("color: red;")
        self.log.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.log.setGeometry(0, 320, 600, 30)
        self.log.setFont(LITTLE_FONT)
        self.log.show()

        self.accept = QPushButton(accept, parent=self)
        self.accept.setGeometry(100, 350, 400, 40)
        self.accept.setFont(FONT)
        self.accept.show()

        self.accept.clicked.connect(function)
        self.accept.released.connect(lambda: self.empty.setFocus())
