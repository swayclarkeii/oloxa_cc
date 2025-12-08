#!/bin/bash

# Voice Dictation System - Automated Installer
# This script installs all required dependencies

set -e  # Exit on error

echo "========================================"
echo "  Voice Dictation System - Installer"
echo "========================================"
echo ""

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Find suitable Python
PYTHON_CMD=""
echo "[1/5] Finding Python installation..."
for py_path in \
    "/Library/Frameworks/Python.framework/Versions/3.12/bin/python3" \
    "/Library/Frameworks/Python.framework/Versions/3.11/bin/python3" \
    "/Library/Frameworks/Python.framework/Versions/3.10/bin/python3" \
    "/opt/homebrew/bin/python3" \
    "/usr/local/bin/python3" \
    "$(which python3 2>/dev/null)"; do

    if [ -x "$py_path" ]; then
        version=$("$py_path" -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")' 2>/dev/null || echo "0.0")
        major=$(echo $version | cut -d. -f1)
        minor=$(echo $version | cut -d. -f2)

        if [ "$major" -eq 3 ] && [ "$minor" -ge 10 ] && [ "$minor" -lt 14 ]; then
            PYTHON_CMD="$py_path"
            echo "  ✓ Found Python $version at: $py_path"
            break
        fi
    fi
done

if [ -z "$PYTHON_CMD" ]; then
    echo "  ❌ Error: Python 3.10-3.13 not found"
    echo ""
    echo "Please install Python from: https://www.python.org/downloads/"
    echo "Recommended version: Python 3.12"
    exit 1
fi

# Check pip
echo ""
echo "[2/5] Checking pip..."
if ! "$PYTHON_CMD" -m pip --version > /dev/null 2>&1; then
    echo "  ❌ Error: pip not found"
    echo "Installing pip..."
    "$PYTHON_CMD" -m ensurepip --upgrade
fi
echo "  ✓ pip is available"

# Install dependencies
echo ""
echo "[3/5] Installing Python packages..."
echo "This may take a few minutes..."
echo ""

# Create requirements.txt if it doesn't exist
cat > "$SCRIPT_DIR/requirements.txt" << 'EOF'
# Core dependencies for dictation service
openai>=1.0.0
openai-whisper>=20230314
sounddevice>=0.4.6
soundfile>=0.12.1
numpy>=1.24.0
pynput>=1.7.6
python-dotenv>=1.0.0
EOF

# Install packages
if "$PYTHON_CMD" -m pip install -r requirements.txt --break-system-packages 2>/dev/null; then
    echo "  ✓ Packages installed successfully"
elif "$PYTHON_CMD" -m pip install -r requirements.txt --user 2>/dev/null; then
    echo "  ✓ Packages installed successfully (user mode)"
elif "$PYTHON_CMD" -m pip install -r requirements.txt; then
    echo "  ✓ Packages installed successfully"
else
    echo "  ❌ Error installing packages"
    echo "Please try manually:"
    echo "  $PYTHON_CMD -m pip install -r requirements.txt"
    exit 1
fi

# Run setup wizard
echo ""
echo "[4/5] Running setup wizard..."
echo ""
if [ ! -f ".env" ]; then
    "$PYTHON_CMD" setup_wizard.py
else
    echo "  ✓ Configuration already exists (.env file found)"
    echo "    Run 'python3 setup_wizard.py' to reconfigure"
fi

# Create auto-start configuration
echo ""
echo "[5/5] Optional: Auto-start configuration"
echo ""
echo "Would you like the dictation service to start automatically when you open Terminal?"
echo "(You can set this up later by adding to your ~/.zshrc)"
read -p "Configure auto-start? (y/N): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    # Check if already configured
    if grep -q "dictation_service.py" ~/.zshrc 2>/dev/null; then
        echo "  ⚠️  Auto-start already configured in ~/.zshrc"
    else
        echo "" >> ~/.zshrc
        echo "# Auto-start dictation service" >> ~/.zshrc
        echo "if ! pgrep -f \"dictation_service.py\" > /dev/null; then" >> ~/.zshrc
        echo "    nohup \"$SCRIPT_DIR/start_dictation.sh\" > /dev/null 2>&1 &" >> ~/.zshrc
        echo "fi" >> ~/.zshrc
        echo "  ✓ Auto-start configured in ~/.zshrc"
    fi
else
    echo "  ⓘ  Skipped auto-start configuration"
    echo "    To start manually: bash start_dictation.sh"
fi

# Installation complete
echo ""
echo "========================================"
echo "  Installation Complete!"
echo "========================================"
echo ""
echo "To start the dictation service:"
echo "  bash start_dictation.sh"
echo ""
echo "Or restart Terminal if you configured auto-start."
echo ""
echo "Controls:"
echo "  • Press Control twice quickly → Start recording"
echo "  • Press Control once → Stop and transcribe"
echo ""
echo "For help, see README.md"
echo ""
