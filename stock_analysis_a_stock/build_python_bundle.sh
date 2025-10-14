#!/bin/bash
# Build script to bundle Python application using PyInstaller

set -e

echo "===================================="
echo "Building Python Bundle with PyInstaller"
echo "===================================="

# Check if poetry is available
if command -v poetry &> /dev/null; then
    echo "Using Poetry environment..."
    poetry run pip install pyinstaller
    poetry run pyinstaller build_pyinstaller.spec --clean
elif [ -n "$VIRTUAL_ENV" ]; then
    # We're in a virtual environment
    echo "Using virtual environment..."
    pip install pyinstaller
    pyinstaller build_pyinstaller.spec --clean
else
    echo "ERROR: No poetry or virtual environment detected!"
    echo "Please install dependencies first:"
    echo "  poetry install --no-root"
    echo "  OR"
    echo "  python -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

echo ""
echo "===================================="
echo "Python bundle created successfully!"
echo "Location: dist/stock_analysis_engine/"
echo "===================================="
