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


def check_files(pkg):
    print("> Checking for files")

    required = ["Schedule.exe", "Schedule.py", "start.py", "requirements.txt", "LICENSE", "src", "python"]
    missing = [element for element in required if not (pkg / element).exists()]

    if missing:
        print(f"[ERROR] Package haven't: {', '.join(missing)}")


def check_isolation(pkg):
    print("> Checking python isolation")

    prefix = Path(sys.prefix).resolve()

    if not prefix.is_relative_to(pkg):
        print(f"[ERROR] {prefix} not in package")

    outside = [path for path in sys.path if path and not Path(path).resolve().is_relative_to(pkg)]

    if outside:
        print(f"[ERROR] Paths not in package: {outside}")


def check_requirements(pkg: Path):
    print("> Checking requirements")

    for line in (pkg / "requirements.txt").read_text(encoding="utf-8").splitlines():
        line = line.split("#")[0].strip()

        if not line or line.startswith("-"):
            continue

        name = re.split(r"[<>=!~;\[ ]", line, maxsplit=1)[0]

        try:
            _ = metadata.version(name)

        except metadata.PackageNotFoundError:
            print(f"Package {name} not installed")

    for module in ("PyQt5.QtCore", "PyQt5.QtGui", "PyQt5.QtWidgets", "PyQt5.QtSvg"):
        try:
            importlib.import_module(module)

        except Exception as e:
            print(f"Import of {module} failed: {e!r}")

def check_qt():
    print("> checking having Qt DLLs")

    from PyQt5.QtCore import QCoreApplication
    from PyQt5.QtGui import QIcon, QImageReader
    from PyQt5.QtWidgets import QApplication

    app = QApplication(["smoke"])

    expected = os.environ.get("QT_QPA_PLATFORM") or ("windows" if os.name == "nt" else "xcb")

    if app.platformName() != expected:
        print(f"[ERROR] Platform Qt {app.platformName()!r}, required {expected!r}")

    formats = {bytes(f).decode() for f in QImageReader.supportedImageFormats()}

    if "svg" not in formats:
        print("[ERROR] Qt not supported SVG")

    paths = [Path(path) for path in QCoreApplication.libraryPaths()]

    for sub, stem in (("imageformats", "qsvg"), ("iconengines", "qsvgicon")):
        if not any(list((path / sub).glob(f"*{stem}*")) for path in paths):
            print(f"[ERROR] Plugin {sub}/{stem} not found")

    svg = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16"><rect width="16" height="16" fill="red"/></svg>'

    with tempfile.TemporaryDirectory() as directory:
        file = Path(directory) / "temp.svg"
        
        file.write_text(svg)
        
        if QIcon(str(file)).pixmap(16, 16).isNull():
            print("[ERROR] Qt not displayed SVG icon")


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


def launch_app(pkg: Path, seconds: int):
    print(f"> Checking running start.py")

    log = Path(tempfile.gettempdir()) / "schedule-smoke.log"

    kwargs = {} if os.name == "nt" else {"start_new_session": True}

    with open(log, "wb") as log:
        path = subprocess.Popen([sys.executable, "start.py"], cwd=pkg, stdout=log, stderr=subprocess.STDOUT, **kwargs)

        dead = time.time() + seconds

        while time.time() < dead and path.poll() is None:
            time.sleep(0.25)

        code = path.poll()

        run(path)

    text = log.read_text(encoding="utf-8", errors="replace")

    if text:
        print(log)

    if code is not None:
        print(f"[ERROR] Application return {code}")

    bad = [error for error in BAD_LOG if error in text]

    if bad:
        print(f"[ERROR] Log have errors: {bad}")


def main():
    ap = argparse.ArgumentParser()

    ap.add_argument("pkg", type=Path)
    ap.add_argument("--seconds", type=int, default=8)
    ap.add_argument("--no-launch", action="store_true")

    args = ap.parse_args()

    pkg = args.pkg.resolve()

    check_files(pkg)
    check_isolation(pkg)
    check_requirements(pkg)

    check_qt()

    if not args.no_launch:
        launch_app(pkg, args.seconds)


if __name__ == "__main__":
    main()
