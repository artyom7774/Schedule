import hjson

LANGUAGE = "en"

BUNDLES = {
    "en": hjson.load(open("src/files/bundles/en.hjson")),
    "ru": hjson.load(open("src/files/bundles/ru.hjson"))
}

def translate(name) -> str:
    return BUNDLES[LANGUAGE].get(name, name)
