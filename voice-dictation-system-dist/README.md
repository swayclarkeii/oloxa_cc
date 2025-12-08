# Voice Dictation System for macOS

Transform your speech into polished, clean text with AI-powered transcription and cleaning.

## What It Does

- **Press Control twice** to start recording your voice
- **Speak naturally** - say whatever you want to write
- **Press Control once** to stop recording
- The system transcribes your speech using Whisper (runs locally on your Mac)
- Cleans up the transcript with OpenAI (removes "um," "uh," fixes grammar)
- **Automatically pastes** the polished text wherever your cursor is

Works in **any application**: browsers, text editors, chat apps, coding tools, anywhere!

## Requirements

- macOS (tested on macOS 10.15+)
- Python 3.10, 3.11, 3.12, or 3.13
- OpenAI API key (for text cleaning)
- Microphone

## Quick Start

### 1. Install

Double-click to run or open Terminal and run:

```bash
bash install.sh
```

This will:
- Check your Python installation
- Install all required packages
- Run the setup wizard to configure your API key

### 2. Get Your OpenAI API Key

You'll need an API key from OpenAI:

1. Visit [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Sign in or create an account
3. Click **"Create new secret key"**
4. Copy the key (starts with `sk-`)
5. Paste it when the setup wizard asks

**Cost:** Very low - typically less than $0.01 per transcription

### 3. Grant Permissions

When you first run the service, macOS will ask for:

- ✅ **Microphone access** - Click "OK" to allow recording
- ✅ **Accessibility access** - Click "Open System Settings" → Enable for Terminal/Python

### 4. Start Using

```bash
bash start_dictation.sh
```

You'll see:
```
Loading Whisper model...
Whisper model 'base' loaded successfully
============================================================
🎙️  Dictation Service Started
============================================================
Controls:
  • Press Control twice quickly → Start recording
  • Press Control once → Stop recording and transcribe
============================================================
Listening for hotkey...
```

Now you can use it in **any app**:
1. Click where you want text to appear
2. Press **Control** twice quickly
3. See notification: "Recording Started"
4. Speak your message
5. Press **Control** once
6. Watch as clean text appears!

## Visual Feedback

You'll see macOS notifications at each step:
- 🎙️ **Recording Started** - Speak now
- 🔄 **Transcribing...** - Converting speech to text
- ✨ **Cleaning Text...** - Polishing your transcript
- ✅ **Complete!** - Text has been pasted

## Troubleshooting

### "No module named..." error
Run the installer again:
```bash
bash install.sh
```

### Recording doesn't start
- Make sure you press Control **twice quickly** (within 0.3 seconds)
- Check that Terminal or Python has Accessibility permission in System Settings

### Text doesn't paste
- The system will copy to clipboard as a fallback
- Paste manually with Cmd+V
- Make sure Terminal/Python has Accessibility permission

### "API key not found" error
Run the setup wizard:
```bash
python3 setup_wizard.py
```

### Service stops working after macOS update
Re-grant permissions in System Settings > Privacy & Security

## Configuration

### Change Whisper Model Speed/Accuracy

Edit `dictation_service.py`, line 46:

```python
WHISPER_MODEL_SIZE = "base"  # Options: tiny, base, small, medium, large
```

- **tiny** - Fastest (~1 sec), less accurate
- **base** - Good balance (~2-3 sec) ← Default
- **small** - Better accuracy (~4-5 sec)
- **medium/large** - Best accuracy (slower, needs more RAM)

### Change Your API Key

```bash
python3 setup_wizard.py
```

Or edit `.env` file directly.

### Auto-Start on Login

The installer can add auto-start to your `~/.zshrc`.

Or manually add:
```bash
# Auto-start dictation service
if ! pgrep -f "dictation_service.py" > /dev/null; then
    nohup /path/to/start_dictation.sh > /dev/null 2>&1 &
fi
```

## Files Included

- `dictation_service.py` - Main service code
- `start_dictation.sh` - Launch script
- `install.sh` - Automated installer
- `setup_wizard.py` - Configuration wizard
- `requirements.txt` - Python dependencies
- `.env.example` - Template for API key
- `README.md` - This file

## Uninstall

1. Remove auto-start from `~/.zshrc` if configured
2. Stop the service: `pkill -f dictation_service.py`
3. Delete this folder

## Privacy & Security

- **Speech transcription** happens locally on your Mac (Whisper)
- **Text cleaning** sends transcripts to OpenAI's API
- **API key** is stored in `.env` file (not shared)
- **No data collection** - everything stays on your computer except the API call

## Credits

Built with:
- [OpenAI Whisper](https://github.com/openai/whisper) - Speech recognition
- [OpenAI API](https://openai.com) - Text cleaning with GPT-4o-mini
- [pynput](https://github.com/moses-palmer/pynput) - Keyboard monitoring
- [sounddevice](https://python-sounddevice.readthedocs.io/) - Audio recording

## Support

For issues or questions:
1. Check the Troubleshooting section above
2. Review the installation guide PDF
3. Make sure all permissions are granted in System Settings

## License

This software is provided as-is for personal use.
