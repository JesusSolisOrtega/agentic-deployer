#!/bin/bash
cd "$(dirname "$0")/.." && .venv/bin/pytest app/tests/ -x -q
