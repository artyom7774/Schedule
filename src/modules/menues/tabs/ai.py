from PyQt5.QtWidgets import QFileDialog, QWidget, QPushButton, QLineEdit
from PyQt5.QtCore import QObject, QThread, pyqtSignal

from src.modules.widgets import ChatAITextEdit
from src.modules.ai import sendChatRequestWithFile, decoder as decodeAIMessage

from src.variables import *

import datetime
import shutil
import json


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

        TabAI.init(self.window, ignore=[TAB_SETTINGS, TAB_CLASSES, TAB_TEACHERS, TAB_GROUPS], reverse=True)
