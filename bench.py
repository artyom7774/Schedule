#!/usr/bin/env python3

from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib

import numpy as np

import subprocess
import argparse
import hashlib
import time
import json
import csv
import sys
import os
import re

from src.modules.translate import translate, language

T_START = 100.0
DEFAULT_COOLING = 0.9999999
DEFAULT_ITERS = 100_000_000
DEFAULT_T_END = T_START * DEFAULT_COOLING ** DEFAULT_ITERS
DEFAULT_KEMPE = 20
LANGS = ["ru", "en", "by"]

COMPONENTS = [
    "equalLessons",
    "notEqualsLessonsCountOnDay",
    "lessonsEmptySlots",
    "daysByHard",
    "teacherFreeTime",
    "teacherSmallDay",
    "groupBonus",
    "lessonShiftCrossing",
    "profileGaps",
    "classroomPriority",
    "teacherLessonLimit"
]

N_COMP = len(COMPONENTS)

PRINT_RE = re.compile(r"^\[PRINT\]\s+(\d+)\s+(\S+)\s+(\S+)\s*\|\s*(.*)$")
FINAL_RE = re.compile(r"^(\d+)\s+(\S+)\s*$")

SPECS = [
    ("class", "lessonsEmptySlots", "bench.spec.class_gaps"),
    ("class", "equalLessons", "bench.spec.class_repeats"),
    ("class", "notEqualsLessonsCountOnDay", "bench.spec.class_variance"),
    ("teacher", "gapSum", "bench.spec.teacher_gaps"),
    ("teacher", "teacherSmallDay", "bench.spec.teacher_small_day"),
    ("teacher", "teacherLessonLimit", "bench.spec.teacher_limit")
]


def t(key, **kw):
    text = translate(key)

    return text.format(**kw) if kw else text


def compTitle(key):
    return t(f"bench.comp.{key}")


def tof(text):
    try:
        return float(text)

    except ValueError:
        return float("nan")


class Cfg:
    def __init__(self, iters, kempe, seed, tEnd, tag, printEvery=100_000):
        self.iters = iters
        self.kempe = kempe
        self.seed = seed
        self.tEnd = tEnd
        self.tag = tag
        self.printEvery = printEvery

    @property
    def cooling(self):
        return (self.tEnd / T_START) ** (1.0 / self.iters)

    @property
    def key(self):
        return f"{self.tag}_it{self.iters}_k{self.kempe}_s{self.seed}_te{self.tEnd:.4g}_p{self.printEvery}"


class Run:
    def __init__(self, cfg, iters, temp, total, comps, finalTotal, moves, wall, warnings, metrics, cached):
        self.cfg = cfg
        self.iters = iters
        self.temp = temp
        self.total = total
        self.comps = comps
        self.finalTotal = finalTotal
        self.moves = moves
        self.wall = wall
        self.warnings = warnings
        self.metrics = metrics
        self.cached = cached


def parseRun(cfg, text, metPath, wall, cached):
    iters = []
    temps = []
    totals = []
    comps = []

    finalMoves = None
    finalTotal = None
    warns = 0

    for raw in text.splitlines():
        line = raw.strip()
        match = PRINT_RE.match(line)

        if match:
            iters.append(int(match.group(1)))
            temps.append(tof(match.group(2)))
            totals.append(tof(match.group(3)))

            values = [tof(value) for value in match.group(4).split()]
            values = (values + [float("nan")] * N_COMP)[:N_COMP]

            comps.append(values)

            continue

        if line.startswith("[WARNING]"):
            warns += 1

            continue

        match = FINAL_RE.match(line)

        if match:
            finalMoves = int(match.group(1))
            finalTotal = tof(match.group(2))

    if finalTotal is None:
        tail = "\n".join(text.splitlines()[-10:])

        raise RuntimeError(f"No final line in solver output. Output tail:\n{tail}")

    metrics = None

    if metPath.exists():
        try:
            metrics = json.loads(metPath.read_text(encoding="utf-8"))

        except Exception:
            metrics = None

    return Run(
        cfg,
        np.array(iters, dtype=float),
        np.array(temps, dtype=float),
        np.array(totals, dtype=float),
        np.array(comps, dtype=float).reshape(-1, N_COMP),
        finalTotal,
        finalMoves or 0,
        wall,
        warns,
        metrics,
        cached
    )


def runOne(cfg, solver, inp, weights, root, logs, force):
    logPath = logs / f"{cfg.key}.log"
    metPath = logs / f"{cfg.key}.metrics.json"
    metaPath = logs / f"{cfg.key}.meta.json"

    if not force and logPath.exists() and metPath.exists() and metaPath.exists():
        wall = json.loads(metaPath.read_text(encoding="utf-8"))["wall"]
        text = logPath.read_text(encoding="utf-8", errors="replace")

        return parseRun(cfg, text, metPath, wall, True)

    cmd = [
        str(solver),
        "--input", str(inp),
        "--iterations", str(cfg.iters),
        "--cooling", f"{cfg.cooling:.15f}",
        "--seed", str(cfg.seed),
        "--kempe-chance", str(cfg.kempe),
        "--print", str(cfg.printEvery),
        "--metrics", str(metPath)
    ]

    if weights:
        cmd += ["--weights", str(weights)]

    start = time.perf_counter()
    proc = subprocess.run(cmd, cwd=str(root), capture_output=True)
    wall = time.perf_counter() - start

    text = proc.stdout.decode("utf-8", errors="replace")

    if proc.returncode != 0:
        error = proc.stderr.decode("utf-8", errors="replace")

        raise RuntimeError(f"solver exited with code {proc.returncode}\ncommand: {' '.join(cmd)}\n{error}\n{text[-800:]}")

    logPath.write_text(text, encoding="utf-8")
    metaPath.write_text(json.dumps({"wall": wall, "cmd": cmd}, ensure_ascii=False), encoding="utf-8")

    return parseRun(cfg, text, metPath, wall, False)


def findSolver(arg):
    variants = [arg] if arg else ["src/modules/solve.exe", "src/modules/solve", "solve.exe", "solve"]

    for variant in variants:
        path = Path(variant)

        if path.is_file():
            return path.resolve()

    sys.exit(f"Solver not found. Specify the path: --solver src/modules/solve.exe\nSearched: {', '.join(map(str, variants))}")


def findInput(arg):
    if arg:
        path = Path(arg)

        if not path.is_file():
            sys.exit(f"File not found: {arg}")

        return path.resolve()

    for variant in ["settings.json", "src/modules/settings.json", "data/settings.json", "last/settings.json", "src/settings.json"]:
        if Path(variant).is_file():
            print(f"[i] input found automatically: {variant}")

            return Path(variant).resolve()

    skip = {"bench", "node_modules", ".git", "__pycache__"}

    for path in Path(".").rglob("settings*.json"):
        if not (set(path.parts) & skip):
            print(f"[i] input found automatically: {path}")

            return path.resolve()

    sys.exit("settings.json not found. Specify it explicitly: --input path/to/settings.json")


def makeTag(inp, weights, solver):
    md5 = hashlib.md5()
    md5.update(inp.read_bytes())

    if weights:
        md5.update(weights.read_bytes())

    md5.update(str(solver.stat().st_mtime_ns).encode())

    return md5.hexdigest()[:8]


def makeCfgs(seeds, iters, kempe, tEnd, tag, printEvery):
    return [Cfg(iters, kempe, seed, tEnd, tag, printEvery) for seed in seeds]


def stack(runs):
    length = min(len(run.iters) for run in runs)

    if length == 0:
        return None

    x = runs[0].iters[:length]
    temp = runs[0].temp[:length]
    total = np.stack([run.total[:length] for run in runs])
    comps = np.stack([run.comps[:length] for run in runs])

    return x, temp, total, comps


def band(ax, x, arr, label=None, color=None, lw=2.0, alpha=0.18):
    med = np.nanmedian(arr, axis=0)
    low = np.nanmin(arr, axis=0)
    high = np.nanmax(arr, axis=0)

    line, = ax.plot(x, med, lw=lw, label=label, color=color)
    ax.fill_between(x, low, high, alpha=alpha, color=line.get_color())

    return line


def describe(runs):
    cfg = runs[0].cfg

    return t("bench.describe", runs=len(runs), iters=f"{cfg.iters / 1e6:g}", kempe=cfg.kempe)


def finish(fig, name, out, show):
    fig.tight_layout()

    path = out / name
    fig.savefig(path, dpi=150)

    print(f"   saved {path}")

    if not show:
        plt.close(fig)


def figConvergence(runs, out, show):
    data = stack(runs)

    if data is None:
        print("   [!] no [PRINT] lines (is --print-every larger than the iteration count?), convergence plot skipped")

        return

    x, temp, total, _ = data
    xMil = x / 1e6

    fig, ax1 = plt.subplots(figsize=(9, 5))

    for row in total:
        ax1.plot(xMil, row, lw=0.8, alpha=0.35, color="tab:blue")

    band(ax1, xMil, total, label=t("bench.conv.median_band"), color="tab:blue")

    ax1.set_xlabel(t("bench.iterations_m"))
    ax1.set_ylabel(t("bench.conv.objective"))
    ax1.set_title(t("bench.conv.title"))
    ax1.legend(loc="upper center")

    ax1Temp = ax1.twinx()
    ax1Temp.plot(xMil, temp, "--", color="gray", lw=1, label=t("bench.conv.temperature_legend"))
    ax1Temp.set_yscale("log")
    ax1Temp.set_ylabel(t("bench.conv.temperature_log"))
    ax1Temp.grid(False)

    fig.suptitle(t("bench.conv.suptitle", desc=describe(runs)))

    finish(fig, "convergence.png", out, show)


def figComponents(runs, out, show):
    data = stack(runs)

    if data is None:
        return

    x, _, total, comps = data
    xMil = x / 1e6

    fig, axes = plt.subplots(3, 4, figsize=(17, 10), sharex=True)

    for i, key in enumerate(COMPONENTS):
        ax = axes.flat[i]

        band(ax, xMil, comps[:, :, i], lw=1.8, color=f"C{i % 10}")

        ax.set_title(f"{compTitle(key)}\n({key})", fontsize=9)

        if i >= 8:
            ax.set_xlabel(t("bench.iterations_m"))

    info = axes.flat[N_COMP]
    info.axis("off")

    finals = np.array([run.finalTotal for run in runs])

    info.text(
        0.0, 0.95,
        t(
            "bench.comp.info",
            desc=describe(runs),
            med=f"{np.median(finals):,.0f}",
            low=f"{finals.min():,.0f}",
            high=f"{finals.max():,.0f}"
        ),
        va="top", fontsize=10
    )

    fig.suptitle(t("bench.comp.suptitle"), fontsize=13)

    finish(fig, "components.png", out, show)


def figTemperature(runs, out, show):
    data = stack(runs)

    if data is None:
        return

    _, temp, total, _ = data

    fig, ax1 = plt.subplots(figsize=(9, 5))

    band(ax1, temp, total, color="tab:red")

    ax1.set_xscale("log")
    ax1.invert_xaxis()
    ax1.set_xlabel(t("bench.temp.xlabel"))
    ax1.set_ylabel("total")
    ax1.set_title(t("bench.temp.title"))

    fig.suptitle(t("bench.temp.suptitle", desc=describe(runs)))

    finish(fig, "temperature.png", out, show)


def figSeeds(runs, out, show):
    finals = np.array([run.finalTotal for run in runs])

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5), gridspec_kw={"width_ratios": [1, 2]})

    ax1.boxplot([finals], widths=0.5, showmeans=True)

    rng = np.random.default_rng(0)
    xs = 1 + (rng.random(len(finals)) - 0.5) * 0.25

    ax1.scatter(xs, finals, color="tab:blue", zorder=3)

    for xj, y, run in zip(xs, finals, runs):
        ax1.annotate(f"s{run.cfg.seed}", (xj, y), xytext=(6, 0), textcoords="offset points", fontsize=8)

    ax1.set_xticks([1])
    ax1.set_xticklabels([t("bench.final_total")])

    cv = finals.std() / abs(finals.mean()) * 100 if finals.mean() else float("nan")

    ax1.set_title(t("bench.seeds.title", cv=f"{cv:.1f}"))
    ax1.set_ylabel("total")

    last = [run.comps[-1] for run in runs if len(run.comps)]

    if last:
        comps = np.stack(last)

        mean = np.nanmean(comps, axis=0)
        std = np.nanstd(comps, axis=0)

        names = [compTitle(key) for key in COMPONENTS]
        ypos = np.arange(N_COMP)
        colors = ["tab:green" if value < 0 else "tab:orange" for value in mean]

        ax2.barh(ypos, mean, xerr=std, color=colors, alpha=0.85)
        ax2.set_yticks(ypos)
        ax2.set_yticklabels(names)
        ax2.invert_yaxis()
        ax2.axvline(0, color="k", lw=0.8)
        ax2.set_xlabel(t("bench.seeds.xlabel2"))
        ax2.set_title(t("bench.seeds.title2"))

    fig.suptitle(t("bench.seeds.suptitle", desc=describe(runs)))

    finish(fig, "seeds.png", out, show)


def figKempe(groups, out, show):
    if len(groups) < 2:
        return

    ks = sorted(groups)

    fig, ax1 = plt.subplots(figsize=(9, 5))

    for i, k in enumerate(ks):
        data = stack(groups[k])

        if data is None:
            continue

        x, _, total, _ = data

        band(ax1, x / 1e6, total, label=f"kempe = {k}%", color=f"C{i}")

    ax1.set_xlabel(t("bench.iterations_m"))
    ax1.set_ylabel("total")
    ax1.set_title(t("bench.kempe.title"))
    ax1.legend()

    fig.suptitle(t("bench.kempe.suptitle"))

    finish(fig, "kempe.png", out, show)


def figIterations(groups, out, show):
    if len(groups) < 2:
        return

    its = sorted(groups)

    wall = np.array([np.median([run.wall for run in groups[i]]) for i in its])
    med = np.array([np.median([run.finalTotal for run in groups[i]]) for i in its])
    low = np.array([min(run.finalTotal for run in groups[i]) for i in its])
    high = np.array([max(run.finalTotal for run in groups[i]) for i in its])

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    ax1.errorbar(wall, med, yerr=[med - low, high - med], fmt="o-", capsize=4, color="tab:purple")

    for w, m, i in zip(wall, med, its):
        ax1.annotate(t("bench.iters.point", n=f"{i / 1e6:g}"), (w, m), xytext=(6, 6), textcoords="offset points")

    ax1.set_xlabel(t("bench.iters.xlabel"))
    ax1.set_ylabel(t("bench.iters.ylabel"))
    ax1.set_title(t("bench.iters.title"))

    ax2.errorbar([i / 1e6 for i in its], med, yerr=[med - low, high - med], fmt="o-", capsize=4, color="tab:brown")
    ax2.set_xscale("log")
    ax2.set_xlabel(t("bench.iters.xlabel2"))
    ax2.set_ylabel(t("bench.final_total"))
    ax2.set_title(t("bench.iters.title2"))

    fig.suptitle(t("bench.iters.suptitle"))

    finish(fig, "iterations.png", out, show)


def figBest(runs, out, show):
    cand = [run for run in runs if run.metrics]

    if not cand:
        print("   [!] no --metrics JSON, best plot skipped")

        return

    best = min(cand, key=lambda run: run.finalTotal)
    metrics = best.metrics

    fig, axes = plt.subplots(2, 3, figsize=(15, 8))

    for ax, (group, key, titleKey) in zip(axes.flat, SPECS):
        values = np.array(metrics.get(group, {}).get(key, []), dtype=float)

        ax.set_title(t(titleKey), fontsize=10)

        if values.size == 0:
            ax.text(0.5, 0.5, t("bench.best.no_data"), ha="center", transform=ax.transAxes)

            continue

        if np.allclose(values, np.round(values)) and values.max() - values.min() <= 60:
            bins = np.arange(values.min(), values.max() + 2) - 0.5

        else:
            bins = 15

        ax.hist(values, bins=bins, color="tab:blue", alpha=0.85, edgecolor="white")
        ax.axvline(values.mean(), color="tab:red", ls="--", lw=1.2)

        zeros = (values == 0).mean() * 100

        ax.text(
            0.97, 0.95,
            t("bench.best.stats", mean=f"{values.mean():.2f}", sum=f"{values.sum():.0f}", zeros=f"{zeros:.0f}"),
            transform=ax.transAxes, ha="right", va="top", fontsize=9,
            bbox=dict(boxstyle="round", fc="white", alpha=0.8)
        )

        ax.set_ylabel(t("bench.best.ylabel"))

    fig.suptitle(
        t("bench.best.suptitle", seed=best.cfg.seed, total=f"{best.finalTotal:,.0f}", unplaced=metrics.get("unplaced", 0)),
        fontsize=12
    )

    finish(fig, "best.png", out, show)


def summarize(groups, out):
    header = ["config", "n", "median", "mean", "std", "cv_%", "min", "max", "time_median_s", "moves_per_iter", "unplaced_max", "warnings_max"]
    rows = []

    for label, runs in groups.items():
        finals = np.array([run.finalTotal for run in runs])

        unplaced = [int(run.metrics.get("unplaced", 0)) if run.metrics else 0 for run in runs]
        moves = [run.moves / run.cfg.iters for run in runs]

        cv = (finals.std() / abs(finals.mean()) * 100) if finals.mean() else float("nan")

        rows.append([
            label, len(runs), f"{np.median(finals):.1f}", f"{finals.mean():.1f}", f"{finals.std():.1f}",
            f"{cv:.2f}",
            f"{finals.min():.1f}", f"{finals.max():.1f}",
            f"{np.median([run.wall for run in runs]):.1f}",
            f"{np.median(moves):.3f}", max(unplaced), max(run.warnings for run in runs)
        ])

    widths = [max(len(str(value)) for value in column) for column in zip(header, *rows)]

    print("\n" + "  ".join(name.ljust(width) for name, width in zip(header, widths)))

    for row in rows:
        print("  ".join(str(cell).ljust(width) for cell, width in zip(row, widths)))

    path = out / "summary.csv"

    with open(path, "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(rows)

    print(f"\n   saved {path}")


def main():
    parser = argparse.ArgumentParser(description="Convergence plots and benchmarks for solve.exe")

    parser.add_argument("--input", help="settings.json (searched automatically if omitted)")
    parser.add_argument("--solver", help="path to solve.exe (default: src/modules/solve.exe)")
    parser.add_argument("--weights", help="weights.json (optional)")
    parser.add_argument("--exp", nargs="+", default=["baseline"], choices=["baseline", "kempe", "iters", "all"])
    parser.add_argument("--seeds", type=int, default=5, help="runs per configuration (seeds 1..N)")
    parser.add_argument("--iterations", type=int, default=DEFAULT_ITERS, help="iterations in the baseline run (solver default is 50M)")
    parser.add_argument("--t-end", dest="tEnd", type=float, default=DEFAULT_T_END, help=f"final temperature; cooling is derived automatically (default {DEFAULT_T_END:.3f})")
    parser.add_argument("--print-every", dest="printEvery", type=int, default=100_000, help="how often the solver prints a [PRINT] line, default 100000 iterations")
    parser.add_argument("--kempe", type=int, default=DEFAULT_KEMPE, help="--kempe-chance for the baseline run")
    parser.add_argument("--kempe-values", dest="kempeValues", type=int, nargs="+", default=[0, 10, 20, 40])
    parser.add_argument("--iter-fractions", dest="iterFractions", type=float, nargs="+", default=[0.1, 0.25, 0.5, 1.0], help="fractions of --iterations for the iters experiment")
    parser.add_argument("--workers", type=int, default=max(1, (os.cpu_count() or 2) // 2), help="parallel runs (timings in the iterations plot are then approximate)")
    parser.add_argument("--langs", nargs="+", default=LANGS, choices=LANGS, help="languages of the generated PNGs (ru, en, by)")
    parser.add_argument("--out", default="bench")
    parser.add_argument("--force", action="store_true", help="ignore the cache")
    parser.add_argument("--show", action="store_true", help="show matplotlib windows")

    args = parser.parse_args()

    if not args.show:
        matplotlib.use("Agg")

    plt.rcParams.update({"axes.grid": True, "grid.alpha": 0.3, "font.size": 10})

    root = Path.cwd()
    solver = findSolver(args.solver)
    inp = findInput(args.input)
    weights = Path(args.weights).resolve() if args.weights else None

    if weights and not weights.is_file():
        sys.exit(f"Weights file not found: {args.weights}")

    out = Path(args.out)
    logs = out / "logs"
    logs.mkdir(parents=True, exist_ok=True)

    exps = set(args.exp)

    if "all" in exps:
        exps = {"baseline", "kempe", "iters"}

    exps.add("baseline")

    tag = makeTag(inp, weights, solver)
    seeds = list(range(1, args.seeds + 1))

    plan = {"baseline": makeCfgs(seeds, args.iterations, args.kempe, args.tEnd, tag, args.printEvery)}

    if "kempe" in exps:
        for k in args.kempeValues:
            plan[f"kempe={k}%"] = makeCfgs(seeds, args.iterations, k, args.tEnd, tag, args.printEvery)

    if "iters" in exps:
        for fraction in args.iterFractions:
            iters = max(args.printEvery * 5, int(round(args.iterations * fraction / 1_000_000)) * 1_000_000)

            plan[f"{iters / 1e6:g}M iterations"] = makeCfgs(seeds, iters, args.kempe, args.tEnd, tag, args.printEvery)

    unique = {cfg.key: cfg for cfgs in plan.values() for cfg in cfgs}

    print(f"solver : {solver}\ninput  : {inp}\nunique runs: {len(unique)}, workers: {args.workers}, t_end: {args.tEnd:.4g}\n")

    results = {}
    done = 0

    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {executor.submit(runOne, cfg, solver, inp, weights, root, logs, args.force): cfg for cfg in unique.values()}

        try:
            for future in as_completed(futures):
                cfg = futures[future]
                run = future.result()

                results[cfg.key] = run
                done += 1

                source = "cache" if run.cached else f"{run.wall:6.1f} s"

                print(f"[{done}/{len(unique)}] it={cfg.iters / 1e6:g}M kempe={cfg.kempe}% seed={cfg.seed}  total={run.finalTotal:,.0f}  ({source})")

        except KeyboardInterrupt:
            executor.shutdown(wait=False, cancel_futures=True)

            sys.exit("\nInterrupted. Completed runs are saved in the cache.")

        except Exception as error:
            executor.shutdown(wait=False, cancel_futures=True)

            sys.exit(f"\nRun failed: {error}")

    groups = {label: [results[cfg.key] for cfg in cfgs] for label, cfgs in plan.items()}

    base = groups["baseline"]

    for lang in args.langs:
        language(lang)

        langOut = out / lang
        langOut.mkdir(parents=True, exist_ok=True)

        print(f"\nBuilding plots [{lang}]...")

        figConvergence(base, langOut, args.show)
        figComponents(base, langOut, args.show)
        figTemperature(base, langOut, args.show)
        figSeeds(base, langOut, args.show)
        figBest(base, langOut, args.show)

        if "kempe" in exps:
            figKempe({k: [results[cfg.key] for cfg in plan[f"kempe={k}%"]] for k in args.kempeValues}, langOut, args.show)

        if "iters" in exps:
            byIters = {}

            for label, cfgs in plan.items():
                if label.endswith("M iterations"):
                    byIters[cfgs[0].iters] = groups[label]

            figIterations(byIters, langOut, args.show)

    summarize(groups, out)

    if args.show:
        plt.show()


if __name__ == "__main__":
    main()
