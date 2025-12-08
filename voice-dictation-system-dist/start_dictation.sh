#!/bin/bash

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Check if .env file exists
if [ ! -f "$SCRIPT_DIR/.env" ]; then
    echo "❌ Error: .env file not found"
    echo "Please run setup_wizard.py first or copy .env.example to .env"
    exit 1
fi

# Find Python 3.12 (preferred) or any Python 3
PYTHON_CMD=""
for py_path in \
    "/Library/Frameworks/Python.framework/Versions/3.12/bin/python3" \
    "/Library/Frameworks/Python.framework/Versions/3.11/bin/python3" \
    "/Library/Frameworks/Python.framework/Versions/3.10/bin/python3" \
    "/opt/homebrew/bin/python3" \
    "/usr/local/bin/python3" \
    "$(which python3)"; do
    if [ -x "$py_path" ]; then
        # Check Python version
        version=$("$py_path" -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
        major=$(echo $version | cut -d. -f1)
        minor=$(echo $version | cut -d. -f2)

        if [ "$major" -eq 3 ] && [ "$minor" -ge 10 ] && [ "$minor" -lt 14 ]; then
            PYTHON_CMD="$py_path"
            break
        fi
    fi
done

if [ -z "$PYTHON_CMD" ]; then
    echo "❌ Error: Python 3.10-3.13 not found"
    echo "Please install Python 3.12 from python.org"
    exit 1
fi

echo "Using Python: $PYTHON_CMD"

# Run the dictation service
exec "$PYTHON_CMD" "$SCRIPT_DIR/dictation_service.py"
