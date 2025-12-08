#!/bin/bash

# Set environment for venv
export PYTHONPATH="/Users/swayclarke/coding_stuff/oloxa_cc/dictation/venv/lib/python3.12/site-packages"

# Run the v2 dictation service with notifications and menu bar
# -u flag = unbuffered output so logs appear in real-time
exec /Library/Frameworks/Python.framework/Versions/3.12/bin/python3.12 -u /Users/swayclarke/coding_stuff/oloxa_cc/dictation/dictation_service_v2.py
