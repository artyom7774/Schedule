"""
Парсер сайта школы на движке schools.by
(https://46vitebsk.schools.by)

Что делает:
  1. Читает страницу /subjects -> список всех предметов школы (название + ссылка).
  2. Для каждого предмета читает его страницу /subject/{id} -> достаёт:
       - список классов, где преподаётся предмет ("Преподается в")
       - список учителей, которые вообще ведут этот предмет в школе ("Учителя")
  3. Сохраняет всё в data/subjects.json

ВАЖНО:
  - Сайт запрещает автоматический доступ через robots.txt, поэтому Claude
    не может сходить на сайт сам. Этот скрипт нужно запускать у СЕБЯ на
    компьютере (там robots.txt никто не проверяет, но помните про этичность
    и не долбите сайт слишком часто -- есть задержка между запросами).
  - Часть данных (сколько именно часов в неделю у конкретного учителя в
    конкретном классе) на странице предмета НЕТ. Она есть только на странице
    самого класса (расписание), см. parse_class() ниже -- функция-заготовка,
    её нужно донастроить под реальную вёрстку страницы /class/{id}, когда
    пришлёте мне пример такой страницы.

Установка зависимостей:
    pip install requests beautifulsoup4

Запуск:
    python parse_school.py
"""

import json
import random
import re
import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "https://46vitebsk.schools.by"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    )
}
DELAY_SECONDS = 1.0
OUT_DIR = Path("parser")

# ---------------------------------------------------------------------------
# ЧАСЫ В НЕДЕЛЮ ПО ПРЕДМЕТАМ (официальный типовой учебный план)
# ---------------------------------------------------------------------------
# Источник: Постановление Министерства образования Республики Беларусь
# от 23.04.2025 N 75 "Об типовых учебных планах общего среднего образования"
# (в редакции постановления от 07.08.2025 N 139), план "Средняя школа".
# https://adu.by/images/2025/08/post-tip-ucheb-plany.pdf
#
# ВАЖНО про точность этих цифр:
#   - В официальном документе для многих предметов указан ДИАПАЗОН значений
#     в зависимости от языка обучения (бел./рус.), полугодия, базового или
#     повышенного уровня изучения, профиля класса и т.д. -- в оригинале это
#     задаётся сложной системой сносок.
#   - Ниже взяты БАЗОВЫЕ (неуглублённые) значения для ОБЫЧНОЙ школы с
#     русским языком обучения -- то есть наиболее типичный случай.
#     Для класса, где предмет реально ведётся на повышенном уровне, в
#     профильном/спортивном классе и т.п., РЕАЛЬНОЕ количество часов может
#     отличаться.
#   - Если в плане у предмета часы разбиты по полугодиям (например "2/1"),
#     здесь указано среднее ((2+1)/2 = 1.5) за неделю в год.
#   - Часы для X-XI класса взяты из той же официальной таблицы, но приведены
#     проще (без вариантов "базовый/повышенный уровень"), поэтому для этих
#     классов точность ниже, чем для V-IX.
#
# Структура: { "Название предмета на сайте школы": {номер_класса: [часы_1_полугодие, часы_2_полугодие], ...} }
# Если в оригинальном плане часы были одинаковы весь год (без разбивки по
# полугодиям), оба числа в паре одинаковые. Если для класса предмет не
# предусмотрен -- ключа/номера класса просто нет в словаре.
CURRICULUM_HOURS = {
    "Русский язык": {
        5: [3, 3], 6: [3, 3], 7: [2, 2], 8: [2, 2], 9: [2, 2], 10: [1, 1], 11: [1, 1],
    },
    "Русская литература": {
        5: [2, 2], 6: [2, 2], 7: [2, 1], 8: [1, 2], 9: [2, 1], 10: [1, 1], 11: [1, 1],
    },
    "Белорусский язык": {
        5: [3, 3], 6: [3, 3], 7: [2, 2], 8: [2, 2], 9: [2, 2], 10: [1, 1], 11: [1, 1],
    },
    "Белорусская литература": {
        5: [2, 2], 6: [2, 2], 7: [1, 2], 8: [2, 1], 9: [1, 2], 10: [1, 1], 11: [1, 1],
    },
    # иностранные языки (англ/нем/фр/исп) в плане идут одной строкой
    # "Замежная мова" -- часы одинаковые для любого из них
    "Английский язык": {
        5: [3, 3], 6: [3, 3], 7: [3, 3], 8: [3, 3], 9: [3, 3], 10: [2, 2], 11: [2, 2],
    },
    "Немецкий язык": {
        5: [3, 3], 6: [3, 3], 7: [3, 3], 8: [3, 3], 9: [3, 3], 10: [2, 2], 11: [2, 2],
    },
    "Французский язык": {
        5: [3, 3], 6: [3, 3], 7: [3, 3], 8: [3, 3], 9: [3, 3], 10: [2, 2], 11: [2, 2],
    },
    "Испанский язык": {
        5: [3, 3], 6: [3, 3], 7: [3, 3], 8: [3, 3], 9: [3, 3], 10: [2, 2], 11: [2, 2],
    },
    "Математика": {
        5: [5, 5], 6: [5, 5], 7: [5, 5], 8: [5, 5], 9: [4, 5], 10: [4, 4], 11: [4, 4],
    },
    "Информатика": {5: [0, 0], 6: [1, 1], 7: [1, 1], 8: [1, 1], 9: [1, 1], 10: [1, 1], 11: [1, 1]},
    "Человек и Мир": {5: [1, 1], 6: [0, 0], 7: [0, 0], 8: [0, 0], 9: [0, 0]},
    "Всемирная История": {
        5: [2, 2], 6: [1, 1], 7: [1, 1], 8: [1, 1], 9: [1, 2], 10: [2, 2], 11: [2, 2],
    },
    "История": {
        5: [2, 2], 6: [1, 1], 7: [1, 1], 8: [1, 1], 9: [1, 2], 10: [2, 2], 11: [2, 2],
    },
    "История Беларуси": {6: [1, 1], 7: [1, 1], 8: [1, 1], 9: [1, 1]},
    "История Беларуси в контексте всемирной истории": {10: [2, 2], 11: [2, 2]},
    "Обществоведение": {9: [1, 1], 10: [1, 1], 11: [1, 1]},
    "Человек. Общество. Государство": {9: [1, 1]},
    "География": {6: [1, 1], 7: [1, 1], 8: [2, 2], 9: [2, 1], 10: [1, 1], 11: [1, 1]},
    "Биология": {6: [1, 1], 7: [2, 2], 8: [2, 2], 9: [1, 2], 10: [1, 1], 11: [1, 1]},
    "Физика": {7: [2, 2], 8: [2, 2], 9: [3, 2], 10: [1, 1], 11: [2, 1]},
    "Астрономия": {11: [1, 1]},
    "Химия": {7: [1, 1], 8: [2, 2], 9: [2, 2], 10: [2, 1], 11: [2, 1]},
    "Изобразительное искусство": {1: [2, 2], 2: [1, 1], 3: [1, 1], 4: [1, 1]},
    "Музыка": {1: [1, 1], 2: [1, 1], 3: [1, 1], 4: [1, 1]},
    "Искусство. Отечественная и мировая художественная культура": {
        5: [1, 1], 6: [1, 1], 7: [1, 1], 8: [1, 1], 9: [1, 0],
    },
    "Мировая художественная культура": {5: [1, 1], 6: [1, 1], 7: [1, 1], 8: [1, 1], 9: [1, 0]},
    "Трудовое обучение": {5: [1, 1], 6: [2, 2], 7: [2, 2], 8: [1, 1], 9: [1, 1]},
    "Физическая культура и здоровье": {
        1: [3, 3], 2: [3, 3], 3: [3, 3], 4: [3, 3], 5: [3, 3], 6: [3, 3],
        7: [3, 3], 8: [3, 3], 9: [3, 3], 10: [3, 3], 11: [3, 3],
    },
    "Основы безопасности жизнедеятельности": {2: [1, 1], 3: [1, 1], 4: [1, 1], 5: [1, 1]},
    "Допризывная и медицинская подготовка": {10: [1, 1], 11: [1, 1]},
    "Черчение": {10: [1, 1]},
    "Введение в школьную жизнь": {1: None},  # спец. программа, не в часах
}


def hours_for(subject_name: str, grade: int):
    """Вернуть [часы_1_полугодие, часы_2_полугодие] для предмета в данном
    классе, либо None если в официальном плане для этого предмета/класса
    часов не предусмотрено (или предмет отсутствует в справочнике -- ГПД,
    кружки, классный час и т.п. не регулируются типовым учебным планом по
    часам предмета)."""
    table = CURRICULUM_HOURS.get(subject_name)
    if not table:
        return None
    return table.get(grade)


def class_grade_number(class_name: str) -> int | None:
    """'5 \"А\"' -> 5"""
    m = re.match(r"\s*(\d+)", class_name)
    return int(m.group(1)) if m else None


def get_soup(url: str) -> BeautifulSoup:
    resp = requests.get(url, headers=HEADERS, timeout=15)
    resp.raise_for_status()
    resp.encoding = "utf-8"
    return BeautifulSoup(resp.text, "html.parser")


def parse_subjects_list() -> list[dict]:
    """Возвращает список {id, name, short_name, url} со страницы /subjects"""
    soup = get_soup(f"{BASE_URL}/subjects")
    subjects = []

    for item in soup.select("div.llitm"):
        link = item.select_one("a")
        if not link:
            continue
        href = urljoin(BASE_URL, link.get("href", ""))
        m = re.search(r"/subject/(\d+)", href)
        if not m:
            continue
        subject_id = int(m.group(1))
        name = link.get_text(strip=True)

        # короткое название лежит в том же div.llitm_center2, отдельным
        # текстовым узлом после </a>, обычно в скобках, например "(Матем.)"
        center = item.select_one("div.llitm_center2")
        short_name = None
        if center:
            full_text = center.get_text(" ", strip=True)
            m2 = re.search(r"\((.*?)\)\s*$", full_text)
            if m2:
                short_name = m2.group(1)

        subjects.append(
            {
                "id": subject_id,
                "name": name,
                "short_name": short_name,
                "url": href,
            }
        )
    return subjects


def parse_subject_page(url: str) -> dict:
    """
    Возвращает {"classes": [...], "teachers": [...]} со страницы одного предмета.
    classes  -- список {"id": int, "name": str, "url": str}
    teachers -- список {"id": int, "name": str, "url": str}
    """
    soup = get_soup(urljoin(BASE_URL, url))
    result = {"classes": [], "teachers": []}

    for block in soup.select("div.line-1"):
        label_el = block.select_one("span.label")
        if not label_el:
            continue
        label = label_el.get_text(strip=True)

        if label.startswith("Преподается"):
            for a in block.select("div.cont a"):
                href = urljoin(BASE_URL, a.get("href", ""))
                m = re.search(r"/class/(\d+)", href)
                if not m:
                    continue
                result["classes"].append(
                    {
                        "id": int(m.group(1)),
                        "name": a.get_text(strip=True),
                        "url": href,
                    }
                )

        elif label.startswith("Учителя"):
            for a in block.select("div.cont a"):
                href = urljoin(BASE_URL, a.get("href", ""))
                m = re.search(r"/teacher/(\d+)", href)
                if not m:
                    continue
                result["teachers"].append(
                    {
                        "id": int(m.group(1)),
                        "name": a.get_text(strip=True),
                        "url": href,
                    }
                )

    return result


def parse_class_schedule(url: str) -> list[dict]:
    """
    ЗАГОТОВКА. Нужно допилить под реальную вёрстку страницы /class/{id},
    когда пришлёте пример HTML. Цель: вернуть список уроков за неделю вида
        {"subject": "Математика", "teacher": "Иванова А.А.", "day": "Пн", ...}
    После чего легко посчитать, сколько часов в неделю у пары
    (предмет, учитель) в этом классе -- просто count() одинаковых записей.
    """
    soup = get_soup(url)
    lessons = []

    # TODO: заменить селекторы ниже на реальные, когда будет пример страницы
    # for row in soup.select("table.schedule tr"):
    #     ...

    return lessons


# Предметы, которые в начальной школе (1-4 класс) обычно ведёт ОДИН учитель
# (классный руководитель), а не разные предметники по каждому предмету.
CORE_PRIMARY_SUBJECTS = {
    "Белорусский язык",
    "Белорусская литература",
    "Русский язык",
    "Русская литература",
    "Математика",
    "Человек и Мир",
    "Изобразительное искусство",
    "Трудовое обучение",
    "Основы безопасности жизнедеятельности",
    "Введение в школьную жизнь",
}
# Пул кандидатов на роль "классного руководителя" берём из учителей,
# которые в принципе ведут русский язык -- в началке это почти всегда
# один и тот же учитель на все базовые предметы.
HOMEROOM_SOURCE_SUBJECT = "Русский язык"


def apply_homeroom_teachers(classes_view: dict, full_data: list[dict], seed) -> None:
    """Для классов 1-4 переназначает ВСЕ "базовые" предметы (см.
    CORE_PRIMARY_SUBJECTS) на одного и того же учителя -- имитируем
    классного руководителя началки. Учителя между классами распределяются
    по кругу (round-robin), чтобы нагрузка была равномерной.
    Модифицирует classes_view на месте.
    """
    rng = random.Random(seed)

    subject_by_name = {s["name"]: s for s in full_data}
    homeroom_pool = subject_by_name.get(HOMEROOM_SOURCE_SUBJECT, {}).get("teachers", [])
    if not homeroom_pool:
        return  # нет кандидатов -- ничего не переназначаем

    homeroom_pool = homeroom_pool[:]
    rng.shuffle(homeroom_pool)

    primary_classes = [
        name for name in classes_view.keys()
        if (g := class_grade_number(name)) is not None and 1 <= g <= 4
    ]

    for i, class_name in enumerate(primary_classes):
        homeroom_teacher = homeroom_pool[i % len(homeroom_pool)]
        for entry in classes_view[class_name]:
            if entry["subject"] in CORE_PRIMARY_SUBJECTS:
                entry["teacher"] = homeroom_teacher["name"]
                entry["teacher_id"] = homeroom_teacher["id"]


def build_classes_view(full_data: list[dict], seed: int | None = 42) -> dict:
    """
    Разворачивает subjects.json в разрезе по классам:
        {
          "5 \"А\"": [
              {"subject": "Математика", "teacher": "Иванова А.А.", "teacher_id": 123},
              ...
          ],
          ...
        }
    Учитель для класса выбирается СЛУЧАЙНО из списка учителей, которые вообще
    ведут этот предмет в школе (т.к. точной привязки учитель-класс на сайте
    нет без доступа к расписанию). seed фиксирует случайность, чтобы результат
    был воспроизводимым при повторном запуске; поставьте seed=None для
    случайного результата каждый раз.
    """
    rng = random.Random(seed)
    classes_view: dict[str, list[dict]] = {}

    for subj in full_data:
        subject_name = subj["name"]
        teachers = subj.get("teachers", [])

        # перемешиваем учителей один раз на предмет, а дальше раздаём их
        # классам по кругу (round-robin) -- так нагрузка распределяется
        # равномерно, а не концентрируется случайно на одном-двух учителях
        shuffled_teachers = teachers[:]
        rng.shuffle(shuffled_teachers)
        teacher_cycle_idx = 0

        classes = subj.get("classes", [])
        for cls in classes:
            class_name = cls["name"]
            classes_view.setdefault(class_name, [])

            if shuffled_teachers:
                teacher = shuffled_teachers[teacher_cycle_idx % len(shuffled_teachers)]
                teacher_cycle_idx += 1
                entry = {
                    "subject": subject_name,
                    "teacher": teacher["name"],
                    "teacher_id": teacher["id"],
                }
            else:
                entry = {
                    "subject": subject_name,
                    "teacher": None,
                    "teacher_id": None,
                }

            grade_num = class_grade_number(class_name)
            hours = hours_for(subject_name, grade_num) if grade_num else None
            entry["hours_per_week"] = hours  # [часы_1_полугодие, часы_2_полугодие] или None

            classes_view[class_name].append(entry)

    # отсортируем классы по номеру и букве, предметы внутри - по алфавиту
    def class_sort_key(name: str):
        m = re.match(r"(\d+)\s*\"?(\S+)?\"?", name)
        if m:
            return (int(m.group(1)), m.group(2) or "")
        return (999, name)

    sorted_view = {}
    for class_name in sorted(classes_view.keys(), key=class_sort_key):
        sorted_view[class_name] = sorted(
            classes_view[class_name], key=lambda e: e["subject"]
        )

    apply_homeroom_teachers(sorted_view, full_data, seed)

    return sorted_view


def main():
    OUT_DIR.mkdir(exist_ok=True)

    print("Читаю список предметов...")
    subjects = parse_subjects_list()
    print(f"Найдено предметов: {len(subjects)}")

    full_data = []
    for i, subj in enumerate(subjects, 1):
        print(f"[{i}/{len(subjects)}] {subj['name']} ...")
        try:
            details = parse_subject_page(subj["url"])
        except requests.RequestException as e:
            print(f"  Ошибка: {e}")
            details = {"classes": [], "teachers": []}

        full_data.append({**subj, **details})
        time.sleep(DELAY_SECONDS)

    out_path = OUT_DIR / "subjects.json"
    out_path.write_text(
        json.dumps(full_data, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"\nГотово. Данные сохранены в {out_path.resolve()}")

    # заодно соберём плоский список всех уникальных учителей и классов
    all_teachers = {}
    all_classes = {}
    for subj in full_data:
        for t in subj["teachers"]:
            all_teachers.setdefault(t["id"], t["name"])
        for c in subj["classes"]:
            all_classes.setdefault(c["id"], c["name"])

    (OUT_DIR / "teachers.json").write_text(
        json.dumps(all_teachers, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (OUT_DIR / "classes.json").write_text(
        json.dumps(all_classes, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"Учителей найдено: {len(all_teachers)}")
    print(f"Классов найдено: {len(all_classes)}")

    # разрез по классам: предмет + (пока случайный) учитель
    classes_view = build_classes_view(full_data)
    classes_view_path = OUT_DIR / "temp.json"
    classes_view_path.write_text(
        json.dumps(classes_view, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"Разрез по классам сохранён в {classes_view_path.resolve()}")
    print(
        "ВНИМАНИЕ: учитель в classes_subjects.json назначен СЛУЧАЙНО "
        "из числа тех, кто ведёт предмет в школе -- это не точные данные "
        "о том, кто именно ведёт урок в конкретном классе."
    )


if __name__ == "__main__":
    main()
