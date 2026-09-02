from PyQt5.QtWidgets import QScrollArea, QMenu, QAction, QVBoxLayout, QTabWidget, QWidget, QComboBox, QListWidget, QTableWidget, QPushButton, QHeaderView, QTableWidgetItem
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

from src.modules.widgets import ButtonGridWidget

from src.modules import dialogs

from src.variables import *

import json


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

        TabTeachers.init(self.window, ignore=[TAB_TEACHERS], reverse=True)


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
        remove = item.text()

        self.window.settings["teachers"].pop(remove)

        if self.window.objects.get("teachers_selected") == remove:
            self.window.objects.pop("teachers_selected", None)
            self.window.objects.pop("shift_selected", None)

        self.window.objects.pop("teachers_scroll", None)

        with open(f"{PATH_TO_FOLDER}/projects/{self.window.project}/settings.json", "w", encoding="utf-8") as file:
            json.dump(self.window.settings, file, ensure_ascii=False)

        TabTeachers.init(self.window, ignore=[TAB_TEACHERS], reverse=True)

    def teacherFreeTabBarClicked(self, idx):
        self.window.objects["shift_selected"] = idx

        TabTeachers.init(self.window, ignore=[TAB_TEACHERS], reverse=True)

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

        TabTeachers.init(self.window, ignore=[TAB_TEACHERS], reverse=True)

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

        TabTeachers.init(self.window, ignore=[TAB_TEACHERS], reverse=True)

    def teachersListItemClicked(self):
        new = self.teachersList.currentItem().text() if self.teachersList.currentItem() is not None else None

        if new == self.teacher:
            return

        self.teacher = new
        self.window.objects["teachers_selected"] = self.teacher

        TabTeachers.init(self.window, ignore=[TAB_TEACHERS], reverse=True)

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

        TabTeachers.init(self.window, ignore=[TAB_TEACHERS], reverse=True)
