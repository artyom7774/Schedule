import hjson
import json

LANGUAGE = "en"

BUNDLES = {
    "en": hjson.load(open("src/files/bundles/en.hjson", "r", encoding="utf-8")),
    "ru": hjson.load(open("src/files/bundles/ru.hjson", "r", encoding="utf-8"))
}

def translate(name) -> str:
    return BUNDLES[LANGUAGE.lower()].get(name, name)


def language(lang):
    global LANGUAGE

    LANGUAGE = lang
