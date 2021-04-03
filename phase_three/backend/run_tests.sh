#!/bin/sh
PYTHONPATH=/src/backend pytest -v --cov /src/backend --cov-fail-under=95 --cov-report=term-missing