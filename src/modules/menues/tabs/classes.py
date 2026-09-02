from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QColor

from src.modules.widgets import MultiTableWidget

from src.variables import *

import json


class TabClasses(QWidget):
    def __init__(self, window):
        super().__init__()

        self.window = window

        self.classesTable = MultiTableWidget(sum(self.window.settings["classes"]["count"]), self.window.settings["subjects_count"], parent=self)

        self.classes = []

        for i, cnt in enumerate(self.window.settings["classes"]["count"]):
            for number in range(cnt):
                self.classes.append(f"{i + 1} {CLASSES_ALPHABET[number + 1]}")

        self.classesTable.setVerticalHeaderLabels(self.classes)
        self.classesTable.setHorizontalHeaderLabels([element[0] for element in self.window.settings["subjects"]])
        self.classesTable.setHeaderLabelsWithTooltip([element[0] for element in self.window.settings["subjects"]])
        self.classesTable.show()

        for i, cls in enumerate(self.classes):
            if cls not in window.settings["classes"]["lessons"]:
                window.settings["classes"]["lessons"][cls] = {}

            for j, [subject, _] in enumerate(window.settings["subjects"]):
                if subject == "":
                    continue

                if subject not in window.settings["classes"]["lessons"][cls]:
                    window.settings["classes"]["lessons"][cls][subject] = 0

                self.classesTable.item(i, j).setText(str(window.settings["classes"]["lessons"][cls][subject]))
                self.classesTable.item(i, j).setBackground(QColor(CLASSES_TABLE_COLORS[min(len(CLASSES_TABLE_COLORS) - 1, window.settings["classes"]["lessons"][cls][subject])]))

        self.classesTable.cellChanged.connect(lambda row, col: self.classesTableCellChanged())

    def classesTableCellChanged(self):
        self.classesTable.blockSignals(True)

        for i, cls in enumerate(self.window.objects["tabs"].widget(1).classes):
            for j, [subject, _] in enumerate(self.window.settings["subjects"]):
                if subject == "":
                    continue

                try:
                    int(self.classesTable.item(i, j).text())

                except BaseException:
                    self.classesTable.item(i, j).setText("0")

                    continue

                if int(self.classesTable.item(i, j).text()) < 0:
                    self.classesTable.item(i, j).setText("0")

                    continue

                self.window.settings["classes"]["lessons"][cls][subject] = int(self.classesTable.item(i, j).text())
                self.window.objects["tabs"].widget(1).classesTable.item(i, j).setBackground(QColor(CLASSES_TABLE_COLORS[min(len(CLASSES_TABLE_COLORS) - 1, self.window.settings["classes"]["lessons"][cls][subject])]))

        self.classesTable.blockSignals(False)

        with open(f"{PATH_TO_FOLDER}/projects/{self.window.project}/settings.json", "w", encoding="utf-8") as file:
            json.dump(self.window.settings, file, ensure_ascii=False)
