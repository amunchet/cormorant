#!/bin/sh
PYTHONPATH=/src/backend pytest -x -v --cov /src/backend --cov-fail-under=95 --cov-report=term-missing