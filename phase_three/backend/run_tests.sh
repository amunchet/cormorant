#!/bin/sh
PYTHONPATH=/src/backend pytest -vvv --cov /src/backend --cov-fail-under=95 --cov-report=term-missing