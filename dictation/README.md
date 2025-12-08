# Audio Transcription with Whisper

A powerful Python script for transcribing audio files using either OpenAI's Whisper API or local Whisper models.

## Features

- **Batch Processing**: Transcribe multiple files at once using glob patterns
- **Local Models**: Use free, local Whisper models (no API key needed)
- **Cloud API**: Use OpenAI's Whisper API for faster processing
- **Language Detection**: Automatic language detection
- **Translation**: Translate audio to English
- **Timestamps**: Get timestamped transcriptions with segment-level detail
- **Multiple Formats**: Support for mp3, mp4, mpeg, mpga, m4a, wav, webm
- **JSON Export**: Export results in JSON format for further processing

## Installation

### Option 1: OpenAI API (Cloud-based)

```bash
pip install openai
export OPENAI_API_KEY='your-api-key-here'
```

### Option 2: Local Whisper (Free, no API key)

```bash
pip install openai-whisper
# Also install ffmpeg (required for audio processing)
# macOS: brew install ffmpeg
# Ubuntu: sudo apt install ffmpeg
# Windows: Download from https://ffmpeg.org/download.html
```

### Install Both

```bash
pip install -r requirements.txt
```

## Usage

### Basic Examples

**Single file with OpenAI API:**
```bash
python transcribe_audio.py audio.mp3
```

**Single file with local model (free):**
```bash
python transcribe_audio.py audio.mp3 --local
```

**Save to file:**
```bash
python transcribe_audio.py audio.mp3 -o transcript.txt
```

### Batch Processing

**Process all MP3 files in current directory:**
```bash
python transcribe_audio.py "*.mp3" --batch --local
```

**Process all audio files in subdirectories:**
```bash
python transcribe_audio.py "podcasts/**/*.wav" --batch -o transcripts/
```

### Advanced Features

**With timestamps:**
```bash
python transcribe_audio.py audio.mp3 --timestamps --local
```

**Translate to English:**
```bash
python transcribe_audio.py spanish_audio.mp3 --translate
```

**Specify language for better accuracy:**
```bash
python transcribe_audio.py audio.mp3 --language fr --local
```

**Use larger model for better accuracy:**
```bash
python transcribe_audio.py audio.mp3 --local --model-size medium
```

**Export as JSON:**
```bash
python transcribe_audio.py audio.mp3 --json -o result.json --local
```

## Model Sizes (Local Whisper)

| Model  | Parameters | Relative Speed | Accuracy |
|--------|------------|----------------|----------|
| tiny   | 39 M       | ~32x           | Good     |
| base   | 74 M       | ~16x (default) | Better   |
| small  | 244 M      | ~6x            | Great    |
| medium | 769 M      | ~2x            | Excellent|
| large  | 1550 M     | 1x             | Best     |

## Command Line Options

```
positional arguments:
  audio_file            Path to audio file or glob pattern

options:
  -h, --help            Show help message
  -o, --output OUTPUT   Output file/directory path
  --batch               Process multiple files matching glob pattern
  --local               Use local Whisper model (free, no API key)
  --model-size SIZE     Local model size: tiny, base, small, medium, large
  -k, --api-key KEY     OpenAI API key
  -m, --model MODEL     OpenAI model (default: whisper-1)
  --language LANG       Language code (en, es, fr, de, ja, zh, etc.)
  --translate           Translate audio to English
  --timestamps          Include timestamps for segments
  --json                Output in JSON format
```

## Language Codes

Common language codes for the `--language` option:
- `en` - English
- `es` - Spanish
- `fr` - French
- `de` - German
- `it` - Italian
- `pt` - Portuguese
- `ja` - Japanese
- `zh` - Chinese
- `ru` - Russian
- `ar` - Arabic

## Output Formats

### Text Output (Default)
```
Detected language: en

--- Transcription ---
This is the transcribed text from the audio file.
```

### With Timestamps
```
Detected language: en

--- Transcription with Timestamps ---
[00:00:00.000 --> 00:00:03.240] This is the first segment.
[00:00:03.240 --> 00:00:07.680] This is the second segment.
```

### JSON Output
```json
{
  "text": "Full transcription text",
  "segments": [
    {
      "start": 0.0,
      "end": 3.24,
      "text": " This is the first segment."
    }
  ],
  "language": "en",
  "file": "audio.mp3"
}
```

## Tips

1. **For quick testing**: Use `--local --model-size tiny` for fastest results
2. **For best accuracy**: Use `--local --model-size large` or OpenAI API
3. **Specify language**: Adding `--language` improves accuracy significantly
4. **Batch processing**: Create output directory first for batch jobs
5. **Large files**: Local models process on your hardware; API has file size limits

## Troubleshooting

**"ffmpeg not found"**: Install ffmpeg for local Whisper
```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt install ffmpeg
```

**"Out of memory"**: Use a smaller model size or the OpenAI API

**Slow processing**: Local models run on your CPU/GPU. Use smaller models or the API for faster results.

## License

This script is provided as-is for personal and commercial use.
