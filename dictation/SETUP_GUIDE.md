# Dictation Service - Setup Guide

A system-wide dictation tool that transcribes and cleans your speech, then pastes it wherever your cursor is.

## Quick Start

### 1. Install Dependencies

Open Terminal and navigate to this folder:
```bash
cd /Users/swayclarke/coding_stuff/oloxa_cc/dictation
```

Run the install script:
```bash
./install.sh
```

### 2. Start the Service

```bash
python3 dictation_service.py
```

You should see:
```
Loading Whisper model...
Whisper model 'base' loaded successfully
🎙️  Dictation Service Started
Controls:
  • Press Control twice quickly → Start recording
  • Press Enter → Stop recording and transcribe
```

### 3. Use It!

1. Put your cursor anywhere (Cursor IDE, Terminal, browser, etc.)
2. **Press Control key twice quickly** → Recording starts
3. Speak your text
4. **Press Enter** → Recording stops, transcribes, cleans, and pastes

## How It Works

```
Press Ctrl twice → Record → Press Enter → Whisper transcribes →
OpenAI cleans → Auto-paste at cursor
```

**Fallback:** If auto-paste fails, text is copied to clipboard (paste with Cmd+V)

## Running in Background

To keep it running without the Terminal window:

```bash
nohup python3 dictation_service.py > dictation.log 2>&1 &
```

Check if it's running:
```bash
ps aux | grep dictation_service
```

Stop it:
```bash
pkill -f dictation_service.py
```

## Auto-Start on Login (Optional)

### Method 1: Create a LaunchAgent

1. Create a plist file:
```bash
mkdir -p ~/Library/LaunchAgents
nano ~/Library/LaunchAgents/com.dictation.service.plist
```

2. Paste this content:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.dictation.service</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/python3</string>
        <string>/Users/swayclarke/coding_stuff/oloxa_cc/dictation/dictation_service.py</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/Users/swayclarke/coding_stuff/oloxa_cc/dictation/dictation.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/swayclarke/coding_stuff/oloxa_cc/dictation/dictation_error.log</string>
</dict>
</plist>
```

3. Load the service:
```bash
launchctl load ~/Library/LaunchAgents/com.dictation.service.plist
```

4. Unload if needed:
```bash
launchctl unload ~/Library/LaunchAgents/com.dictation.service.plist
```

### Method 2: Add to Login Items

1. Create a simple launcher script:
```bash
nano ~/start_dictation.sh
```

2. Add:
```bash
#!/bin/bash
cd /Users/swayclarke/coding_stuff/oloxa_cc/dictation
python3 dictation_service.py
```

3. Make executable:
```bash
chmod +x ~/start_dictation.sh
```

4. Add to Login Items:
   - System Settings → General → Login Items
   - Click "+" and add `start_dictation.sh`

## Customization

### Change Hotkey

Edit [dictation_service.py](dictation_service.py:59):

```python
# Current: Double Control press
# To change, modify the on_press method around line 190
```

### Change Whisper Model

Edit [dictation_service.py](dictation_service.py:37):

```python
WHISPER_MODEL_SIZE = "base"  # Options: tiny, base, small, medium, large
```

Larger models = more accurate but slower

### Modify Cleaning Prompt

Edit the `CLEANING_PROMPT` variable starting at [dictation_service.py](dictation_service.py:40)

## Troubleshooting

### "No module named 'sounddevice'"
```bash
pip3 install sounddevice soundfile numpy pynput openai-whisper openai rumps
```

### "Permission denied" when recording
Grant Terminal microphone access:
- System Settings → Privacy & Security → Microphone
- Enable for Terminal

### Auto-paste not working
The service falls back to clipboard. Check:
- macOS Accessibility permissions for Terminal
- Try pasting with Cmd+V

### Recording not starting
- Make sure you press Control twice **quickly** (within 0.3 seconds)
- Check Terminal output for errors

### Service crashes
Check logs:
```bash
tail -f dictation.log
tail -f dictation_error.log
```

## Performance Tips

1. **Faster transcription**: Use `tiny` or `base` model
2. **Better accuracy**: Use `medium` or `large` model
3. **Network issues**: Service works 100% offline except for cleaning (OpenAI API)
4. **Battery saving**: Use smaller models or only run when needed

## Files

- `dictation_service.py` - Main service script
- `requirements.txt` - Python dependencies
- `install.sh` - Installation script
- `SETUP_GUIDE.md` - This file
- `README.md` - Original transcription script docs

## Security Note

Your OpenAI API key is stored in the `dictation_service.py` file. Keep this file private and don't share it publicly.

To use environment variable instead:
1. Remove the API key from the script
2. Add to your `~/.zshrc` or `~/.bash_profile`:
```bash
export OPENAI_API_KEY="your-key-here"
```
3. Reload: `source ~/.zshrc`

## Support

If something isn't working:
1. Check Terminal output for error messages
2. Verify all dependencies are installed: `pip3 list`
3. Test Whisper separately with the original `transcribe_audio.py`
4. Check microphone permissions in System Settings
