#!/bin/bash

echo "black formatter..."
black --check kdlc tests setup.py --exclude kdlc/parser
echo ""

echo "flake8 style guide..."
flake8 kdlc/ tests/ setup.py --ignore kdlc/parser && echo "passed 👍"
echo ""

echo ""
pytest --cov=./
