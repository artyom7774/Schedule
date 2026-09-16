from PyQt5.QtWidgets import QLabel, QPushButton, QDialog, QLineEdit, QListWidget, QListWidgetItem, QMenu, QAction
from PyQt5.QtCore import Qt

from src.variables import *


class ClassroomsPriorityDialog(QDialog):
    def __init__(self, parent, title, groups, selected, function):
        super().__init__(parent)

        self.setWindowTitle(title)
        self.setFixedSize(400, 500)

        self.function = function
        self.groups = groups
        self.selected = list(selected)

        self.list = QListWidget(parent=self)
        self.list.setGeometry(2, 2, 400 - 4, 500 - 4)
        self.list.setFont(FONT)
        self.list.itemClicked.connect(lambda item: self.itemClicked(item))
        self.list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.list.customContextMenuRequested.connect(lambda pos: self.showContextMenu(pos))
        self.list.show()

        self.refresh()

    def refresh(self, current=None):
        self.list.clear()

        ordered = self.selected + [group for group in self.groups if group not in self.selected]

        for group in ordered:
            if group in self.selected:
                priority = self.selected.index(group) + 1
                text = f"{priority}. {group}"

            else:
                text = f"-  {group}"

            item = QListWidgetItem(text)
            item.setData(Qt.UserRole, group)

            self.list.addItem(item)

            if group == current:
                self.list.setCurrentItem(item)

    def itemClicked(self, item):
        group = item.data(Qt.UserRole)

        if group in self.selected:
            self.selected.remove(group)

        else:
            self.selected.append(group)

        self.refresh(current=group)

    def showContextMenu(self, pos):
        item = self.list.itemAt(pos)

        if item is None:
            return

        group = item.data(Qt.UserRole)

        if group not in self.selected:
            return

        menu = QMenu(self)

        up = QAction(translate("dialog.classrooms_priority.up"), self)
        up.triggered.connect(lambda: self.moveUp(group))

        down = QAction(translate("dialog.classrooms_priority.down"), self)
        down.triggered.connect(lambda: self.moveDown(group))

        menu.addAction(up)
        menu.addAction(down)

        menu.exec_(self.list.mapToGlobal(pos))

    def moveUp(self, group):
        idx = self.selected.index(group)

        if idx == 0:
            return

        self.selected[idx - 1], self.selected[idx] = self.selected[idx], self.selected[idx - 1]

        self.refresh(current=group)

    def moveDown(self, group):
        idx = self.selected.index(group)

        if idx >= len(self.selected) - 1:
            return

        self.selected[idx + 1], self.selected[idx] = self.selected[idx], self.selected[idx + 1]

        self.refresh(current=group)

    def closeEvent(self, event):
        self.function(self.selected)

        super().closeEvent(event)
