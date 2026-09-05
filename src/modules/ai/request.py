import requests
import time
import sys
import os

URL = "https://ge3.pythonanywhere.com/"
MODEL = "gemini-3.6-flash"

if os.name == "nt":
    try:
        import ctypes

        ctypes.windll.kernel32.SetConsoleOutputCP(65001)
        ctypes.windll.kernel32.SetConsoleCP(65001)

    except Exception:
        pass

sys.stdout.reconfigure(encoding='utf-8')


def sendChatRequestWithFiles(message: str, file_paths: list = None):
    interval = 1.5
    timeout = 300

    data = {
        "message": message,
        "model": MODEL,
    }

    files = []
    handles = []

    try:
        for path in file_paths or []:
            if path and os.path.isfile(path):
                handle = open(path, "rb")
                handles.append(handle)
                files.append(("files", (os.path.basename(path), handle)))

        response = requests.post(
            f"{URL}/chat-ai-file",
            data=data,
            files=files or None,
            timeout=timeout,
        )
        response.raise_for_status()

    finally:
        for handle in handles:
            handle.close()

    result = response.json()

    ids = result["ids"]

    start_time = time.time()

    while True:
        if time.time() - start_time > timeout:
            raise Exception("timeout")

        now = requests.get(f"{URL}/ai/status/{ids}", timeout=30)
        now.raise_for_status()

        save = now.json()

        status = save.get("status")

        if status == "completed":
            return save.get("response", ""), status

        elif status == "error":
            raise Exception(f"{save.get('error')}")

        elif status == "processing":
            time.sleep(interval)

        else:
            raise Exception(f"{save}")


def sendChatRequestWithFile(message: str, file_path: str = None):
    return sendChatRequestWithFiles(message, [file_path] if file_path else [])
