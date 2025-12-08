#!/usr/bin/env python3
"""
Simple script to test microphone access and trigger permission popup
"""

import sounddevice as sd
import time

print("Testing microphone access...")
print("This will trigger a permission popup if needed.")
print("\nRecording for 3 seconds...")

# This should trigger the microphone permission popup
recording = sd.rec(int(3 * 16000), samplerate=16000, channels=1)
sd.wait()

print("✅ Recording successful! Microphone access granted.")
print("\nNow the dictation service should work properly.")
