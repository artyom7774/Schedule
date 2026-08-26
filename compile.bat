@echo off

chcp 65001 > nul

g++ -std=c++17 -O2 -static-libgcc -static-libstdc++ -static v2.cpp -o v2.exe
g++ -std=c++17 -O2 -static-libgcc -static-libstdc++ -static v3.cpp -o v3.exe

echo done
