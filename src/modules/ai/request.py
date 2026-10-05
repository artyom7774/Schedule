import requests
import time
import sys
import os

URL = "https://request.tail1af8d9.ts.net"
# URL = "http://127.0.0.1:5000"

MODEL = "muse-spark-1-3-contributor:free"

REQUEST_ENDPOINT = f"{URL}/api/ai/request"
STATUS_ENDPOINT = f"{URL}/api/ai/status"

RETRIES = 5

if os.name == "nt":
    try:
        import ctypes

        ctypes.windll.kernel32.SetConsoleOutputCP(65001)
        ctypes.windll.kernel32.SetConsoleCP(65001)

    except Exception:
        pass

try:
    sys.stdout.reconfigure(encoding="utf-8")

except Exception:
    pass


def sendChatRequestWithFiles(message: str, paths: list = None, retry: int = 0):
    interval = 1.5
    timeout = 300

    data = {
        "message": message,
        "model": MODEL,
    }

    handles = []
    files = []

    try:
        for path in paths or []:
            if path and os.path.isfile(path):
                handle = open(path, "rb")
                handles.append(handle)

                files.append(("files", (os.path.basename(path), handle)))

        response = requests.post(REQUEST_ENDPOINT, data=data, files=files or None, timeout=timeout)

    finally:
        for handle in handles:
            handle.close()

    if not response.ok:
        raise Exception(f"HTTP {response.status_code}: {response.text}")

    try:
        result = response.json()

    except ValueError:
        raise Exception(f"bad server response: HTTP {response.status_code} {response.text}")

    if "ids" not in result:
        raise Exception(f"no ids in response: {result}")

    ids = result["ids"]

    start = time.time()

    while True:
        if time.time() - start > timeout:
            raise Exception("timeout")

        now = requests.get(f"{STATUS_ENDPOINT}/{ids}", timeout=30)
        now.raise_for_status()

        save = now.json()

        status = save.get("status")

        print(status)

        if status == "completed":
            answer = save.get("response", "")

            print(answer)

            return answer, status

        elif status == "error":
            err = save.get("error", "")

            if isinstance(err, str) and err.startswith("HTTP 503") and retry < RETRIES:
                time.sleep(interval * (retry + 1))

                return sendChatRequestWithFiles(message, paths, retry + 1)

            raise Exception(f"{err}")

        elif status == "processing":
            time.sleep(interval)

        else:
            raise Exception(f"{save}")


def sendChatRequestWithFile(message: str, file_path: str = None):
    return sendChatRequestWithFiles(message, [file_path] if file_path else [])
