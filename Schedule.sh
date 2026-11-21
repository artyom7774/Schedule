#!/usr/bin/env bash

cd "$(dirname "$(readlink -f "$0")")"

if [ -e "python/bin/python3" ]; then
    exec ./python/bin/python3 start.py "$@"
else
    exec ./linux/bin/python3 start.py "$@"
fi
