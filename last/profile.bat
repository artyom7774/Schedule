@echo off

chcp 65001 > nul

set SLEEPY_PATH = "C:\Program Files\Very Sleepy\sleepy.exe"
set EXE_PATH = solve.exe

g++ -g -O0 -o %EXE_PATH% solve.cpp

if errorlevel 1 (
    echo error
    exit /b
)

%SLEEPY_PATH% /r %EXE_PATH% /o profile.sleepy

if errorlevel 1 (
    echo error
    exit /b
)

echo done
