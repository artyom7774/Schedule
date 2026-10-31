from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QAbstractItemView
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt

from src.modules.widgets import MultiTableWidget

from src.variables import *

import json


class TabSubjects(QWidget):
    def __init__(self, window):
        super().__init__()

        self.window = window

        self.window.settings.setdefault("crossing", {})

        self.subjectsTable = MultiTableWidget(self.window.settings["subjects_count"], self.window.settings["subjects_count"], parent=self, base="")
        self.subjectsTable.setSelectionMode(QAbstractItemView.NoSelection)

        self.subjectsTable.setVerticalHeaderLabels([element[0] for element in self.window.settings["subjects"]])
        self.subjectsTable.setHorizontalHeaderLabels([element[0] for element in self.window.settings["subjects"]])

        self.subjectsTable.setHeaderLabelsWithTooltip([element[0] for element in self.window.settings["subjects"]])
        self.subjectsTable.show()

        self.subjectsTable.setEditTriggers(self.subjectsTable.NoEditTriggers)

        self.subjectsTable.blockSignals(True)

        for i, [si, _] in enumerate(self.window.settings["subjects"]):
            for j, [sj, _] in enumerate(self.window.settings["subjects"]):
                if si == "" or sj == "":
                    continue

                item = self.subjectsTable.item(i, j)

                if item is None:
                    item = QTableWidgetItem()
                    item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)

                    self.subjectsTable.setItem(i, j, item)

                item.setBackground(QColor(f"#{COLORS['green'] if self.get(si, sj) else COLORS['red']}"))

        self.subjectsTable.blockSignals(False)

        self.subjectsTable.cellDoubleClicked.connect(self.subjectsTableCellClicked)
        self.subjectsTable.cellClicked.connect(self.subjectsTableCellClicked)

    def get(self, si, sj):
        var = self.window.settings["crossing"].get(si, {})

        if sj in var:
            return var[sj]

        if si == sj:
            return False

        return True

    def subjectsTableCellClicked(self, row, col):
        subjects = self.window.settings["subjects"]

        if row >= len(subjects) or col >= len(subjects):
            return

        si = subjects[row][0]
        sj = subjects[col][0]

        if si == "" or sj == "":
            return

        crossing = self.window.settings["crossing"]

        current = self.get(si, sj)

        crossing.setdefault(si, {})[sj] = not current
        crossing.setdefault(sj, {})[si] = not current

        with open(f"{PATH_TO_FOLDER}/projects/{self.window.project}/settings.json", "w", encoding="utf-8") as file:
            json.dump(self.window.settings, file, indent=4, ensure_ascii=False)

        item = self.subjectsTable.item(row, col)
        item.setBackground(QColor(f"#{COLORS['green'] if self.get(si, sj) else COLORS['red']}"))

        item = self.subjectsTable.item(col, row)
        item.setBackground(QColor(f"#{COLORS['green'] if self.get(si, sj) else COLORS['red']}"))
