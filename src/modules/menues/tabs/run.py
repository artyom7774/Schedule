from PyQt5.QtWidgets import QTextEdit, QWidget, QPushButton, QLabel, QLineEdit, QScrollArea, QVBoxLayout, QGridLayout, QStyle, QStyleOptionButton, QStylePainter

from PyQt5.QtCore import QProcess, QTimer, Qt
from PyQt5.QtGui import QTextCursor

from src.modules.widgets import NoFocusPushButton

from src.variables import *

import json
import time


class CollapsibleSection(QWidget):
    def __init__(self, title: str, parent=None):
        super().__init__(parent)

        self.title = title

        self.open = True
        self.row = 0

        self.header = NoFocusPushButton(parent=self)
        self.header.setFont(FONT)

        self.header.clicked.connect(self.toggle)

        self.update()

        self.content = QWidget(parent=self)

        self.grid = QGridLayout(self.content)
        self.grid.setContentsMargins(0, 2, 0, 0)
        self.grid.setHorizontalSpacing(10)
        self.grid.setVerticalSpacing(2)
        self.grid.setColumnStretch(0, 9)
        self.grid.setColumnStretch(1, 11)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        layout.addWidget(self.header)
        layout.addWidget(self.content)

    def addRow(self, label: QLabel, edit: QLineEdit) -> None:
        label.setMinimumHeight(30)
        edit.setMinimumHeight(30)

        self.grid.addWidget(label, self.row, 0)
        self.grid.addWidget(edit, self.row, 1)

        self.row += 1

    def update(self) -> None:
        self.header.setText(f"{self.title}")

    def toggle(self) -> None:
        self.open = not self.open

        self.content.setVisible(self.open)
        self.update()


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

        self.settingsRama = QScrollArea(parent=self)
        self.settingsRama.setWidgetResizable(True)
        self.settingsRama.setFrameShape(QScrollArea.NoFrame)
        self.settingsRama.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.settingsContent = QWidget()
        self.sectionsLayout = QVBoxLayout(self.settingsContent)
        self.sectionsLayout.setContentsMargins(0, 0, 0, 0)
        self.sectionsLayout.setSpacing(2)

        self.settingsRama.setWidget(self.settingsContent)
        self.settingsRama.show()

        self.objects = {}

        self.parameters = {}
        self.weights = {}

        self.initializate()

        self.stdTextEdit.setReadOnly(True)
        self.stdTextEdit.setFont(ANOTHER_FONT)
        self.stdTextEdit.show()

        self.runPushButton = QPushButton(parent=self)
        self.runPushButton.clicked.connect(lambda: self.runPushButtonClicked())
        self.runPushButton.setText(translate("menu.main.tab.run.run"))
        self.runPushButton.setFont(FONT)
        self.runPushButton.show()

        self.warningsPushButton = QPushButton(parent=self)
        self.warningsPushButton.clicked.connect(lambda: self.runPushButtonClicked(warnings=1))
        self.warningsPushButton.setText(translate("menu.main.tab.run.warnings"))
        self.warningsPushButton.setFont(FONT)
        self.warningsPushButton.show()

        self.number = 0
        self.timer = None

        self.timeLabel = QLabel(parent=self)
        self.timeLabel.setFont(FONT)
        self.timeLabel.show()

    def load(self, name: str) -> dict:
        try:
            with open(f"{PATH_TO_FOLDER}/projects/{self.window.project}/{name}.json", "r", encoding="utf-8") as file:
                return json.load(file)

        except FileNotFoundError:
            return {}

    def save(self, name: str, data: dict) -> None:
        with open(f"{PATH_TO_FOLDER}/projects/{self.window.project}/{name}.json", "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    def data(self, type: str) -> dict:
        return self.weights if type == "weights" else self.parameters

    def parse(self, type: str, text: str):
        if type == "weights":
            return int(text)

        try:
            return int(text)

        except ValueError:
            return float(text)

    def initializate(self):
        while self.sectionsLayout.count():
            item = self.sectionsLayout.takeAt(0)

            widget = item.widget()

            if widget is not None:
                widget.setParent(None)
                widget.deleteLater()

        self.objects = {}

        self.weights = self.load("weights")
        self.parameters = self.load("parameters")

        labels = []

        for type in ("parameters", "weights"):
            data = self.data(type)

            if not data:
                continue

            section = CollapsibleSection(translate(f"menu.main.tab.run.{type}"))
            section.setParent(self.settingsContent)

            for name, value in data.items():
                label = QLabel(translate(f"{type}.{name}") + ":")
                label.setFont(FONT)

                edit = QLineEdit(str(value))
                edit.setFont(FONT)
                edit.editingFinished.connect(lambda f=type, n=name: self.valueLineEditEditingFinished(f, n))

                section.addRow(label, edit)
                labels.append(label)

                self.objects[f"label_{type}_{name}"] = label
                self.objects[f"edit_{type}_{name}"] = edit

            self.sectionsLayout.addWidget(section)

        if labels:
            width = max(label.sizeHint().width() for label in labels) + 2

            for label in labels:
                label.setMinimumWidth(width)

        self.sectionsLayout.addStretch(1)

    def valueLineEditEditingFinished(self, type: str, name: str):
        edit = self.objects[f"edit_{type}_{name}"]
        text = edit.text()

        data = self.data(type)

        try:
            value = self.parse(type, text)

        except (ValueError, TypeError):
            edit.setText(str(data[name]))

            return

        data[name] = value
        self.save(type, data)

    def runPushButtonClicked(self, warnings: int = 0):
        try:
            if self.process and self.process.state() != QProcess.NotRunning:
                return

        except RuntimeError:
            pass

        for name in list(self.weights.keys()):
            self.valueLineEditEditingFinished("weights", name)

        for name in list(self.parameters.keys()):
            self.valueLineEditEditingFinished("parameters", name)

        self.time = time.time()
        self.number = 0

        self.timer = QTimer()
        self.timer.timeout.connect(self.counter)
        self.timer.start(1000)

        self.stdTextEdit.clear()

        self.runPushButton.setDisabled(True)
        self.warningsPushButton.setDisabled(True)

        TabRun.process = QProcess(self)

        self.process.setProcessChannelMode(QProcess.MergedChannels)

        self.process.readyReadStandardOutput.connect(self.stdout)
        self.process.readyReadStandardError.connect(self.stderr)
        self.process.finished.connect(self.finish)

        args = [
            "--weights",    f"{PATH_TO_FOLDER}/projects/{self.window.project}/weights.json",
            "--input",      f"{PATH_TO_FOLDER}/projects/{self.window.project}/settings.json",
            "--output",     f"{PATH_TO_FOLDER}/projects/{self.window.project}/answer.json",

            "--iterations", f"{self.parameters['iterations']}",
            "--cooling",    f"{self.parameters['cooling']}",

            "--warnings",   f"{warnings}"
        ]

        print("src/modules/solve.exe", " ".join(args))

        self.process.start("src/modules/solve.exe", args)

    def counter(self):
        self.number += 1

        self.timeLabel.setText(translate("menu.main.tab.run.time_passed") + ": " + str(self.number) + " s")

    def update(self):
        cursor = self.stdTextEdit.textCursor()
        cursor.movePosition(QTextCursor.End)

        self.stdTextEdit.setTextCursor(cursor)
        self.stdTextEdit.ensureCursorVisible()

    def stdout(self):
        self.update()
        self.stdTextEdit.insertPlainText(bytes(self.process.readAllStandardOutput()).decode("utf-8", errors="replace"))
        self.update()

    def stderr(self):
        self.update()
        self.stdTextEdit.insertPlainText(bytes(self.process.readAllStandardError()).decode("utf-8", errors="replace"))
        self.update()

    def finish(self, code, status):
        self.runPushButton.setDisabled(False)
        self.warningsPushButton.setDisabled(False)

        self.timer.stop()

        self.update()
        self.stdTextEdit.insertPlainText(f"\n=== Process finished with exit code {code} ===\n")
        self.update()

        TabRun.init(self.window, ignore=[TAB_RUN])

    def stop(self):
        if self.process is not None and self.process.state() != QProcess.NotRunning:
            self.process.terminate()

            if not self.process.waitForFinished(1000):
                self.process.kill()

                self.process.waitForFinished()
