from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtGui import QTextCursor

from src.variables import *


class ChatAITextEdit(QTextEdit):
    history = []

    def __init__(self, window, parent):
        super().__init__(parent)

        self.window = window

        if len(self.history) == 0:
            self.answer(translate("menu.main.tab.AI.ai_first_message"))

    @staticmethod
    def escape(text):
        return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\n", "<br>")

    def print(self, role, text, color):
        self.moveCursor(QTextCursor.End)

        self.append(f'<p><b style="color:{color};">{role}:</b> {self.escape(text)}</p>')

        self.moveCursor(QTextCursor.End)

    def send(self, text):
        if not text:
            return

        self.print(translate("menu.main.tab.AI.you"), text, "#1a73e8")

        self.history.append({"role": "user", "content": text})

    def answer(self, answer):
        self.print(translate("menu.main.tab.AI.ai"), answer, "#188038")

        self.history.append({"role": "assistant", "content": answer})

    def error(self, error):
        self.print(translate("menu.main.tab.AI.error"), error, "#d93025")
