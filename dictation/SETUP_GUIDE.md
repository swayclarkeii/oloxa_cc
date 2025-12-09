# Dictation Service - Setup Guide

A system-wide dictation tool that transcribes and cleans your speech, then pastes it wherever your cursor is.

## Quick Start

### 1. Navigate to this folder

```bash
cd path/to/dictation
```

### 2. Set up your API key

```bash
# Copy the example file
cp .env.example .env

# Edit and add your OpenAI API key
nano .env
# Or open with any text editor
```

Your `.env` file should contain:
```
OPENAI_API_KEY=sk-your-actual-api-key-here
```

Get an API key at: https://platform.openai.com/api-keys

### 3. Create a virtual environment and install dependencies

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 4. Start the Service

```bash
./start_dictation.sh
```

Or manually:
```bash
source venv/bin/activate
python3 dictation_service.py
```

You should see:
```
Loading Whisper model...
Whisper model 'base' loaded successfully
🎙️  Dictation Service Started
Controls:
  • Press Control twice quickly → Start recording
  • Press Control once → Stop recording and transcribe
```

### 5. Use It!

1. Put your cursor anywhere (Cursor IDE, Terminal, browser, etc.)
2. **Press Control key twice quickly** → Recording starts
3. Speak your text
4. **Press Control once** → Recording stops, transcribes, cleans, and pastes

## How It Works

```
Press Ctrl twice → Record → Press Ctrl once → Whisper transcribes →
OpenAI cleans → Auto-paste at cursor
```

**Fallback:** If auto-paste fails, text is copied to clipboard (paste with Cmd+V)

## Running in Background

Double-click `start_dictation.command` to run in background, or:

```bash
./launch_service.sh
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

1. Create the LaunchAgents directory:
```bash
mkdir -p ~/Library/LaunchAgents
```

2. Create a plist file - replace `YOUR_PATH` with your actual installation path:
```bash
nano ~/Library/LaunchAgents/com.dictation.service.plist
```

3. Paste this content (update paths):
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.dictation.service</string>
    <key>ProgramArguments</key>
    <array>
        <string>YOUR_PATH/dictation/venv/bin/python3</string>
        <string>YOUR_PATH/dictation/dictation_service.py</string>
    </array>
    <key>WorkingDirectory</key>
    <string>YOUR_PATH/dictation</string>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>YOUR_PATH/dictation/dictation.log</string>
    <key>StandardErrorPath</key>
    <string>YOUR_PATH/dictation/dictation_error.log</string>
</dict>
</plist>
```

4. Load the service:
```bash
launchctl load ~/Library/LaunchAgents/com.dictation.service.plist
```

5. Unload if needed:
```bash
launchctl unload ~/Library/LaunchAgents/com.dictation.service.plist
```

### Method 2: Add to Login Items

1. System Settings → General → Login Items
2. Click "+" and add `start_dictation.command`

## Customization

### Change Whisper Model

Edit `dictation_service.py`:

```python
WHISPER_MODEL_SIZE = "base"  # Options: tiny, base, small, medium, large
```

| Model  | Speed    | Accuracy  |
|--------|----------|-----------|
| tiny   | Fastest  | Good      |
| base   | Fast     | Better    |
| small  | Medium   | Great     |
| medium | Slow     | Excellent |
| large  | Slowest  | Best      |

### Modify Cleaning Prompt

Edit the `CLEANING_PROMPT` variable in `dictation_service.py`

## Troubleshooting

### "OPENAI_API_KEY not found"
Make sure you've created the `.env` file:
```bash
cp .env.example .env
# Edit .env and add your API key
```

### "No module named 'sounddevice'"
```bash
source venv/bin/activate
pip install -r requirements.txt
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

## Files

| File | Description |
|------|-------------|
| `dictation_service.py` | Main service script |
| `.env.example` | Template for API key configuration |
| `.env` | Your API key (create from .env.example) |
| `requirements.txt` | Python dependencies |
| `install.sh` | Installation script |
| `start_dictation.sh` | Start script for terminal |
| `start_dictation.command` | Double-click launcher |
| `launch_service.sh` | Background launcher |
| `SETUP_GUIDE.md` | This file |

## Security

- Your API key is stored in `.env` which is gitignored (never committed)
- Never share your `.env` file
- The `.env.example` file is safe to share (contains no real keys)

## Support

If something isn't working:
1. Check Terminal output for error messages
2. Verify `.env` file exists with valid API key
3. Verify all dependencies are installed: `pip list`
4. Check microphone permissions in System Settings
