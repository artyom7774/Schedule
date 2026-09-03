from PyQt5.QtWidgets import QWidget, QTableWidget, QHeaderView, QCheckBox, QTableWidgetItem
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

from src.variables import *

import json


class TabGroups(QWidget):
    def __init__(self, window):
        super().__init__()

        self.window = window

        self.subjects = [element[0] for element in self.window.settings["subjects"]]

        self.groupsTable = QTableWidget(self.window.settings["subjects_count"], self.window.settings["subjects_count"], parent=self)
        self.groupsTable.cellClicked.connect(lambda row, col: self.groupsTableCellClicked(row, col))
        self.groupsTable.setStyleSheet("""QHeaderView::section { padding-right: 8px; }""")

        for row, subject1 in enumerate(self.subjects):
            for col, subject2 in enumerate(self.subjects):
                item = QTableWidgetItem()

                if row == col:
                    item.setBackground(QColor("#3f4042"))

                elif f"{subject1}-{subject2}" in self.window.settings["groups"]:
                    item.setBackground(QColor("#109012"))

                else:
                    item.setBackground(QColor("#202124"))

                self.groupsTable.setItem(row, col, item)

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

        if "groups_scroll" in self.window.objects:
            self.groupsTable.verticalScrollBar().setValue(self.window.objects["groups_scroll"])

        self.groupsTable.show()

    def groupsTableCellClicked(self, row, col):
        if row == col:
            return

        subject1 = self.subjects[row]
        subject2 = self.subjects[col]

        if subject1 == "" or subject2 == "":
            return

        if f"{subject1}-{subject2}" in self.window.settings["groups"]:
            self.window.settings["groups"].pop(f"{subject1}-{subject2}")
            self.window.settings["groups"].pop(f"{subject2}-{subject1}")

        else:
            self.window.settings["groups"][f"{subject1}-{subject2}"] = 1
            self.window.settings["groups"][f"{subject2}-{subject1}"] = 1

        with open(f"{PATH_TO_FOLDER}/projects/{self.window.project}/settings.json", "w", encoding="utf-8") as file:
            json.dump(self.window.settings, file, ensure_ascii=False)

        self.window.objects["groups_scroll"] = self.groupsTable.verticalScrollBar().value()

        TabGroups.init(self.window, ignore=[TAB_GROUPS], reverse=True)
