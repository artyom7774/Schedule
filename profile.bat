@echo off

chcp 65001 > nul

cd /d "%~dp0"

set "SLEEPY_PATH=C:\Program Files\Very Sleepy\sleepy.exe"

set "EXE_PATH=%~dp0src\modules\solve.exe"
set "SRC_PATH=src\modules\solve.cpp"

set "WEIGHTS=C:\Users\Артём\AppData\Roaming\Schedule-Maker-1\projects\r2\weights.json"
set "INPUT=C:\Users\Артём\AppData\Roaming\Schedule-Maker-1\projects\r2\settings.json"
set "OUTPUT=C:\Users\Артём\AppData\Roaming\Schedule-Maker-1\projects\r2\answer.json"

"%SLEEPY_PATH%" /r "\"%EXE_PATH%\" --weights \"%WEIGHTS%\" --input \"%INPUT%\" --output \"%OUTPUT%\" --iterations 10000000 --cooling 0.9999999 --warnings 0" /o profile.sleepy

if errorlevel 1 (
    echo error

    exit /b
)

echo done
