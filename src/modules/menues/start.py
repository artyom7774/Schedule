from PyQt5.QtWidgets import QLabel, QToolButton, QFrame
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize

from src.modules.functions.tree import createProject, openProject
from src.modules import dialogs

from src.variables import *

import os


def init(window) -> None:
    window.objects["labelName"] = QLabel(translate("menu.start.label_name"), parent=window)
    window.objects["labelName"].setAlignment(Qt.AlignCenter)
    window.objects["labelName"].setFont(BIG_FONT)
    window.objects["labelName"].show()

    window.objects["frameLine"] = QFrame(window)
    window.objects["frameLine"].setObjectName("frameLine")
    window.objects["frameLine"].setFrameShape(QFrame.HLine)
    window.objects["frameLine"].setFrameShadow(QFrame.Plain)
    window.objects["frameLine"].show()

    buttons = [
        ("buttonCreateProject", "menu.start.button_create_project", "src/files/icons/create.svg", lambda: buttonCreateProject(window)),
        ("buttonOpenProject", "menu.start.button_open_project", "src/files/icons/open.svg", lambda: buttonOpenProject(window)),
        ("buttonExit", "menu.start.button_exit", "src/files/icons/exit.svg", lambda: window.close()),
    ]

    for name, key, icon, callback in buttons:
        btn = QToolButton(parent=window)
        btn.setObjectName("bigMenuButton")
        btn.setText(translate(key))
        btn.setIcon(QIcon(icon))
        btn.setIconSize(QSize(96, 96))
        btn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        btn.setFont(FONT)
        btn.setCursor(Qt.PointingHandCursor)
        btn.clicked.connect(callback)
        btn.show()
        window.objects[name] = btn

    resize(window)


def resize(window) -> None:
    w, h = window.width(), window.height()

    window.objects["labelName"].setGeometry(0, 40, w, 60)
    window.objects["frameLine"].setGeometry(w // 2 - 150, 100, 300, 2)

    btn_size = 150
    gap = 20
    total_width = btn_size * 3 + gap * 2
    start_x = (w - total_width) // 2
    y = h // 2 - btn_size // 2

    window.objects["buttonCreateProject"].setGeometry(start_x, y, btn_size, btn_size)
    window.objects["buttonOpenProject"].setGeometry(start_x + btn_size + gap, y, btn_size, btn_size)
    window.objects["buttonExit"].setGeometry(start_x + 2 * (btn_size + gap), y, btn_size, btn_size)


def buttonCreateProject(window):
    title = translate("dialog.create_project.title")
    label = translate("dialog.create_project.label")
    allow = translate("dialog.create_project.allow")

    window.dialog = dialogs.TextInputDialog(window, title, label, allow, lambda: createProject(window))
    window.dialog.exec()


def buttonOpenProject(window):
    title = translate("dialog.open_project.title")
    label = translate("dialog.open_project.label")
    allow = translate("dialog.open_project.allow")

    chooses = os.listdir(f"{PATH_TO_FOLDER}/projects/")

    window.dialog = dialogs.ChooseInputDialog(window, chooses, title, label, allow, lambda: openProject(window))
    window.dialog.exec()
