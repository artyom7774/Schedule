import subprocess
import threading
import os

thr = threading.Thread(target=lambda: subprocess.run(
    ["./python/Scripts/python.exe", "-OO", "-s", "Schedule.py"] if os.path.exists("./python/Scripts/python.exe") else ["./python/python.exe", "-OO", "-s", "Schedule.py"],
    capture_output=True,
    text=True,
    creationflags=subprocess.CREATE_NO_WINDOW
))

thr.start()
