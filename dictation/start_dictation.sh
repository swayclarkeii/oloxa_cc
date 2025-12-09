#!/bin/bash

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Set PYTHONPATH to use venv's site-packages (auto-detect Python version)
VENV_SITE_PACKAGES=$(find "$SCRIPT_DIR/venv/lib" -name "site-packages" -type d 2>/dev/null | head -1)
if [ -n "$VENV_SITE_PACKAGES" ]; then
    export PYTHONPATH="$VENV_SITE_PACKAGES:$PYTHONPATH"
fi

# Use the venv Python with dynamic path
exec "$SCRIPT_DIR/venv/bin/python3" "$SCRIPT_DIR/dictation_service.py"
