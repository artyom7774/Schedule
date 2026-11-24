import subprocess
import threading
import platform
import os


def run():
    if platform.system() == "Windows":
        thr = threading.Thread(target=lambda: subprocess.run(
            ["./python/Scripts/python.exe", "-OO", "-s", "Schedule.py"] if os.path.exists(
                "python/Scripts/python.exe") else ["./python/python.exe", "-OO", "-s", "Schedule.py"],
            capture_output=True,
            text=True,
            creationflags=subprocess.CREATE_NO_WINDOW
        ))

        thr.start()

    else:
        subprocess.run(
            ["./python/bin/python3", "-OO", "Schedule.py"] if os.path.exists("python/bin/python3") else ["./linux/bin/python3", "-OO", "Schedule.py"],
            capture_output=True,
            text=True,
            start_new_session=True
        )

if __name__ == "__main__":
    run()
