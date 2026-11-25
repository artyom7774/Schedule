import natsort
import copy
import json
import os

EMPTY = "#"

DEFAULT_EDIT_ITERATIONS = 1000000


def emptyCell() -> dict:
    return {"subject": EMPTY, "teachers": [], "classrooms": [], "extra": []}


def key(day: int, lesson: int) -> str:
    return f"{day}-{lesson}"


def classNames(settings: dict) -> list:
    alphabet = "-АБВГДЕЖЗИКЛМНОПРСТУФХЦЧШЩЭЮЯ"

    result = []

    for i, count in enumerate(settings["classes"]["count"]):
        for number in range(count):
            result.append(f"{i + 1} {alphabet[number + 1]}")

    return result


def entries(cell: dict) -> list:
    if cell.get("subject", EMPTY) == EMPTY:
        return []

    result = [(cell["subject"], list(cell.get("teachers", [])), list(cell.get("classrooms", [])))]

    for extra in cell.get("extra", []):
        if extra.get("subject", EMPTY) == EMPTY:
            continue

        result.append((extra["subject"], list(extra.get("teachers", [])), list(extra.get("classrooms", []))))

    return result


def subjectsOf(cell: dict) -> list:
    return [subject for subject, _, _ in entries(cell)]


def cellFromEntries(items: list) -> dict:
    if not items:
        return emptyCell()

    subject, teachers, classrooms = items[0]

    cell = {"subject": subject, "teachers": list(teachers), "classrooms": list(classrooms), "extra": []}

    for subject, teachers, classrooms in items[1:]:
        cell["extra"].append({"subject": subject, "teachers": list(teachers), "classrooms": list(classrooms)})

    return cell


def getCell(answer: dict, cls: str, day: int, lesson: int) -> dict:
    try:
        return answer[cls][day][lesson]

    except (KeyError, IndexError, TypeError):
        return emptyCell()


def setCell(answer: dict, cls: str, day: int, lesson: int, cell: dict) -> None:
    answer[cls][day][lesson] = cell


def upgradeCell(settings: dict, cls: str, day: list, lesson: int) -> bool:
    cell = day[lesson]

    if not isinstance(cell, dict):
        day[lesson] = emptyCell()

        return True

    changed = False

    for name, default in (("subject", EMPTY), ("teachers", []), ("classrooms", []), ("extra", [])):
        if name not in cell or cell[name] is None:
            cell[name] = default

            changed = True

    if cell["subject"] != EMPTY and not cell["teachers"]:
        teachers = teachersFor(settings, cls, cell["subject"])

        if teachers:
            cell["teachers"] = teachers

            changed = True

    for extra in cell["extra"]:
        for name in ("teachers", "classrooms"):
            if name not in extra or extra[name] is None:
                extra[name] = []

                changed = True

        if extra.get("subject", EMPTY) != EMPTY and not extra["teachers"]:
            teachers = teachersFor(settings, cls, extra["subject"])

            if teachers:
                extra["teachers"] = teachers

                changed = True

    return changed


def normalize(settings: dict, answer: dict) -> bool:
    days = settings["working_days_per_week"]
    lessons = settings["max_lesson_count_per_day"]

    changed = False

    for cls in classNames(settings):
        data = answer.get(cls)

        if not isinstance(data, list):
            data = []

            changed = True

        while len(data) < days:
            data.append([])

            changed = True

        for day in range(days):
            if not isinstance(data[day], list):
                data[day] = []

                changed = True

            while len(data[day]) < lessons:
                data[day].append(emptyCell())

                changed = True

            for lesson in range(len(data[day])):
                if upgradeCell(settings, cls, data[day], lesson):
                    changed = True

        answer[cls] = data

    return changed


def teachersFor(settings: dict, cls: str, subject: str) -> list:
    result = []

    for name, teacher in settings["teachers"].items():
        for element in teacher.get("subjects", []):
            if element.get("subject") == subject and cls in element.get("classes", []):
                result.append(name)

                break

    return result


def plan(settings: dict, cls: str) -> dict:
    result = {}

    for subject, hours in settings["classes"]["lessons"].get(cls, {}).items():
        if hours > 0 and teachersFor(settings, cls, subject):
            result[subject] = hours

    return result


def placed(answer: dict, cls: str) -> dict:
    result = {}

    for day in answer.get(cls, []):
        for cell in day:
            for subject in subjectsOf(cell):
                result[subject] = result.get(subject, 0) + 1

    return result


def pool(settings: dict, answer: dict, cls: str) -> dict:
    have = placed(answer, cls)

    result = {}

    for subject, hours in plan(settings, cls).items():
        left = hours - have.get(subject, 0)

        if left > 0:
            result[subject] = left

    return result


def groups(settings: dict, cls: str) -> list:
    return [set(subjects) for subjects in settings.get("groups", {}).get(cls, {}).values()]


def canCombine(settings: dict, cls: str, subjects: list) -> bool:
    items = groups(settings, cls)

    if len(set(subjects)) != len(subjects):
        return False

    if not all(any(s in group for group in items) for s in subjects):
        return False

    return not any(sum(s in group for s in subjects) > 1 for group in items)


def removeLesson(answer: dict, cls: str, day: int, lesson: int) -> list:
    removed = subjectsOf(getCell(answer, cls, day, lesson))

    if removed:
        setCell(answer, cls, day, lesson, emptyCell())

    return removed


def addLesson(settings: dict, answer: dict, cls: str, day: int, lesson: int, subject: str) -> list:
    if pool(settings, answer, cls).get(subject, 0) <= 0:
        return None

    teachers = teachersFor(settings, cls, subject)

    current = entries(getCell(answer, cls, day, lesson))

    if current and canCombine(settings, cls, [s for s, _, _ in current] + [subject]):
        current.append((subject, teachers, []))

        setCell(answer, cls, day, lesson, cellFromEntries(current))

        return []

    replaced = [s for s, _, _ in current]

    setCell(answer, cls, day, lesson, cellFromEntries([(subject, teachers, [])]))

    return replaced


def swapLessons(answer: dict, cls: str, first: tuple, second: tuple) -> None:
    a = copy.deepcopy(getCell(answer, cls, first[0], first[1]))
    b = copy.deepcopy(getCell(answer, cls, second[0], second[1]))

    for cell in (a, b):
        cell["classrooms"] = []

        for extra in cell["extra"]:
            extra["classrooms"] = []

    setCell(answer, cls, first[0], first[1], b)
    setCell(answer, cls, second[0], second[1], a)


def teacherNames(settings: dict) -> list:
    return list(natsort.natsorted(settings["teachers"].keys()))


def teacherClasses(settings: dict, shifts: dict, teacher: str, shift: int = None) -> list:
    names = classNames(settings)

    found = set()

    for element in settings["teachers"].get(teacher, {}).get("subjects", []):
        for cls in element.get("classes", []):
            if cls not in names:
                continue

            if shift is not None and shifts.get(cls, 0) != shift:
                continue

            if settings["classes"]["lessons"].get(cls, {}).get(element["subject"], 0) > 0:
                found.add(cls)

    return [cls for cls in names if cls in found]


def teacherLessons(answer: dict, classes: list, teacher: str, day: int, lesson: int) -> list:
    result = []

    for cls in classes:
        for subject, teachers, classrooms in entries(getCell(answer, cls, day, lesson)):
            if teacher in teachers:
                result.append((cls, subject, classrooms))

    return result


def teacherSlot(settings: dict, teacher: str, shift: int, day: int, lesson: int):
    data = settings["teachers"].get(teacher, {})

    for name in ("free", "reserve"):
        slots = data.get(name, [])

        if shift < len(slots) and [day, lesson] in slots[shift]:
            return name

    return None


def teacherPools(settings: dict, pools: dict) -> dict:
    result = {teacher: [] for teacher in settings["teachers"]}

    for cls, subjects in pools.items():
        for subject, left in subjects.items():
            for teacher in teachersFor(settings, cls, subject):
                result[teacher].append((cls, subject, left))

    return result


def removeTeacherLesson(answer: dict, teacher: str, cls: str, day: int, lesson: int) -> list:
    current = entries(getCell(answer, cls, day, lesson))

    removed = [subject for subject, teachers, _ in current if teacher in teachers]

    if removed:
        setCell(answer, cls, day, lesson, cellFromEntries([item for item in current if teacher not in item[1]]))

    return removed


def swapTeacherLessons(answer: dict, classes: list, teacher: str, first: tuple, second: tuple) -> list:
    changed = [cls for cls in classes if teacherLessons(answer, [cls], teacher, first[0], first[1]) or teacherLessons(answer, [cls], teacher, second[0], second[1])]

    for cls in changed:
        swapLessons(answer, cls, first, second)

    return changed


def windows(settings: dict, answer: dict, shifts: dict) -> dict:
    days = settings["working_days_per_week"]
    lessons = settings["max_lesson_count_per_day"]

    step = lessons - max(int(settings.get("shift_crossing", 0)), 0)

    used = {}

    for teacher, data in settings["teachers"].items():
        used[teacher] = [set() for _ in range(days)]

        for shift, slots in enumerate(data.get("reserve", [])):
            for day, lesson in slots:
                if day < days and lesson < lessons:
                    used[teacher][day].add(shift * step + lesson)

    for cls in classNames(settings):
        shift = shifts.get(cls, 0)

        for day in range(days):
            for lesson in range(lessons):
                for _, teachers, _ in entries(getCell(answer, cls, day, lesson)):
                    for teacher in teachers:
                        if teacher in used:
                            used[teacher][day].add(shift * step + lesson)

    result = {}

    for teacher, week in used.items():
        result[teacher] = 0

        for positions in week:
            if len(positions) >= 2:
                result[teacher] += (max(positions) - min(positions) + 1) - len(positions)

    return result


def crossingAllowed(settings: dict, first: str, second: str) -> bool:
    crossing = settings.get("crossing", {})

    if first == second:
        return crossing.get(first, {}).get(first, 0) == 1

    one = crossing.get(first, {}).get(second)
    two = crossing.get(second, {}).get(first)

    return not (one == 0 or two == 0 or one is False or two is False)


def conflicts(settings: dict, answer: dict, shifts: dict) -> dict:
    result = {}

    days = settings["working_days_per_week"]
    lessons = settings["max_lesson_count_per_day"]

    busy = {}

    def add(cls, day, lesson, reason):
        result.setdefault((cls, day, lesson), [])

        if reason not in result[(cls, day, lesson)]:
            result[(cls, day, lesson)].append(reason)

    for cls in classNames(settings):
        shift = shifts.get(cls, 0)

        for day in range(days):
            seen = {}

            for lesson in range(lessons):
                for subject, teachers, _ in entries(getCell(answer, cls, day, lesson)):
                    for teacher in teachers:
                        busy.setdefault((teacher, shift, day, lesson), set()).add((cls, lesson))

                        data = settings["teachers"].get(teacher, {})

                        for name in ("free", "reserve"):
                            slots = data.get(name, [])

                            if shift < len(slots) and [day, lesson] in slots[shift]:
                                add(cls, day, lesson, ("unavailable", teacher))

                    seen.setdefault(subject, []).append(lesson)

            subjects = list(seen.keys())

            for i, first in enumerate(subjects):
                if len(seen[first]) > 1 and not crossingAllowed(settings, first, first) and settings["classes"]["lessons"].get(cls, {}).get(first, 0) < days + 1:
                    for lesson in seen[first]:
                        add(cls, day, lesson, ("repeat", first))

                for second in subjects[i + 1:]:
                    if not crossingAllowed(settings, first, second):
                        for lesson in seen[first] + seen[second]:
                            add(cls, day, lesson, ("pair", f"{first} / {second}"))

    for (teacher, shift, day, lesson), places in busy.items():
        if len({cls for cls, _ in places}) > 1:
            for cls, _ in places:
                add(cls, day, lesson, ("busy", teacher))

    return result


def partial(settings: dict, answer: dict, free: dict) -> dict:
    result = copy.deepcopy(settings)

    result["constants"] = {}
    result["blocked"] = {}

    days = settings["working_days_per_week"]
    lessons = settings["max_lesson_count_per_day"]

    for cls in classNames(settings):
        pinned = {}
        gaps = []

        for day in range(days):
            for lesson in range(lessons):
                if (day, lesson) in free.get(cls, set()):
                    continue

                subjects = subjectsOf(getCell(answer, cls, day, lesson))

                if not subjects:
                    gaps.append(key(day, lesson))

                elif len(subjects) == 1:
                    pinned[key(day, lesson)] = subjects[0]

                else:
                    pinned[key(day, lesson)] = subjects

        result["constants"][cls] = pinned
        result["blocked"][cls] = gaps

    return result


def difference(before: dict, after: dict) -> int:
    count = 0

    for cls, data in before.items():
        for day in range(len(data)):
            for lesson in range(len(data[day])):
                if subjectsOf(data[day][lesson]) != subjectsOf(getCell(after, cls, day, lesson)):
                    count += 1

    return count


def solver() -> str:
    return "src/modules/solve.exe" if os.name == "nt" else "./src/modules/solve"


def loadParameters(path: str) -> dict:
    try:
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file).get("parameters", {})

    except (FileNotFoundError, ValueError):
        return {}


def saveParameter(path: str, name: str, value) -> None:
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)

    data.setdefault("parameters", {})[name] = value

    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def localCooling(parameters: dict, iterations: int) -> float:
    full = max(int(parameters.get("iterations", 100000000)), 1)
    cooling = float(parameters.get("cooling", 0.9999999))

    return min(cooling ** (full / max(iterations, 1)), 0.9999999)
