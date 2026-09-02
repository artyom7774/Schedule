from PyQt5.QtWidgets import QTabWidget, QWidget, QComboBox, QListWidget, QTableWidget, QHeaderView, QLabel, QTableWidgetItem, QAbstractItemView
from PyQt5.QtCore import Qt

from src.variables import *

import json


class TabView(QWidget):
    def __init__(self, window):
        super().__init__()

        self.window = window

        self.classes = []

        for i, cnt in enumerate(self.window.settings["classes"]["count"]):
            for number in range(cnt):
                self.classes.append(f"{i + 1} {CLASSES_ALPHABET[number + 1]}")

        self.teachers = list(sorted(window.settings["teachers"].keys()))

        self.answer = None

        answerPath = f"{PATH_TO_FOLDER}/projects/{self.window.project}/answer.json"

        if os.path.exists(answerPath):
            try:
                with open(answerPath, "r", encoding="utf-8") as file:
                    self.answer = json.load(file)

            except BaseException:
                self.answer = None

        self.modeComboBox = QComboBox(parent=self)
        self.modeComboBox.addItems([translate("menu.main.tab.view.classes"), translate("menu.main.tab.view.teachers")])
        self.modeComboBox.setFont(FONT)

        mode = window.objects.get("mode", 0)

        if not (0 <= mode <= 1):
            mode = 0

        self.modeComboBox.blockSignals(True)

        self.modeComboBox.setCurrentIndex(mode)

        self.modeComboBox.blockSignals(False)

        self.modeComboBox.currentIndexChanged.connect(lambda idx: self.modeChanged(idx))
        self.modeComboBox.show()

        self.items = QListWidget(parent=self)
        self.items.itemClicked.connect(lambda: self.itemsItemClicked())
        self.items.setFont(FONT)

        items = self.classes if mode == 0 else self.teachers

        self.items.addItems(items)

        select = window.objects.get("view_selected")

        if select in items:
            self.items.setCurrentRow(items.index(select))

        elif items:
            self.items.setCurrentRow(0)

        self.items.show()

        self.selected = self.items.currentItem().text() if self.items.currentItem() is not None else None

        window.objects["view_selected"] = self.selected

        self.info = QLabel(parent=self)
        self.info.setAlignment(Qt.AlignCenter)
        self.info.setWordWrap(True)
        self.info.setFont(FONT)

        self.tabs = QTabWidget(parent=self)
        self.tabs.tabBar().setFont(FONT)
        self.tabs.tabBarClicked.connect(lambda idx: self.shiftTabClicked(idx))

        shifts = ["I", "II", "III"][:self.window.settings["number_of_shifts"] + 1] + list([f"{element}" for element in range(4, self.window.settings["number_of_shifts"] + 1)])

        self.tables = {}

        for shift in range(self.window.settings["number_of_shifts"]):
            table = QTableWidget(self.window.settings["max_lesson_count_per_day"], self.window.settings["working_days_per_week"], parent=self)

            table.setEditTriggers(QAbstractItemView.NoEditTriggers)
            table.setSelectionMode(QAbstractItemView.NoSelection)

            table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

            table.setVerticalHeaderLabels([f"{i + 1}" for i in range(self.window.settings["max_lesson_count_per_day"])])
            table.setHorizontalHeaderLabels([f"{translate('day.' + str(i))}" for i in range(self.window.settings["working_days_per_week"])])

            table.setFont(FONT)

            self.tables[shift] = table

            self.tabs.addTab(table, shifts[shift])

        self.tabs.show()

        if self.answer is None:
            self.tabs.hide()

            self.info.setText(translate("menu.main.tab.view.schedule_not_created"))
            self.info.show()

            return

        if self.selected is None:
            self.tabs.hide()

            return

        self.info.hide()
        self.tabs.show()

        if mode == 0:
            classShift = self.classShift(self.selected)

            self.fillClassSchedule(self.selected)

            for shift in range(self.window.settings["number_of_shifts"]):
                self.tabs.setTabEnabled(shift, shift == classShift)

            self.tabs.setCurrentIndex(classShift)

        else:
            self.fillTeacherSchedule(self.selected)

            for shift in range(self.window.settings["number_of_shifts"]):
                self.tabs.setTabEnabled(shift, True)

            shift = window.objects.get("view_shift_selected", 0)

            if not (0 <= shift < self.window.settings["number_of_shifts"]):
                shift = 0

            self.tabs.setCurrentIndex(shift)

    def classShift(self, name: str) -> int:
        grade = int(name.split(" ")[0]) - 1

        return self.window.settings["classes"]["shift"][grade]

    def modeChanged(self, idx):
        self.window.objects["mode"] = idx

        self.window.objects.pop("view_selected", None)
        self.window.objects.pop("view_shift_selected", None)

        TabView.init(self.window, ignore=[TAB_VIEW], reverse=True)

    def itemsItemClicked(self):
        item = self.items.currentItem()

        new = item.text() if item is not None else None

        if new == self.selected:
            return

        self.selected = new
        self.window.objects["view_selected"] = self.selected

        TabView.init(self.window, ignore=[TAB_VIEW], reverse=True)

    def shiftTabClicked(self, idx):
        self.window.objects["view_shift_selected"] = idx

    @staticmethod
    def entries(cell: dict):
        if cell.get("subject", "#") == "#":
            return []

        entries = [(cell["subject"], cell.get("teachers", []))]

        for extra in cell.get("extra", []):
            if extra.get("subject", "#") == "#":
                continue

            entries.append((extra["subject"], extra.get("teachers", [])))

        return entries

    def fillClassSchedule(self, cls: str):
        days = self.window.settings["working_days_per_week"]
        lessons = self.window.settings["max_lesson_count_per_day"]

        shift = self.classShift(cls)
        table = self.tables[shift]

        data = self.answer.get(cls, [])

        for day in range(days):
            for lesson in range(lessons):
                text = "-"
                tooltip = ""

                if day < len(data) and lesson < len(data[day]):
                    entries = self.entries(data[day][lesson])

                    if entries:
                        text = " / ".join(subject for subject, _ in entries)
                        tooltip = "\n".join(
                            f"{subject}: {', '.join(teachers)}" if teachers else subject
                            for subject, teachers in entries
                        )

                item = QTableWidgetItem(text)
                item.setTextAlignment(Qt.AlignCenter)
                item.setToolTip(tooltip)

                table.setItem(lesson, day, item)

    def fillTeacherSchedule(self, teacher: str):
        days = self.window.settings["working_days_per_week"]
        lessons = self.window.settings["max_lesson_count_per_day"]

        for shift in range(self.window.settings["number_of_shifts"]):
            table = self.tables[shift]

            classesInShift = [cls for cls in self.classes if self.classShift(cls) == shift]

            for day in range(days):
                for lesson in range(lessons):
                    tooltip = ""
                    text = "-"

                    for cls in classesInShift:
                        data = self.answer.get(cls, [])

                        if day >= len(data) or lesson >= len(data[day]):
                            continue

                        entries = self.entries(data[day][lesson])

                        found = False

                        for subject, teachers in entries:
                            if teacher in teachers:
                                tooltip = f"{cls}: {subject}"
                                text = f"{cls}\n{subject}"

                                found = True

                                break

                        if found:
                            break

                    item = QTableWidgetItem(text)
                    item.setTextAlignment(Qt.AlignCenter)
                    item.setToolTip(tooltip)

                    table.setItem(lesson, day, item)
