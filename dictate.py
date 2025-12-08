#!/usr/bin/env python3
"""
Audio Dictation Tool using Whisper
Records audio from microphone and transcribes it to text.
"""

import pyaudio
import wave
import whisper
import subprocess
import os
import tempfile
from datetime import datetime

# Configuration
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
RECORD_SECONDS = 5  # Default recording duration
WAVE_OUTPUT_DIR = tempfile.gettempdir()

# Whisper model: tiny, base, small, medium, large
# Recommendation: 'base' for good balance of speed and accuracy
MODEL_SIZE = "base"

class AudioRecorder:
    def __init__(self):
        self.audio = pyaudio.PyAudio()
        self.frames = []
        self.is_recording = False

    def start_recording(self):
        """Start recording audio from microphone"""
        self.frames = []
        self.is_recording = True

        self.stream = self.audio.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK
        )

        print("🎤 Recording... Press Ctrl+C to stop")

    def record_chunk(self):
        """Record a chunk of audio"""
        if self.is_recording:
            data = self.stream.read(CHUNK)
            self.frames.append(data)

    def stop_recording(self):
        """Stop recording and save to file"""
        if self.is_recording:
            self.is_recording = False
            self.stream.stop_stream()
            self.stream.close()

            # Save to temporary WAV file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.join(WAVE_OUTPUT_DIR, f"dictation_{timestamp}.wav")

            wf = wave.open(filename, 'wb')
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(self.audio.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(self.frames))
            wf.close()

            print(f"✅ Recording saved to: {filename}")
            return filename
        return None

    def cleanup(self):
        """Clean up audio resources"""
        self.audio.terminate()


class WhisperTranscriber:
    def __init__(self, model_size=MODEL_SIZE):
        """Initialize Whisper model"""
        print(f"📥 Loading Whisper '{model_size}' model...")
        self.model = whisper.load_model(model_size)
        print("✅ Model loaded!")

    def transcribe(self, audio_file):
        """Transcribe audio file to text"""
        print("🔄 Transcribing...")
        result = self.model.transcribe(audio_file)
        return result["text"].strip()


def copy_to_clipboard(text):
    """Copy text to macOS clipboard"""
    process = subprocess.Popen(
        'pbcopy',
        env={'LANG': 'en_US.UTF-8'},
        stdin=subprocess.PIPE
    )
    process.communicate(text.encode('utf-8'))
    print("📋 Text copied to clipboard!")


def main():
    print("=" * 50)
    print("🎙️  Audio Dictation Tool")
    print("=" * 50)

    # Initialize transcriber
    transcriber = WhisperTranscriber()

    # Initialize recorder
    recorder = AudioRecorder()

    try:
        # Start recording
        recorder.start_recording()

        # Record until user stops (Ctrl+C)
        while recorder.is_recording:
            recorder.record_chunk()

    except KeyboardInterrupt:
        print("\n⏹️  Stopping recording...")

    finally:
        # Stop recording and get filename
        audio_file = recorder.stop_recording()

        if audio_file:
            # Transcribe
            text = transcriber.transcribe(audio_file)

            print("\n" + "=" * 50)
            print("📝 TRANSCRIPTION:")
            print("=" * 50)
            print(text)
            print("=" * 50)

            # Copy to clipboard
            copy_to_clipboard(text)

            # Clean up temporary file
            os.remove(audio_file)
            print(f"🗑️  Temporary file removed")

        recorder.cleanup()
        print("\n✨ Done!")


if __name__ == "__main__":
    main()
