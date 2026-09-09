import requests
import time
import sys
import os

URL = "https://ge3.pythonanywhere.com/"
MODEL = "gemini-3.7-flash"

if os.name == "nt":
    try:
        import ctypes

        ctypes.windll.kernel32.SetConsoleOutputCP(65001)
        ctypes.windll.kernel32.SetConsoleCP(65001)

    except Exception:
        pass

sys.stdout.reconfigure(encoding='utf-8')


def sendChatRequestWithFiles(message: str, paths: list = None):
    interval = 1.5
    timeout = 300

    data = {
        "message": message,
        "model": MODEL,
    }

    files = []
    handles = []

    try:
        for path in paths or []:
            if path and os.path.isfile(path):
                handle = open(path, "rb")
                
                handles.append(handle)
                files.append(("files", (os.path.basename(path), handle)))

        response = requests.post(f"{URL}/chat-ai-file", data=data, files=files or None, timeout=timeout)
        response.raise_for_status()

    finally:
        for handle in handles:
            handle.close()

    result = response.json()

    ids = result["ids"]

    start = time.time()

    while True:
        if time.time() - start > timeout:
            raise Exception("timeout")

        now = requests.get(f"{URL}/ai/status/{ids}", timeout=30)
        now.raise_for_status()

        save = now.json()

        status = save.get("status")

        print(status)

        if status == "completed":
            print(save.get("response"))

            return save.get("response", ""), status

        elif status == "error" and save.get("error").startswith("503"):
            return sendChatRequestWithFiles(message, paths)

        elif status == "error":
            raise Exception(f"{save.get('error')}")

        elif status == "processing":
            time.sleep(interval)

        else:
            raise Exception(f"{save}")


def sendChatRequestWithFile(message: str, file_path: str = None):
    return sendChatRequestWithFiles(message, [file_path] if file_path else [])
