from PyQt5.QtWidgets import QApplication

from src.variables import *

import json
import os


def createProject(window):
    name = window.dialog.edit.text()

    try:
        with open(f"{PATH_TO_FOLDER}/using/{name}", "w") as file:
            pass

    except BaseException:
        window.dialog.log.setText(translate("log.text.impossible_project_name"))

        return

    if os.path.exists(f"{PATH_TO_FOLDER}/projects/{name}"):
        window.dialog.log.setText(translate("log.text.project_name_already_exists"))

        return

    os.mkdir(f"{PATH_TO_FOLDER}/projects/{name}")

    window.dialog.close()

    initProject(window, name)


def openProject(window):
    name = window.dialog.edit.currentText()

    window.dialog.close()

    initProject(window, name)


def initProject(window, project):
    window.project = project
    window.menu = "main"

    path = f"{PATH_TO_FOLDER}/projects/{window.project}"

    if not os.path.exists(f"{path}/data"):
        os.mkdir(f"{path}/data")

    names = {"classes.json", "hards.json", "lessons.json", "main.json", "subjects.json", "teachers.json"}

    for name in names:
        if not os.path.exists(f"{path}/data/{name}"):
            with open(f"{path}/data/{name}", "w", encoding="UTF-8") as file:
                file.write("{}")

    parameters = {
        "working_days_per_week": 1,
        "max_lesson_count_per_day": 1,
        "subjects": {},
        "classes_count": {
            "count": 0,
            "classes": [

            ]
        }
    }

    if not os.path.exists(f"{path}/settings.json"):
        with open(f"{path}/settings.json", "w", encoding="UTF-8") as file:
            file.write("{}")

    try:
        with open(f"{path}/settings.json", "r", encoding="UTF-8") as file:
            settings = json.load(file)

    except json.decoder.JSONDecodeError:
        with open(f"{path}/settings.json", "w", encoding="UTF-8") as file:
            file.write("{}")

        with open(f"{path}/settings.json", "r", encoding="UTF-8") as file:
            settings = json.load(file)

    for key, value in parameters.items():
        if key not in settings:
            settings[key] = value

    window.settings = settings

    with open(f"{path}/settings.json", "w", encoding="UTF-8") as file:
        json.dump(window.settings, file, indent=4, ensure_ascii=False)

    window.init()

    window.showMaximized()
