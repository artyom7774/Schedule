from src.variables import *

import shutil
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

    if not os.path.exists(f"{path}/requests"):
        os.mkdir(f"{path}/requests")

    if not os.path.exists(f"{path}/backups"):
        os.mkdir(f"{path}/backups")

    if not os.path.exists(f"{path}/weights.json"):
        shutil.copy(f"src/files/weights.json", f"{path}/weights.json")

    parameters = {
        "working_days_per_week": 5,
        "max_lesson_count_per_day": 8,
        "classes_count": 11,
        "subjects_count": 20,
        "number_of_shifts": 2,
        "subjects": [

        ],
        "classes": {
            "count": [

            ],
            "shift": [

            ],
            "lessons": {

            }
        },
        "teachers": {

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
