from PySide6.QtWidgets import QWidget, QComboBox, QListWidget, QListWidgetItem, QTabWidget, QTableWidget, QTableWidgetItem, QHeaderView, QPushButton, QLabel, QTextEdit, QMenu, QMessageBox, QAbstractItemView
from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtGui import QColor, QCursor, QBrush, QTextCursor, QAction

from src.modules.functions import editor

from src.variables import *

import shutil
import json
import copy
import os

HISTORY = 100


class EditTable(QTableWidget):
    leftClicked = Signal(int, int)
    rightClicked = Signal(int, int)

    def __init__(self, rows: int, columns: int, parent=None):
        super().__init__(rows, columns, parent)

        self.pressedCell = None
        self.pressedModifiers = Qt.NoModifier

    def cellAt(self, event):
        index = self.indexAt(event.pos())

        return (index.column(), index.row()) if index.isValid() else None

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            cell = self.cellAt(event)

            if cell is not None:
                self.rightClicked.emit(*cell)

            event.accept()

            return

        if event.button() == Qt.LeftButton:
            self.pressedCell = self.cellAt(event)
            self.pressedModifiers = event.modifiers()

        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)

        if event.button() != Qt.LeftButton:
            return

        cell = self.cellAt(event)
        pressed = self.pressedCell

        self.pressedCell = None

        multi = bool(self.pressedModifiers & (Qt.ControlModifier | Qt.ShiftModifier))

        if cell is not None and cell == pressed and not multi:
            QTimer.singleShot(0, lambda c=cell: self.leftClicked.emit(*c))


class TabEdit(QWidget):
    def __init__(self, window):
        super().__init__()

        self.window = window

        settings = self.window.settings

        if teachersNormalize(settings):
            with open(f"{PATH_TO_FOLDER}/projects/{self.window.project}/settings.json", "w", encoding="utf-8") as file:
                json.dump(settings, file, indent=4, ensure_ascii=False)

        self.days = settings["working_days_per_week"]
        self.lessons = settings["max_lesson_count_per_day"]
        self.shiftsCount = settings["number_of_shifts"]

        self.classes = editor.classNames(settings)
        self.teachers = editor.teacherNames(settings)
        self.shifts = {cls: shiftGetClass(settings, cls) for cls in self.classes}
        self.classesByShift = {shift: [cls for cls in self.classes if self.shifts.get(cls, 0) == shift] for shift in range(self.shiftsCount)}

        self.classroomsEnabled = bool(settings.get("classrooms", {}).get("enable", 0))

        self.redBrush = QBrush(QColor(f"#{COLORS['red']}"))
        self.yellowBrush = QBrush(QColor(f"#{COLORS['yellow']}"))
        self.defaultBrush = QBrush()

        self.dirtyShifts = set()

        self.answer = self.solve()

        self.window.objects.setdefault("history", [])

        self.conflicts = {}
        self.pools = {}
        self.teachersPools = {}

        mode = self.window.objects.get("edit_mode", 0)

        if not (0 <= mode <= 1):
            mode = 0

        self.mode = mode
        self.selectedKey = "edit_selected" if mode == 0 else "edit_teacher_selected"

        self.modeComboBox = QComboBox(parent=self)
        self.modeComboBox.addItems([translate("menu.main.tab.edit.classes"), translate("menu.main.tab.edit.teachers")])
        self.modeComboBox.setFont(FONT)

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

        select = self.window.objects.get(self.selectedKey)

        if select in items:
            self.items.setCurrentRow(items.index(select))

        elif items:
            self.items.setCurrentRow(0)

        self.items.show()

        self.selected = self.items.currentItem().text() if self.items.currentItem() is not None else None
        self.window.objects[self.selectedKey] = self.selected

        self.info = QLabel(parent=self)
        self.info.setAlignment(Qt.AlignCenter)
        self.info.setWordWrap(True)
        self.info.setFont(FONT)
        self.info.setText(translate("menu.main.tab.edit.schedule_not_created"))

        self.tabs = QTabWidget(parent=self)
        self.tabs.tabBar().setFont(FONT)

        self.tables = {}

        for shift in range(self.shiftsCount):
            self.tables[shift] = self.createTable()

            self.tabs.addTab(self.tables[shift], shiftName(shift))

        self.tabs.show()

        self.selectTabs()

        self.tabs.currentChanged.connect(lambda idx: self.tabsCurrentChanged(idx))

        self.poolList = QListWidget(parent=self)
        self.poolList.setFont(FONT)
        self.poolList.itemDoubleClicked.connect(lambda item: self.poolListItemDoubleClicked(item))
        self.poolList.show()

        self.logTextEdit = QTextEdit(parent=self)
        self.logTextEdit.setReadOnly(True)
        self.logTextEdit.setFont(ANOTHER_FONT)
        self.logTextEdit.setPlainText(self.window.objects.get("edit_log", ""))
        self.logTextEdit.show()

        self.statsLabel = QLabel(parent=self)
        self.statsLabel.setAlignment(Qt.AlignCenter)
        self.statsLabel.setFont(FONT)
        self.statsLabel.setText(self.statsText(0, 0))
        self.statsLabel.show()

        self.deletePushButton = QPushButton(parent=self)
        self.deletePushButton.clicked.connect(lambda: self.deletePushButtonClicked())
        self.deletePushButton.setText(translate("menu.main.tab.edit.delete"))
        self.deletePushButton.setFont(FONT)
        self.deletePushButton.show()

        self.addPushButton = QPushButton(parent=self)
        self.addPushButton.clicked.connect(lambda: self.addPushButtonClicked())
        self.addPushButton.setText(translate("menu.main.tab.edit.add"))
        self.addPushButton.setFont(FONT)
        self.addPushButton.show()

        self.undoPushButton = QPushButton(parent=self)
        self.undoPushButton.clicked.connect(lambda: self.undoPushButtonClicked())
        self.undoPushButton.setText(translate("menu.main.tab.edit.undo"))
        self.undoPushButton.setFont(FONT)
        self.undoPushButton.show()

        self.revertPushButton = QPushButton(parent=self)
        self.revertPushButton.clicked.connect(lambda: self.revertPushButtonClicked())
        self.revertPushButton.setText(translate("menu.main.tab.edit.revert"))
        self.revertPushButton.setFont(FONT)
        self.revertPushButton.show()

        if self.answer is None or self.selected is None:
            self.tabs.hide()

            self.poolList.hide()
            self.logTextEdit.hide()
            self.statsLabel.hide()

            for button in self.buttons():
                button.hide()

            self.info.setText(translate("menu.main.tab.edit.schedule_not_created") if self.answer is None else "")
            self.info.show()

            return

        self.info.hide()

        self.refresh()

    def buttons(self) -> list:
        return [self.deletePushButton, self.addPushButton, self.undoPushButton, self.revertPushButton]

    def path(self, name: str) -> str:
        return f"{PATH_TO_FOLDER}/projects/{self.window.project}/{name}"

    def solve(self):
        if not os.path.exists(self.path("answer.json")):
            return None

        try:
            with open(self.path("answer.json"), "r", encoding="utf-8") as file:
                answer = json.load(file)

        except BaseException:
            return None

        editor.normalize(self.window.settings, answer)

        return answer

    def saveAnswer(self) -> None:
        with open(self.path("answer.json"), "w", encoding="utf-8") as file:
            json.dump(self.answer, file, indent=4, ensure_ascii=False)

    def createTable(self) -> QTableWidget:
        table = EditTable(self.lessons, self.days, parent=self)

        table.leftClicked.connect(lambda day, lesson: self.cellLeftClicked(day, lesson))
        table.rightClicked.connect(lambda day, lesson: self.cellRightClicked(day, lesson))

        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        table.setSelectionMode(QAbstractItemView.ExtendedSelection)
        table.setSelectionBehavior(QAbstractItemView.SelectItems)
        table.setWordWrap(True)
        table.setTextElideMode(Qt.ElideNone)

        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

        table.setVerticalHeaderLabels([f"{i + 1}" for i in range(self.lessons)])
        table.setHorizontalHeaderLabels([f"{translate('day.' + str(i))}" for i in range(self.days)])

        table.setFont(FONT)

        for day in range(self.days):
            for lesson in range(self.lessons):
                item = QTableWidgetItem()
                item.setTextAlignment(Qt.AlignCenter)

                table.setItem(lesson, day, item)

        table.show()

        return table

    def currentShift(self) -> int:
        return max(self.tabs.currentIndex(), 0)

    def currentTable(self) -> QTableWidget:
        return self.tables[self.currentShift()]

    def shiftClasses(self) -> list:
        return self.classesByShift.get(self.currentShift(), [])

    def selectTabs(self) -> None:
        self.tabs.blockSignals(True)

        if self.mode == 0:
            shift = self.shifts.get(self.selected, 0)

            for index in range(self.shiftsCount):
                self.tabs.setTabEnabled(index, index == shift)

        else:
            shift = self.window.objects.get("edit_shift_selected", 0)

            if not (0 <= shift < self.shiftsCount):
                shift = 0

            for index in range(self.shiftsCount):
                self.tabs.setTabEnabled(index, True)

        self.tabs.setCurrentIndex(shift)

        self.tabs.blockSignals(False)

    def reason(self, item: tuple) -> str:
        return f"{translate('menu.main.tab.edit.conflict.' + item[0])}: {item[1]}"

    def relevant(self, problem: tuple) -> bool:
        return problem[0] not in ("unavailable", "busy") or problem[1] == self.selected

    def statsText(self, windows: int, conflicts: int, teacher: str = None) -> str:
        if not teacher:
            return f"{translate('menu.main.tab.edit.windows')}: {windows}  /  {translate('menu.main.tab.edit.conflicts')}: {conflicts}"

        return f"{translate('menu.main.tab.edit.windows')}: {self.calculateWindow(teacher)} ({windows})  /  {translate('menu.main.tab.edit.conflicts')}: {conflicts}"

    def calculateWindow(self, teacher) -> int:
        days = self.days
        lessons = self.lessons
        shiftsCount = self.shiftsCount
        step = lessons - self.window.settings.get("shift_crossing", 0)

        busy = {}

        for cls in self.classes:
            shift = self.shifts.get(cls, 0)

            if not (0 <= shift < shiftsCount):
                continue

            offset = shift * step
            data = self.answer.get(cls, [])

            for day in range(min(days, len(data))):
                dayData = data[day]

                for lesson in range(min(lessons, len(dayData))):
                    pos = offset + lesson

                    for _, teachers, _ in editor.entries(dayData[lesson]):
                        for var in teachers:
                            busy.setdefault(var, {}).setdefault(day, set()).add(pos)

        teachersSettings = self.window.settings.get("teachers", {})

        teacherBusy = busy.get(teacher, {})
        reserve = teachersSettings.get(teacher, {}).get("reserve", [])

        reserveByDay = {}

        for shift in range(min(shiftsCount, len(reserve))):
            offset = shift * step

            for item in reserve[shift]:
                if isinstance(item, (list, tuple)) and len(item) == 2:
                    day, lesson = item

                    if 0 <= day < days and 0 <= lesson < lessons:
                        reserveByDay.setdefault(day, set()).add(offset + lesson)

        total = 0

        for day in range(days):
            if teacherBusy.get(day) and reserveByDay.get(day):
                elements = teacherBusy.get(day) | reserveByDay.get(day)

            elif teacherBusy.get(day):
                elements = teacherBusy.get(day)

            elif reserveByDay.get(day):
                elements = reserveByDay.get(day)

            else:
                continue

            if len(elements) >= 2:
                total += (max(elements) - min(elements) + 1) - len(elements)

        return total

    def calculateWindows(self) -> int:
        total = 0

        for teacher in self.teachers:
            total += self.calculateWindow(teacher)

        return total

    def calculate(self) -> None:
        settings = self.window.settings

        self.conflicts = editor.conflicts(settings, self.answer, self.shifts)

        windows = self.calculateWindows()

        self.pools = {cls: editor.pool(settings, self.answer, cls) for cls in self.classes}
        self.teachersPools = editor.teacherPools(settings, self.pools)

        conflictsCount = sum(len(items) for items in self.conflicts.values())

        teacher = self.items.currentItem().text() if self.items.currentItem().text() in self.teachers else None

        self.statsLabel.setText(self.statsText(windows, conflictsCount, teacher))

        summary = {}

        for reasons in self.conflicts.values():
            for name, _ in reasons:
                summary[name] = summary.get(name, 0) + 1

        self.statsLabel.setToolTip("\n".join(f"{translate('menu.main.tab.edit.conflict.' + name)}: {count}" for name, count in sorted(summary.items())))

    def fillTables(self) -> None:
        shift = self.shifts.get(self.selected, 0) if self.mode == 0 else self.currentShift()

        if shift not in self.tables:
            return

        table = self.tables[shift]
        classes = self.classesByShift.get(shift, [])

        table.setUpdatesEnabled(False)
        table.blockSignals(True)

        try:
            for day in range(self.days):
                for lesson in range(self.lessons):
                    if self.mode == 0:
                        self.updateClassCell(table, day, lesson)

                    else:
                        self.updateTeacherCell(table, classes, shift, day, lesson)

        finally:
            table.blockSignals(False)
            table.setUpdatesEnabled(True)

        self.dirtyShifts.discard(shift)

    def updateClassCell(self, table: QTableWidget, day: int, lesson: int) -> None:
        item = table.item(lesson, day)

        text = []
        tooltip = []

        for subject, teachers, classrooms in editor.entries(editor.getCell(self.answer, self.selected, day, lesson)):
            part = subject

            if self.classroomsEnabled and classrooms:
                part += f" - {translate('abbreviate.room')} {', '.join(classrooms)}"

            text.append(part)

            line = subject

            if teachers:
                line += f" - {', '.join(teachers)}"

            tooltip.append(line)

        problems = self.conflicts.get((self.selected, day, lesson), [])

        newText = "\n".join(text) if text else "-"
        newTooltip = "\n".join(tooltip + [self.reason(problem) for problem in problems])
        newBrush = self.redBrush if problems else self.defaultBrush

        if item.text() != newText:
            item.setText(newText)

        if item.toolTip() != newTooltip:
            item.setToolTip(newTooltip)

        if item.background() != newBrush:
            item.setBackground(newBrush)

    def updateTeacherCell(self, table: QTableWidget, classes: list, shift: int, day: int, lesson: int) -> None:
        item = table.item(lesson, day)

        text = []
        tooltip = []
        problems = []

        for cls, subject, classrooms in editor.teacherLessons(self.answer, classes, self.selected, day, lesson):
            part = f"{subject} - {cls}"

            if self.classroomsEnabled and classrooms:
                part += f" - {translate('abbreviate.room')} {', '.join(classrooms)}"

            text.append(part)
            tooltip.append(part)

            for problem in self.conflicts.get((cls, day, lesson), []):
                if self.relevant(problem) and problem not in problems:
                    problems.append(problem)

        slot = editor.teacherSlot(self.window.settings, self.selected, shift, day, lesson)

        newText = "\n".join(text) if text else "-"
        newTooltip = "\n".join(tooltip + [self.reason(problem) for problem in problems] + ([translate("menu.main.tab.edit.reserve")] if slot == "reserve" else []))

        if problems:
            newBrush = self.redBrush

        elif not text and slot == "reserve":
            newBrush = self.yellowBrush

        else:
            newBrush = self.defaultBrush

        if item.text() != newText:
            item.setText(newText)

        if item.toolTip() != newTooltip:
            item.setToolTip(newTooltip)

        if item.background() != newBrush:
            item.setBackground(newBrush)

    def addPoolItem(self, text: str, cls: str, subject: str) -> None:
        item = QListWidgetItem(text)

        item.setData(Qt.UserRole, subject)
        item.setData(Qt.UserRole + 1, cls)

        self.poolList.addItem(item)

    def fillPool(self) -> None:
        self.poolList.setUpdatesEnabled(False)

        try:
            self.poolList.clear()

            if self.mode == 0:
                for subject, left in self.pools.get(self.selected, {}).items():
                    self.addPoolItem(f"{subject} - {left}", self.selected, subject)

                return

            for cls, subject, left in self.teachersPools.get(self.selected, []):
                self.addPoolItem(f"{subject} - {cls} - {left}", cls, subject)

        finally:
            self.poolList.setUpdatesEnabled(True)

    def fillItems(self) -> None:
        conflictClasses = set()
        problems = set()

        if self.mode == 0:
            conflictClasses = {key[0] for key in self.conflicts}

        else:
            for (cls, day, lesson), reasons in self.conflicts.items():
                subjects = set()

                for name, value in reasons:
                    if name in ("unavailable", "busy"):
                        problems.add(value)

                    else:
                        subjects.update(value.split(" / "))

                if subjects:
                    for subject, teachers, _ in editor.entries(editor.getCell(self.answer, cls, day, lesson)):
                        if subject in subjects:
                            problems.update(teachers)

        self.items.setUpdatesEnabled(False)

        try:
            for index, name in enumerate(self.classes if self.mode == 0 else self.teachers):
                item = self.items.item(index)

                if self.mode == 0:
                    red = name in conflictClasses
                    yellow = bool(self.pools.get(name))

                else:
                    red = name in problems
                    yellow = bool(self.teachersPools.get(name))

                if red:
                    brush = self.redBrush

                elif yellow:
                    brush = self.yellowBrush

                else:
                    brush = self.defaultBrush

                if item.background() != brush:
                    item.setBackground(brush)

        finally:
            self.items.setUpdatesEnabled(True)

    def refresh(self) -> None:
        if self.answer is None or self.selected is None:
            return

        selected = self.selectedCells()

        self.calculate()

        self.dirtyShifts = set(range(self.shiftsCount))

        self.fillTables()
        self.fillPool()
        self.fillItems()

        if self.selectedCells() != selected:
            table = self.currentTable()

            table.setUpdatesEnabled(False)

            try:
                table.clearSelection()

                for day, lesson in selected:
                    table.item(lesson, day).setSelected(True)

            finally:
                table.setUpdatesEnabled(True)

    def selectedCells(self) -> list:
        table = self.currentTable()

        return sorted({(index.column(), index.row()) for index in table.selectedIndexes()})

    def clearSelection(self) -> None:
        for table in self.tables.values():
            table.clearSelection()

    def log(self, text: str) -> None:
        TabEdit.write(self.window, text + "\n")

    @staticmethod
    def write(window, text: str) -> None:
        window.objects["edit_log"] = window.objects.get("edit_log", "") + text

        tab = TabEdit.current(window)

        if tab is None:
            return

        cursor = tab.logTextEdit.textCursor()
        cursor.movePosition(QTextCursor.End)

        tab.logTextEdit.setTextCursor(cursor)
        tab.logTextEdit.insertPlainText(text)
        tab.logTextEdit.ensureCursorVisible()

    @staticmethod
    def current(window):
        tabs = window.objects.get("tabs")

        if tabs is None:
            return None

        tab = tabs.widget(TAB_EDIT)

        return tab if isinstance(tab, TabEdit) else None

    def modeChanged(self, idx: int) -> None:
        self.window.objects["edit_mode"] = idx

        TabEdit.init(self.window, ignore=[TAB_EDIT], reverse=True)

    def itemsItemClicked(self) -> None:
        item = self.items.currentItem()

        new = item.text() if item is not None else None

        if new == self.selected:
            return

        self.selected = new
        self.window.objects[self.selectedKey] = self.selected

        self.clearSelection()

        self.selectTabs()

        if self.answer is None or self.selected is None:
            return

        self.dirtyShifts = set(range(self.shiftsCount))

        self.fillTables()
        self.fillPool()

        self.calculate()

    def tabsCurrentChanged(self, idx: int) -> None:
        if self.mode == 1:
            self.window.objects["edit_shift_selected"] = idx

            if self.answer is not None and self.selected is not None and idx in self.dirtyShifts:
                self.fillTables()

        self.clearSelection()

    def snapshot(self) -> None:
        history = self.window.objects["history"]

        history.append(copy.deepcopy(self.answer))

        while len(history) > HISTORY:
            history.pop(0)

        if not os.path.exists(self.path("answer.backup.json")):
            shutil.copy(self.path("answer.json"), self.path("answer.backup.json"))

    def commit(self, text: str) -> None:
        self.saveAnswer()

        self.refresh()

        self.log(f"{text}")

    def deleteCells(self, cells: list) -> None:
        if not cells:
            self.log(translate("menu.main.tab.edit.log.select_any"))

            return

        self.snapshot()

        removed = []

        for day, lesson in cells:
            if self.mode == 0:
                removed += editor.removeLesson(self.answer, self.selected, day, lesson)

            else:
                for cls in self.shiftClasses():
                    removed += [f"{subject} - {cls}" for subject in editor.removeTeacherLesson(self.answer, self.selected, cls, day, lesson)]

        if not removed:
            self.window.objects["history"].pop()

            return

        self.commit(f"{translate('menu.main.tab.edit.log.deleted')}: {', '.join(removed)}")

    def deletePushButtonClicked(self) -> None:
        self.deleteCells(self.selectedCells())

    def openMenu(self, day: int, lesson: int) -> None:
        if not self.addMenu(day, lesson):
            return

        menu = QMenu(self)
        menu.setAttribute(Qt.WA_DeleteOnClose)
        menu.setFont(FONT)

        self.addMenu(day, lesson, menu)

        menu.exec_(QCursor.pos())

    def cellLeftClicked(self, day: int, lesson: int) -> None:
        self.openMenu(day, lesson)

    def cellRightClicked(self, day: int, lesson: int) -> None:
        cells = self.selectedCells()

        if len(cells) > 1 and (day, lesson) in cells:
            self.deleteCells(cells)

        else:
            self.deleteCells([(day, lesson)])

    def addLessonTo(self, cls: str, day: int, lesson: int, subject: str) -> None:
        if self.shifts.get(cls, 0) != self.currentShift():
            self.log(translate("menu.main.tab.edit.log.other_shift"))

            return

        self.snapshot()

        replaced = editor.addLesson(self.window.settings, self.answer, cls, day, lesson, subject)

        if replaced is None:
            self.window.objects["history"].pop()

            self.log(translate("menu.main.tab.edit.log.nothing_to_add"))

            return

        text = f"{translate('menu.main.tab.edit.log.added')}: {subject}" if self.mode == 0 else f"{translate('menu.main.tab.edit.log.added')}: {subject} - {cls}"

        if replaced:
            text += f" ({translate('menu.main.tab.edit.log.replaced')}: {', '.join(replaced)})"

        self.commit(text)

    def addMenu(self, day: int, lesson: int, menu: QMenu = None) -> list:
        available = []

        if self.mode == 0:
            for subject, left in self.pools.get(self.selected, {}).items():
                available.append((f"{subject} - {left}", self.selected, subject))

        else:
            for cls, subject, left in self.teachersPools.get(self.selected, []):
                if self.shifts.get(cls, 0) == self.currentShift():
                    available.append((f"{subject} - {cls} - {left}", cls, subject))

        if menu:
            if not available:
                action = QAction(translate("menu.main.tab.edit.pool_empty"), menu)
                action.setEnabled(False)

                menu.addAction(action)

                return []

            for text, cls, subject in available:
                action = QAction(text, menu)
                action.triggered.connect(lambda *_, c=cls, s=subject: QTimer.singleShot(0, lambda: self.addLessonTo(c, day, lesson, s)))

                menu.addAction(action)

        return available

    def addPushButtonClicked(self) -> None:
        cells = self.selectedCells()

        if len(cells) != 1:
            self.log(translate("menu.main.tab.edit.log.select_one"))

            return

        self.openMenu(cells[0][0], cells[0][1])

    def poolListItemDoubleClicked(self, item) -> None:
        cells = self.selectedCells()

        if len(cells) != 1:
            self.log(translate("menu.main.tab.edit.log.select_one"))

            return

        self.addLessonTo(item.data(Qt.UserRole + 1), cells[0][0], cells[0][1], item.data(Qt.UserRole))

    def undoPushButtonClicked(self) -> None:
        history = self.window.objects["history"]

        if not history:
            self.log(translate("menu.main.tab.edit.log.nothing_to_undo"))

            return

        self.answer = history.pop()

        self.commit(translate("menu.main.tab.edit.log.undone"))

    def revertPushButtonClicked(self) -> None:
        if not os.path.exists(self.path("answer.backup.json")):
            self.log(translate("menu.main.tab.edit.log.no_backup"))

            return

        answer = QMessageBox.question(self, translate("menu.main.tab.edit.revert"), translate("menu.main.tab.edit.revert_question"), QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if answer != QMessageBox.Yes:
            return

        self.snapshot()

        shutil.copy(self.path("answer.backup.json"), self.path("answer.json"))

        self.answer = self.solve()

        self.commit(translate("menu.main.tab.edit.log.reverted"))
