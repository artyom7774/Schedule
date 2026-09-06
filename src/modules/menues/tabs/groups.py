from PyQt5.QtWidgets import QWidget, QTableWidget, QHeaderView, QCheckBox, QTableWidgetItem, QComboBox, QVBoxLayout
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

        self.subjects = [element[0] for element in self.window.settings["subjects"]]

        self.classSelector = QComboBox(self)
        self.classSelector.setFont(FONT)
        self.classSelector.addItems(self.classes)
        self.classSelector.currentTextChanged.connect(self.load)
        self.classSelector.show()

        self.groupsTable = QTableWidget(self.window.settings["subjects_count"], self.window.settings["subjects_count"], parent=self)
        self.groupsTable.cellClicked.connect(lambda row, col: self.groupsTableCellClicked(row, col))
        self.groupsTable.setStyleSheet("""QHeaderView::section { padding-right: 8px; }""")
        self.groupsTable.show()

        self.groupsTable.setHorizontalHeaderLabels(self.subjects)
        
        for col in range(self.groupsTable.columnCount()):
            self.groupsTable.setColumnWidth(col, 80)

        self.groupsTable.verticalHeader().setFixedWidth(80)

        for col, text in enumerate(self.subjects):
            header = self.groupsTable.horizontalHeaderItem(col)
            
            if header is not None:
                header.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                header.setToolTip(text)

        self.groupsTable.setVerticalHeaderLabels(self.subjects)

        for row, text in enumerate(self.subjects):
            header = self.groupsTable.verticalHeaderItem(row)
            
            if header is not None:
                header.setToolTip(text)

        self.groupsTable.setVerticalHeaderLabels(self.subjects)
        self.groupsTable.setHorizontalHeaderLabels(self.subjects)

        self.load()

    def load(self):
        select = self.classSelector.currentText()

        if not select:
            return

        groups = self.window.settings["groups"]

        for row, subject1 in enumerate(self.subjects):
            for col, subject2 in enumerate(self.subjects):
                item = QTableWidgetItem()

                key = f"{subject1}-{subject2}"

                if row == col:
                    item.setBackground(QColor("#3f4042"))

                elif key in groups and select in groups[key]:
                    item.setBackground(QColor("#109012"))

                else:
                    item.setBackground(QColor("#202124"))

                self.groupsTable.setItem(row, col, item)

        if "groups_scroll" in self.window.objects:
            self.groupsTable.verticalScrollBar().setValue(self.window.objects["groups_scroll"])

    def groupsTableCellClicked(self, row, col):
        if row == col:
            return

        subject1 = self.subjects[row]
        subject2 = self.subjects[col]

        if subject1 == "" or subject2 == "":
            return

        select = self.classSelector.currentText()

        if not select:
            return

        groups = self.window.settings["groups"]

        key1 = f"{subject1}-{subject2}"
        key2 = f"{subject2}-{subject1}"

        if key1 in groups and select in groups[key1]:
            if key1 in groups and select in groups[key1]:
                groups[key1].remove(select)

            if key2 in groups and select in groups[key2]:
                groups[key2].remove(select)

            if key1 in groups and not groups[key1]:
                groups.pop(key1, None)

            if key2 in groups and not groups[key2]:
                groups.pop(key2, None)
                
        else:
            if key1 not in groups:
                groups[key1] = []

            if key2 not in groups:
                groups[key2] = []

            if select not in groups[key1]:
                groups[key1].append(select)
                
            if select not in groups[key2]:
                groups[key2].append(select)

        with open(f"{PATH_TO_FOLDER}/projects/{self.window.project}/settings.json", "w", encoding="utf-8") as file:
            json.dump(self.window.settings, file, ensure_ascii=False)

        self.window.objects["groups_scroll"] = self.groupsTable.verticalScrollBar().value()

        self.load()
