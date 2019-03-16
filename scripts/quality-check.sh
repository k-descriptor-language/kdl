#!/bin/bash

echo "black formatter..."
black --check kdlc tests setup.py
echo ""

echo "flake8 style guide..."
flake8 kdlc/ tests/ setup.py && echo "passed 👍"
echo ""

echo ""
pytest --cov=./
