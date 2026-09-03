from PyQt5.QtWidgets import QTabWidget, QWidget, QPushButton

from src.modules.menues.tabs import *

from src.variables import *


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

    tabs = [TabSettings, TabClasses, TabTeachers, TabGroups, TabAI, TabConstants, TabRun, TabView, TabExport]

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

    elements = [
        (TabSettings, "menu.main.tab.settings"),
        (TabClasses, "menu.main.tab.classes"),
        (TabTeachers, "menu.main.tab.teachers"),
        (QWidget, "/"),
        (TabAI, "menu.main.tab.AI"),
        (QWidget, "->"),
        (TabConstants, "menu.main.tab.constants"),
        (TabGroups, "menu.main.tab.groups"),
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
    tab.settingsShiftCrossingLabel.setGeometry(10, 210, x(15), 30)
    tab.settingsShiftCrossingEdit.setGeometry(20 + x(15), 210, x(33) - x(15) - 30, 30)

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

    tab = window.objects["tabs"].widget(TAB_GROUPS)

    tab.groupsTable.setGeometry(0, 0, x(100), y(100))

    tab = window.objects["tabs"].widget(TAB_AI)

    tab.chatTextEdit.setGeometry(0, 0, x(100), y(100) - 60)
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
