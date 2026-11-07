import subprocess
import time

count = 10

start = time.perf_counter()

for _ in range(count):
    process = subprocess.run([
        "src/modules/solve.exe",
        "--weights",    r"C:\Users\Артём\AppData\Roaming/Schedule-Maker-1/projects/r2/weights.json",
        "--input",      r"C:\Users\Артём\AppData\Roaming/Schedule-Maker-1/projects/r2/settings.json",
        "--output",     r"C:\Users\Артём\AppData\Roaming/Schedule-Maker-1/projects/r2/answer.json",
        "--iterations", r"1000000",
        "--cooling",    r"0.9999999",
        "--warnings",   r"0"

    ], capture_output=True)

get = time.perf_counter() - start

print()
print(f"{get / count:.2f}s")
