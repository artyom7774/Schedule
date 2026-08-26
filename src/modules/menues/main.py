from PyQt5.QtWidgets import QTabWidget, QWidget, QTableWidget, QPushButton, QHeaderView, QLabel, QLineEdit, QTableWidgetItem

from src.variables import *

import typing
import json


class Tab1(QWidget):
    def __init__(self, window):
        super().__init__()

        self.settingsRama = QTableWidget(0, 0, parent=self)
        self.settingsRama.horizontalHeader().setVisible(False)
        self.settingsRama.verticalHeader().setVisible(False)
        self.settingsRama.show()

        self.settingsDaysLabel = QLabel(translate("menu.main.tab.settings.working_days_per_week"), parent=self)
        self.settingsDaysLabel.setFont(FONT)
        self.settingsDaysLabel.show()

        self.settingsDaysEdit = QLineEdit(parent=self)
        self.settingsDaysEdit.setText(str(window.settings["working_days_per_week"]))
        self.settingsDaysEdit.editingFinished.connect(lambda: save(window, "working_days_per_week", self.settingsDaysEdit))
        self.settingsDaysEdit.setFont(FONT)
        self.settingsDaysEdit.show()

        self.settingsLessonsLabel = QLabel(translate("menu.main.tab.settings.max_lesson_count_per_day"), parent=self)
        self.settingsLessonsLabel.setFont(FONT)
        self.settingsLessonsLabel.show()

        self.settingsLessonsEdit = QLineEdit(parent=self)
        self.settingsLessonsEdit.setText(str(window.settings["max_lesson_count_per_day"]))
        self.settingsLessonsEdit.editingFinished.connect(lambda: save(window, "max_lesson_count_per_day", self.settingsLessonsEdit))
        self.settingsLessonsEdit.setFont(FONT)
        self.settingsLessonsEdit.show()

        self.subjectsTable = QTableWidget(len(window.settings["subjects"]) + 1, 2, parent=self)

        idx = 0

        for key, value in window.settings["subjects"].items():
            self.subjectsTable.setItem(idx, 0, QTableWidgetItem(str(key)))
            self.subjectsTable.setItem(idx, 1, QTableWidgetItem(str(value)))

            idx += 1

        self.subjectsTable.cellChanged.connect(lambda row, col: save(window, "subjects", self.subjectsTable, [row, col]))
        self.subjectsTable.setHorizontalHeaderLabels([translate("menu.main.tab.settings.subject"), translate("menu.main.tab.settings.hard")])
        self.subjectsTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.subjectsTable.verticalHeader().setVisible(False)
        self.subjectsTable.setFont(FONT)
        self.subjectsTable.show()


class Tab2(QWidget):
    def __init__(self, window):
        super().__init__()


class Tab3(QWidget):
    def __init__(self, window):
        super().__init__()


def save(window, parameter, object, another: typing.Any = None):
    if parameter in ("working_days_per_week", "max_lesson_count_per_day"):
        text: str = object.text()

        try:
            int(text)

        except BaseException:
            object.setText(str(window.settings[parameter]))

            return

        window.settings[parameter] = int(text)

    if parameter in ("subjects", ):
        print(parameter, another)

    with open(f"{PATH_TO_FOLDER}/projects/{window.project}/settings.json", "w", encoding="UTF-8") as file:
        json.dump(window.settings, file, indent=4, ensure_ascii=False)


def init(window) -> None:
    window.objects["empty"] = QPushButton(parent=window)
    window.objects["empty"].setGeometry(0, 0, 0, 0)

    window.objects["tabs"] = QTabWidget(parent=window)
    window.setCentralWidget(window.objects["tabs"])

    window.objects["tabs"].currentChanged.connect(lambda: resize(window))

    window.objects["tabs"].tabBar().setFont(FONT)
    window.objects["tabs"].setStyleSheet("""QTabBar::tab {padding-left: 10px; padding-right: 10px}""")

    window.objects["tabs"].addTab(Tab1(window), translate("menu.main.tab.settings"))
    window.objects["tabs"].addTab(Tab2(window), translate("menu.main.tab.teachers"))
    window.objects["tabs"].addTab(Tab3(window), translate("menu.main.tab.lessons"))

    resize(window)


def resize(window) -> None:
    if "tabs" not in window.objects:
        return

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

    tab.subjectsTable.setGeometry(x(33), 0, x(34), y(100))

    tab = window.objects["tabs"].widget(1)
