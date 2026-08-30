from src.variables import *

import subprocess
import traceback
import importlib
import sys
import re


def decoder(window, output, function):
    def write(text):
        function.answer(text)

    def module(names):
        for name in names:
            try:
                importlib.import_module(name)

            except ImportError:
                result = subprocess.run([sys.executable, "-m", "pip", "install", name], capture_output=True, text=True)

                if result.returncode != 0:
                    raise Exception(result.stderr)

    match = re.search(r"```(?:python|py)?\s*\n(.*?)```", output, re.DOTALL)
    output = (match.group(1) if match else output).strip().replace("```python", "").replace("```py", "").replace("```", "")

    with open(f"{PATH_TO_FOLDER}/projects/{window.project}/log.txt", "w", encoding="UTF-8") as file:
        file.write(output)

    try:
        exec(output, {"write": write, "module": module, "__builtins__": __builtins__})

    except Exception as e:
        return 1, traceback.format_exc()

    return 0, output
