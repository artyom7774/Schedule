from PyQt5.QtWidgets import QScrollArea, QMenu, QAction, QFileDialog, QVBoxLayout, QTextEdit, QTabWidget, QSlider, QWidget, QComboBox, QListWidget, QTableWidget, QPushButton, QHeaderView, QLabel, QLineEdit, QTableWidgetItem, QAbstractItemView
from PyQt5.QtCore import Qt, QObject, QThread, pyqtSignal, QProcess, QTimer
from PyQt5.QtGui import QColor, QTextCursor

from src.modules.widgets import MultiTableWidget, ButtonGridWidget, ChatAITextEdit
from src.modules.ai import sendChatRequestWithFile, decoder as decodeAIMessage

from src.modules import dialogs

from src.variables import *

import datetime
import shutil
import typing
import json
import time

TAB_SETTINGS  = 0
TAB_CLASSES   = 1
TAB_TEACHERS  = 2
TAB_AI        = 4
TAB_CONSTANTS = 6
TAB_RUN       = 8
TAB_VIEW      = 10
TAB_EXPORT    = 12


class TabSettings(QWidget):
    def __init__(self, window):
        super().__init__()

        self.window = window

        self.settingsRama = QTableWidget(0, 0, parent=self)
        self.settingsRama.horizontalHeader().setVisible(False)
        self.settingsRama.verticalHeader().setVisible(False)
        self.settingsRama.show()

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
        self.subjectsTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.subjectsTable.verticalHeader().setVisible(False)
        self.subjectsTable.setFont(FONT)
        self.subjectsTable.show()

        self.classesRama = QTableWidget(0, 0, parent=self)
        self.classesRama.horizontalHeader().setVisible(False)
        self.classesRama.verticalHeader().setVisible(False)
        self.classesRama.show()

        while len(window.settings["classes"]["count"]) > window.settings["classes_count"]:
            window.settings["classes"]["count"].pop(-1)

            flag = True

        while len(window.settings["classes"]["count"]) < window.settings["classes_count"]:
            window.settings["classes"]["count"].append(0)

            flag = True

        while len(window.settings["classes"]["shift"]) > window.settings["classes_count"]:
            window.settings["classes"]["shift"].pop(-1)

            flag = True

        while len(window.settings["classes"]["shift"]) < window.settings["classes_count"]:
            window.settings["classes"]["shift"].append(0)

            flag = True

        if flag:
            with open(f"{PATH_TO_FOLDER}/projects/{self.window.project}/settings.json", "w", encoding="utf-8") as file:
                json.dump(self.window.settings, file, indent=4, ensure_ascii=False)

        self.classesObjects = {}

        for number in range(window.settings["classes_count"]):
            self.initClassCountObject(number)

    def initClassCountObject(self, number, slider: bool = True):
        elements = [f"label_{number}", f"scroll_{number}", f"info_{number}", f"shift_{number}"]

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

        shifts = ["I", "II"][:self.window.settings["number_of_shifts"] + 1] + list([f"{element}" for element in range(3, self.window.settings["number_of_shifts"] + 1)])
        shift = self.window.settings["classes"]["shift"][number]

        self.classesObjects[f"shift_{number}"] = QPushButton(parent=self)
        self.classesObjects[f"shift_{number}"].clicked.connect(lambda value: TabSettings.save(self.window, "classes/shift", self.classesObjects[f"shift_{number}"], number))
        self.classesObjects[f"shift_{number}"].setText(shifts[shift])
        self.classesObjects[f"shift_{number}"].setFont(FONT)
        self.classesObjects[f"shift_{number}"].show()

    @staticmethod
    def save(window, parameter, object, another: typing.Any = None, ignore: list = None):
        if ignore is None:
            ignore = []

        refresh = []

        if parameter in ("working_days_per_week", "max_lesson_count_per_day", "classes_count", "subjects_count", "number_of_shifts"):
            text = object.text()

            try:
                int(text)

            except BaseException:
                object.setText(str(window.settings[parameter]))

                return

            window.settings[parameter] = int(text)

            refresh = [TAB_SETTINGS, TAB_CLASSES, TAB_TEACHERS]

        elif parameter in ("subjects", ):
            row, col = another

            text = object.item(row, col).text()

            print(row, col, text)

            if col == 0:
                window.settings[parameter][row][col] = text

            if col == 1:
                try:
                    int(text)

                except BaseException:
                    object.item(row, col).setText(str(window.settings[parameter][row][col]) if window.settings[parameter][row][col] != -1 else "")

                    return

                window.settings[parameter][row][col] = int(text)

            refresh = [TAB_CLASSES, TAB_TEACHERS]

        elif parameter in ("classes/count", ):
            window.settings["classes"]["count"][another[0]] = another[1]

            if window.objects["tabs"].widget(TAB_SETTINGS):
                window.objects["tabs"].widget(TAB_SETTINGS).initClassCountObject(another[0], False)

            refresh = [TAB_CLASSES, TAB_TEACHERS]

        elif parameter in ("classes/shift", ):
            window.settings["classes"]["shift"][another] = (window.settings["classes"]["shift"][another] + 1) % window.settings["number_of_shifts"]

            if window.objects["tabs"].widget(TAB_SETTINGS):
                window.objects["tabs"].widget(TAB_SETTINGS).initClassCountObject(another, False)

            refresh = []

        with open(f"{PATH_TO_FOLDER}/projects/{window.project}/settings.json", "w", encoding="utf-8") as file:
            json.dump(window.settings, file, indent=4, ensure_ascii=False)

        if refresh:
            init(window, ignore=refresh, reverse=True)

        else:
            resize(window)


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
        self.classesTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
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


class TeacherSubjectWidget(QTableWidget):
    def __init__(self, window, teacher, subjects, classes, using, index, current=None, changed=None, parent=None):
        super().__init__(0, 0, parent)

        self.window = window
        self.index = index

        self.subjects = subjects
        self.classes = classes
        self.using = using

        self.horizontalHeader().setVisible(False)
        self.verticalHeader().setVisible(False)

        self.subject = QComboBox(parent=self)
        self.subject.addItems(self.subjects)

        self.teacher = teacher

        if current is not None and current in self.subjects:
            self.subject.setCurrentIndex(self.subjects.index(current))

        else:
            self.subject.setCurrentIndex(0)

        if changed is not None:
            self.subject.currentIndexChanged.connect(lambda _, idx=self.index: changed(idx))

        self.subject.setFont(FONT)

        if self.subject.currentIndex() != 0:
            self.grid = ButtonGridWidget(self.classes, 5, onClick=lambda text: self.clicked(text), parent=self)

            for button in self.grid.buttons:
                if button.text() not in self.using:
                    button.setStyleSheet("background: #901112")

                else:
                    button.setStyleSheet("background: #109012")

        self.show()

    def clicked(self, text):
        if text in self.window.settings["teachers"][self.teacher]["subjects"][self.index]["classes"]:
            self.window.settings["teachers"][self.teacher]["subjects"][self.index]["classes"].remove(text)

        else:
            self.window.settings["teachers"][self.teacher]["subjects"][self.index]["classes"].append(text)

        with open(f"{PATH_TO_FOLDER}/projects/{self.window.project}/settings.json", "w", encoding="utf-8") as file:
            json.dump(self.window.settings, file, ensure_ascii=False)

        init(self.window, ignore=[TAB_TEACHERS], reverse=True)


class TabTeachers(QWidget):
    def __init__(self, window):
        super().__init__()

        self.window = window

        self.classes = []

        for i, cnt in enumerate(self.window.settings["classes"]["count"]):
            for number in range(cnt):
                self.classes.append(f"{i + 1} {CLASSES_ALPHABET[number + 1]}")

        teachers = list(sorted(window.settings["teachers"].keys()))

        self.teachersList = QListWidget(parent=self)
        self.teachersList.itemClicked.connect(lambda: self.teachersListItemClicked())
        self.teachersList.addItems([teacher for teacher in teachers])

        self.teachersList.setContextMenuPolicy(Qt.CustomContextMenu)
        self.teachersList.customContextMenuRequested.connect(lambda pos: self.showContextMenu(pos))

        select = window.objects.get("teachers_selected")

        if select in teachers:
            self.teachersList.setCurrentRow(teachers.index(select))

        else:
            self.teachersList.setCurrentRow(0)

        self.teachersList.setFont(FONT)
        self.teachersList.show()

        self.createTeacherButton = QPushButton(parent=self)
        self.createTeacherButton.clicked.connect(lambda: self.createTeacherButtonClicked())
        self.createTeacherButton.setText(translate("menu.main.tab.teachers.add_teacher"))
        self.createTeacherButton.setFont(FONT)
        self.createTeacherButton.show()

        self.teachersScrollContainer = container = QWidget()

        layout = QVBoxLayout(container)

        self.teachersSubjects = {}
        self.teacher = self.teachersList.currentItem().text() if self.teachersList.currentItem() is not None else None

        self.subjects = ["-"] + [subject for [subject, _] in window.settings["subjects"] if subject != ""]

        if self.teacher is None:
            return

        self.window.settings["teachers"][self.teacher].setdefault("subjects", [])
        self.window.settings["teachers"][self.teacher].setdefault("free", [])

        self.teachersScroll = QScrollArea(parent=self)
        self.teachersScroll.show()

        i = 0

        while i < len(self.window.settings["teachers"][self.teacher]["subjects"]) + 1:
            if i < len(self.window.settings["teachers"][self.teacher]["subjects"]):
                if self.window.settings["teachers"][self.teacher]["subjects"][i]["subject"] == "-" or self.window.settings["teachers"][self.teacher]["subjects"][i]["subject"] not in self.subjects:
                    self.window.settings["teachers"][self.teacher]["subjects"].pop(i)

                    continue

            self.teachersSubjects[f"object_{i}"] = TeacherSubjectWidget(self.window, self.teacher, self.subjects, self.classes, self.window.settings["teachers"][self.teacher]["subjects"][i]["classes"] if i < len(self.window.settings["teachers"][self.teacher]["subjects"]) else [], i, self.window.settings["teachers"][self.teacher]["subjects"][i]["subject"] if i < len(self.window.settings["teachers"][self.teacher]["subjects"]) else None, self.teachersSubjectsSubjectCurrentIndexChanged, container)

            layout.addWidget(self.teachersSubjects[f"object_{i}"])

            i += 1

        self.teachersScroll.setWidget(container)

        self.teacherFree = QTabWidget(parent=self)
        self.teacherFree.tabBarClicked.connect(lambda idx: self.teacherFreeTabBarClicked(idx))
        self.teacherFree.tabBar().setFont(FONT)

        flag = False

        while len(self.window.settings["teachers"][self.teacher]["free"]) < self.window.settings["number_of_shifts"]:
            self.window.settings["teachers"][self.teacher]["free"].append([])

            flag = True

        while len(self.window.settings["teachers"][self.teacher]["free"]) > self.window.settings["number_of_shifts"]:
            self.window.settings["teachers"][self.teacher]["free"].pop(-1)

            flag = True

        if flag:
            with open(f"{PATH_TO_FOLDER}/projects/{self.window.project}/settings.json", "w", encoding="utf-8") as file:
                json.dump(self.window.settings, file, indent=4, ensure_ascii=False)

        shifts = ["I", "II", "III"][:self.window.settings["number_of_shifts"] + 1] + list([f"{element}" for element in range(4, self.window.settings["number_of_shifts"] + 1)])

        for i in range(self.window.settings["number_of_shifts"]):
            teacherFreeTable = QTableWidget(self.window.settings["max_lesson_count_per_day"], self.window.settings["working_days_per_week"], parent=self)
            teacherFreeTable.cellClicked.connect(lambda row, col: self.teacherFreeTableCellClicked(row, col))

            teacherFreeTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            teacherFreeTable.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
            teacherFreeTable.setVerticalHeaderLabels([f"{i + 1}" for i in range(self.window.settings["max_lesson_count_per_day"])])
            teacherFreeTable.setHorizontalHeaderLabels([f"{translate('day.' + str(i))}" for i in range(self.window.settings["working_days_per_week"])])

            shift = self.window.objects.get("shift_selected", 0)

            for row in range(self.window.settings["max_lesson_count_per_day"]):
                for col in range(self.window.settings["working_days_per_week"]):
                    item = QTableWidgetItem()

                    if [col, row] in self.window.settings["teachers"][self.teacher]["free"][shift]:
                        item.setBackground(QColor("#901112"))

                    else:
                        item.setBackground(QColor("#109012"))

                    teacherFreeTable.setItem(row, col, item)

            self.teacherFree.addTab(teacherFreeTable, shifts[i])

        if 0 <= self.window.objects.get("shift_selected", -1) < self.window.settings["number_of_shifts"]:
            self.teacherFree.setCurrentIndex(self.window.objects.get("shift_selected"))

    def showContextMenu(self, pos):
        item = self.teachersList.itemAt(pos)

        if item is None:
            return

        menu = QMenu(self)

        delete = QAction(translate("menu.main.tab.teachers.delete"), self)
        delete.triggered.connect(lambda: self.teacherFreeDeleteElement(item))

        menu.addAction(delete)

        menu.exec_(self.teachersList.mapToGlobal(pos))

    def teacherFreeDeleteElement(self, item):
        pos = self.teachersList.row(item)
        teachers = list(self.window.settings["teachers"].keys())

        if pos < 0 or pos >= len(teachers):
            return

        remove = teachers[pos]
        self.window.settings["teachers"].pop(remove)

        if self.window.objects.get("teachers_selected") == remove:
            self.window.objects.pop("teachers_selected", None)
            self.window.objects.pop("shift_selected", None)

        self.window.objects.pop("teachers_scroll", None)

        with open(f"{PATH_TO_FOLDER}/projects/{self.window.project}/settings.json", "w", encoding="utf-8") as file:
            json.dump(self.window.settings, file, ensure_ascii=False)

        init(self.window, ignore=[TAB_TEACHERS], reverse=True)

    def teacherFreeTabBarClicked(self, idx):
        self.window.objects["shift_selected"] = idx

        init(self.window, ignore=[TAB_TEACHERS], reverse=True)

    def teacherFreeTableCellClicked(self, row, col):
        shift = self.teacherFree.currentIndex()
        pos = [col, row]

        if pos in self.window.settings["teachers"][self.teacher]["free"][shift]:
            self.window.settings["teachers"][self.teacher]["free"][shift].remove(pos)

        else:
            self.window.settings["teachers"][self.teacher]["free"][shift].append(pos)

        self.window.objects["shift_selected"] = shift

        with open(f"{PATH_TO_FOLDER}/projects/{self.window.project}/settings.json", "w", encoding="utf-8") as file:
            json.dump(self.window.settings, file, ensure_ascii=False)

        init(self.window, ignore=[TAB_TEACHERS], reverse=True)

    def teachersSubjectsSubjectCurrentIndexChanged(self, idx):
        pos = self.teachersSubjects[f"object_{idx}"].subject.currentIndex()
        subject = self.subjects[pos]

        if len(self.window.settings["teachers"][self.teacher]["subjects"]) == idx:
            self.window.settings["teachers"][self.teacher]["subjects"].append({
                "subject": subject,
                "classes": []
            })

        self.window.settings["teachers"][self.teacher]["subjects"][idx]["subject"] = subject

        self.window.objects["teachers_scroll"] = self.teachersScroll.verticalScrollBar().value()
        self.window.objects["teachers_selected"] = self.teacher

        with open(f"{PATH_TO_FOLDER}/projects/{self.window.project}/settings.json", "w", encoding="utf-8") as file:
            json.dump(self.window.settings, file, ensure_ascii=False)

        init(self.window, ignore=[TAB_TEACHERS], reverse=True)

    def teachersListItemClicked(self):
        new = self.teachersList.currentItem().text() if self.teachersList.currentItem() is not None else None

        if new == self.teacher:
            return

        self.teacher = new
        self.window.objects["teachers_selected"] = self.teacher

        init(self.window, ignore=[TAB_TEACHERS], reverse=True)

    def createTeacherButtonClicked(self):
        title = translate("dialog.add_teacher.title")
        label = translate("dialog.add_teacher.label")
        allow = translate("dialog.add_teacher.allow")

        self.window.dialog = dialogs.TextInputDialog(self.window, title, label, allow, lambda: self.createTeacher())
        self.window.dialog.exec()

    def createTeacher(self):
        name = self.window.dialog.edit.text()

        if name == "":
            window.dialog.log.setText(translate("log.text.teacher_name_is_empty"))

            return

        if name in self.window.settings["teachers"]:
            window.dialog.log.setText(translate("log.text.teacher_name_already_exists"))

            return

        self.window.settings["teachers"][name] = {
            "subjects": [

            ],
            "free": [

            ]
        }

        self.window.dialog.close()

        with open(f"{PATH_TO_FOLDER}/projects/{self.window.project}/settings.json", "w", encoding="utf-8") as file:
            json.dump(self.window.settings, file, ensure_ascii=False)

        init(self.window, ignore=[TAB_TEACHERS], reverse=True)



class AIWorker(QObject):
    finished = pyqtSignal(str, str)
    error = pyqtSignal(str)

    def __init__(self, prompt, path):
        super().__init__()

        self.prompt = prompt
        self.path = path

    def run(self):
        try:
            text, status = sendChatRequestWithFile(self.prompt, self.path)
            self.finished.emit(text, status)

        except Exception as e:
            self.error.emit(str(e))


class TabAI(QWidget):
    chatTextEdit = None
    path = None

    def __init__(self, window):
        super().__init__()

        self.window = window

        self.thread = None
        self.worker = None

        if TabAI.chatTextEdit is None:
            TabAI.chatTextEdit = ChatAITextEdit(self.window, parent=self)

        else:
            TabAI.chatTextEdit.setParent(self)

        self.chatTextEdit = TabAI.chatTextEdit

        self.chatTextEdit.setReadOnly(True)
        self.chatTextEdit.setFont(FONT)
        self.chatTextEdit.show()

        self.messageLineEdit = QLineEdit(parent=self)
        self.messageLineEdit.returnPressed.connect(lambda: self.messageLineEditReturnPressed())
        self.messageLineEdit.setPlaceholderText(translate("menu.main.tab.AI.write_your_request_and_press_enter"))
        self.messageLineEdit.setFont(FONT)
        self.messageLineEdit.show()

        self.sendPushButton = QPushButton(parent=self)
        self.sendPushButton.setText(translate("menu.main.tab.AI.send"))
        self.sendPushButton.clicked.connect(lambda: self.messageLineEditReturnPressed())
        self.sendPushButton.setFont(FONT)
        self.sendPushButton.show()

        self.loadPushButton = QPushButton(parent=self)
        self.loadPushButton.setText(translate("menu.main.tab.AI.choose_file") if self.path is None else self.path)
        self.loadPushButton.clicked.connect(lambda: self.loadPushButtonClicked())
        self.loadPushButton.setFont(FONT)
        self.loadPushButton.show()

        self.removePushButton = QPushButton(parent=self)
        self.removePushButton.setText(translate("menu.main.tab.AI.remove_file"))
        self.removePushButton.clicked.connect(lambda: self.removePushButtonClicked())
        self.removePushButton.setFont(FONT)
        self.removePushButton.show()

    def removePushButtonClicked(self):
        self.loadPushButton.setText(translate("menu.main.tab.AI.choose_file"))
        self.path = None

    def loadPushButtonClicked(self):
        path, _ = QFileDialog.getOpenFileName(self, "Choose file", "", "All files (*)")

        if not path:
            return

        self.path = path
        self.loadPushButton.setText(path)

    def messageLineEditReturnPressed(self):
        if self.messageLineEdit.text() == "" and self.path is None:
            return

        self.messageLineEdit.setEnabled(False)
        self.loadPushButton.setEnabled(False)

        name = "$FILE$"
        path = None

        if self.path is not None:
            name = f"requests/request.{self.path[self.path.rfind('.') + 1:]}"
            path = f"{PATH_TO_FOLDER}/projects/{self.window.project}/{name}"

            shutil.copyfile(self.path, path)

        prompt = open("src/files/prompts/loader.txt", "r", encoding="utf-8").read()

        prompt = prompt.replace("$FILE$", name)
        prompt = prompt.replace("$HISTORY$", str(self.chatTextEdit.history))
        prompt = prompt.replace("$MESSAGE$", self.messageLineEdit.text())
        prompt = prompt.replace("$PATH_TO_FOLDER$", PATH_TO_FOLDER)
        prompt = prompt.replace("$PROJECT$", self.window.project)

        self.chatTextEdit.send(self.messageLineEdit.text() + (f" ({self.path})" if self.path is not None else ""))
        self.messageLineEdit.setText("")

        self.thread = QThread()

        self.worker = AIWorker(prompt, path)
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)

        self.worker.finished.connect(self.finish)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)

        self.worker.error.connect(self.error)
        self.worker.error.connect(self.thread.quit)
        self.worker.error.connect(self.worker.deleteLater)

        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()

    def error(self, error):
        self.messageLineEdit.setEnabled(True)
        self.loadPushButton.setEnabled(True)

        self.chatTextEdit.error(error)

    def finish(self, text, status):
        status, message = decodeAIMessage(self.window, text, self.chatTextEdit)

        self.messageLineEdit.setEnabled(True)
        self.loadPushButton.setEnabled(True)

        if status:
            self.chatTextEdit.error(message)

            return

        date = str(datetime.datetime.now()).replace(":", "-")

        with open(f"{PATH_TO_FOLDER}/projects/{self.window.project}/backups/{date}.json", "w", encoding="utf-8") as file:
            json.dump(self.window.settings, file, indent=4, ensure_ascii=False)

        if not os.path.exists(f"{PATH_TO_FOLDER}/projects/{self.window.project}/out.json"):
            return

        with open(f"{PATH_TO_FOLDER}/projects/{self.window.project}/out.json", "r", encoding="utf-8") as file:
            self.window.settings = json.load(file)

        os.remove(f"{PATH_TO_FOLDER}/projects/{self.window.project}/out.json")

        with open(f"{PATH_TO_FOLDER}/projects/{self.window.project}/settings.json", "w", encoding="utf-8") as file:
            json.dump(self.window.settings, file, ensure_ascii=False)

        init(self.window, ignore=[TAB_SETTINGS, TAB_CLASSES, TAB_TEACHERS], reverse=True)


class TabConstants(QWidget):
    def __init__(self, window):
        super().__init__()

        self.window = window


class TabRun(QWidget):
    stdTextEdit = None
    process = None
    time = 0

    def __init__(self, window):
        super().__init__()

        self.window = window

        if TabRun.stdTextEdit is None:
            TabRun.stdTextEdit = QTextEdit(parent=self)

        else:
            TabRun.stdTextEdit.setParent(self)

        self.stdTextEdit = TabRun.stdTextEdit

        self.settingsRama = QTableWidget(0, 0, parent=self)
        self.settingsRama.horizontalHeader().setVisible(False)
        self.settingsRama.verticalHeader().setVisible(False)
        self.settingsRama.show()

        self.objects = {}
        self.weights = {}

        self.settingsInputsInit()

        self.stdTextEdit.setReadOnly(True)
        self.stdTextEdit.setFont(ANOTHER_FONT)
        self.stdTextEdit.show()

        self.runPushButton = QPushButton(parent=self)
        self.runPushButton.clicked.connect(lambda: self.runPushButtonClicked())
        self.runPushButton.setText(translate("menu.main.tab.run.run"))
        self.runPushButton.setFont(FONT)
        self.runPushButton.show()

        self.number = 0
        self.timer = None

        self.timeLabel = QLabel(parent=self)
        self.timeLabel.setFont(FONT)
        self.timeLabel.show()

    def settingsInputsInit(self):
        for obj in self.objects.values():
            obj.deleteLater()

        self.objects = {}

        with open(f"{PATH_TO_FOLDER}/projects/{self.window.project}/weights.json", "r", encoding="utf-8") as file:
            self.weights = json.load(file)

        for name, value in self.weights.items():
            self.objects[f"label_{name}"] = QLabel(parent=self)
            self.objects[f"label_{name}"].setText(translate(f"weights.{name}") + ": ")
            self.objects[f"label_{name}"].setFont(FONT)
            self.objects[f"label_{name}"].show()

            self.objects[f"lineedit_{name}"] = QLineEdit(parent=self)
            self.objects[f"lineedit_{name}"].editingFinished.connect(lambda var = name: self.weightLineEditEditingFinished(var))
            self.objects[f"lineedit_{name}"].setText(str(value))
            self.objects[f"lineedit_{name}"].setFont(FONT)
            self.objects[f"lineedit_{name}"].show()

    def weightLineEditEditingFinished(self, name):
        value = self.objects[f"lineedit_{name}"].text()

        print(name, value)

        try:
            int(value)

        except BaseException:
            self.objects[f"lineedit_{name}"].setText(str(self.weights[name]))

            return

        self.weights[name] = int(value)

        with open(f"{PATH_TO_FOLDER}/projects/{self.window.project}/weights.json", "w", encoding="utf-8") as file:
            json.dump(self.weights, file, indent=4, ensure_ascii=False)

    def runPushButtonClicked(self):
        if self.process and self.process.state() != QProcess.NotRunning:
            return

        init(self.window, ignore=[TAB_RUN])

        self.time = time.time()
        self.number = 0

        self.timer = QTimer()
        self.timer.timeout.connect(self.counter)
        self.timer.start(1000)

        self.stdTextEdit.clear()

        TabRun.process = QProcess(self)

        self.process.setProcessChannelMode(QProcess.MergedChannels)

        self.process.readyReadStandardOutput.connect(self.stdout)
        self.process.readyReadStandardError.connect(self.stderr)

        self.process.finished.connect(self.finish)

        self.process.start("src/modules/solve.exe", [
            "--weights",    f"{PATH_TO_FOLDER}/projects/{self.window.project}/weights.json",
            "--input",      f"{PATH_TO_FOLDER}/projects/{self.window.project}/settings.json",
            "--output",     f"{PATH_TO_FOLDER}/projects/{self.window.project}/answer.json",
            "--iterations", f"100000000"
        ])

        self.runPushButton.setDisabled(True)

        if not self.process.waitForStarted(3000):
            raise Exception()

    def counter(self):
        self.number += 1

        self.timeLabel.setText(translate("menu.main.tab.run.time_passed") + ": " + str(self.number) + " s")

    def update(self):
        cursor = self.stdTextEdit.textCursor()
        cursor.movePosition(QTextCursor.End)

        self.stdTextEdit.setTextCursor(cursor)
        self.stdTextEdit.ensureCursorVisible()

    def stdout(self):
        self.stdTextEdit.insertPlainText(bytes(self.process.readAllStandardOutput()).decode("utf-8", errors="replace"))

        self.update()

    def stderr(self):
        self.stdTextEdit.insertPlainText(bytes(self.process.readAllStandardError()).decode("utf-8", errors="replace"))

        self.update()

    def finish(self, code, status):
        self.runPushButton.setDisabled(False)

        self.timer.stop()

        self.stdTextEdit.insertPlainText(f"\n=== Process finished with exit code {code} ===\n")

        self.update()

        init(self.window, ignore=[TAB_VIEW], reverse=True)

    def stop(self):
        if self.process is not None and self.process.state() != QProcess.NotRunning:
            self.process.terminate()

            if not self.process.waitForFinished(1000):
                self.process.kill()
                self.process.waitForFinished()


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

        init(self.window, ignore=[TAB_VIEW], reverse=True)

    def itemsItemClicked(self):
        item = self.items.currentItem()
        
        new = item.text() if item is not None else None

        if new == self.selected:
            return

        self.selected = new
        self.window.objects["view_selected"] = self.selected

        init(self.window, ignore=[TAB_VIEW], reverse=True)

    def shiftTabClicked(self, idx):
        self.window.objects["view_shift_selected"] = idx

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
                    cell = data[day][lesson]

                    if cell.get("subject", "#") != "#":
                        text = cell["subject"]
                        tooltip = ", ".join(cell.get("teachers", []))

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

                        cell = data[day][lesson]

                        if cell.get("subject", "#") == "#":
                            continue

                        if teacher in cell.get("teachers", []):
                            tooltip = f"{cls}: {cell['subject']}"
                            text = f"{cls}\n{cell['subject']}"

                            break

                    item = QTableWidgetItem(text)
                    item.setTextAlignment(Qt.AlignCenter)
                    item.setToolTip(tooltip)

                    table.setItem(lesson, day, item)


class TabExport(QWidget):
    def __init__(self, window):
        super().__init__()

        self.window = window


def init(window, ignore: list = None, reverse: bool = False) -> None:
    if ignore is None:
        ignore = []

    tabs = window.objects.get("tabs")

    if tabs is None:
        window.objects["empty"] = QPushButton(parent=window)
        window.objects["empty"].setGeometry(0, 0, 0, 0)

        tabs = QTabWidget(parent=window)

        window.objects["tabs"] = tabs
        window.setCentralWidget(tabs)

        tabs.currentChanged.connect(lambda: resize(window))
        tabs.tabBar().setFont(FONT)
        tabs.setStyleSheet("""QTabBar::tab {padding-left: 10px; padding-right: 10px}""")

    elements = [
        (TabSettings, "menu.main.tab.settings"),
        (TabClasses, "menu.main.tab.classes"),
        (TabTeachers, "menu.main.tab.teachers"),
        (QWidget, "/"),
        (TabAI, "menu.main.tab.AI"),
        (QWidget, "->"),
        (TabConstants, "menu.main.tab.constants"),
        (QWidget, "->"),
        (TabRun, "menu.main.tab.run"),
        (QWidget, "->"),
        (TabView, "menu.main.tab.view"),
        (QWidget, "->"),
        (TabExport, "menu.main.tab.export")
    ]

    index = tabs.currentIndex()

    tabs.blockSignals(True)

    for i, (cls, label) in enumerate(elements):
        if (i in ignore) if not reverse else (i not in ignore):
            continue

        if cls is QWidget and i < tabs.count() and tabs.widget(i) is not None:
            continue

        if i < tabs.count():
            old = tabs.widget(i)
            tabs.removeTab(i)

            if old is not None:
                old.deleteLater()

        tabs.insertTab(i, cls(window), translate(label))

        if cls == QWidget:
            tabs.setTabEnabled(i, False)

    if 0 <= index < tabs.count():
        tabs.setCurrentIndex(index)

    tabs.blockSignals(False)

    resize(window)


def resize(window) -> None:
    tab = None

    def x(prec):
        return int(tab.width() * prec / 100)

    def y(prec):
        return int(tab.height() * prec / 100)

    for i in range(3):
        if window.objects["tabs"].widget(i) is None:
            return

    tab = window.objects["tabs"].widget(TAB_SETTINGS)

    tab.settingsRama.setGeometry(0, 0, x(33), y(100))
    tab.settingsDaysLabel.setGeometry(10, 10, x(15), 30)
    tab.settingsDaysEdit.setGeometry(20 + x(15), 10, x(33) - x(15) - 30, 30)
    tab.settingsLessonsLabel.setGeometry(10, 50, x(15), 30)
    tab.settingsLessonsEdit.setGeometry(20 + x(15), 50, x(33) - x(15) - 30, 30)
    tab.settingsClassesCountLabel.setGeometry(10, 90, x(15), 30)
    tab.settingsClassesCountEdit.setGeometry(20 + x(15), 90, x(33) - x(15) - 30, 30)
    tab.settingsSubjectsCountLabel.setGeometry(10, 130, x(15), 30)
    tab.settingsSubjectsCountEdit.setGeometry(20 + x(15), 130, x(33) - x(15) - 30, 30)
    tab.settingsShiftsCountLabel.setGeometry(10, 170, x(15), 30)
    tab.settingsShiftsCountEdit.setGeometry(20 + x(15), 170, x(33) - x(15) - 30, 30)

    tab.subjectsTable.setGeometry(x(33), 0, x(34), y(100))

    tab.classesRama.setGeometry(x(67), 0, x(33), y(100))

    for number in range(window.settings["classes_count"]):
        tab.classesObjects[f"label_{number}"].setGeometry(x(67) + 10, 10 + 50 * number, 50, 30)
        tab.classesObjects[f"scroll_{number}"].setGeometry(x(67) + 50, 10 + 50 * number, x(33) - 170, 30)
        tab.classesObjects[f"info_{number}"].setGeometry(x(100) - 110, 10 + 50 * number, 60, 30)
        tab.classesObjects[f"shift_{number}"].setGeometry(x(100) - 40, 10 + 50 * number, 30, 30)

    tab = window.objects["tabs"].widget(TAB_CLASSES)

    tab.classesTable.setGeometry(0, 0, x(100), y(100))

    tab = window.objects["tabs"].widget(TAB_TEACHERS)

    tab.teachersList.setGeometry(0, 0, x(20), y(100) - 30)
    tab.createTeacherButton.setGeometry(1, y(100) - 30 + 1, x(20) - 2, 30 - 2)

    if tab.teacher is not None:
        tab.teachersScroll.setGeometry(x(20), y(50), x(80) + 1, y(50))
        tab.teachersScroll.setWidgetResizable(False)

        count = len(window.settings["teachers"][tab.teacher]["subjects"]) + 1

        height = max(y(50), count * y(20))
        width = x(80) - tab.teachersScroll.verticalScrollBar().sizeHint().width() - 6

        tab.teachersScrollContainer.setGeometry(0, 0, width, height)

        for i in range(count):
            tab.teachersSubjects[f"object_{i}"].setGeometry(0, i * y(20), width, y(20))

            tab.teachersSubjects[f"object_{i}"].subject.setGeometry(4, 4, x(30), 30)

            if hasattr(tab.teachersSubjects[f"object_{i}"], "grid"):
                tab.teachersSubjects[f"object_{i}"].grid.setGeometry(3, 35, x(80) - 26, y(20) - 38)

        tab.teacherFree.setGeometry(x(20) + 1, 0, x(80) - 1, y(50) - 1)

    if "teachers_scroll" in window.objects:
        tab.teachersScroll.verticalScrollBar().setValue(window.objects.pop("teachers_scroll", None))

    tab = window.objects["tabs"].widget(TAB_AI)

    tab.chatTextEdit.setGeometry(x(0), 0, x(100), y(100) - 60)
    tab.messageLineEdit.setGeometry(x(0), y(100) - 60 + 1, x(80), 28)
    tab.sendPushButton.setGeometry(x(80) + 2, y(100) - 60 + 1, x(20) - 2, 28)
    tab.loadPushButton.setGeometry(x(0) + 1, y(100) - 30 + 1, x(80) - 1, 28)
    tab.removePushButton.setGeometry(x(80) + 2, y(100) - 30 + 1, x(20) - 2, 28)

    tab = window.objects["tabs"].widget(TAB_CONSTANTS)

    tab = window.objects["tabs"].widget(TAB_RUN)

    tab.settingsRama.setGeometry(0, 0, x(33), y(100))
    tab.stdTextEdit.setGeometry(x(33), 0, x(100 - 33), y(100) - 30)
    tab.runPushButton.setGeometry(x(33) + 1, y(100) - 30 + 1, x(30) - 2, 28)
    tab.timeLabel.setGeometry(x(63) + 10, y(100) - 30, x(50), 30)

    idx = 0

    for name, value in tab.weights.items():
        tab.objects[f"label_{name}"].setGeometry(10, 10 + 40 * idx, x(15), 30)
        tab.objects[f"lineedit_{name}"].setGeometry(20 + x(15), 10 + 40 * idx, x(33) - x(15) - 30, 30)

        idx += 1

    tab = window.objects["tabs"].widget(TAB_VIEW)

    tab.modeComboBox.setGeometry(1, 1, x(20) - 2, 30 - 4)

    tab.info.setGeometry(x(20) + 1, 0, x(80) - 1, y(100))
    tab.items.setGeometry(0, 30 - 2, x(20), y(100) - 30 + 2)
    tab.tabs.setGeometry(x(20) + 1, 0, x(80) - 1, y(100) - 1)

    tab = window.objects["tabs"].widget(TAB_EXPORT)
