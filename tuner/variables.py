import subprocess
import tempfile
import pathlib
import numpy
import json
import os

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent

T_START = 100.0
T_END = 0.5

DEFAULT_BENCH = str(REPO_ROOT / "tuner" / "bench")
DEFAULT_POOL  = str(REPO_ROOT / "tuner" / "pool")


def solver():
    env = os.environ.get("SOLVER")

    if env:
        return str(pathlib.Path(env))

    preferred = "solve.exe" if os.name == "nt" else "solve"
    fallback  = "solve"     if os.name == "nt" else "solve.exe"

    for name in (preferred, fallback):
        p = REPO_ROOT / "src" / "modules" / name

        if p.exists():
            return str(p)

    return str(REPO_ROOT / "src" / "modules" / preferred)


SOLVER = solver()


def compute(iterations):
    return (T_END / T_START) ** (1.0 / max(iterations, 1))


DEFAULTS = {
    "equalLessons":               5,
    "notEqualsLessonsCountOnDay": 25,
    "lessonsEmptySlots":          200,
    "daysByHard":                 2,
    "teacherFreeTime":            5,
    "teacherSmallDay":            5,
    "groupBonus":                 10,
    "lessonShiftCrossing":        250,
    "profileGaps":                200,
    "classroomPriority":          50,
    "teacherLessonLimit":         25,
}

TUNABLE = [
    "equalLessons",
    "notEqualsLessonsCountOnDay",
    "daysByHard",
    "teacherFreeTime",
    "teacherSmallDay",
    "groupBonus",
    "profileGaps",
    "classroomPriority",
]

CRITERIA = {
    ("class",   "lessonsEmptySlots"):           3.0,
    ("class",   "equalLessons"):                2.0,
    ("class",   "notEqualsLessonsCountOnDay"):  1.5,
    ("class",   "daysByHard"):                  1.0,
    ("class",   "profileGaps"):                 2.0,
    ("teacher", "gapSum"):                      1.0,
    ("teacher", "teacherSmallDay"):             0.5,
    ("teacher", "teacherLessonLimit"):          2.0,
    ("teacher", "lessonShiftCrossing"):         3.0,
    ("teacher", "classroomPriority"):           0.5,
}

AGG = {
    ("class",   "equalLessons"):               {"mean": 0.5,  "p90": 0.30, "max": 0.20},
    ("class",   "notEqualsLessonsCountOnDay"): {"mean": 0.5,  "p90": 0.30, "max": 0.20},
    ("class",   "lessonsEmptySlots"):          {"mean": 0.4,  "p90": 0.35, "max": 0.25},
    ("class",   "daysByHard"):                 {"mean": 0.5,  "p90": 0.30, "max": 0.20},
    ("class",   "groupBonus"):                 {"mean": 0.5,  "p90": 0.30, "max": 0.20},
    ("class",   "profileGaps"):                {"mean": 0.4,  "p90": 0.35, "max": 0.25},
    ("teacher", "gapSum"):                     {"mean": 0.4,  "p90": 0.35, "max": 0.25},
    ("teacher", "teacherFreeTimeGapSq"):       {"mean": 0.2,  "p90": 0.40, "max": 0.20, "p95": 0.2},
    ("teacher", "teacherSmallDay"):            {"mean": 0.3,  "p90": 0.40, "max": 0.30},
    ("teacher", "teacherLessonLimit"):         {"max":  0.6,  "nz":  0.40},
    ("teacher", "lessonShiftCrossing"):        {"max":  0.6,  "nz":  0.40},
    ("teacher", "classroomPriority"):          {"mean": 0.5,  "p90": 0.30, "max": 0.20},
}


def AGGeights(src, key):
    try:
        return AGG[(src, key)]

    except KeyError:
        raise KeyError(
            f"AGG has no entry for ({src!r}, {key!r}). "
            f"Known keys: {sorted(AGG)}"
        )


def aggregates(var, agg_names):
    names = list(agg_names)

    var = numpy.asarray(var, float)

    if var.size == 0:
        return {n: 0.0 for n in names}

    out = {}

    for n in names:
        if   n == "mean":  out[n] = float(var.mean())
        elif n == "p50":   out[n] = float(numpy.quantile(var, 0.50))
        elif n == "p75":   out[n] = float(numpy.quantile(var, 0.75))
        elif n == "p90":   out[n] = float(numpy.quantile(var, 0.90))
        elif n == "p95":   out[n] = float(numpy.quantile(var, 0.95))
        elif n == "p99":   out[n] = float(numpy.quantile(var, 0.99))
        elif n == "max":   out[n] = float(var.max())
        elif n == "min":   out[n] = float(var.min())
        elif n == "std":   out[n] = float(var.std())
        elif n == "range": out[n] = float(var.max() - var.min())
        elif n == "nz":    out[n] = float((var > 0).mean())
        else:
            raise ValueError(f"unknown aggregate: {n}")

    return out


def run(settings, weights, seed, iterations, fair=100.0, cooling=None):
    if cooling is None:
        cooling = compute(iterations)

    with tempfile.TemporaryDirectory() as tmp:
        tmp = pathlib.Path(tmp)

        cmd = [
            SOLVER,
            "--seed", str(seed),
            "--iterations", str(iterations),
            "--cooling", repr(cooling),
            "--fair", repr(fair),
        ]

        if weights is not None:
            (tmp / "weights.json").write_text(json.dumps(weights, indent=4), encoding="utf-8")

            cmd += ["--weights", str(tmp / "weights.json")]

        cmd += ["--metrics", str(tmp / "metrics.json")]

        subprocess.run(cmd, check=True, capture_output=True)

        return json.loads((tmp / "metrics.json").read_text(encoding="utf-8"))


def reference(settings, count=10):
    runs = [run(settings, DEFAULTS, 1000 + s, 0) for s in range(count)]

    answer = {}

    for (src, key) in CRITERIA:
        aggs = AGGeights(src, key)
        per = [aggregates(r[src][key], aggs) for r in runs]

        answer[(src, key)] = {a: float(numpy.mean([x[a] for x in per])) for a in aggs}

    return answer


def quality(metrics, ref):
    total = wsum = 0.0

    for (src, key), weight in CRITERIA.items():
        aggs = AGGeights(src, key)
        agg  = aggregates(metrics[src][key], aggs)

        sm = used = 0.0

        for a, value in aggs.items():
            worst = ref[(src, key)].get(a, 0.0)

            if worst <= 0:
                continue

            sm += value * min(agg[a] / worst, 1.5)
            used += value

        if used:
            total += weight * sm / used
            wsum  += weight

    return total / wsum if wsum else 0.0


def reconstruct(metrics, weights, fair):
    total = weights["equalLessons"] * sum(metrics["class"]["equalLessons"]) + weights["notEqualsLessonsCountOnDay"] * sum(metrics["class"]["notEqualsLessonsCountOnDay"]) + weights["lessonsEmptySlots"] * sum(metrics["class"]["lessonsEmptySlots"]) + weights["daysByHard"] * sum(metrics["class"]["daysByHard"]) - weights["groupBonus"] * sum(metrics["class"]["groupBonus"]) + weights["profileGaps"] * sum(metrics["class"]["profileGaps"])

    for i in range(len(metrics["teacher"]["teacherFreeTimeGapSq"])):
        g = weights["teacherFreeTime"] * metrics["teacher"]["teacherFreeTimeGapSq"][i]

        total += g + g * g / fair
        total += weights["teacherSmallDay"] * metrics["teacher"]["teacherSmallDay"][i] + weights["teacherLessonLimit"]  * metrics["teacher"]["teacherLessonLimit"][i] + weights["lessonShiftCrossing"] * metrics["teacher"]["lessonShiftCrossing"][i] + weights["classroomPriority"] * metrics["teacher"]["classroomPriority"][i]

    return total
