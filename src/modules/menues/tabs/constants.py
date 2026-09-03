from PyQt5.QtWidgets import QWidget, QListWidget, QTableWidget, QTableWidgetItem, QHeaderView, QPushButton, QLabel, QMenu, QAction, QAbstractItemView
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor

from src.variables import *

import json


class TabConstants(QWidget):
    """
    Формат хранения в settings.json:
        "constants": {
            "1 А": {
                "0-2": "Математика",   # "<день>-<урок>" (нулевая индексация): предмет
                "3-0": "Физкультура"
            },
            ...
        }
    Незафиксированные ячейки в словаре отсутствуют.
    """

    def __init__(self, window):
        super().__init__()

        self.window = window

        settings = self.window.settings

        self.days = settings["working_days_per_week"]
        self.lessons = settings["max_lesson_count_per_day"]

        self.classes = []

        for i, cnt in enumerate(settings["classes"]["count"]):
            for number in range(cnt):
                self.classes.append(f"{i + 1} {CLASSES_ALPHABET[number + 1]}")

        self.subjects = ["-"] + [subject for [subject, _] in settings["subjects"] if subject != ""]

        self.normalize()

        self.classesList = QListWidget(parent=self)
        self.classesList.addItems(self.classes)
        self.classesList.itemClicked.connect(lambda: self.classesListItemClicked())
        self.classesList.setFont(FONT)

        self.classesList.setContextMenuPolicy(Qt.CustomContextMenu)
        self.classesList.customContextMenuRequested.connect(lambda pos: self.showContextMenu(pos))

        select = self.window.objects.get("constants_selected")

        if select in self.classes:
            self.classesList.setCurrentRow(self.classes.index(select))

        elif self.classes:
            self.classesList.setCurrentRow(0)

        self.classesList.show()

        self.cls = self.classesList.currentItem().text() if self.classesList.currentItem() is not None else None
        self.window.objects["constants_selected"] = self.cls

        self.table = QTableWidget(self.lessons, self.days, parent=self)

        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionMode(QAbstractItemView.NoSelection)

        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.table.setVerticalHeaderLabels([f"{i + 1}" for i in range(self.lessons)])
        self.table.setHorizontalHeaderLabels([f"{translate('day.' + str(i))}" for i in range(self.days)])

        self.table.setFont(FONT)

        self.table.cellClicked.connect(lambda row, col: self.cellClicked(row, col))
        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(lambda pos: self.tableContextMenu(pos))

        self.table.show()

        self.fillTable()

    @staticmethod
    def key(day, lesson) -> str:
        return f"{day}-{lesson}"

    def getSubject(self, cls, day, lesson) -> str:
        return self.window.settings["constants"].get(cls, {}).get(self.key(day, lesson), "-")

    def normalize(self):
        settings = self.window.settings

        changed = False

        constants = settings.get("constants")

        if not isinstance(constants, dict):
            constants = {}

            changed = True

        settings["constants"] = constants

        for cls in list(constants.keys()):
            if cls not in self.classes:
                constants.pop(cls)

                changed = True

        for cls in self.classes:
            data = constants.get(cls)

            if not isinstance(data, dict):
                data = {}

                changed = True

            for key in list(data.keys()):
                valid = False

                try:
                    day, lesson = map(int, key.split("-"))

                    valid = 0 <= day < self.days and 0 <= lesson < self.lessons and data[key] in self.subjects and data[key] != "-"

                except (ValueError, AttributeError):
                    valid = False

                if not valid:
                    data.pop(key)

                    changed = True

            constants[cls] = data

        if changed:
            self.save()

    def save(self):
        with open(f"{PATH_TO_FOLDER}/projects/{self.window.project}/settings.json", "w", encoding="utf-8") as file:
            json.dump(self.window.settings, file, ensure_ascii=False)

    def fillTable(self):
        for day in range(self.days):
            for lesson in range(self.lessons):
                item = QTableWidgetItem()
                item.setTextAlignment(Qt.AlignCenter)

                self.table.setItem(lesson, day, item)

                self.updateCell(day, lesson)

    def updateCell(self, day, lesson):
        subject = self.getSubject(self.cls, day, lesson)

        item = self.table.item(lesson, day)

        item.setText(subject)
        item.setToolTip("" if subject == "-" else subject)

    def updateRowSizes(self):
        if self.cls is None:
            return

        header = self.table.verticalHeader()

        available = self.table.height() - self.table.horizontalHeader().height() - 2 * self.table.frameWidth()
        minHeight = self.table.fontMetrics().height() + 12

        if self.lessons * minHeight <= available:
            header.setSectionResizeMode(QHeaderView.Stretch)

        else:
            header.setSectionResizeMode(QHeaderView.Fixed)
            header.setDefaultSectionSize(minHeight)

    def cellClicked(self, row, col):
        day, lesson = col, row

        current = self.getSubject(self.cls, day, lesson)

        menu = QMenu(self)
        menu.setFont(FONT)

        for subject in self.subjects:
            action = QAction(subject if subject != "-" else translate("menu.main.tab.constants.none"), self)
            action.setCheckable(True)
            action.setChecked(subject == current)
            action.triggered.connect(lambda _, s=subject: self.setSubject(day, lesson, s))

            menu.addAction(action)

            if subject == "-":
                menu.addSeparator()

        menu.exec_(QCursor.pos())

    def tableContextMenu(self, pos):
        item = self.table.itemAt(pos)

        if item is None:
            return

        self.setSubject(item.column(), item.row(), "-")

    def setSubject(self, day, lesson, subject):
        data = self.window.settings["constants"].setdefault(self.cls, {})
        key = self.key(day, lesson)

        if subject not in self.subjects or subject == "-":
            data.pop(key, None)

        else:
            data[key] = subject

        self.updateCell(day, lesson)

        self.save()

    def classesListItemClicked(self):
        item = self.classesList.currentItem()

        new = item.text() if item is not None else None

        if new == self.cls:
            return

        self.cls = new
        self.window.objects["constants_selected"] = self.cls

        TabConstants.init(self.window, ignore=[TAB_CONSTANTS], reverse=True)

    def clearButtonClicked(self):
        if self.cls is None:
            return

        self.clearClass(self.cls)

    def showContextMenu(self, pos):
        item = self.classesList.itemAt(pos)

        if item is None:
            return

        menu = QMenu(self)
        menu.setFont(FONT)

        clear = QAction(translate("menu.main.tab.constants.clear"), self)
        clear.triggered.connect(lambda: self.clearClass(item.text()))

        copyToParallel = QAction(translate("menu.main.tab.constants.copy_to_parallel"), self)
        copyToParallel.triggered.connect(lambda: self.copyToParallel(item.text()))

        menu.addAction(clear)
        menu.addAction(copyToParallel)

        menu.exec_(self.classesList.mapToGlobal(pos))

    def clearClass(self, cls):
        self.window.settings["constants"][cls] = {}

        self.window.objects["constants_selected"] = cls

        self.save()

        TabConstants.init(self.window, ignore=[TAB_CONSTANTS], reverse=True)

    def copyToParallel(self, cls):
        grade = cls.split(" ")[0]
        source = self.window.settings["constants"].get(cls, {})

        for other in self.classes:
            if other != cls and other.split(" ")[0] == grade:
                self.window.settings["constants"][other] = dict(source)

        self.window.objects["constants_selected"] = cls

        self.save()

        TabConstants.init(self.window, ignore=[TAB_CONSTANTS], reverse=True)
