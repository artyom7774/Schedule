@echo off

chcp 65001 > nul

pprofile --exclude-syspath v1.py --view 0
