#!/usr/bin/env python3

import concurrent.futures
import subprocess
import argparse
import pathlib
import random
import time
import json
import csv
import sys
import os

sys.path.insert(0, str(pathlib.Path(__file__).parent))

from variables import DEFAULTS, TUNABLE, compute, SOLVER

INPUT   = pathlib.Path("tuner/bench")
OUTPUT  = pathlib.Path("tuner/pool")
PATTERN = '*.json'
RANGE   = 1.0
TIMEOUT = 3600


def run(task):
    out = pathlib.Path(task["out"])
    out.mkdir(parents=True, exist_ok=True)

    weights_path = out / "weights.json"
    metrics_path = out / "metrics.json"

    weights_path.write_text(json.dumps(task["weights"], indent=4), encoding="utf-8")
    
    (out / "meta.json").write_text(json.dumps({
        "settings": task["settings"],
        "seed": task["seed"],
        "iterations": task["iterations"],
        "fair": task["fair"],
        "cooling": task["cooling"],
    }, indent=4), encoding="utf-8")

    cmd = [
        SOLVER,
        "--input", task["settings"],
        "--weights", str(weights_path),
        "--seed", str(task["seed"]),
        "--iterations", str(task["iterations"]),
        "--cooling", repr(task["cooling"]),
        "--fair", repr(task["fair"]),
        "--metrics", str(metrics_path),
    ]

    start = time.time()

    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors='replace', timeout=TIMEOUT)

    except subprocess.TimeoutExpired:
        return {"id": task["id"], "error": "timeout", "elapsed": time.time() - start}

    elapsed = time.time() - start

    if proc.returncode != 0:
        return {"id": task["id"], "error": (proc.stderr or proc.stdout or "")[-500:], "elapsed": elapsed}

    try:
        metrics = json.loads(metrics_path.read_text(encoding="utf-8"))

    except Exception as e:
        return {"id": task["id"], "error": f"bad metrics: {e}", "elapsed": elapsed}

    row = {
        "id": task["id"],
        "settings": task["settings"],
        "seed": task["seed"],
        "fair": task["fair"],
        "iterations": task["iterations"],
        "unplaced": metrics.get("unplaced", -1),
        "total": metrics.get("total", 0.0),
        "moves": metrics.get("moves", 0),
        "dir": str(out),
        "request": round(elapsed, 1),
    }

    for key, value in task["weights"].items():
        row[f"{key}"] = value

    return row


def weights(rng):
    var = dict(DEFAULTS)

    for name in TUNABLE:
        var[name] = DEFAULTS[name] * float(10 ** rng.uniform(-RANGE, +RANGE))

    return var


def build(runs, iterations, seed, shard=0, shards=1):
    OUTPUT.mkdir(parents=True, exist_ok=True)

    files = sorted(p for p in INPUT.glob(PATTERN) if p.is_file())

    rng = random.Random(seed)
    tasks = []

    for settings in files:
        for i in range(runs):
            id = f"{settings.stem}_{i:03d}"
            tasks.append({
                "id": id,
                "settings": str(settings),
                "weights": weights(rng),
                "seed": rng.randint(1, 2**31 - 1),
                "iterations": iterations,
                "fair": float(10 ** rng.uniform(1.0, 3.0)),
                "cooling": compute(iterations),
                "out": str(OUTPUT / id),
            })

    if shards > 1:
        tasks = tasks[shard::shards]

    return tasks


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--runs",       type=int, default=30)
    parser.add_argument("--iterations", type=int, default=1000000)
    parser.add_argument("--workers",    type=int, default=None)
    parser.add_argument("--seed",       type=int, default=0)
    parser.add_argument("--shard",      type=int, default=0)
    parser.add_argument("--shards",     type=int, default=1)

    args = parser.parse_args()

    print(f"solver: {SOLVER}")

    tasks = build(args.runs, args.iterations, args.seed, args.shard, args.shards)
    workers = args.workers or min(len(tasks) or 1, os.cpu_count() or 4)

    print(f"runs: {args.runs}, shard: {args.shard}/{args.shards}, total: {len(tasks)}, workers: {workers}")
    print()

    manifest = []
    
    start = time.time()
    
    done = 0
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as execute:
        futures = {execute.submit(run, task): task for task in tasks}
        
        for fut in concurrent.futures.as_completed(futures):
            task = futures[fut]
            
            done += 1
            
            try:
                row = fut.result()
                
            except Exception as e:
                print(f"[{done}/{len(tasks)}] {task['id']}: EXCEPTION {e}", file=sys.stderr)
                
                continue
                
            if "error" in row:
                print(f"[{done}/{len(tasks)}] {task['id']}: FAIL {row['error']}", file=sys.stderr)
                
                continue
                
            manifest.append(row)

            print(f"[{done}/{len(tasks)}] {task['id']} - {row['request']:.1f}s: unplaced={row['unplaced']} total={row['total']:.1f}")

    with open(OUTPUT / "manifest.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(manifest[0].keys()))
        writer.writeheader()
        
        writer.writerows(manifest)

    print()
    print(f"Done: {len(manifest)}/{len(tasks)} in {(time.time() - start)/60:.1f}")
    print(f"Manifest: {OUTPUT / 'manifest.csv'}")


if __name__ == '__main__':
    main()
