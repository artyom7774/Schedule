#!/usr/bin/env bash

cd "$(dirname "$(readlink -f "$0")")"

if [ -e "python/bin/python3" ]; then
    chmod +x ./python/bin/python3
    exec     ./python/bin/python3 start.py "$@"
else
    chmod +x ./linux/bin/python3
    exec     ./linux/bin/python3 start.py "$@"
fi
