from PyQt5.QtWidgets import QLabel, QToolButton, QFrame, QPushButton
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtCore import Qt, QSize, QTimer

from src.modules.functions.tree import createProject, openProject
from src.modules import dialogs, widgets

from src.variables import *

import subprocess
import threading
import os

languages = [
    ["ru", "src/files/sprites/languages/ru.jpg"],
    ["en", "src/files/sprites/languages/en.jpg"],
    ["by", "src/files/sprites/languages/by.png"]
]


def init(window) -> None:
    for obj in window.objects.values():
        try:
            obj.hide()

            obj.deleteLater()

        except AttributeError:
            pass

    window.objects.clear()

    window.objects["labelName"] = QLabel(translate("menu.start.label_name"), parent=window)
    window.objects["labelName"].setAlignment(Qt.AlignCenter)
    window.objects["labelName"].setFont(BIG_FONT)
    window.objects["labelName"].show()

    window.objects["labelVersion"] = QLabel(f"v{VERSION}", parent=window)
    window.objects["labelVersion"].setAlignment(Qt.AlignCenter)
    window.objects["labelVersion"].setFont(FONT)
    window.objects["labelVersion"].show()

    window.objects["frameLine"] = QFrame(window)
    window.objects["frameLine"].setObjectName("frameLine")
    window.objects["frameLine"].setFrameShape(QFrame.HLine)
    window.objects["frameLine"].setFrameShadow(QFrame.Plain)
    window.objects["frameLine"].show()

    window.objects["themePushButton"] = widgets.CircleButton(QColor("#202124" if THEME == "light" else "#f0f0f0"), 25, parent=window)
    window.objects["themePushButton"].clicked.connect(lambda: setTheme(window))
    window.objects["themePushButton"].show()

    buttons = [
        ("buttonCreateProject", "menu.start.button_create_project", f"src/files/sprites/{THEME}/create.svg", lambda: buttonCreateProject(window)),
        ("buttonOpenProject", "menu.start.button_open_project", f"src/files/sprites/{THEME}/open.svg", lambda: buttonOpenProject(window)),
        ("buttonExit", "menu.start.button_exit", f"src/files/sprites/{THEME}/exit.svg", lambda: window.close()),
    ]

    for name, text, icon, callback in buttons:
        btn = QToolButton(parent=window)
        btn.setObjectName("bigMenuButton")
        btn.setText(translate(text))
        btn.setIcon(QIcon(icon))
        btn.setIconSize(QSize(96, 96))
        btn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        btn.setFont(FONT)
        btn.setCursor(Qt.PointingHandCursor)
        btn.clicked.connect(callback)
        btn.show()

        window.objects[name] = btn

    buttons = [
        ("buttonAbout", f"src/files/sprites/{THEME}/about.svg", lambda: buttonAbout(window))
    ]

    for name, icon, callback in buttons:
        btn = QToolButton(parent=window)
        btn.setObjectName("bigMenuButton")
        btn.setIcon(QIcon(icon))
        btn.setIconSize(QSize(48, 48))
        btn.setToolButtonStyle(Qt.ToolButtonIconOnly)
        btn.setFont(FONT)
        btn.setCursor(Qt.PointingHandCursor)
        btn.clicked.connect(callback)
        btn.show()

        window.objects[name] = btn

    for type, icon in languages:
        btn = QPushButton(parent=window)
        btn.setIcon(QIcon(icon))
        btn.setIconSize(QSize(50, 25))
        btn.setFixedSize(50, 25)
        btn.clicked.connect(lambda _, lang=type: language(window, lang))
        btn.show()

        window.objects[type] = btn

    resize(window)


def language(window, lang):
    with open(f"{PATH_TO_FOLDER}/settings.json", "r", encoding="utf-8") as file:
        settings = json.load(file)

    settings["language"] = lang

    with open(f"{PATH_TO_FOLDER}/settings.json", "w", encoding="utf-8") as file:
        json.dump(settings, file, indent=4)

    setLanguage(lang)

    init(window)


def resize(window) -> None:
    w, h = window.width(), window.height()

    window.objects["labelName"].setGeometry(0, 40, w, 60)
    window.objects["frameLine"].setGeometry(w // 2 - 150, 100, 300, 2)

    window.objects["labelVersion"].setGeometry(0, h - 30, w, 30)

    btn_size = 140
    gap = 20
    total_width = btn_size * 3 + gap * 2
    start_x = (w - total_width) // 2
    y = h // 2 - btn_size // 2

    window.objects["buttonCreateProject"].setGeometry(start_x, y, btn_size, btn_size)
    window.objects["buttonOpenProject"].setGeometry(start_x + btn_size + gap, y, btn_size, btn_size)
    window.objects["buttonExit"].setGeometry(start_x + 2 * (btn_size + gap), y, btn_size, btn_size)

    btn_size = 60
    gap = 20
    y = y + 140 + 10

    window.objects["buttonAbout"].setGeometry(start_x, y, btn_size, btn_size)

    idx = 0

    for type, path in languages:
        window.objects[type].setGeometry(5 + 55 * idx, Size.y(100) - 30, 60, 30)

        idx += 1

    window.objects["themePushButton"].setGeometry(w - 30, h - 30, 25, 25)


def setTheme(window):
    global SETTINGS

    SETTINGS["theme"] = "light" if THEME == "dark" else "dark"

    with open(f"{PATH_TO_FOLDER}/settings.json", "w", encoding="utf-8") as file:
        json.dump(SETTINGS, file, indent=4)

    thr = threading.Thread(target=lambda: subprocess.run(
        ["./python/Scripts/python.exe", "-OO", "-s", "Schedule.py"] if os.path.exists("python/Scripts/python.exe") else ["./python/python.exe", "-OO", "-s", "Schedule.py"],
        capture_output=True,
        text=True,
        creationflags=subprocess.CREATE_NO_WINDOW
    ))

    thr.start()

    window.close()


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


def buttonAbout(window):
    window.dialog = dialogs.AboutDialog(window)
    window.dialog.exec()
