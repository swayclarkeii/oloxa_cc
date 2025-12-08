#!/usr/bin/env python3
"""Test microphone recording"""

import sounddevice as sd
import numpy as np
import time

print("Available audio devices:")
print(sd.query_devices())
print("\n" + "="*60)

# Get default input device
default_device = sd.default.device[0]
print(f"\nDefault input device: {default_device}")

# Test recording
print("\nRecording 3 seconds of audio...")
duration = 3  # seconds
sample_rate = 16000

try:
    audio = sd.rec(int(duration * sample_rate),
                   samplerate=sample_rate,
                   channels=1,
                   dtype=np.float32)
    sd.wait()

    # Check if audio was captured
    max_amplitude = np.max(np.abs(audio))
    mean_amplitude = np.mean(np.abs(audio))

    print(f"\n✅ Recording completed!")
    print(f"Audio stats:")
    print(f"  Max amplitude: {max_amplitude:.6f}")
    print(f"  Mean amplitude: {mean_amplitude:.6f}")

    if max_amplitude < 0.001:
        print("\n⚠️  WARNING: Very low amplitude - microphone may not be working!")
    else:
        print("\n✅ Microphone appears to be working!")

except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
