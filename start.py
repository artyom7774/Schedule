import subprocess
import threading

thr = threading.Thread(target=lambda: subprocess.run(
    ["./python/python.exe", "-OO", "-s", "Schedule.py"],
    capture_output=True,
    text=True,
    creationflags=subprocess.CREATE_NO_WINDOW
))

thr.start()
