from concurrent.futures import ThreadPoolExecutor, as_completed

import subprocess
import requests
import optuna
import random
import json
import time
import os

PATH_EXE = "solve.exe"
PATH_STUDY_DB = "learning/study.db"
PATH_BEST = "learning/best.json"

TRIALS = 1000
ITERATIONS = 5000000
WORKERS = 2

API_URL = "https://openrouter.ai/api/v1/chat/completions"
API_KEY = "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"

MAX_RETRIES = 12

SLEEP_BASE = 1
SLEEP_MAX = 300


prompt = lambda schedule: f"""
Ты — эксперт по школьным расписаниям. Оцени качество расписания ниже.

Относительная сложность каждого предмета: {json.load(open("data/hards.json", "r", encoding="utf-8"))}

Расписание:
{json.dumps(schedule, ensure_ascii=False, indent=2)}

Оцени по шкале от 1 (очень плохое) до 10 (отличное). Учитывай реальное удобстводля учеников и учителей, а не только числа выше.
Будь достаточно строг к тому что читаешь

Ответь СТРОГО в формате: одно число от 1 до 10, без пояснений.
"""


def request(payload: dict) -> dict:
    sleep = SLEEP_BASE

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            resp = requests.post(
                API_URL,
                headers={
                    "Authorization": f"Bearer {API_KEY}",
                    "Content-Type": "application/json",
                },
                json=payload,
                timeout=120,
            )

            if resp.status_code == 429:
                retry = resp.headers.get("Retry-After")

                if retry is not None:
                    try:
                        wait = float(retry)
                        
                    except ValueError:
                        wait = sleep
                        
                else:
                    wait = sleep

                time.sleep(wait)
                
                sleep = min(sleep * 2, SLEEP_MAX)

                print("sleep:", sleep)
                
                continue

            resp.raise_for_status()
            return resp.json()

        except requests.RequestException as e:
            print("sleep:", sleep, f"error:", repr(e))

            time.sleep(sleep)

            sleep = min(sleep * 2, SLEEP_MAX)

    raise RuntimeError()


def run(weights: dict, iterations: int) -> dict:
    id = random.randint(1000000000, 9999999999)

    with open(f"learning/weights/{id}.json", "w", encoding="utf-8") as f:
        json.dump(weights, f, indent=4)

    result = subprocess.run(
        [PATH_EXE, "--iterations", str(iterations), "--weights", f"learning/weights/{id}.json", "--output", f"learning/answer/{id}.json"],
        capture_output=True,
        text=True,
        timeout=600
    )

    if result.returncode != 0:
        raise RuntimeError(f"solve.exe завершился с ошибкой:\n{result.stderr}")

    return id


def solve(text: str) -> tuple[str, dict]:
    data = request({
        "model": "stealth/ox-alpha",
        "messages": [{"role": "user", "content": text}],
        "temperature": 0,
    })

    content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
    usage = data.get("usage", {})

    return content, usage


def parse(text: str) -> int:
    sleep = 1

    for attempt in range(5):
        try:
            answer, usage = solve(text)
            
            return int(answer.split()[0])
        
        except (KeyError, IndexError, ValueError) as e:
            time.sleep(sleep)
            sleep *= 2

    raise RuntimeError()


def grade(weights: dict, id: int) -> float:
    with open(f"learning/answer/{id}.json", "r", encoding="utf-8") as file:
        schedule = json.load(file)

    for name, value in schedule.items():
        for i in range(len(value)):
            schedule[name][i] = [element for element in value[i] if not (element["subject"] == "#" and element["teacher"] == "#")]

    text = prompt(schedule)

    scores = []

    with ThreadPoolExecutor(max_workers=WORKERS) as executor:
        futures = [executor.submit(parse, text) for _ in range(WORKERS)]

        for future in as_completed(futures):
            scores.append(future.result())

    score = sum(scores) / len(scores)

    print(f"scores: {scores}, avg: {score:.2f}")

    return -score


def objective(trial: optuna.Trial) -> float:
    weights = {
        "lessonsOrder":                         200.0,
        "equalLessons":                         trial.suggest_float("equalLessons", 1, 50, log=True),
        "notEqualsLessonsCountOnDay":           trial.suggest_float("notEqualsLessonsCountOnDay", 0.1, 50, log=True),
        "daysByHard":                           trial.suggest_float("daysByHard", 1, 50, log=True),
        "teacherFreeTime":                      trial.suggest_float("teacherFreeTime", 1, 50, log=True),

        "lessonsOrderCapacity":                 1.0,
        "equalLessonsCapacity":                 1.0,  # trial.suggest_float("equalLessonsCapacity", 0.5, 2.5)
        "notEqualsLessonsCountOnDayCapacity":   1.0,  # trial.suggest_float("notEqualsCapacity", 0.5, 2.5)
        "daysByHardCapacity":                   1.0,  # trial.suggest_float("daysByHardCapacity", 0.5, 2.5)
        "teacherFreeTimeCapacity":              1.0,  # trial.suggest_float("teacherFreeTimeCapacity", 0.5, 2.5)
    }

    id = run(weights, ITERATIONS)

    return grade(weights, id)


def callback(study, trial):
    print(f"Trial {trial.number} finished with value: {-trial.value}")


def main():
    os.makedirs("learning", exist_ok=True)

    optuna.logging.set_verbosity(optuna.logging.WARNING)

    study = optuna.create_study(
        study_name="program",
        storage=f"sqlite:///{PATH_STUDY_DB}",
        load_if_exists=True,
        direction="minimize",
        sampler=optuna.samplers.TPESampler(seed=os.getpid()),
    )

    study.optimize(objective, n_trials=TRIALS, n_jobs=4, show_progress_bar=False, callbacks=[callback])

    with open(PATH_BEST, "w", encoding="utf-8") as file:
        json.dump(study.best_params, file, indent=4, ensure_ascii=False)

    print(json.dumps(study.best_params, indent=4, ensure_ascii=False))


if __name__ == "__main__":
    main()
