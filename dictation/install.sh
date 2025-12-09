#!/bin/bash

echo "======================================"
echo "Installing Dictation Service"
echo "======================================"
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"
echo ""

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo ""
echo "✅ All dependencies installed successfully!"
echo ""
echo "======================================"
echo "Setup Complete!"
echo "======================================"
echo ""
echo "To start the dictation service, run:"
echo "  python3 dictation_service.py"
echo ""
echo "Or to run in background:"
echo "  python3 dictation_service.py &"
echo ""
echo "Controls:"
echo "  • Press Control twice → Start recording"
echo "  • Press Control once → Stop & transcribe"
echo ""
echo "IMPORTANT: Create a .env file with your OpenAI API key:"
echo "  cp .env.example .env"
echo "  # Edit .env and add your API key"
echo ""
