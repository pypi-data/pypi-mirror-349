#!/bin/bash

# Activate virtual environment
source venv/bin/activate

# Build the package
echo "Building package..."
python3 -m build

# Upload to PyPI
echo "Uploading to PyPI..."
python3 -m twine upload dist/*

# Deactivate virtual environment
deactivate

echo "Done! Package has been built and published to PyPI." 