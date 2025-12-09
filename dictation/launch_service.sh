#!/bin/bash

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Set environment for venv (auto-detect Python version)
VENV_SITE_PACKAGES=$(find "$SCRIPT_DIR/venv/lib" -name "site-packages" -type d 2>/dev/null | head -1)
if [ -n "$VENV_SITE_PACKAGES" ]; then
    export PYTHONPATH="$VENV_SITE_PACKAGES:$PYTHONPATH"
fi

# Run the v2 dictation service with notifications and menu bar
# -u flag = unbuffered output so logs appear in real-time
exec "$SCRIPT_DIR/venv/bin/python3" -u "$SCRIPT_DIR/dictation_service_v2.py"
