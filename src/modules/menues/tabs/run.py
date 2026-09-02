from PyQt5.QtWidgets import QTextEdit, QWidget, QTableWidget, QPushButton, QLabel, QLineEdit
from PyQt5.QtCore import QProcess, QTimer
from PyQt5.QtGui import QTextCursor

from src.variables import *

import json
import time


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
            self.objects[f"lineedit_{name}"].setText(str(value))
            self.objects[f"lineedit_{name}"].editingFinished.connect(lambda var = name: self.weightLineEditEditingFinished(var))
            self.objects[f"lineedit_{name}"].setFont(FONT)
            self.objects[f"lineedit_{name}"].show()

    def weightLineEditEditingFinished(self, name):
        value = self.objects[f"lineedit_{name}"].text()

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

        TabRun.init(self.window, ignore=[TAB_RUN])

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

        print("src/modules/solve.exe", " ".join([
            "--weights",    f"{PATH_TO_FOLDER}/projects/{self.window.project}/weights.json",
            "--input",      f"{PATH_TO_FOLDER}/projects/{self.window.project}/settings.json",
            "--output",     f"{PATH_TO_FOLDER}/projects/{self.window.project}/answer.json",
            "--iterations", f"100000000"
        ]))

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

        TabRun.init(self.window, ignore=[TAB_VIEW], reverse=True)

    def stop(self):
        if self.process is not None and self.process.state() != QProcess.NotRunning:
            self.process.terminate()

            if not self.process.waitForFinished(1000):
                self.process.kill()
                self.process.waitForFinished()
