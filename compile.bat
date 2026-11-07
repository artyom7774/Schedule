@echo off

chcp 65001 > nul

g++ -std=c++17 -O3 -static-libgcc -static-libstdc++ -static src/modules/solve.cpp -o src/modules/solve.exe

if errorlevel 1 (
    echo error

    exit /b
)

echo done
