from PyQt5.QtWidgets import QFileDialog, QWidget, QPushButton, QLineEdit
from PyQt5.QtCore import QObject, QThread, pyqtSignal

from src.modules.widgets import ChatAITextEdit
from src.modules.ai import sendChatRequestWithFiles, decoder as decodeAIMessage

from src.variables import *

import datetime
import shutil
import json
import os


class AIWorker(QObject):
    finished = pyqtSignal(str, str)
    error = pyqtSignal(str)

    def __init__(self, prompt, paths):
        super().__init__()

        self.prompt = prompt
        self.paths = paths

    def run(self):
        try:
            text, status = sendChatRequestWithFiles(self.prompt, self.paths)
            self.finished.emit(text, status)

        except Exception as e:
            self.error.emit(str(e))


class TabAI(QWidget):
    chatTextEdit = None
    paths = []

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
        self.loadPushButton.clicked.connect(lambda: self.loadPushButtonClicked())
        self.loadPushButton.setFont(FONT)
        self.loadPushButton.show()

        self.removePushButton = QPushButton(parent=self)
        self.removePushButton.setText(translate("menu.main.tab.AI.remove_files"))
        self.removePushButton.clicked.connect(lambda: self.removePushButtonClicked())
        self.removePushButton.setFont(FONT)
        self.removePushButton.show()

        self.updateLoadButtonText()

    def updateLoadButtonText(self):
        if not self.paths:
            self.loadPushButton.setText(translate("menu.main.tab.AI.choose_file"))

        else:
            names = ", ".join(os.path.basename(p) for p in self.paths)

            self.loadPushButton.setText(f"{names}, {translate('menu.main.tab.AI.choose_file').lower()}")

    def removePushButtonClicked(self):
        self.paths = []
        self.updateLoadButtonText()

    def loadPushButtonClicked(self):
        paths, _ = QFileDialog.getOpenFileNames(self, "Choose files", "", "All files (*)")

        if not paths:
            return

        for p in paths:
            if p not in self.paths:
                self.paths.append(p)

        self.updateLoadButtonText()

    def messageLineEditReturnPressed(self):
        if self.messageLineEdit.text() == "" and not self.paths:
            return

        self.messageLineEdit.setEnabled(False)
        self.loadPushButton.setEnabled(False)

        requestsDir = f"{PATH_TO_FOLDER}/projects/{self.window.project}/requests"
        os.makedirs(requestsDir, exist_ok=True)

        for f in os.listdir(requestsDir):
            try:
                os.remove(os.path.join(requestsDir, f))

            except OSError:
                pass

        names = []
        copiedPaths = []

        for i, src in enumerate(self.paths):
            base = os.path.basename(src)
            ext = base[base.rfind(".") + 1:] if "." in base else ""

            name = f"requests/request-{i}.{ext}" if ext else f"requests/request-{i}"
            dst = f"{PATH_TO_FOLDER}/projects/{self.window.project}/{name}"

            shutil.copyfile(src, dst)

            names.append(name)
            copiedPaths.append(dst)

        prompt = open("src/files/prompts/loader.txt", "r", encoding="utf-8").read()

        prompt = prompt.replace("$FILE$", ", ".join(names) if names else "NO FILES")
        prompt = prompt.replace("$HISTORY$", str(self.chatTextEdit.history))
        prompt = prompt.replace("$MESSAGE$", self.messageLineEdit.text())
        prompt = prompt.replace("$PATH_TO_FOLDER$", PATH_TO_FOLDER)
        prompt = prompt.replace("$PROJECT$", self.window.project)

        shown = self.messageLineEdit.text()

        if self.paths:
            shown += " (" + ", ".join(os.path.basename(p) for p in self.paths) + ")"

        self.chatTextEdit.send(shown)
        self.messageLineEdit.setText("")

        self.thread = QThread()

        self.worker = AIWorker(prompt, copiedPaths)
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

        shutil.copyfile(f"{PATH_TO_FOLDER}/projects/{self.window.project}/out.json", f"{PATH_TO_FOLDER}/projects/{self.window.project}/temp.json")

        os.remove(f"{PATH_TO_FOLDER}/projects/{self.window.project}/out.json")

        with open(f"{PATH_TO_FOLDER}/projects/{self.window.project}/settings.json", "w", encoding="utf-8") as file:
            json.dump(self.window.settings, file, ensure_ascii=False)

        TabAI.init(self.window, ignore=[TAB_SETTINGS, TAB_CLASSES, TAB_TEACHERS, TAB_GROUPS, TAB_CONSTANTS], reverse=True)
