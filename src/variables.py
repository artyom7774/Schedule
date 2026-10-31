from PyQt5.QtGui import QFont

from src.modules.translate import translate, language as setLanguage, LANGUAGE, BUNDLES

import faulthandler
import json
import os

faulthandler.enable()

NAME = "Schedule Maker 1"

CLASSES_ALPHABET = "-АБВГДЕЖЗИКЛМНОПРСТУФХЦЧШЩЭЮЯ"

SIZE = {}
PLUS = 64 + 8 - 1

TAB_SETTINGS    = 0
TAB_CLASSES     = 1
TAB_CLASSROOMS  = 2
TAB_SUBJECTS    = 3
TAB_TEACHERS    = 4
TAB_AI          = 6
TAB_CONSTANTS   = 8
TAB_GROUPS      = 9
TAB_RUN         = 11
TAB_VIEW        = 13
TAB_EXPORT      = 15


def shiftName(index: int) -> str:
    names = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"]

    return names[index] if 0 <= index < len(names) else str(index + 1)


def shiftNormalize(settings: dict) -> bool:
    classes = settings.setdefault("classes", {})
    shifts = classes.setdefault("shift", [])

    changed = False

    count = settings.get("classes_count", len(shifts))
    maxShift = max(int(settings.get("number_of_shifts", 1)), 1) - 1

    while len(shifts) < count:
        shifts.append([0] * (len(CLASSES_ALPHABET) - 1))

        changed = True

    while len(shifts) > count:
        shifts.pop(-1)

        changed = True

    for grade in range(len(shifts)):
        row = shifts[grade]

        if not isinstance(row, list):
            try:
                value = int(row)

            except BaseException:
                value = 0

            row = [value] * (len(CLASSES_ALPHABET) - 1)

            changed = True

        if len(row) != (len(CLASSES_ALPHABET) - 1):
            row = (row + [0] * (len(CLASSES_ALPHABET) - 1))[:len(CLASSES_ALPHABET) - 1]

            changed = True

        for letter in range(len(CLASSES_ALPHABET) - 1):
            try:
                value = int(row[letter])

            except BaseException:
                value = 0

            value = min(max(value, 0), maxShift)

            if row[letter] != value:
                row[letter] = value

                changed = True

        shifts[grade] = row

    return changed


def shiftGetClass(settings: dict, name: str) -> int:
    try:
        grade, letter = name.split(" ", 1)

        value = int(settings["classes"]["shift"][int(grade) - 1][CLASSES_ALPHABET.index(letter) - 1])

    except BaseException:
        return 0

    return min(max(value, 0), max(int(settings.get("number_of_shifts", 1)), 1) - 1)


def getAppDataDir():
    if os.name == "nt":
        base = os.getenv("APPDATA")

    else:
        base = os.getcwd()

    return base


PATH_TO_FOLDER = f"{getAppDataDir()}/Schedule-Maker-1"

if not os.path.exists(PATH_TO_FOLDER):
    os.mkdir(PATH_TO_FOLDER)

if not os.path.exists(f"{PATH_TO_FOLDER}/using"):
    os.mkdir(f"{PATH_TO_FOLDER}/using")

if not os.path.exists(f"{PATH_TO_FOLDER}/projects"):
    os.mkdir(f"{PATH_TO_FOLDER}/projects")

if not os.path.exists(f"{PATH_TO_FOLDER}/settings.json"):
    with open(f"{PATH_TO_FOLDER}/settings.json", "w", encoding="utf-8") as file:
        json.dump({"language": "en", "theme": "dark"}, file, indent=4)

with open(f"{PATH_TO_FOLDER}/settings.json", "r", encoding="utf-8") as file:
    SETTINGS = json.load(file)

VERSION = json.load(open("src/files/version.json", "r", encoding="utf-8"))["version"]

setLanguage(SETTINGS["language"])
THEME = SETTINGS.get("theme", "dark")

CLASSES_TABLE_COLORS = ["#FFFFFF", "#F2F2F3", "#E5E5E6", "#D8D8D9", "#CBCBCC", "#BEBEBF", "#B1B1B2", "#A4A4A5"]

COLORS = {
    "green": "4caf50",
    "yellow": "ffc107",
    "red": "f44336"
}

if THEME == "dark":
    CLASSES_TABLE_COLORS = ["#202124", "#37383B", "#4E4F52", "#656669", "#7B7C7F", "#929396", "#A9AAAD", "#C0C0C0"]

    COLORS = {
        "green": "109012",
        "yellow": "907810",
        "red": "901112"
    }


class Size:
    @staticmethod
    def x(var) -> int:
        return round(SIZE["width"] * (var / 100))

    @staticmethod
    def y(var) -> int:
        return round((SIZE["height"] + PLUS) * (var / 100))


BIG_FONT = QFont("Courier New")
BIG_FONT.setPointSize(30)

FONT = QFont("Verdana")
FONT.setPixelSize(16)

ANOTHER_FONT = QFont("Courier New")
ANOTHER_FONT.setPixelSize(16)

LITTLE_FONT = QFont("Verdana")
LITTLE_FONT.setPixelSize(14)
