from PyQt5.QtWidgets import QTabWidget, QWidget, QPushButton

from src.modules.menues.tabs import *
from src.variables import *


TABS = [
    (TabSettings, "menu.main.tab.settings", False),
    (TabClasses, "menu.main.tab.classes", False),
    (TabClassrooms, "menu.main.tab.classrooms", False),
    (TabTeachers, "menu.main.tab.teachers", False),
    (QWidget, "/", True),
    (TabAI, "menu.main.tab.AI", False),
    (QWidget, "->", True), 
    (TabConstants, "menu.main.tab.constants", False),
    (TabGroups, "menu.main.tab.groups", False),
    (QWidget, "->", True),  
    (TabRun, "menu.main.tab.run", False),
    (QWidget, "->", True),  
    (TabView, "menu.main.tab.view", False),
    (QWidget, "->", True),  
    (TabExport, "menu.main.tab.export", False)
]


class Import:
    @classmethod
    def init(cls, window, ignore: list = None, reverse: bool = False):
        init(window, ignore, reverse)

    @classmethod
    def resize(cls, window):
        resize(window)


def init(window, ignore: list = None, reverse: bool = False) -> None:
    if ignore is None:
        ignore = []

    tabs = [TabSettings, TabClasses, TabClassrooms, TabTeachers, TabGroups, TabAI, TabConstants, TabRun, TabView, TabExport]
    
    for tab in tabs:
        tab.resize = Import.resize
        tab.init = Import.init

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

        tabs.blockSignals(True)

        for cls, label, sep in TABS:
            widget = cls(window) if not sep else QWidget(window)
            idx = tabs.addTab(widget, translate(label) if not sep else label)

            if sep:
                tabs.setTabEnabled(idx, False)

        tabs.tabBarClicked.connect(lambda idx: update(window, idx))

        tabs.blockSignals(False)
        resize(window)

        return

    current_index = tabs.currentIndex()
    
    tabs.blockSignals(True)
    tabs.setUpdatesEnabled(False)

    try:
        for i, (cls, label, sep) in enumerate(TABS):
            if sep:
                continue

            if not ((i not in ignore) if not reverse else (i in ignore)):
                continue

            old = tabs.widget(i)
            new = cls(window)

            tabs.removeTab(i)
            tabs.insertTab(i, new, translate(label))

            if old is not None:
                old.deleteLater()

        if 0 <= current_index < tabs.count():
            tabs.setCurrentIndex(current_index)

    finally:
        tabs.setUpdatesEnabled(True)
        tabs.blockSignals(False)

    resize(window)


def update(window, idx):
    if idx == TAB_TEACHERS:
        init(window, ignore=[TAB_TEACHERS], reverse=True)

    if idx == TAB_CONSTANTS:
        init(window, ignore=[TAB_CONSTANTS], reverse=True)


def resize(window) -> None:
    tabs = window.objects.get("tabs")

    if tabs is None or tabs.count() == 0:
        return

    tab = None

    def x(prec):
        return int(tab.width() * prec / 100) if tab else 0

    def y(prec):
        return int(tab.height() * prec / 100) if tab else 0

    tab = tabs.widget(0)

    if tab and isinstance(tab, TabSettings):
        try:
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
            tab.settingsShiftCrossingLabel.setGeometry(10, 210, x(15), 30)
            tab.settingsShiftCrossingEdit.setGeometry(20 + x(15), 210, x(33) - x(15) - 30, 30)
            tab.maxLessonForTeacherLabel.setGeometry(10, 250, x(15), 30)
            tab.maxLessonForTeacherEdit.setGeometry(20 + x(15), 250, x(33) - x(15) - 30, 30)

            tab.subjectsTable.setGeometry(x(33), 0, x(34), y(100))
            tab.classesRama.setGeometry(x(67), 0, x(33), y(100))

            for number in range(window.settings.get("classes_count", 0)):
                if f"label_{number}" in tab.classesObjects:
                    tab.classesObjects[f"label_{number}"].setGeometry(x(67) + 10, 10 + 50 * number, 50, 30)
                    tab.classesObjects[f"scroll_{number}"].setGeometry(x(67) + 50, 10 + 50 * number, x(33) - 170, 30)
                    tab.classesObjects[f"info_{number}"].setGeometry(x(100) - 110, 10 + 50 * number, 60, 30)
                    tab.classesObjects[f"shift_{number}"].setGeometry(x(100) - 40, 10 + 50 * number, 30, 30)

            tab.subjectsTable.setColumnWidth(0, int(tab.subjectsTable.viewport().width() * 2 / 3))
            tab.subjectsTable.setColumnWidth(1, int(tab.subjectsTable.viewport().width() * 1 / 3 + tab.subjectsTable.viewport().width() % 3))

        except (AttributeError, KeyError):
            pass

    tab = tabs.widget(1)

    if tab and isinstance(tab, TabClasses):
        try:
            tab.classesTable.setGeometry(0, 0, x(100), y(100))

        except AttributeError:
            pass

    tab = tabs.widget(2)

    if tab and isinstance(tab, TabClassrooms):
        try:
            tab.enablePushButton.setGeometry(1, 1, x(100) - 2, 28)
            tab.roomGroupsListWidget.setGeometry(0, 30, x(20), y(100) - 60)
            tab.createGroupPushButton.setGeometry(1, y(100) - 30 + 1, x(20) - 2, 28)
            tab.addRoomPushButton.setGeometry(x(20) + 1, y(100) - 30 + 1, x(80) - 1, 28)
            tab.chooseRoomPushButton.setGeometry(x(20) + 1, y(100) - 60 + 1, x(80) - 1, 28)
            tab.roomsListWidget.setGeometry(x(20), 30, x(80) + 1, y(100) - 90)

        except AttributeError:
            pass

    tab = tabs.widget(3)

    if tab and isinstance(tab, TabTeachers):
        try:
            tab.teachersList.setGeometry(0, 0, x(20), y(100) - 30)
            tab.createTeacherButton.setGeometry(1, y(100) - 30 + 1, x(20) - 2, 30 - 2)

            if getattr(tab, "teacher", None) is not None:
                tab.teachersScroll.setGeometry(x(20), y(50), x(80) + 1, y(50))
                tab.teachersScroll.setWidgetResizable(False)

                count = len(window.settings["teachers"][tab.teacher]["subjects"]) + 1
                height = max(y(50), count * y(20))

                width = x(80) - tab.teachersScroll.verticalScrollBar().sizeHint().width() - 6

                tab.teachersScrollContainer.setGeometry(0, 0, width, height)

                for i in range(count):
                    if f"object_{i}" in tab.teachersSubjects:
                        tab.teachersSubjects[f"object_{i}"].setGeometry(0, i * y(20), width, y(20))
                        tab.teachersSubjects[f"object_{i}"].subject.setGeometry(4, 4, x(30), 30)
                        tab.teachersSubjects[f"object_{i}"].classrooms.setGeometry(5 + x(30), 3, width - x(30) - 8, 30 + 2)

                        if hasattr(tab.teachersSubjects[f"object_{i}"], "grid"):
                            tab.teachersSubjects[f"object_{i}"].grid.setGeometry(3, 35, x(80) - 26, y(20) - 38)

                tab.teacherFree.setGeometry(x(20) + 1, 0, x(80) - 1, y(50) - 1)

            if "teachers_scroll" in window.objects:
                tab.teachersScroll.verticalScrollBar().setValue(window.objects.pop("teachers_scroll", None))

        except (AttributeError, KeyError):
            pass

    tab = tabs.widget(8)

    if tab and isinstance(tab, TabGroups):
        try:
            tab.classSelector.setGeometry(1, 1, 141, 28)
            tab.addGroupButton.setGeometry(144, 1, x(20), 28)
            tab.groupsTable.setGeometry(0, 30, x(100), y(100) - 30)

        except AttributeError:
            pass

    tab = tabs.widget(5)

    if tab and isinstance(tab, TabAI):
        try:
            tab.chatTextEdit.setGeometry(0, 0, x(100), y(100) - 60)
            tab.messageLineEdit.setGeometry(x(0), y(100) - 60 + 1, x(80), 28)
            tab.sendPushButton.setGeometry(x(80) + 2, y(100) - 60 + 1, x(20) - 2, 28)
            tab.loadPushButton.setGeometry(x(0) + 1, y(100) - 30 + 1, x(80) - 1, 28)
            tab.removePushButton.setGeometry(x(80) + 2, y(100) - 30 + 1, x(20) - 2, 28)

        except AttributeError:
            pass

    tab = tabs.widget(7)

    if tab and isinstance(tab, TabConstants):
        try:
            tab.classesList.setGeometry(0, 0, x(20), y(100))
            tab.table.setGeometry(x(20) + 1, 0, x(80), y(100))

        except AttributeError:
            pass

    tab = tabs.widget(10)

    if tab and isinstance(tab, TabRun):
        try:
            tab.settingsRama.setGeometry(0, 0, x(33), y(100))
            tab.stdTextEdit.setGeometry(x(33), 0, x(100 - 33), y(100) - 30)
            tab.runPushButton.setGeometry(x(33) + 1, y(100) - 30 + 1, x(30) - 2, 28)
            tab.timeLabel.setGeometry(x(63) + 10, y(100) - 30, x(50), 30)

            idx = 0

            for name, value in tab.weights.items():
                tab.objects[f"label_{name}"].setGeometry(10, 10 + 40 * idx, x(15), 30)
                tab.objects[f"lineedit_{name}"].setGeometry(20 + x(15), 10 + 40 * idx, x(33) - x(15) - 30, 30)

                idx += 1

        except AttributeError:
            pass

    tab = tabs.widget(12)

    if tab and isinstance(tab, TabView):
        try:
            tab.modeComboBox.setGeometry(1, 1, x(20) - 2, 30 - 4)
            tab.info.setGeometry(x(20) + 1, 0, x(80) - 1, y(100))
            tab.items.setGeometry(0, 30 - 2, x(20), y(100) - 30 + 2)
            tab.tabs.setGeometry(x(20) + 1, 0, x(80) - 1, y(100) - 1)

        except AttributeError:
            pass

    tab = tabs.widget(14)

    if tab and isinstance(tab, TabExport):
        try:
            tab.timesRama.setGeometry(0, 0, x(33), y(100))
            tab.exportByClassPushButton.setGeometry(x(33) + 1, 1, x(100 - 33) - 1, 30 - 2)
            tab.exportByTeacherPushButton.setGeometry(x(33) + 1, 31, x(100 - 33) - 1, 30 - 2)

            lessons = window.settings.get("max_lesson_count_per_day", 0)
            shifts = window.settings.get("number_of_shifts", 0)

            idx = 0

            for shift in range(shifts):
                for lesson in range(lessons):
                    tab.objects[f"time_{shift}-{lesson}_label"].setGeometry(10, 10 + 40 * idx, x(15), 30)
                    tab.objects[f"time_{shift}-{lesson}_lineedit"].setGeometry(20 + x(15), 10 + 40 * idx, x(33) - x(15) - 30, 30)

                    idx += 1

        except (AttributeError, KeyError):
            pass
