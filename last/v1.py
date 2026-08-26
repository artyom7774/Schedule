from pprint import pprint as vprint

import argparse
import random
import numba
import json
import copy
import math

parser = argparse.ArgumentParser()

parser.add_argument('--view', type=int, choices=[0, 1], default=1)

args = parser.parse_args()

random.seed(623412352)


class Class:
    def __init__(self, classes, information, now = None):
        self.classes = classes
        self.information = information

        if now is None:
            self.now = [[[] for _ in range(5)], [[] for _ in range(5)]]

        else:
            self.now = now

    def __deepcopy__(self, memo):
        return Class(self.classes, self.information, copy.deepcopy(self.now))

    def init(self):
        queue = [[], []]

        for i, element in enumerate(self.information):
            if element["hours"] is None:
                continue

            for pos in range(2):
                for _ in range(element["hours"][pos]):
                    queue[pos].append({
                        "subject": element["subject"],
                        "teacher": element["teacher"],
                    })


        for pos in range(2):
            while queue[pos]:
                position = random.randint(0, 4)
                use = random.choice(queue[pos])

                flag = (use["teacher"], pos, position, len(self.now[pos][position])) not in teachers

                if not flag:
                    continue

                teachers.add((use["teacher"], pos, position, len(self.now[pos][position])))
                self.now[pos][position].append(use)

                queue[pos].remove(use)

            for position in range(0, 5):
                while len(self.now[pos][position]) < 10:
                    self.now[pos][position].append(None)

    def move(self, pos, day1, lesson1, day2, lesson2):
        days = self.now[pos]

        teacher1 = days[day1][lesson1]["teacher"] if days[day1][lesson1] is not None else None
        teacher2 = days[day2][lesson2]["teacher"] if days[day2][lesson2] is not None else None

        flag = (teacher2, pos, day1, lesson1) not in teachers and (teacher1, pos, day2, lesson2) not in teachers

        if not flag:
            return False

        days[day1][lesson1], days[day2][lesson2] = days[day2][lesson2], days[day1][lesson1]

        return True

    def view(self):
        return self.now


with open("data/main.json", "r", encoding="utf-8") as file:
    data = json.load(file)

teachers = set()
classes = {}
answers = []

keys = []

for key, value in data["classes"].items():
    keys.append(key)

random.shuffle(keys)

for i, key in enumerate(keys):
    classes[key] = Class(classes, data["classes"][key])
    classes[key].init()

    print(str(i + 1) if i > 9 else f"0{i + 1}", "/", len(keys), ":", key)

# vprint(classes["5 \"Г\""].view(), indent=4, width=200)

"""
for pos in range(2):
    nx = 0

    for element in classes["5 \"Г\""].now[pos]:
        nx += len(element)

    print(nx)
"""


class Functions:
    @staticmethod
    @numba.njit(fastmath=True)
    def not_equals_lessons_count_on_day(lenghts):
        avr = sum(lenghts) / len(lenghts)

        value = sum([(element - avr) ** 2 for element in lenghts])

        return 10 * value ** 1.7

    @staticmethod
    def equal_lessons(lessons):
        value = len(lessons) - len(set(lessons))

        return 10 * value ** 2

    @staticmethod
    def lessons_order(lessons):
        value = lessons.count("-1")

        return 500 * value ** 2


def getClassPoints(value):
    points = {
        "equal-lessons": 0,
        "not-equals-lessons-count-on-day": 0,
        "lessons-order": 0
    }

    for pos in range(2):
        for day in value.now[pos]:
            end = 0

            for i, element in enumerate(day):
                if element is not None:
                    end = i

            lessons = [element["subject"] if element else "-1" for i, element in enumerate(day) if i <= end]

            points["equal-lessons"] += Functions.equal_lessons(lessons)
            points["lessons-order"] += Functions.lessons_order(lessons)

        points["not-equals-lessons-count-on-day"] += Functions.not_equals_lessons_count_on_day([len([element for element in day if element]) for day in value.now[pos]])

    return points


def getClassesPoints(values):
    points = {
        "equal-lessons": 0,
        "not-equals-lessons-count-on-day": 0,
        "lessons-order": 0
    }

    for value in values.values():
        now = getClassPoints(value)

        for k, v in now.items():
            points[k] += v

    return points


def getClassesTotal(values):
    ans = 0

    for key, value in getClassesPoints(values).items():
        ans += value

    return ans


def getClassTotal(value):
    ans = 0

    for key, value in getClassPoints(value).items():
        ans += value

    return ans


def solve():
    global classes, teachers

    total = getClassesTotal(classes)

    temperature = 100

    equal = 0

    for iter in range(1_000_000):
        temperature *= 0.999998

        pos = random.randint(0, 1)
        key = random.choice(data["class"])

        day1 = random.randint(0, 4)
        day2 = random.randint(0, 4)

        lesson1 = random.randint(0, len(classes[key].now[pos][day1]) - 1)
        lesson2 = random.randint(0, len(classes[key].now[pos][day2]) - 1)

        cell1 = classes[key].now[pos][day1][lesson1]
        cell2 = classes[key].now[pos][day2][lesson2]

        teacher1 = classes[key].now[pos][day1][lesson1]["teacher"] if classes[key].now[pos][day1][lesson1] else None
        teacher2 = classes[key].now[pos][day2][lesson2]["teacher"] if classes[key].now[pos][day2][lesson2] else None

        last = getClassTotal(classes[key])

        if classes[key].move(pos, day1, lesson1, day2, lesson2):
            now = getClassTotal(classes[key])

            delta = now - last

            if delta < 0 or random.random() < math.exp(-delta / temperature):
                total = total - last + now

                if teacher1 is not None:
                    teachers.remove((teacher1, pos, day1, lesson1))
                    teachers.add((teacher1, pos, day2, lesson2))

                if teacher2 is not None:
                    teachers.remove((teacher2, pos, day2, lesson2))
                    teachers.add((teacher2, pos, day1, lesson1))

                equal = 0 if delta > 0 else equal + 1

            else:
                classes[key].now[pos][day1][lesson1] = cell1
                classes[key].now[pos][day2][lesson2] = cell2

                equal += 1

        else:
            equal += 1

        if equal == 1000:
            temperature = max(20, temperature)

            equal = 0

            print()
            print("[EQUAL]", iter + 1, temperature, total, equal)
            vprint(getClassesPoints(classes), width=200)

            answers.append(classes)

        if (iter + 1) % 1000 == 0:
            print()
            print("[PRINT]", iter + 1, temperature, total, equal)

            vprint(getClassesPoints(classes), width=200)

    answers.append(classes)

    for value in classes.values():
        for pos in range(2):
            for i in range(5):
                enter = 0

                for j, element in enumerate(value.now[pos][i]):
                    if element is not None:
                        enter = j

                value.now[pos][i] = value.now[pos][i][:enter + 1]


solve()

cnt = {}

for i in range(20):
    cnt[i] = 0

for value in classes.values():
    for pos in range(2):
        for i in range(5):
            cnt[len([element for element in value.now[pos][i] if element])] += 1

print(cnt)

if args.view == 1:
    from display_python import *

    for cls in answers:
        root = tk.Tk()
        app = ScheduleGUI(root, cls)
        root.mainloop()
