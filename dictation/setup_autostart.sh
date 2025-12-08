#!/bin/bash

echo "======================================"
echo "Setting up Dictation Service Auto-Start"
echo "======================================"
echo ""

# First, make sure dependencies are installed
echo "Checking dependencies..."
if ! pip3 show openai-whisper &> /dev/null; then
    echo "📦 Installing dependencies first..."
    ./install.sh
    echo ""
fi

# Load the LaunchAgent
echo "🔧 Loading LaunchAgent..."
launchctl unload ~/Library/LaunchAgents/com.dictation.service.plist 2>/dev/null
launchctl load ~/Library/LaunchAgents/com.dictation.service.plist

if [ $? -eq 0 ]; then
    echo "✅ LaunchAgent loaded successfully!"
    echo ""
    echo "======================================"
    echo "Setup Complete!"
    echo "======================================"
    echo ""
    echo "The dictation service will now:"
    echo "  ✓ Start automatically when you log in"
    echo "  ✓ Restart automatically if it crashes"
    echo "  ✓ Run in the background (no Terminal needed)"
    echo ""
    echo "To use it:"
    echo "  • Press Control twice → Start recording"
    echo "  • Press Enter → Stop & transcribe"
    echo ""
    echo "To check if it's running:"
    echo "  ps aux | grep dictation_service"
    echo ""
    echo "To view logs:"
    echo "  tail -f ~/coding_stuff/oloxa_cc/dictation/dictation.log"
    echo ""
    echo "To stop the service:"
    echo "  launchctl unload ~/Library/LaunchAgents/com.dictation.service.plist"
    echo ""
    echo "To restart the service:"
    echo "  launchctl unload ~/Library/LaunchAgents/com.dictation.service.plist"
    echo "  launchctl load ~/Library/LaunchAgents/com.dictation.service.plist"
    echo ""
else
    echo "❌ Failed to load LaunchAgent"
    echo "Check for errors above"
    exit 1
fi
