from PyQt5.QtGui import QFont

from src.modules.translate import translate

import os

NAME = "Schedule Maker 1"

CLASSES_ALPHABET = "-АБВГДЕЖЗИКЛМНОПРСТУФХЦЧШЩЭЮЯ"
CLASSES_TABLE_COLORS = ["#202124", "#37383B", "#4E4F52", "#656669", "#7B7C7F", "#929396", "#A9AAAD", "#C0C0C0"]

SIZE = {}
PLUS = 64 + 8 - 1

TAB_SETTINGS    = 0
TAB_CLASSES     = 1
TAB_TEACHERS    = 2
TAB_AI          = 4
TAB_CONSTANTS   = 6
TAB_GROUPS      = 7
TAB_RUN         = 9
TAB_VIEW        = 11
TAB_EXPORT      = 13


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
