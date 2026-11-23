#!/usr/bin/env bash

set -euo pipefail

cd "$(dirname "$0")"

g++ -std=c++17 -O3 src/modules/solve.cpp -o src/modules/solve

echo "done"
