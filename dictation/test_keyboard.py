#!/usr/bin/env python3
"""Test keyboard listener permissions"""

from pynput import keyboard
import time

print("Testing keyboard listener...")
print("Press any key (this will trigger accessibility permission if needed)")
print("Press ESC to exit")

def on_press(key):
    print(f"Key pressed: {key}")
    if key == keyboard.Key.esc:
        return False

def on_release(key):
    pass

# Start listener
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    print("Listener started. Waiting for key presses...")
    listener.join()

print("Test complete!")
