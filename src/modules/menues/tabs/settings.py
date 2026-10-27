from PyQt5.QtWidgets import QSlider, QWidget, QTableWidget, QPushButton, QHeaderView, QLabel, QLineEdit, QTableWidgetItem, QAbstractItemView
from PyQt5.QtGui import QBrush, QColor
from PyQt5.QtCore import Qt

from src.variables import *

import typing
import json


class TabSettings(QWidget):
    def __init__(self, window):
        super().__init__()

        self.window = window

        self.settingsRama = QTableWidget(0, 0, parent=self)
        self.settingsRama.horizontalHeader().setVisible(False)
        self.settingsRama.verticalHeader().setVisible(False)
        self.settingsRama.show()

        self.settingsRamaSecond = QTableWidget(0, 0, parent=self)
        self.settingsRamaSecond.horizontalHeader().setVisible(False)
        self.settingsRamaSecond.verticalHeader().setVisible(False)
        self.settingsRamaSecond.show()

        self.settingsDaysLabel = QLabel(translate("menu.main.tab.settings.working_days_per_week"), parent=self)
        self.settingsDaysLabel.setFont(FONT)
        self.settingsDaysLabel.show()

        self.settingsDaysEdit = QLineEdit(parent=self)
        self.settingsDaysEdit.setText(str(window.settings["working_days_per_week"]))
        self.settingsDaysEdit.editingFinished.connect(lambda: TabSettings.save(window, "working_days_per_week", self.settingsDaysEdit))
        self.settingsDaysEdit.setFont(FONT)
        self.settingsDaysEdit.show()

        self.settingsLessonsLabel = QLabel(translate("menu.main.tab.settings.max_lesson_count_per_day"), parent=self)
        self.settingsLessonsLabel.setFont(FONT)
        self.settingsLessonsLabel.show()

        self.settingsLessonsEdit = QLineEdit(parent=self)
        self.settingsLessonsEdit.setText(str(window.settings["max_lesson_count_per_day"]))
        self.settingsLessonsEdit.editingFinished.connect(lambda: TabSettings.save(window, "max_lesson_count_per_day", self.settingsLessonsEdit))
        self.settingsLessonsEdit.setFont(FONT)
        self.settingsLessonsEdit.show()

        self.settingsClassesCountLabel = QLabel(translate("menu.main.tab.settings.classes_count"), parent=self)
        self.settingsClassesCountLabel.setFont(FONT)
        self.settingsClassesCountLabel.show()

        self.settingsClassesCountEdit = QLineEdit(parent=self)
        self.settingsClassesCountEdit.setText(str(window.settings["classes_count"]))
        self.settingsClassesCountEdit.editingFinished.connect(lambda: TabSettings.save(window, "classes_count", self.settingsClassesCountEdit))
        self.settingsClassesCountEdit.setFont(FONT)
        self.settingsClassesCountEdit.show()

        self.settingsSubjectsCountLabel = QLabel(translate("menu.main.tab.settings.subjects_count"), parent=self)
        self.settingsSubjectsCountLabel.setFont(FONT)
        self.settingsSubjectsCountLabel.show()

        self.settingsSubjectsCountEdit = QLineEdit(parent=self)
        self.settingsSubjectsCountEdit.setText(str(window.settings["subjects_count"]))
        self.settingsSubjectsCountEdit.editingFinished.connect(lambda: TabSettings.save(window, "subjects_count", self.settingsSubjectsCountEdit))
        self.settingsSubjectsCountEdit.setFont(FONT)
        self.settingsSubjectsCountEdit.show()

        self.settingsShiftsCountLabel = QLabel(translate("menu.main.tab.settings.number_of_shifts"), parent=self)
        self.settingsShiftsCountLabel.setFont(FONT)
        self.settingsShiftsCountLabel.show()

        self.settingsShiftsCountEdit = QLineEdit(parent=self)
        self.settingsShiftsCountEdit.setText(str(window.settings["number_of_shifts"]))
        self.settingsShiftsCountEdit.editingFinished.connect(lambda: TabSettings.save(window, "number_of_shifts", self.settingsShiftsCountEdit))
        self.settingsShiftsCountEdit.setFont(FONT)
        self.settingsShiftsCountEdit.show()

        self.settingsShiftCrossingLabel = QLabel(translate("menu.main.tab.settings.shift_crossing"), parent=self)
        self.settingsShiftCrossingLabel.setFont(FONT)
        self.settingsShiftCrossingLabel.show()

        self.settingsShiftCrossingEdit = QLineEdit(parent=self)
        self.settingsShiftCrossingEdit.setText(str(window.settings["shift_crossing"]))
        self.settingsShiftCrossingEdit.editingFinished.connect(lambda: TabSettings.save(window, "shift_crossing", self.settingsShiftCrossingEdit))
        self.settingsShiftCrossingEdit.setFont(FONT)
        self.settingsShiftCrossingEdit.show()

        self.maxLessonForTeacherLabel = QLabel(translate("menu.main.tab.settings.max_lesson_for_teacher_per_day"), parent=self)
        self.maxLessonForTeacherLabel.setFont(FONT)
        self.maxLessonForTeacherLabel.show()

        self.maxLessonForTeacherEdit = QLineEdit(parent=self)
        self.maxLessonForTeacherEdit.setText(str(window.settings["max_lesson_for_teacher"]))
        self.maxLessonForTeacherEdit.editingFinished.connect(lambda: TabSettings.save(window, "max_lesson_for_teacher", self.maxLessonForTeacherEdit))
        self.maxLessonForTeacherEdit.setFont(FONT)
        self.maxLessonForTeacherEdit.show()

        flag = False

        self.subjectsTable = QTableWidget(window.settings["subjects_count"], 2, parent=self)

        while len(window.settings["subjects"]) > window.settings["subjects_count"]:
            window.settings["subjects"].pop(-1)

        while len(window.settings["subjects"]) < window.settings["subjects_count"]:
            window.settings["subjects"].append(["", -1])

        idx = 0

        for element in window.settings["subjects"]:
            self.subjectsTable.setItem(idx, 0, QTableWidgetItem(str(element[0])))

            if isinstance(element[1], str):
                window.settings["subjects"][idx][1] = int(element[1])

            if element[1] != -1:
                self.subjectsTable.setItem(idx, 1, QTableWidgetItem(str(element[1])))

            idx += 1

        self.subjectsTable.cellChanged.connect(lambda row, col: TabSettings.save(window, "subjects", self.subjectsTable, [row, col], [0]))
        self.subjectsTable.setHorizontalHeaderLabels([translate("menu.main.tab.settings.subject"), translate("menu.main.tab.settings.hard")])
        # TODO
        self.subjectsTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.subjectsTable.verticalHeader().setVisible(False)
        self.subjectsTable.setFont(FONT)
        self.subjectsTable.show()

        while len(window.settings["classes"]["count"]) > window.settings["classes_count"]:
            window.settings["classes"]["count"].pop(-1)

            flag = True

        while len(window.settings["classes"]["count"]) < window.settings["classes_count"]:
            window.settings["classes"]["count"].append(0)

            flag = True

        if shiftNormalize(window.settings):
            flag = True

        if flag:
            with open(f"{PATH_TO_FOLDER}/projects/{self.window.project}/settings.json", "w", encoding="utf-8") as file:
                json.dump(self.window.settings, file, indent=4, ensure_ascii=False)

        self.shiftsTable = QTableWidget(len(CLASSES_ALPHABET) - 1, window.settings["classes_count"], parent=self)
        self.shiftsTable.setHorizontalHeaderLabels([str(i + 1) for i in range(window.settings["classes_count"])])
        self.shiftsTable.setVerticalHeaderLabels([CLASSES_ALPHABET[i + 1] for i in range(len(CLASSES_ALPHABET) - 1)])
        self.shiftsTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.shiftsTable.setSelectionMode(QAbstractItemView.NoSelection)
        self.shiftsTable.setFont(LITTLE_FONT)
        self.shiftsTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.shiftsTable.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.shiftsTable.show()

        self.classesObjects = {}

        for number in range(window.settings["classes_count"]):
            self.initClassCountObject(number)

    def initClassCountObject(self, number, slider: bool = True):
        elements = [f"label_{number}", f"scroll_{number}", f"info_{number}"]

        for element in elements:
            if element in self.classesObjects:
                if element == f"scroll_{number}" and not slider:
                    continue

                self.classesObjects[element].deleteLater()

        name = f"{' ' if number + 1 < 10 else ''}{number + 1}:"

        self.classesObjects[f"label_{number}"] = QLabel(name, parent=self)
        self.classesObjects[f"label_{number}"].setFont(FONT)
        self.classesObjects[f"label_{number}"].show()

        if slider:
            self.classesObjects[f"scroll_{number}"] = QSlider(Qt.Horizontal, parent=self)
            self.classesObjects[f"scroll_{number}"].valueChanged.connect(lambda value: TabSettings.save(self.window, "classes/count", self.classesObjects[f"scroll_{number}"], [number, value], [0]))
            self.classesObjects[f"scroll_{number}"].setMinimum(0)
            self.classesObjects[f"scroll_{number}"].setMaximum(len(CLASSES_ALPHABET) - 1)

            self.classesObjects[f"scroll_{number}"].blockSignals(True)

            self.classesObjects[f"scroll_{number}"].setValue(self.window.settings["classes"]["count"][number])

            self.classesObjects[f"scroll_{number}"].blockSignals(False)

        name = "-" if self.window.settings["classes"]["count"][number] == 0 else f"A-{CLASSES_ALPHABET[self.window.settings['classes']['count'][number]]}"

        self.classesObjects[f"info_{number}"] = QLabel(name, parent=self)
        self.classesObjects[f"info_{number}"].setAlignment(Qt.AlignCenter)
        self.classesObjects[f"info_{number}"].setFont(FONT)
        self.classesObjects[f"info_{number}"].show()

        self.initShiftColumn(number)

    def initShiftColumn(self, grade: int):
        count = self.window.settings["classes"]["count"][grade]

        for letter in range(len(CLASSES_ALPHABET) - 1):
            if letter < count:
                self.initShiftButton(grade, letter)

                continue

            self.shiftsTable.removeCellWidget(letter, grade)

            item = QTableWidgetItem()
            item.setFlags(Qt.NoItemFlags)
            item.setBackground(QBrush(QColor(CLASSES_TABLE_COLORS[1])))

            self.shiftsTable.setItem(letter, grade, item)

    def initShiftButton(self, grade: int, letter: int):
        self.shiftsTable.takeItem(letter, grade)

        button = QPushButton(shiftName(self.window.settings["classes"]["shift"][grade][letter]), parent=self.shiftsTable)
        button.setFont(LITTLE_FONT)
        button.setToolTip(f"{grade + 1} {CLASSES_ALPHABET[letter + 1]}")
        button.clicked.connect(lambda checked=False, g=grade, l=letter: TabSettings.save(self.window, "classes/shift", button, [g, l]))

        self.shiftsTable.setCellWidget(letter, grade, button)

    @staticmethod
    def save(window, parameter, object, another: typing.Any = None, ignore: list = None):
        if ignore is None:
            ignore = []

        if parameter in ("working_days_per_week", "max_lesson_count_per_day", "classes_count", "subjects_count", "number_of_shifts", "shift_crossing", "max_lesson_for_teacher"):
            text = object.text()

            try:
                int(text)

            except BaseException:
                object.setText(str(window.settings[parameter]))

                return

            window.settings[parameter] = int(text)

        elif parameter in ("subjects", ):
            row, col = another

            text = object.item(row, col).text()

            if col == 0:
                window.settings[parameter][row][col] = text

            if col == 1:
                try:
                    int(text)

                except BaseException:
                    object.item(row, col).setText(str(window.settings[parameter][row][col]) if window.settings[parameter][row][col] != -1 else "")

                    return

                window.settings[parameter][row][col] = int(text)

            with open(f"{PATH_TO_FOLDER}/projects/{window.project}/settings.json", "w", encoding="utf-8") as file:
                json.dump(window.settings, file, indent=4, ensure_ascii=False)

            TabSettings.init(window, ignore=[TAB_CLASSES, TAB_GROUPS], reverse=True)

            return

        elif parameter in ("classes/count", ):
            window.settings["classes"]["count"][another[0]] = another[1]

            if window.objects["tabs"].widget(TAB_SETTINGS):
                window.objects["tabs"].widget(TAB_SETTINGS).initClassCountObject(another[0], False)

            with open(f"{PATH_TO_FOLDER}/projects/{window.project}/settings.json", "w", encoding="utf-8") as file:
                json.dump(window.settings, file, indent=4, ensure_ascii=False)

            TabSettings.init(window, ignore=[TAB_CLASSES, TAB_GROUPS], reverse=True)

            return

        elif parameter in ("classes/shift", ):
            grade, letter = another

            shifts = max(window.settings["number_of_shifts"], 1)

            window.settings["classes"]["shift"][grade][letter] = (window.settings["classes"]["shift"][grade][letter] + 1) % shifts

            with open(f"{PATH_TO_FOLDER}/projects/{window.project}/settings.json", "w", encoding="utf-8") as file:
                json.dump(window.settings, file, indent=4, ensure_ascii=False)

            if window.objects["tabs"].widget(TAB_SETTINGS):
                window.objects["tabs"].widget(TAB_SETTINGS).initShiftButton(grade, letter)

            TabSettings.init(window, ignore=[TAB_VIEW, TAB_EXPORT], reverse=True)

            return

        with open(f"{PATH_TO_FOLDER}/projects/{window.project}/settings.json", "w", encoding="utf-8") as file:
            json.dump(window.settings, file, indent=4, ensure_ascii=False)

        TabSettings.init(window)
