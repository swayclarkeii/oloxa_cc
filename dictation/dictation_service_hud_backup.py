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
    import tkinter as tk
except ImportError as e:
    print(f"Missing dependency: {e}")
    print("\nPlease install required packages:")
    print("pip install sounddevice soundfile numpy pynput openai-whisper openai python-dotenv")
    sys.exit(1)

# Load environment variables from .env file
load_dotenv()

# Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    print("❌ Error: OPENAI_API_KEY not found!")
    print("\nPlease create a .env file in the same directory as this script with:")
    print("OPENAI_API_KEY=your-api-key-here")
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


class StatusHUD:
    """On-screen heads-up display with rounded corners and animations"""

    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()  # Hide initially
        self.root.overrideredirect(True)  # Remove window decorations
        self.root.attributes('-topmost', True)  # Always on top

        # Make background transparent for rounded corners
        self.root.config(bg='systemTransparent')
        self.root.wm_attributes('-transparent', True)

        # Get screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # HUD dimensions - compact and modern
        self.hud_width = 300
        self.hud_height = 80
        self.target_x = (screen_width - self.hud_width) // 2
        self.target_y = screen_height // 3
        self.current_x = self.target_x
        self.current_y = self.target_y - 30  # Start above target

        self.root.geometry(f'{self.hud_width}x{self.hud_height}+{self.current_x}+{self.current_y}')

        # Create canvas for rounded rectangle
        self.canvas = tk.Canvas(
            self.root,
            width=self.hud_width,
            height=self.hud_height,
            bg='systemTransparent',
            highlightthickness=0
        )
        self.canvas.pack()

        # Colors
        self.bg_color = '#FFFFFF'
        self.border_color = '#D1D1D6'
        self.text_color = '#1D1D1F'

        # Draw rounded rectangle background
        self.bg_rect = self._create_rounded_rectangle(
            2, 2, self.hud_width-2, self.hud_height-2,
            radius=16,
            fill=self.bg_color,
            outline=self.border_color,
            width=2
        )

        # Create text elements
        self.emoji_text = self.canvas.create_text(
            self.hud_width // 2,
            self.hud_height // 2 - 5,
            text="",
            font=('SF Pro Display', 24),
            fill=self.text_color
        )

        self.status_text = self.canvas.create_text(
            self.hud_width // 2,
            self.hud_height // 2 + 15,
            text="",
            font=('SF Pro Text', 13),
            fill=self.text_color
        )

        self.hide_timer = None
        self.current_alpha = 0.0
        self.animation_running = False

    def _create_rounded_rectangle(self, x1, y1, x2, y2, radius=20, **kwargs):
        """Create a rounded rectangle on canvas"""
        points = [
            x1+radius, y1,
            x1+radius, y1,
            x2-radius, y1,
            x2-radius, y1,
            x2, y1,
            x2, y1+radius,
            x2, y1+radius,
            x2, y2-radius,
            x2, y2-radius,
            x2, y2,
            x2-radius, y2,
            x2-radius, y2,
            x1+radius, y2,
            x1+radius, y2,
            x1, y2,
            x1, y2-radius,
            x1, y2-radius,
            x1, y1+radius,
            x1, y1+radius,
            x1, y1
        ]
        return self.canvas.create_polygon(points, **kwargs, smooth=True)

    def slide_and_fade_in(self, steps=15, duration=300):
        """Slide down and fade in animation"""
        def animate(step=0):
            if step <= steps:
                # Calculate progress
                progress = step / steps

                # Easing function (ease-out)
                eased = 1 - (1 - progress) ** 3

                # Fade in
                alpha = eased * 0.97
                self.root.attributes('-alpha', alpha)
                self.current_alpha = alpha

                # Slide down
                y = int(self.current_y + (self.target_y - self.current_y) * eased)
                self.root.geometry(f'{self.hud_width}x{self.hud_height}+{self.target_x}+{y}')

                # Scale effect on canvas (subtle grow)
                scale = 0.9 + (0.1 * eased)
                self.canvas.scale('all', self.hud_width//2, self.hud_height//2, scale/((step-1)/steps*0.1+0.9) if step > 0 else 1, scale/((step-1)/steps*0.1+0.9) if step > 0 else 1)

                self.root.after(duration // steps, lambda s=step: animate(s + 1))

        self.animation_running = True
        self.root.after(0, animate)

    def slide_and_fade_out(self, steps=12, duration=250):
        """Slide up and fade out animation"""
        def animate(step=0):
            if step <= steps:
                progress = step / steps
                eased = progress ** 2

                # Fade out
                alpha = self.current_alpha * (1 - eased)
                self.root.attributes('-alpha', alpha)

                # Slide up
                y = int(self.target_y - 20 * eased)
                self.root.geometry(f'{self.hud_width}x{self.hud_height}+{self.target_x}+{y}')

                self.root.after(duration // steps, lambda s=step: animate(s + 1))
            else:
                self.root.withdraw()
                self.animation_running = False

        self.root.after(0, animate)

    def pulse_emoji(self, count=2):
        """Pulse the emoji for visual feedback"""
        def pulse(iteration=0, growing=True):
            if iteration >= count * 2:
                return

            if growing:
                scale = 1.15
            else:
                scale = 1.0 / 1.15

            # Scale emoji text
            self.canvas.scale(self.emoji_text, self.hud_width//2, self.hud_height//2 - 5, scale, scale)

            self.root.after(150, lambda: pulse(iteration + 1, not growing))

        self.root.after(0, pulse)

    def show(self, message, emoji="", auto_hide=False, delay=2.0):
        """Show HUD with slide-in animation"""
        def _show():
            # Update text
            self.canvas.itemconfig(self.emoji_text, text=emoji)
            self.canvas.itemconfig(self.status_text, text=message)

            # Reset position
            self.current_y = self.target_y - 30
            self.root.geometry(f'{self.hud_width}x{self.hud_height}+{self.target_x}+{self.current_y}')

            # Show and animate
            self.root.deiconify()
            self.root.lift()
            self.slide_and_fade_in()

            if auto_hide:
                if self.hide_timer:
                    self.root.after_cancel(self.hide_timer)
                self.hide_timer = self.root.after(int(delay * 1000), self.hide)

        self.root.after(0, _show)

    def hide(self):
        """Hide HUD with slide-out animation"""
        def _hide():
            if not self.animation_running:
                self.slide_and_fade_out()

        self.root.after(0, _hide)

    def update_message(self, message, emoji=""):
        """Update message with pulse animation"""
        def _update():
            # Update text
            self.canvas.itemconfig(self.emoji_text, text=emoji)
            self.canvas.itemconfig(self.status_text, text=message)

            # Pulse the emoji
            if emoji:
                self.pulse_emoji(count=1)

        self.root.after(0, _update)


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

        # Initialize HUD
        self.hud = StatusHUD()

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
        self.hud.show("Recording...\nSpeak now!", emoji="🎙️")

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
            self.hud.update_message("Transcribing...", emoji="🔄")
            result = self.whisper_model.transcribe(temp_audio_path, language="en")
            raw_transcript = result["text"].strip()

            print(f"📝 Raw transcript: {raw_transcript[:100]}...")

            # Clean transcript with OpenAI
            print("✨ Cleaning transcript...")
            self.hud.update_message("Cleaning text...", emoji="✨")
            cleaned_text = self.clean_transcript(raw_transcript)

            print(f"✅ Cleaned: {cleaned_text[:100]}...")

            # Paste to cursor location
            self.paste_text(cleaned_text)
            self.hud.show("Complete!", emoji="✅", auto_hide=True, delay=2.0)

            # Cleanup
            try:
                os.remove(temp_audio_path)
            except:
                pass

        except Exception as e:
            print(f"❌ Error processing audio: {e}")
            self.hud.show("Error!\nCheck Terminal", emoji="❌", auto_hide=True, delay=3.0)
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

        # Start keyboard listener in background thread
        self.listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release
        )
        self.listener.start()

        # Run tkinter mainloop (blocks until window closed)
        try:
            self.hud.root.mainloop()
        except KeyboardInterrupt:
            self.listener.stop()
            raise


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
