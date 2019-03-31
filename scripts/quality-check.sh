#!/bin/bash

echo "black formatter..."
black --check kdlc tests setup.py --exclude kdlc/parser
echo ""

echo "flake8 style guide..."
flake8 kdlc/ tests/ setup.py --ignore kdlc/parser && echo "passed 👍"
echo ""

echo ""
pytest --cov=kdlc
echo ""

echo "documentation..."
sphinx-build -nWT -c docs/source/ -b html docs/source/ docs/build/html
