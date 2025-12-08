#!/bin/bash
# Launcher for dictation service - runs in background
# Double-click this file to start the service

cd "$(dirname "$0")"

# Set environment
export PYTHONPATH="/Users/swayclarke/coding_stuff/oloxa_cc/dictation/venv/lib/python3.12/site-packages"

# Check if already running
if pgrep -f "dictation_service_v2.py" > /dev/null; then
    osascript -e 'display notification "Dictation service is already running" with title "⚠️ Already Running"'
    exit 0
fi

# Run the dictation service in background, detached from terminal
nohup /Library/Frameworks/Python.framework/Versions/3.12/bin/python3.12 -u dictation_service_v2.py >> dictation.log 2>> dictation_error.log &

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
