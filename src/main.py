from PyQt5.QtWidgets import QMainWindow, QApplication

from src.modules import menues

from src.variables import *

import faulthandler
import qdarktheme
import ctypes
import sys

faulthandler.enable()


class Window(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(True)

        except AttributeError:
            pass

        STYLE = """
        QPushButton {
            color: white;
        }
        
        QFrame#frameLine {
            background-color: #3f4042;
            border: none;
        }

        QToolButton#bigMenuButton {
            border: 2px solid #3f4042;
            border-radius: 16px;
            font-weight: 450;
        }
        
        QToolButton#bigMenuButton:hover {
            background-color: rgba(255, 255, 255, 10);
        }
        
        QToolButton#bigMenuButton:pressed {
            background-color: rgba(255, 255, 255, 20);
        }
        
        QTableWidget {
            background-color: #202124;
        }
        """

        qdarktheme.setup_theme(theme="dark", additional_qss=STYLE)

        self.setWindowTitle(NAME)

        self.settings = {}
        self.objects = {}

        self.project = None
        self.menu = "start"

        SIZE["width"] = self.width()
        SIZE["height"] = self.height() - PLUS

        self.dialog = None

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
