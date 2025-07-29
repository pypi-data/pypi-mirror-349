#!/bin/bash

# Activate virtual environment
source venv/bin/activate

# Build the package
python3 -m build

# Deactivate virtual environment
deactivate 