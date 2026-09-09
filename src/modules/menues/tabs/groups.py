from PyQt5.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QComboBox, QPushButton, QInputDialog, QMenu, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

from src.variables import *

import json


class TabGroups(QWidget):
    def __init__(self, window):
        super().__init__()

        self.window = window

        self.classes = []

        for i, cnt in enumerate(self.window.settings["classes"]["count"]):
            for number in range(cnt):
                self.classes.append(f"{i + 1} {CLASSES_ALPHABET[number + 1]}")

        self.subjects = [element[0] for element in self.window.settings["subjects"] if element[0]]

        self.window.settings.setdefault("groups", {})

        self.classSelector = QComboBox(self)
        self.classSelector.setFont(FONT)
        self.classSelector.addItems(self.classes)
        self.classSelector.currentTextChanged.connect(self.load)

        self.addGroupButton = QPushButton("Добавить группу", self)
        self.addGroupButton.clicked.connect(self.addGroup)
        self.addGroupButton.setFont(FONT)

        self.groupsTable = QTableWidget(len(self.subjects), 0, self)
        self.groupsTable.cellClicked.connect(self.groupsTableCellClicked)

        self.groupsTable.setStyleSheet("""QHeaderView::section { padding-right: -12px; }""")

        self.groupsTable.setVerticalHeaderLabels(self.subjects)
        self.groupsTable.verticalHeader().setFixedWidth(140)

        for row, subject in enumerate(self.subjects):
            header = self.groupsTable.verticalHeaderItem(row)

            if header is not None:
                header.setToolTip(subject)

        horizontalHeader = self.groupsTable.horizontalHeader()
        horizontalHeader.setContextMenuPolicy(Qt.CustomContextMenu)
        horizontalHeader.customContextMenuRequested.connect(self.context)

        self.load()

    def currentGroupsData(self):
        if not self.classSelector.currentText():
            return {}

        return self.window.settings["groups"].setdefault(self.classSelector.currentText(), {})

    def currentGroupNames(self):
        return sorted(self.currentGroupsData().keys())

    def save(self):
        with open(f"{PATH_TO_FOLDER}/projects/{self.window.project}/settings.json", "w", encoding="utf-8") as file:
            json.dump(self.window.settings, file, ensure_ascii=False, indent=4)

    def load(self):
        if not self.classSelector.currentText():
            self.groupsTable.setColumnCount(0)

            return

        names = self.currentGroupNames()
        data = self.currentGroupsData()

        self.groupsTable.setRowCount(len(self.subjects))
        self.groupsTable.setColumnCount(len(names))

        self.groupsTable.setVerticalHeaderLabels(self.subjects)
        self.groupsTable.setHorizontalHeaderLabels(names)

        for col, group in enumerate(names):
            header = self.groupsTable.horizontalHeaderItem(col)

            if header is not None:
                header.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                header.setToolTip(group)

        for row, subject in enumerate(self.subjects):
            for col, group in enumerate(names):
                item = QTableWidgetItem()
                item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)

                subjectsForGroup = data.get(group, [])

                if subject in subjectsForGroup:
                    item.setBackground(QColor("#109012"))

                else:
                    item.setBackground(QColor("#901010"))

                self.groupsTable.setItem(row, col, item)

        self.groupsTable.resizeColumnsToContents()

        if "groups_scroll" in self.window.objects:
            self.groupsTable.verticalScrollBar().setValue(self.window.objects["groups_scroll"])

    def groupsTableCellClicked(self, row, col):
        cls = self.classSelector.currentText()

        if not cls:
            return

        if row < 0 or row >= len(self.subjects):
            return

        names = self.currentGroupNames()

        if col < 0 or col >= len(names):
            return

        subject = self.subjects[row]
        group = names[col]

        data = self.currentGroupsData()

        subjectsForGroup = data.setdefault(group, [])

        if subject in subjectsForGroup:
            subjectsForGroup.remove(subject)

        else:
            subjectsForGroup.append(subject)

        self.window.objects["groups_scroll"] = self.groupsTable.verticalScrollBar().value()

        self.save()
        self.load()

    def addGroup(self):
        if not self.classSelector.currentText():
            return

        group, ok = QInputDialog.getText(self, "Новая группа", "Введите название группы:")

        if not ok:
            return

        group = group.strip()

        if not group:
            return

        data = self.currentGroupsData()

        if group in data:
            QMessageBox.warning(self, "Ошибка", f"Группа «{group}» уже существует.")

            return

        data[group] = []

        self.save()
        self.load()

    def context(self, pos):
        header = self.groupsTable.horizontalHeader()
        col = header.logicalIndexAt(pos)

        if col < 0:
            return

        names = self.currentGroupNames()

        if col >= len(names):
            return

        old = names[col]

        menu = QMenu(self)

        renameAction = menu.addAction("Переименовать")
        deleteAction = menu.addAction("Удалить")

        selectedAction = menu.exec_(header.mapToGlobal(pos))

        if selectedAction == renameAction:
            self.renameGroup(old)

        elif selectedAction == deleteAction:
            self.deleteGroup(old)

    def renameGroup(self, old):
        new, ok = QInputDialog.getText(self, "Переименовать группу", "Введите новое название:", text=old)

        if not ok:
            return

        new = new.strip()

        if not new or new == old:
            return

        data = self.currentGroupsData()

        if new in data:
            QMessageBox.warning(self, "Ошибка", f"Группа «{new}» уже существует.")

            return

        data[new] = data.pop(old)

        self.save()
        self.load()

    def deleteGroup(self, group):
        answer = QMessageBox.question(self, "Удаление группы", f"Удалить группу «{group}»?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if answer != QMessageBox.Yes:
            return

        data = self.currentGroupsData()

        data.pop(group, None)

        self.save()
        self.load()
