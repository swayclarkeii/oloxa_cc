# Quick Start (After Pulling)

## 1. Set up your API key
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

## 2. Create venv & install deps (first time only)
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 3. Run
```bash
./start_dictation.sh
```

## Controls
- **Double-press Control** → Start recording
- **Single-press Control** → Stop & transcribe
