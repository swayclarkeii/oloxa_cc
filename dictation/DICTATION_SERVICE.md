# Dictation Service Documentation

## Overview
System-wide dictation service for macOS that uses OpenAI Whisper for transcription and GPT-4o-mini for text cleaning.

**Controls:**
- Press **Control twice** quickly → Start recording
- Press **Control once** → Stop recording and transcribe
- Copies cleaned text to clipboard
- **Press Cmd+V** to paste text where you want it
- Shows status via macOS notifications and menu bar icon (🎙️)

## Current Status
✅ **Working as of:** December 7, 2025 (11:41 PM CET)
- Version: v2.3 (clipboard-only mode - manual paste)
- Running as: User application (not LaunchAgent)
- Microphone access: Enabled
- Keyboard monitoring: Enabled
- Pasting method: Clipboard only (manual Cmd+V required)
- Launcher: Background mode (terminal auto-closes)

## Recent Changes

### v2.3 - Clipboard-Only Mode (Dec 7, 2025, 11:41 PM)
**CHANGED:** Switched to manual pasting for 100% reliability
- **Problem:** Automated pasting (pynput, AppleScript) caused duplicates and fragmentation in some IDEs (especially Cursor)
- **Solution:** Service now only copies to clipboard, shows notification when ready
- **Impact:** User manually pastes with Cmd+V - 100% reliable, no duplicates, no fragmentation
- **Workflow:**
  1. Control x2 → Start recording
  2. Speak your text
  3. Control → Stop and process
  4. Notification: "📋 Ready to Paste"
  5. Press Cmd+V to paste

### v2.2 - Background Launcher (Dec 7, 2025, 9:30 PM)
**FIXED:** Terminal no longer needs to stay open
- **Problem:** Menu bar icon disappeared when Terminal window was closed
- **Solution:** Launcher now uses `nohup` to run service in background, detached from terminal
- **Impact:** Terminal auto-closes after launch, service stays running
- **Features:**
  - Auto-close Terminal after successful launch
  - Duplicate detection (won't start if already running)
  - Status notifications on launch/failure
  - Service persists independently of Terminal

### v2.1 - Pasting Fix (Dec 7, 2025, 9:15 PM)
**FIXED:** Text no longer fragments or executes as commands when pasted
- **Problem:** Previously used `keyboard.type()` which interpreted special characters, causing text to break into chunks and trigger unwanted commands (especially Enter) in IDEs
- **Solution:** Switched to clipboard-based pasting (pbcopy + Cmd+V)
- **Impact:** 100% reliable pasting regardless of text content

---

## Files

### Core Application
- **`dictation_service_v2.py`** - Main application (ACTIVE)
  - Menu bar app using `rumps`
  - Native macOS notifications via `osascript`
  - Keyboard listener using `pynput`
  - Whisper transcription (local model: "base")
  - OpenAI GPT-4o-mini for text cleaning

### Launcher
- **`start_dictation.command`** - Double-click to start service (v2.2)
  - Runs service in background using `nohup`
  - Terminal auto-closes after launch
  - Duplicate detection prevents multiple instances
  - Shows notifications on success/failure
  - Added to Login Items for auto-start
  - Sets PYTHONPATH for venv packages
  - Logs to dictation.log and dictation_error.log

### Legacy/Backup Files
- `dictation_service.py` - Original minimal version (no HUD, no menu bar)
- `dictation_service_hud_backup.py` - Version with tkinter StatusHUD (deprecated)
- `dictation_service_fixed.py` - Attempted tkinter + rumps (FAILED - threading conflicts)
- `launch_service.sh` - LaunchAgent wrapper (no longer used)
- `com.dictation.service.plist` - LaunchAgent config (REMOVED - microphone access blocked)

### Configuration
- **`.env`** - Contains `OPENAI_API_KEY` (required)

### Logs
- `dictation.log` - Application output and debug info
- `dictation_error.log` - stderr output (warnings, errors)

---

## Dependencies

### Python Packages (in venv)
```
sounddevice      # Audio recording
soundfile        # WAV file handling
numpy           # Audio processing
pynput          # Keyboard monitoring
openai-whisper  # Local speech-to-text
openai          # GPT API client
python-dotenv   # Environment variables
rumps           # macOS menu bar app
```

### System Requirements
- macOS with Accessibility permissions (for keyboard monitoring)
- macOS with Microphone permissions (for audio recording)
- Python 3.12 at `/Library/Frameworks/Python.framework/Versions/3.12/bin/python3.12`
- Virtual environment at `/Users/swayclarke/coding_stuff/oloxa_cc/dictation/venv`

---

## Configuration

### Environment Variables
Create `.env` file in the dictation directory:
```bash
OPENAI_API_KEY=your-api-key-here
```

### Application Settings (in dictation_service_v2.py)
```python
WHISPER_MODEL_SIZE = "base"  # Options: tiny, base, small, medium, large
SAMPLE_RATE = 16000          # Audio sample rate
CHANNELS = 1                 # Mono audio
ctrl_double_press_threshold = 0.3  # Time window for double-press (seconds)
```

### GPT Cleaning Model
- Model: `gpt-4o-mini`
- Temperature: 0.3
- Max tokens: 2000
- Prompt: See `CLEANING_PROMPT` in dictation_service_v2.py (lines 51-96)

---

## How to Start/Stop

### Start the Service
1. **Double-click** `start_dictation.command` in Finder
2. Terminal window opens briefly
3. You'll see notification: "✅ Service Started - you can close this terminal"
4. Terminal auto-closes (or you can close it manually)
5. Menu bar icon 🎙️ appears
6. Ready to use - service runs in background!

**Note:** Service runs independently of Terminal - you can close all Terminal windows and it keeps running.

### Auto-Start on Login
Already configured in **System Settings → General → Login Items**
- The service will start automatically when you log in
- Terminal will briefly open and auto-close
- No manual interaction needed after login

### Stop the Service
**Method 1 (Recommended):**
1. Click 🎙️ icon in menu bar
2. Select "Quit"

**Method 2 (Command line):**
```bash
pkill -f dictation_service_v2.py
```

**Check if running:**
```bash
ps aux | grep dictation_service_v2.py | grep -v grep
```

---

## Troubleshooting

### Issue: No audio captured (transcription returns "..." or "you you")

**Symptoms:**
- Recording starts (icon changes to 🔴)
- Transcription completes but text is gibberish or empty
- Debug logs show `Max amplitude: 0.000000`

**Causes & Solutions:**

1. **Running as LaunchAgent (background service)**
   - ❌ **DOES NOT WORK** - macOS blocks microphone access for LaunchAgents
   - ✅ **SOLUTION:** Run as user application via `start_dictation.command`

2. **Microphone permissions not granted**
   - Check: System Settings → Privacy & Security → Microphone
   - Ensure Python (or Terminal) has microphone access
   - May need to run service directly once to trigger permission prompt

3. **Wrong audio input device selected**
   - Check available devices:
     ```bash
     python3 -c "import sounddevice as sd; print(sd.query_devices())"
     ```
   - Service uses default input device (marked with `>`)

4. **Another app using microphone**
   - Close Zoom, Teams, or other apps that might lock the microphone

---

### Issue: Keyboard hotkey not working

**Symptoms:**
- Control x2 doesn't start recording
- No response to keyboard input

**Causes & Solutions:**

1. **Accessibility permissions not granted**
   - Go to: System Settings → Privacy & Security → Accessibility
   - Add Python or Terminal to the list
   - Toggle it off and on if already present

2. **Service not running**
   - Check: `ps aux | grep dictation_service_v2.py`
   - If not running, launch via `start_dictation.command`

3. **Keyboard listener crashed**
   - Check logs: `tail -f dictation.log`
   - Look for errors in key handler
   - Restart service

---

### Issue: Menu bar icon not appearing

**Symptoms:**
- Service seems to run but no 🎙️ icon

**Causes & Solutions:**

1. **rumps not installed or failing**
   - Check: `pip list | grep rumps`
   - Install: `pip install rumps`

2. **Running in wrong Python environment**
   - Verify using: `/Library/Frameworks/Python.framework/Versions/3.12/bin/python3.12`
   - Ensure PYTHONPATH set correctly in launcher

3. **Menu bar too crowded**
   - macOS may hide the icon if menu bar is full
   - Try hiding other menu bar items

---

### Issue: Menu bar icon disappears when Terminal closes (FIXED in v2.2)

**Symptoms:**
- Icon appears when Terminal is open
- Icon disappears when Terminal window is closed
- Service stops when Terminal is closed

**Root Cause:**
- Earlier versions ran in foreground, attached to Terminal process
- Closing Terminal killed the parent process, terminating the service

**Solution (implemented in v2.2):**
- ✅ Launcher now uses `nohup` to run service in background
- ✅ Service detaches from Terminal completely
- ✅ Terminal auto-closes, service keeps running
- ✅ Menu bar icon persists independently

**If still experiencing issues:**
1. Ensure you're using the latest launcher:
   - Check: `head -3 start_dictation.command`
   - Should show: "Launcher for dictation service - runs in background"
2. Restart service using updated launcher

---

### Issue: Text pasting incorrectly (FIXED in v2.1)

**Symptoms:**
- Text appears fragmented when pasted
- Parts of text execute as commands (e.g., Enter key triggered)
- Only portion of transcript appears, rest seems to "run" in IDE
- Text broken into chunks with unintended actions between them

**Root Cause:**
- Earlier versions used `pynput.keyboard.type()` which interpreted special characters
- Newlines, punctuation, and special chars triggered keyboard commands
- Text would fragment and execute parts as code

**Solution (implemented in v2.1):**
- ✅ Now uses clipboard-based pasting (pbcopy + Cmd+V)
- Text remains intact regardless of content
- No interpretation of special characters
- Reliable pasting in all applications

**If still experiencing issues:**
1. Ensure you're running v2.1 or later:
   - Check: `head -20 dictation_service_v2.py | grep "Paste text at cursor location via clipboard"`
   - Should see the clipboard-based method
2. Restart the service:
   - Click 🎙️ → Quit
   - Double-click `start_dictation.command`

---

### Issue: Service won't start

**Symptoms:**
- Double-clicking `start_dictation.command` does nothing
- Terminal opens then closes immediately

**Check logs:**
```bash
tail -f /Users/swayclarke/coding_stuff/oloxa_cc/dictation/dictation.log
tail -f /Users/swayclarke/coding_stuff/oloxa_cc/dictation/dictation_error.log
```

**Common causes:**

1. **Missing .env file**
   - Error: "OPENAI_API_KEY not found"
   - Create `.env` with API key

2. **Missing dependencies**
   - Error: "ModuleNotFoundError"
   - Install: `pip install -r requirements.txt` (or install packages individually)

3. **Python path incorrect**
   - Verify: `which python3.12`
   - Should be: `/Library/Frameworks/Python.framework/Versions/3.12/bin/python3.12`

4. **Virtual environment issues**
   - Check PYTHONPATH in `start_dictation.command`
   - Should point to: `/Users/swayclarke/coding_stuff/oloxa_cc/dictation/venv/lib/python3.12/site-packages`

---

## Architecture & Code Flow

### Initialization (main function)
1. Create `DictationMenuBarApp` (rumps)
2. Create `DictationService`
3. Load Whisper model ("base")
4. Initialize OpenAI client
5. Start keyboard listener
6. Run menu bar app (blocks in main thread)

### Recording Flow
1. User presses Control twice (within 0.3s)
2. `on_press()` detects double-press
3. `start_recording()` called:
   - Sets `is_recording = True`
   - Updates menu icon to 🔴
   - Shows notification "Recording"
   - Starts `sounddevice.InputStream` with callback
4. Audio chunks arrive via `audio_callback()`:
   - Added to `audio_queue`
5. User presses Control once
6. `stop_recording()` called:
   - Sets `is_recording = False`
   - Stops and closes stream
   - Collects all audio chunks from queue
   - Spawns background thread for processing

### Processing Flow
1. `process_audio()` runs in background thread:
2. Concatenates audio chunks into single array
3. Saves to temporary WAV file
4. Transcribes with Whisper:
   - Model: "base"
   - Returns raw text
5. Cleans transcript with OpenAI:
   - Model: gpt-4o-mini
   - Extracts content after "### Clean Transcript"
6. Copies text to clipboard:
   - Copies cleaned text to clipboard via `pbcopy`
   - Shows notification: "📋 Ready to Paste - Press Cmd+V to paste"
   - User manually pastes with Cmd+V (100% reliable, no automation issues)
7. Processing complete - text ready in clipboard

---

## Known Issues & Limitations

### 1. LaunchAgent Microphone Access
- **Issue:** macOS security prevents LaunchAgents from accessing microphone
- **Impact:** Background service mode doesn't work
- **Workaround:** Run as user application via `start_dictation.command`
- **Status:** Working as intended with current setup

### 2. Whisper FP16 Warning
- **Warning:** "FP16 is not supported on CPU; using FP32 instead"
- **Impact:** None - automatic fallback to FP32
- **Status:** Cosmetic only, can be ignored

### 3. Resource Tracker Semaphore Leak
- **Warning:** "There appear to be 1 leaked semaphore objects to clean up at shutdown"
- **Impact:** Minor - cleaned up on exit
- **Status:** Known Whisper/multiprocessing issue, harmless

### 4. Secure Coding Warning
- **Warning:** "Secure coding is not enabled for restorable state"
- **Impact:** None for our use case
- **Status:** rumps framework issue, can be ignored

### 5. Double-press Sensitivity
- **Issue:** Sometimes requires practice to get timing right
- **Impact:** May miss start recording if pressed too slowly
- **Workaround:** Adjust `ctrl_double_press_threshold` in code (currently 0.3s)

---

## Version History

### v2.2 (Current - Dec 7, 2025, 9:30 PM CET)
- ✅ **FIXED:** Background launcher - Terminal no longer needs to stay open
- ✅ Service runs detached using `nohup`
- ✅ Terminal auto-closes after successful launch
- ✅ Duplicate detection prevents multiple instances
- ✅ Launch notifications show success/failure status
- ✅ Menu bar icon persists independently of Terminal

### v2.1 (Dec 7, 2025, 9:15 PM CET)
- ✅ **FIXED:** Clipboard-based pasting (pbcopy + Cmd+V)
- ✅ Prevents text fragmentation during paste
- ✅ No more unwanted command execution in IDEs
- ✅ Reliable pasting regardless of text content (newlines, special chars, etc.)

### v2 (Dec 7, 2025, 8:00 PM CET)
- ✅ Native macOS notifications (osascript)
- ✅ Menu bar icon with rumps
- ✅ Runs as user application (not LaunchAgent)
- ✅ Full microphone access
- ✅ Auto-start via Login Items
- ❌ Removed tkinter HUD (threading conflicts)
- ❌ Had pasting issues with keyboard.type() method

### v1.5 (Attempted)
- ❌ Tried combining tkinter HUD + rumps menu bar
- ❌ Failed: Threading conflicts ("Calling Tcl from different apartment")

### v1 (Backup)
- Basic recording and transcription
- No UI feedback
- No menu bar icon

---

## File Locations

### Application Directory
```
/Users/swayclarke/coding_stuff/oloxa_cc/dictation/
├── dictation_service_v2.py      # Main app (ACTIVE)
├── start_dictation.command      # Launcher
├── .env                         # API key
├── dictation.log               # Application logs
├── dictation_error.log         # Error logs
├── venv/                       # Virtual environment
│   └── lib/python3.12/site-packages/
├── dictation_service.py        # Backup
├── dictation_service_hud_backup.py  # Backup
└── dictation_service_fixed.py  # Failed attempt
```

### Login Items
```
System Settings → General → Login Items
- start_dictation.command (enabled)
```

### Temporary Files
```
/var/folders/.../T/tmpXXXXXX/recording_*.wav
```
- Created during transcription
- Automatically cleaned up after processing

---

## Performance Notes

### Whisper Model Sizes
- **tiny**: Fastest, lowest quality (~1GB RAM)
- **base**: Good balance (current) (~1.5GB RAM)
- **small**: Better accuracy (~2.5GB RAM)
- **medium**: High accuracy (~5GB RAM)
- **large**: Best accuracy (~10GB RAM)

Current setting: **base** - Good enough for most dictation

### Processing Time
- Recording: Real-time
- Whisper transcription: ~2-5 seconds for 10s audio (base model)
- GPT cleaning: ~1-2 seconds
- Total latency: ~3-7 seconds for typical dictation

### Resource Usage
- Idle: ~150MB RAM
- With Whisper model loaded: ~1.5GB RAM
- During transcription: ~2GB RAM, 50-100% CPU (brief spike)

---

## API Costs

### OpenAI API (GPT-4o-mini)
- Model: gpt-4o-mini
- Cost: ~$0.0001 per cleaning (very cheap)
- Average transcript: 100-500 tokens
- Estimated: $0.01 per 100 transcriptions

### Whisper
- Runs locally (no API calls)
- No additional costs

---

## Security & Privacy

### Local Processing
- ✅ Audio recorded locally
- ✅ Whisper transcription runs locally (no data sent to cloud)

### Cloud Processing
- ⚠️ Raw transcripts sent to OpenAI for cleaning
- API calls encrypted (HTTPS)
- OpenAI doesn't train on API data (per policy)

### Sensitive Data
- Store OPENAI_API_KEY in `.env` (not committed to git)
- `.env` should be in `.gitignore`

---

## Development & Debugging

### Enable Debug Logging
Add to `audio_callback()` in dictation_service_v2.py:
```python
max_amp = np.max(np.abs(indata))
print(f"DEBUG: Audio chunk received, max amplitude: {max_amp:.6f}")
```

Add to `stop_recording()`:
```python
print(f"DEBUG: Collected {len(self.audio_data)} audio chunks")
```

Add to `process_audio()`:
```python
max_amp = np.max(np.abs(audio_array))
mean_amp = np.mean(np.abs(audio_array))
duration = len(audio_array) / SAMPLE_RATE
print(f"DEBUG: Combined audio - Duration: {duration:.2f}s, Max amp: {max_amp:.6f}, Mean amp: {mean_amp:.6f}")
```

### Watch Logs in Real-Time
```bash
tail -f /Users/swayclarke/coding_stuff/oloxa_cc/dictation/dictation.log
```

### Test Microphone Directly
```bash
cd /Users/swayclarke/coding_stuff/oloxa_cc/dictation
PYTHONPATH="venv/lib/python3.12/site-packages" python3.12 test_mic.py
```

### Check Running Processes
```bash
ps aux | grep dictation_service_v2.py
```

### Manual Start (for debugging)
```bash
cd /Users/swayclarke/coding_stuff/oloxa_cc/dictation
export PYTHONPATH="venv/lib/python3.12/site-packages"
/Library/Frameworks/Python.framework/Versions/3.12/bin/python3.12 -u dictation_service_v2.py
```

---

## Future Improvements

### Potential Enhancements
- [ ] Configurable hotkey (not just Control x2)
- [ ] Multiple Whisper model sizes selectable from menu
- [ ] Option to skip GPT cleaning (paste raw transcript)
- [ ] History of recent transcriptions
- [ ] Export transcription history
- [ ] Custom cleaning prompts
- [ ] Language selection for Whisper
- [ ] Visual feedback during recording (waveform?)
- [ ] Keyboard shortcuts for paste/copy instead of auto-paste

### Code Improvements
- [ ] Package as proper .app bundle
- [ ] Automatic updates
- [ ] Settings UI instead of editing code
- [ ] Better error handling and user feedback
- [ ] Unit tests
- [ ] Installation script

---

## Contact & Support

**Location:** `/Users/swayclarke/coding_stuff/oloxa_cc/dictation/`

**Documentation:** This file (DICTATION_SERVICE.md)

**Logs:**
- Application: `dictation.log`
- Errors: `dictation_error.log`

**Last Updated:** December 7, 2025, 9:30 PM CET (v2.2 - background launcher)
