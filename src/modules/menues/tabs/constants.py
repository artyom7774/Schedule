from PyQt5.QtWidgets import QWidget, QListWidget, QTableWidget, QTableWidgetItem, QHeaderView, QPushButton, QLabel, QMenu, QAction, QAbstractItemView
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor

from src.variables import *

import json


class TabConstants(QWidget):
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

    def groups(self, cls) -> list:
        return [set(subjects) for subjects in self.window.settings.get("groups", {}).get(cls, {}).values()]

    def canCombine(self, cls, subjects) -> bool:
        groups = self.groups(cls)

        if len(set(subjects)) != len(subjects):
            return False

        if not all(any(s in group for group in groups) for s in subjects):
            return False

        return not any(sum(s in group for s in subjects) > 1 for group in groups)

    def getSubjects(self, cls, day, lesson) -> list:
        value = self.window.settings["constants"].get(cls, {}).get(self.key(day, lesson))

        if value is None:
            return []

        if isinstance(value, list):
            return list(value)

        return [value]

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

                    values = data[key] if isinstance(data[key], list) else [data[key]]

                    valid = 0 <= day < self.days and 0 <= lesson < self.lessons and len(values) > 0 and all(s in self.subjects and s != "-" for s in values) and (len(values) == 1 or self.canCombine(cls, values))

                except (ValueError, AttributeError, TypeError):
                    valid = False

                if not valid:
                    data.pop(key)

                    changed = True

            constants[cls] = data

        if changed:
            self.save()

    def save(self):
        with open(f"{PATH_TO_FOLDER}/projects/{self.window.project}/settings.json", "w", encoding="utf-8") as file:
            json.dump(self.window.settings, file, indent=4, ensure_ascii=False)

    def fillTable(self):
        for day in range(self.days):
            for lesson in range(self.lessons):
                item = QTableWidgetItem()
                item.setTextAlignment(Qt.AlignCenter)

                self.table.setItem(lesson, day, item)

                self.updateCell(day, lesson)

    def updateCell(self, day, lesson):
        subjects = self.getSubjects(self.cls, day, lesson)
        text = " / ".join(subjects) if subjects else "-"

        item = self.table.item(lesson, day)

        item.setText(text)
        item.setToolTip("" if not subjects else "\n".join(subjects))

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

        current = self.getSubjects(self.cls, day, lesson)

        menu = QMenu(self)
        menu.setFont(FONT)

        for subject in self.subjects:
            action = QAction(subject if subject != "-" else translate("menu.main.tab.constants.none"), self)
            action.setCheckable(True)
            action.setChecked(subject in current if subject != "-" else not current)
            action.triggered.connect(lambda _, s=subject: self.toggleSubject(day, lesson, s))

            menu.addAction(action)

            if subject == "-":
                menu.addSeparator()

        menu.exec_(QCursor.pos())

    def tableContextMenu(self, pos):
        item = self.table.itemAt(pos)

        if item is None:
            return

        self.setSubject(item.column(), item.row(), "-")

    def toggleSubject(self, day, lesson, subject):
        current = self.getSubjects(self.cls, day, lesson)
        groups = self.groups(self.cls)

        if subject == "-" or not any(subject in group for group in groups):
            self.setSubject(day, lesson, subject)

            return

        if subject in current:
            current.remove(subject)

        elif self.canCombine(self.cls, current + [subject]):
            current.append(subject)

        else:
            current = [subject]

        self.setSubjects(day, lesson, current)

    def setSubject(self, day, lesson, subject):
        self.setSubjects(day, lesson, [subject])

    def setSubjects(self, day, lesson, subjects):
        data = self.window.settings["constants"].setdefault(self.cls, {})
        key = self.key(day, lesson)

        subjects = [s for s in subjects if s in self.subjects and s != "-"]

        if not subjects:
            data.pop(key, None)

        elif len(subjects) == 1:
            data[key] = subjects[0]

        else:
            data[key] = subjects

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
                self.window.settings["constants"][other] = {key: list(value) if isinstance(value, list) else value for key, value in source.items()}

        self.window.objects["constants_selected"] = cls

        self.save()

        TabConstants.init(self.window, ignore=[TAB_CONSTANTS], reverse=True)
