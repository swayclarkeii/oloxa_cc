#!/usr/bin/env python3
"""
System-wide dictation service for macOS
- Press Control key twice to start recording
- Press Control once to stop and transcribe
- Auto-pastes cleaned text at cursor location
"""

import os
import sys
import time
import tempfile
import threading
import queue
import subprocess
from pathlib import Path
from datetime import datetime

try:
    import sounddevice as sd
    import soundfile as sf
    import numpy as np
    from pynput import keyboard
    from pynput.keyboard import Key, Controller
    import whisper
    import openai
    from dotenv import load_dotenv
except ImportError as e:
    print(f"Missing dependency: {e}")
    print("\nPlease run the installer script:")
    print("bash install.sh")
    sys.exit(1)

# Load environment variables from .env file in the same directory as this script
script_dir = Path(__file__).parent.absolute()
env_path = script_dir / ".env"
load_dotenv(dotenv_path=env_path)

# Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY or OPENAI_API_KEY == "your-openai-api-key-here":
    print("❌ Error: OPENAI_API_KEY not configured!")
    print(f"\nPlease edit the .env file at: {env_path}")
    print("Add your OpenAI API key:")
    print("OPENAI_API_KEY=sk-proj-your-actual-key-here")
    print("\nOr run the setup wizard: python3 setup_wizard.py")
    sys.exit(1)

WHISPER_MODEL_SIZE = "base"  # tiny, base, small, medium, large
SAMPLE_RATE = 16000
CHANNELS = 1

CLEANING_PROMPT = '''# Role

You are an expert linguistic editor and communication specialist, skilled at transforming raw, messy transcripts into clean, clear, and logically structured text.
You combine precision, restraint, and linguistic discipline to preserve meaning while eliminating noise.
Your refined outputs empower users to convert spoken or rough-written material into publication- or prompt-ready clarity.

⸻

# Task

Clean and refine transcripts according to the following process:
	1.	Concise — Remove filler words such as "um," "ah," "you know," "like," "so yeah," "I mean," etc. Keep sentences short, direct, and to the point.
	2.	Logical — Delete repetitions or restated thoughts. Reorder only if needed for smooth, step-by-step logic.
	3.	Explicit — Complete broken or unfinished sentences so they read clearly and fully. State output formats explicitly.
	4.	Adaptive — Rephrase incomplete lines only for readability. Do not infer missing meaning or invent content. If something is unclear, insert [unclear phrase].
	5.	Reflective — Perform an internal verification check: confirm that meaning is preserved, clarity is achieved, and the output is ready to paste.

⸻

# Specifics
	•	Always output one section only:
	•	Clean Transcript — A filler-free, natural, and readable version of the input.
	•	Use the format marker below:

              ### Clean Transcript
              [Your cleaned transcript here]

⸻

# Context

Our organization produces a wide range of analytical and creative content that begins as spoken transcripts or loosely structured notes.
Your task is a critical quality-control step in this process: every refined transcript you produce becomes the foundation for prompt design, data interpretation, or client-facing documentation.
By ensuring clarity and structural precision, you help maintain the professional integrity of our work and the credibility of our communication.
Your attention to detail directly affects the success and clarity of all downstream outputs.

⸻

# Notes
	•	Always assume every input is a transcript unless explicitly stated: "This is not a transcript."
	•	Never provide commentary, analysis, or conversational remarks.
	•	Avoid inference: if meaning is unclear, use [unclear phrase].
	•	Prioritize meaning preservation over stylistic flair.
	•	Handle sensitive content with neutrality; do not alter tone or intent.
	•	Your disciplined accuracy ensures trust and reliability across every phase of the workflow.
'''


class DictationService:
    def __init__(self):
        self.is_recording = False
        self.audio_data = []
        self.whisper_model = None
        self.keyboard_controller = Controller()
        self.temp_dir = tempfile.mkdtemp()

        # For detecting double Control press
        self.last_ctrl_press_time = 0
        self.ctrl_double_press_threshold = 0.3  # seconds

        # Thread-safe queue for audio chunks
        self.audio_queue = queue.Queue()
        self.recording_stream = None

        print("Loading Whisper model...")
        self.whisper_model = whisper.load_model(WHISPER_MODEL_SIZE)
        print(f"Whisper model '{WHISPER_MODEL_SIZE}' loaded successfully")

        # Initialize OpenAI client
        self.openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)

    def audio_callback(self, indata, frames, time_info, status):
        """Callback for audio recording"""
        if status:
            print(f"Audio status: {status}")
        self.audio_queue.put(indata.copy())

    def start_recording(self):
        """Start audio recording"""
        if self.is_recording:
            return

        self.is_recording = True
        self.audio_data = []
        print("🎙️  Recording started... (Press Control to stop)")
        self.send_notification("Recording Started", "Speak now... Press Control to stop")

        # Start recording stream
        self.recording_stream = sd.InputStream(
            samplerate=SAMPLE_RATE,
            channels=CHANNELS,
            callback=self.audio_callback,
            dtype=np.float32
        )
        self.recording_stream.start()

    def stop_recording(self):
        """Stop recording and process audio"""
        if not self.is_recording:
            return

        self.is_recording = False

        # Stop the stream
        if self.recording_stream:
            self.recording_stream.stop()
            self.recording_stream.close()
            self.recording_stream = None

        print("⏹️  Recording stopped. Processing...")

        # Collect all audio data
        while not self.audio_queue.empty():
            self.audio_data.append(self.audio_queue.get())

        if not self.audio_data:
            print("❌ No audio recorded")
            return

        # Process in background thread
        threading.Thread(target=self.process_audio, daemon=True).start()

    def process_audio(self):
        """Transcribe and clean audio"""
        try:
            # Combine audio chunks
            audio_array = np.concatenate(self.audio_data, axis=0)

            # Save temporary audio file
            temp_audio_path = os.path.join(self.temp_dir, f"recording_{int(time.time())}.wav")
            sf.write(temp_audio_path, audio_array, SAMPLE_RATE)

            # Transcribe with Whisper
            print("🔄 Transcribing...")
            self.send_notification("Transcribing...", "Converting speech to text")
            result = self.whisper_model.transcribe(temp_audio_path, language="en")
            raw_transcript = result["text"].strip()

            print(f"📝 Raw transcript: {raw_transcript[:100]}...")

            # Clean transcript with OpenAI
            print("✨ Cleaning transcript...")
            self.send_notification("Cleaning Text...", "Polishing your transcript")
            cleaned_text = self.clean_transcript(raw_transcript)

            print(f"✅ Cleaned: {cleaned_text[:100]}...")

            # Paste to cursor location
            self.paste_text(cleaned_text)
            self.send_notification("Complete!", "Text has been pasted")

            # Cleanup
            try:
                os.remove(temp_audio_path)
            except:
                pass

        except Exception as e:
            print(f"❌ Error processing audio: {e}")
            self.send_notification("Error", "Processing failed - check Terminal")
            import traceback
            traceback.print_exc()

    def clean_transcript(self, raw_text):
        """Clean transcript using OpenAI"""
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": CLEANING_PROMPT},
                    {"role": "user", "content": raw_text}
                ],
                temperature=0.3
            )

            cleaned = response.choices[0].message.content.strip()

            # Extract only the content under "### Clean Transcript"
            if "### Clean Transcript" in cleaned:
                parts = cleaned.split("### Clean Transcript", 1)
                if len(parts) > 1:
                    # Get everything after the header
                    content = parts[1].strip()
                    # Remove any subsequent headers if present
                    if "###" in content:
                        content = content.split("###")[0].strip()

                    # Remove "[No input provided.]" artifact
                    content = content.replace("[No input provided.]", "").strip()

                    return content

            # Fallback: remove artifact from raw cleaned text
            cleaned = cleaned.replace("[No input provided.]", "").strip()
            return cleaned

        except Exception as e:
            print(f"❌ Error cleaning transcript: {e}")
            return raw_text

    def paste_text(self, text):
        """Paste text at cursor location"""
        try:
            # Small delay to ensure focus
            time.sleep(0.1)

            # Type the text
            self.keyboard_controller.type(text)
            print("✅ Text pasted successfully")

        except Exception as e:
            print(f"⚠️  Could not auto-paste. Copying to clipboard instead...")
            # Fallback: copy to clipboard using subprocess (safe method)
            try:
                subprocess.run(['pbcopy'], input=text.encode('utf-8'), check=True)
                print("📋 Text copied to clipboard - paste with Cmd+V")
            except Exception as clipboard_error:
                print(f"❌ Clipboard copy failed: {clipboard_error}")

    def send_notification(self, title, message):
        """Send macOS notification"""
        try:
            script = f'display notification "{message}" with title "{title}"'
            subprocess.run(['osascript', '-e', script], check=False)
        except Exception as e:
            # Silently fail - notifications are not critical
            pass

    def on_press(self, key):
        """Handle key press events"""
        try:
            # Check for Control press
            if key == Key.ctrl_l or key == Key.ctrl_r:
                current_time = time.time()

                # If already recording, single Control press stops it
                if self.is_recording:
                    self.stop_recording()
                    self.last_ctrl_press_time = 0  # Reset
                # If not recording, check for double press to start
                elif current_time - self.last_ctrl_press_time < self.ctrl_double_press_threshold:
                    # Double press detected - start recording
                    self.start_recording()
                    self.last_ctrl_press_time = 0  # Reset
                else:
                    # First press - just update timestamp
                    self.last_ctrl_press_time = current_time

        except Exception as e:
            print(f"Error in key handler: {e}")

    def on_release(self, key):
        """Handle key release events"""
        pass

    def run(self):
        """Start the dictation service"""
        print("=" * 60)
        print("🎙️  Dictation Service Started")
        print("=" * 60)
        print("Controls:")
        print("  • Press Control twice quickly → Start recording")
        print("  • Press Control once → Stop recording and transcribe")
        print("=" * 60)
        print("Listening for hotkey...\n")

        # Start keyboard listener
        with keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release
        ) as listener:
            listener.join()


def main():
    try:
        service = DictationService()
        service.run()
    except KeyboardInterrupt:
        print("\n\n👋 Dictation service stopped")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
