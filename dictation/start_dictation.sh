#!/bin/bash

# Set PYTHONPATH to use venv's site-packages
export PYTHONPATH="/Users/swayclarke/coding_stuff/oloxa_cc/dictation/venv/lib/python3.12/site-packages:$PYTHONPATH"

# Use the venv Python with explicit path
exec /Users/swayclarke/coding_stuff/oloxa_cc/dictation/venv/bin/python3 /Users/swayclarke/coding_stuff/oloxa_cc/dictation/dictation_service.py
