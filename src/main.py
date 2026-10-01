from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QPushButton
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIcon

from src.modules import menues

from src.variables import *

import faulthandler
import qdarktheme
import webbrowser
import threading
import requests
import ctypes
import json
import sys

faulthandler.enable()

try:
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(f"Schedule-Maker-1 {VERSION}")

except AttributeError:
    pass

class Window(QMainWindow):
    versionWasChecked = False

    signal = pyqtSignal(str, str)

    def __init__(self) -> None:
        super().__init__()

        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(True)

        except AttributeError:
            pass

        qdarktheme.setup_theme(theme=THEME, additional_qss=open(f"src/files/styles/{THEME}.qss", "r", encoding="utf-8").read())

        self.setWindowTitle("СуперЗавуч")
        self.setWindowIcon(QIcon("src/files/sprites/icon.ico"))

        self.settings = {}
        self.objects = {}

        self.project = None
        self.menu = "start"

        SIZE["width"] = self.width()
        SIZE["height"] = self.height() - PLUS

        self.dialog = None

        self.signal.connect(self.showVersionDialog)

        self.init()

        self.resize(800, 450)

        desktop = QApplication.desktop()
        self.move((desktop.width() - self.geometry().width()) // 2, (desktop.height() - self.geometry().height()) // 2)

        self.show()

    def init(self) -> None:
        for obj in self.objects.values():
            try:
                obj.deleteLater()

            except BaseException as e:
                print("error:", e)

        QApplication.processEvents()

        self.objects = {}

        getattr(menues, self.menu).init(self)

        if self.versionWasChecked:
            return

        thr = threading.Thread(target=self.version)
        thr.daemon = True
        thr.start()

        self.versionWasChecked = True

    def version(self):
        url = "https://raw.githubusercontent.com/artyom7774/versions/main/Schedule-Maker-1.json"

        try:
            response = requests.get(url, timeout=10)
            
        except requests.RequestException as e:
            return

        if response.status_code == 200:
            newVersion = json.loads(response.text)["version"]

            print(f"now version = {VERSION}, new version = {newVersion}")

            if newVersion > VERSION:
                self.signal.emit(VERSION, newVersion)

    def showVersionDialog(self, oldVersion, newVersion):
        msg = QMessageBox(self)

        msg.setWindowTitle(f"{translate('dialog.new_version.update')} {oldVersion} -> {newVersion}")
        msg.setText(translate("dialog.new_version.message"))
        msg.setIcon(QMessageBox.Information)

        openButton = QPushButton(translate("dialog.new_version.open"))
        openButton.clicked.connect(lambda: webbrowser.open("https://superzavych.pythonanywhere.com/"))

        msg.addButton(openButton, QMessageBox.ActionRole)

        okButton = msg.addButton(QMessageBox.Ok)

        msg.exec_()

    def showMaximized(self) -> None:
        super().showMaximized()

        QApplication.processEvents()

        SIZE["width"] = self.width()
        SIZE["height"] = self.height() - PLUS

        self.resize()

    def resize(self, width: int = None, height: int = None) -> None:
        if width and height:
            super().resize(width, height)

        QApplication.processEvents()

        getattr(menues, self.menu).resize(self)

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)

        QApplication.processEvents()

        SIZE["width"] = self.width()
        SIZE["height"] = self.height() - PLUS

        self.resize()


def run():
    app = QApplication(sys.argv)

    window = Window()
    window.show()

    sys.exit(app.exec())
