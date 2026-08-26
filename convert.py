import json
import os


with open("parser/temp.json", "r", encoding="utf-8") as file:
    data = json.load(file)

main = {

}

subjects = set()

for key, value in data.items():
    main[key] = [

    ]

    for element in value:
        main[key].append({
            "subject": element["subject"],
            "teacher": element["teacher"],
            "hours": element["hours_per_week"][0] if element["hours_per_week"] else None
        })

        subjects.add(element["subject"])

if not os.path.exists("data"):
    os.mkdir("data")

with open("data/lessons.json", "w+", encoding="utf-8") as file:
    json.dump(main, file, indent=4, ensure_ascii=False)

print(main)

with open("parser/teachers.json", "r", encoding="utf-8") as file:
    v = json.load(file)

out = []

for value in v.values():
    out.append(value)

with open("data/teachers.json", "w+", encoding="utf-8") as file:
    json.dump(out, file, indent=4, ensure_ascii=False)

with open("data/subjects.json", "w+", encoding="utf-8") as file:
    json.dump(list(subjects), file, indent=4, ensure_ascii=False)

with open("data/classes.json", "w+", encoding="utf-8") as file:
    json.dump([element for element in list(data.keys()) if element[0] not in ("3", "4")], file, indent=4, ensure_ascii=False)
