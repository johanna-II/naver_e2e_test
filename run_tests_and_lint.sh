#!/bin/bash
set -e

echo "Running Pylint..."
pylint page_objects tests utils.py conftest.py

echo "Running tests..."
pytest -v --html=report.html