@echo off

chcp 65001 > nul

g++ solve.cpp -o solve.exe

start "" "solve.exe"

echo done
