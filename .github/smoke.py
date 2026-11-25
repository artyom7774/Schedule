#!/usr/bin/env python3

from importlib import metadata
from pathlib import Path

import subprocess
import importlib
import tempfile
import argparse
import signal
import time
import sys
import os
import re

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

BAD_LOG = (
    "Traceback",
    "ModuleNotFoundError",
    "ImportError",
    "Could not load the Qt platform plugin",
    "Could not find the Qt platform plugin",
)


def error(message):
    print(f"[ERROR] {message}", flush=True)


def check_files(pkg):
    print("> Checking for files", flush=True)

    ok = True

    required = ["Schedule.py", "start.py", "requirements.txt", "LICENSE", "src", "python"]

    if os.name == "nt":
        required.append("Schedule.exe")

    else:
        required.append("src/modules/solve")

    missing = [element for element in required if not (pkg / element).exists()]

    if missing:
        error(f"Package haven't: {', '.join(missing)}")

        ok = False

    solver = pkg / "src" / "modules" / "solve"

    if os.name != "nt" and solver.exists() and not os.access(solver, os.X_OK):
        error(f"{solver} is not executable")

        ok = False

    return ok


def check_isolation(pkg):
    print("> Checking python isolation", flush=True)

    ok = True

    pkg = Path(pkg).resolve()
    script = Path(__file__).resolve().parent

    prefix = Path(sys.prefix).resolve()

    if not prefix.is_relative_to(pkg):
        error(f"sys.prefix {prefix} not in package")

        ok = False

    outside = []

    for path in sys.path:
        if not path:
            continue

        resolved = Path(path).resolve()

        if resolved == script:
            continue

        if not resolved.is_relative_to(pkg):
            outside.append(str(resolved))

    if outside:
        error(f"Paths not in package: {outside}")

        ok = False

    return ok


def check_requirements(pkg: Path):
    print("> Checking requirements", flush=True)

    ok = True

    for line in (pkg / "requirements.txt").read_text(encoding="utf-8").splitlines():
        line = line.split("#")[0].strip()

        if not line or line.startswith("-"):
            continue

        name = re.split(r"[<>=!~;\[ ]", line, maxsplit=1)[0]

        try:
            _ = metadata.version(name)

        except metadata.PackageNotFoundError:
            error(f"Package {name} not installed")

            ok = False

    for module in ("PyQt5.QtCore", "PyQt5.QtGui", "PyQt5.QtWidgets", "PyQt5.QtSvg"):
        try:
            importlib.import_module(module)

        except Exception as e:
            error(f"Import of {module} failed: {e!r}")

            ok = False

    return ok


def check_qt():
    print("> Checking Qt", flush=True)

    ok = True

    try:
        from PySide6.QtCore import QCoreApplication
        from PySide6.QtGui import QIcon, QImageReader
        from PySide6.QtWidgets import QApplication

    except Exception as e:
        error(f"Qt import failed: {e!r}")

        return False

    app = QApplication(["smoke"])

    expected = os.environ.get("QT_QPA_PLATFORM") or ("windows" if os.name == "nt" else "xcb")

    if app.platformName() != expected:
        error(f"Platform Qt {app.platformName()!r}, required {expected!r}")

        ok = False

    formats = {bytes(f).decode() for f in QImageReader.supportedImageFormats()}

    if "svg" not in formats:
        error("Qt not supported SVG")

        ok = False

    paths = [Path(path) for path in QCoreApplication.libraryPaths()]

    for sub, stem in (("imageformats", "qsvg"), ("iconengines", "qsvgicon")):
        if not any(list((path / sub).glob(f"*{stem}*")) for path in paths):
            error(f"Plugin {sub}/{stem} not found")

            ok = False

    svg = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16"><rect width="16" height="16" fill="red"/></svg>'

    with tempfile.TemporaryDirectory() as directory:
        file = Path(directory) / "temp.svg"

        file.write_text(svg)

        if QIcon(str(file)).pixmap(16, 16).isNull():
            error("Qt not displayed SVG icon")

            ok = False

    return ok


def run(process: subprocess.Popen):
    if process.poll() is not None:
        return

    if os.name == "nt":
        subprocess.run(["taskkill", "/PID", str(process.pid), "/T", "/F"], capture_output=True)

    else:
        os.killpg(process.pid, signal.SIGTERM)

    try:
        process.wait(10)

    except subprocess.TimeoutExpired:
        if os.name == "nt":
            process.kill()

        else:
            os.killpg(process.pid, signal.SIGKILL)


def app_command(pkg: Path):
    if os.name == "nt":
        exe = pkg / "python" / "Scripts" / "python.exe"

        if not exe.exists():
            exe = pkg / "python" / "python.exe"

        return [str(exe), "-OO", "-s", "Schedule.py"]

    exe = pkg / "python" / "bin" / "python3"

    if not exe.exists():
        exe = pkg / "linux" / "bin" / "python3"

    return [str(exe), "-OO", "Schedule.py"]


def launch_app(pkg: Path, seconds: int):
    print("> Checking running Schedule.py", flush=True)

    ok = True

    obj = Path(tempfile.gettempdir()) / "schedule-smoke.log"

    kwargs = {} if os.name == "nt" else {"start_new_session": True}

    env = os.environ.copy()
    env["PYTHONUNBUFFERED"] = "1"

    try:
        with open(obj, "wb") as log:
            path = subprocess.Popen(app_command(pkg), cwd=pkg, env=env, stdout=log, stderr=subprocess.STDOUT, **kwargs)

            dead = time.time() + seconds

            while time.time() < dead and path.poll() is None:
                time.sleep(0.25)

            code = path.poll()

            run(path)

    except OSError as e:
        error(f"Cannot start application: {e!r}")

        return False

    text = obj.read_text(encoding="utf-8", errors="replace")

    if text:
        print(text, flush=True)

    if code is not None:
        error(f"Application exited with code {code} before {seconds} s")

        ok = False

    bad = [message for message in BAD_LOG if message in text]

    if bad:
        error(f"Log have errors: {bad}")

        ok = False

    return ok


def main():
    ap = argparse.ArgumentParser()

    ap.add_argument("pkg", type=Path)
    ap.add_argument("--seconds", type=int, default=8)
    ap.add_argument("--no-launch", action="store_true")

    args = ap.parse_args()

    pkg = args.pkg.resolve()

    results = {}

    results["files"] = check_files(pkg)
    results["isolation"] = check_isolation(pkg)
    results["requirements"] = check_requirements(pkg)

    results["qt"] = check_qt()

    if not args.no_launch:
        results["launch"] = launch_app(pkg, args.seconds)

    if not all(results.values()):
        sys.exit(1)


if __name__ == "__main__":
    main()
