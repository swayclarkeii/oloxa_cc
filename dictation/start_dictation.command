#!/bin/bash
# Launcher for dictation service - runs in background
# Double-click this file to start the service

cd "$(dirname "$0")"
SCRIPT_DIR="$(pwd)"

# Set environment (auto-detect Python version)
VENV_SITE_PACKAGES=$(find "$SCRIPT_DIR/venv/lib" -name "site-packages" -type d 2>/dev/null | head -1)
if [ -n "$VENV_SITE_PACKAGES" ]; then
    export PYTHONPATH="$VENV_SITE_PACKAGES:$PYTHONPATH"
fi

# Check if already running
if pgrep -f "dictation_service_v2.py" > /dev/null; then
    osascript -e 'display notification "Dictation service is already running" with title "⚠️ Already Running"'
    exit 0
fi

# Run the dictation service in background, detached from terminal
nohup "$SCRIPT_DIR/venv/bin/python3" -u "$SCRIPT_DIR/dictation_service_v2.py" >> "$SCRIPT_DIR/dictation.log" 2>> "$SCRIPT_DIR/dictation_error.log" &

# Give it a moment to start
sleep 1

# Check if it started successfully
if pgrep -f "dictation_service_v2.py" > /dev/null; then
    osascript -e 'display notification "Dictation service started - you can close this terminal" with title "✅ Service Started"'
else
    osascript -e 'display notification "Failed to start - check logs" with title "❌ Startup Failed"'
    exit 1
fi

# Terminal can now be closed - service runs in background
exit 0
