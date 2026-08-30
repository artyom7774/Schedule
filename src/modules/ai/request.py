import requests
import time
import sys
import os

URL = "https://ge3.pythonanywhere.com/"
MODEL = "gemini-2.5-flash"

if os.name == "nt":
    try:
        import ctypes

        ctypes.windll.kernel32.SetConsoleOutputCP(65001)
        ctypes.windll.kernel32.SetConsoleCP(65001)

    except Exception:
        pass

sys.stdout.reconfigure(encoding='utf-8')


def sendChatRequestWithFile(message: str, file_path: str = None):
    poll_interval = 1.5
    timeout = 300

    data = {
        "message": message,
        "model": MODEL,
    }

    files = None
    file_handle = None

    try:
        if file_path and os.path.isfile(file_path):
            file_handle = open(file_path, "rb")
            files = {"file": (os.path.basename(file_path), file_handle)}

        response = requests.post(
            f"{URL}/chat-ai-file",
            data=data,
            files=files,
            timeout=timeout,
        )
        response.raise_for_status()

    finally:
        if file_handle:
            file_handle.close()

    result = response.json()

    ids = result["ids"]

    start_time = time.time()

    while True:
        if time.time() - start_time > timeout:
            raise Exception("timeout")

        status_resp = requests.get(f"{URL}/ai/status/{ids}", timeout=30)
        status_resp.raise_for_status()
        status_data = status_resp.json()

        status = status_data.get("status")

        if status == "completed":
            return status_data.get("response", ""), status

        elif status == "error":
            raise Exception(f"{status_data.get('error')}")

        elif status == "processing":
            time.sleep(poll_interval)

        else:
            raise Exception(f"{status_data}")
