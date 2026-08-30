from PyQt5.QtWidgets import QApplication, QScrollArea, QVBoxLayout, QTextEdit, QTabWidget, QSlider, QWidget, QComboBox, QListWidget, QTableWidget, QPushButton, QHeaderView, QLabel, QLineEdit, QTableWidgetItem
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

from src.modules.widgets import MultiTableWidget, ButtonGridWidget, ChatAITextEdit

from src.modules import dialogs

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

        self.subjectsTable = QTableWidget(window.settings["subjects_count"], 2, parent=self)

        while len(window.settings["subjects"]) > window.settings["subjects_count"]:
            window.settings["subjects"].pop(-1)

        while len(window.settings["subjects"]) < window.settings["subjects_count"]:
            window.settings["subjects"].append(["", -1])

        idx = 0

        for element in window.settings["subjects"]:
            self.subjectsTable.setItem(idx, 0, QTableWidgetItem(str(element[0])))

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

        flag = False

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
            with open(f"{PATH_TO_FOLDER}/projects/{self.window.project}/settings.json", "w", encoding="UTF-8") as file:
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

        if parameter in ("working_days_per_week", "max_lesson_count_per_day", "classes_count", "subjects_count", "number_of_shifts"):
            text = object.text()

            try:
                int(text)

            except BaseException:
                object.setText(str(window.settings[parameter]))

                return

            window.settings[parameter] = int(text)

        if parameter in ("subjects", ):
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

        if parameter in ("classes/count", ):
            window.settings["classes"]["count"][another[0]] = another[1]

            if window.objects["tabs"].widget(0):
                window.objects["tabs"].widget(0).initClassCountObject(another[0], False)

            resize(window)

        if parameter in ("classes/shift", ):
            window.settings["classes"]["shift"][another] = (window.settings["classes"]["shift"][another] + 1) % window.settings["number_of_shifts"]

        with open(f"{PATH_TO_FOLDER}/projects/{window.project}/settings.json", "w", encoding="UTF-8") as file:
            json.dump(window.settings, file, indent=4, ensure_ascii=False)

        init(window, ignore)


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
        self.classesTable.setHorizontalHeaderLabels([(element[0][:3] + "-" + element[0][-2:] if len(element[0]) > 8 else element[0]) for element in self.window.settings["subjects"]])
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

        with open(f"{PATH_TO_FOLDER}/projects/{self.window.project}/settings.json", "w", encoding="UTF-8") as file:
            json.dump(self.window.settings, file, indent=4, ensure_ascii=False)

        init(self.window, [1])


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

        with open(f"{PATH_TO_FOLDER}/projects/{self.window.project}/settings.json", "w", encoding="UTF-8") as file:
            json.dump(self.window.settings, file, indent=4, ensure_ascii=False)

        init(self.window)


class TabTeachers(QWidget):
    def __init__(self, window):
        super().__init__()

        self.window = window

        self.classes = []

        for i, cnt in enumerate(self.window.settings["classes"]["count"]):
            for number in range(cnt):
                self.classes.append(f"{i + 1} {CLASSES_ALPHABET[number + 1]}")

        self.teachersList = QListWidget(parent=self)
        self.teachersList.itemClicked.connect(lambda: self.teachersListItemClicked())
        self.teachersList.addItems([teacher for teacher in window.settings["teachers"].keys()])

        teachers = list(window.settings["teachers"].keys())
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
            with open(f"{PATH_TO_FOLDER}/projects/{self.window.project}/settings.json", "w", encoding="UTF-8") as file:
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

    def teacherFreeTabBarClicked(self, idx):
        self.window.objects["shift_selected"] = idx

        init(self.window)

    def teacherFreeTableCellClicked(self, row, col):
        shift = self.teacherFree.currentIndex()
        pos = [col, row]

        if pos in self.window.settings["teachers"][self.teacher]["free"][shift]:
            self.window.settings["teachers"][self.teacher]["free"][shift].remove(pos)

        else:
            self.window.settings["teachers"][self.teacher]["free"][shift].append(pos)

        self.window.objects["shift_selected"] = shift

        with open(f"{PATH_TO_FOLDER}/projects/{self.window.project}/settings.json", "w", encoding="UTF-8") as file:
            json.dump(self.window.settings, file, indent=4, ensure_ascii=False)

        init(self.window)

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

        with open(f"{PATH_TO_FOLDER}/projects/{self.window.project}/settings.json", "w", encoding="UTF-8") as file:
            json.dump(self.window.settings, file, indent=4, ensure_ascii=False)

        init(self.window)

    def teachersListItemClicked(self):
        new = self.teachersList.currentItem().text() if self.teachersList.currentItem() is not None else None

        if new == self.teacher:
            return

        self.teacher = new
        self.window.objects["teachers_selected"] = self.teacher

        init(self.window)

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

        with open(f"{PATH_TO_FOLDER}/projects/{self.window.project}/settings.json", "w", encoding="UTF-8") as file:
            json.dump(self.window.settings, file, indent=4, ensure_ascii=False)

        init(self.window)


class TabAILoad(QWidget):
    def __init__(self, window):
        super().__init__()

        self.window = window

        self.chat = ChatAITextEdit(self.window, parent=self)
        self.chat.setReadOnly(True)
        self.chat.setFont(FONT)
        self.chat.show()

        self.message = QLineEdit(parent=self)
        self.message.returnPressed.connect(lambda: self.messageLineEditReturnPressed())
        self.message.setPlaceholderText(translate("menu.main.tab.AI.write_your_request_and_press_enter"))
        self.message.setFont(FONT)
        self.message.show()

    def messageLineEditReturnPressed(self):
        print("->", self.message.text())

        self.chat.send(self.message.text())

        self.message.setText("")


class Tab3(QWidget):
    def __init__(self, window):
        super().__init__()


def init(window, ignore: list = None) -> None:
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
        (TabAILoad, "menu.main.tab.AI"),
        (QWidget, "->"),
        (Tab3, "menu.main.tab.lessons")
    ]

    index = tabs.currentIndex()

    tabs.blockSignals(True)

    for i, (cls, label) in enumerate(elements):
        if i in ignore:
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

    QApplication.processEvents()

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

    tab = window.objects["tabs"].widget(0)

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

    tab = window.objects["tabs"].widget(1)

    tab.classesTable.setGeometry(0, 0, x(100), y(100))

    tab = window.objects["tabs"].widget(2)

    tab.teachersList.setGeometry(0, 0, x(20), y(100) - 30)
    tab.createTeacherButton.setGeometry(0, y(100) - 30, x(20), 30)

    if tab.teacher is not None:
        tab.teachersScroll.setGeometry(x(20), y(50), x(80) + 1, y(50) + 2)
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

    tab = window.objects["tabs"].widget(4)

    tab.chat.setGeometry(x(20), 0, x(60), y(100) - 30)
    tab.message.setGeometry(x(20), y(100) - 30 + 1, x(60), 28)
