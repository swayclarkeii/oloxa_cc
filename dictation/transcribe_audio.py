#!/usr/bin/env python3
"""
Audio transcription script using OpenAI's Whisper model or local Whisper.
Supports multiple audio formats: mp3, mp4, mpeg, mpga, m4a, wav, webm
Features:
- Batch processing of multiple files
- Local Whisper model support (free, no API needed)
- Language detection and translation
- Timestamp support for segments
"""

import argparse
import sys
import json
from pathlib import Path
from typing import List, Optional, Dict, Any
import glob

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    import whisper
    WHISPER_AVAILABLE = True
except ImportError:
    WHISPER_AVAILABLE = False


def transcribe_with_openai(
    audio_file_path: str,
    api_key: Optional[str] = None,
    model: str = "whisper-1",
    language: Optional[str] = None,
    timestamps: bool = False,
    translate: bool = False
) -> Dict[str, Any]:
    """Transcribe audio file using OpenAI's Whisper API."""
    if not OPENAI_AVAILABLE:
        raise ImportError("openai package not installed. Install with: pip install openai")

    if api_key:
        client = openai.OpenAI(api_key=api_key)
    else:
        client = openai.OpenAI()

    audio_path = Path(audio_file_path)
    if not audio_path.exists():
        raise FileNotFoundError(f"Audio file not found: {audio_file_path}")

    print(f"Transcribing: {audio_path.name}")

    with open(audio_file_path, "rb") as audio_file:
        if translate:
            response = client.audio.translations.create(
                model=model,
                file=audio_file,
                response_format="verbose_json" if timestamps else "text"
            )
        else:
            kwargs = {"model": model, "file": audio_file}
            if language:
                kwargs["language"] = language
            kwargs["response_format"] = "verbose_json" if timestamps else "text"

            response = client.audio.transcriptions.create(**kwargs)

    if timestamps and isinstance(response, dict):
        return {
            "text": response.get("text", ""),
            "segments": response.get("segments", []),
            "language": response.get("language", "")
        }
    else:
        return {"text": str(response), "segments": [], "language": language or "unknown"}


def transcribe_with_local_whisper(
    audio_file_path: str,
    model_size: str = "base",
    language: Optional[str] = None,
    timestamps: bool = False,
    translate: bool = False
) -> Dict[str, Any]:
    """Transcribe audio file using local Whisper model."""
    if not WHISPER_AVAILABLE:
        raise ImportError("whisper package not installed. Install with: pip install openai-whisper")

    audio_path = Path(audio_file_path)
    if not audio_path.exists():
        raise FileNotFoundError(f"Audio file not found: {audio_file_path}")

    print(f"Loading Whisper model '{model_size}'...")
    model = whisper.load_model(model_size)

    print(f"Transcribing: {audio_path.name}")

    kwargs = {"verbose": False}
    if language:
        kwargs["language"] = language
    if translate:
        kwargs["task"] = "translate"

    result = model.transcribe(str(audio_file_path), **kwargs)

    return {
        "text": result["text"],
        "segments": result.get("segments", []) if timestamps else [],
        "language": result.get("language", language or "unknown")
    }


def format_timestamp(seconds: float) -> str:
    """Format seconds into HH:MM:SS.mmm format."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{secs:06.3f}"


def format_output(result: Dict[str, Any], timestamps: bool = False) -> str:
    """Format transcription result as text."""
    output = []

    if result.get("language"):
        output.append(f"Detected language: {result['language']}\n")

    if timestamps and result.get("segments"):
        output.append("--- Transcription with Timestamps ---\n")
        for segment in result["segments"]:
            start = format_timestamp(segment.get("start", 0))
            end = format_timestamp(segment.get("end", 0))
            text = segment.get("text", "").strip()
            output.append(f"[{start} --> {end}] {text}")
    else:
        output.append("--- Transcription ---")
        output.append(result["text"].strip())

    return "\n".join(output)


def find_audio_files(pattern: str) -> List[Path]:
    """Find audio files matching the given pattern."""
    paths = []
    for match in glob.glob(pattern, recursive=True):
        path = Path(match)
        if path.is_file():
            paths.append(path)
    return sorted(paths)


def main():
    parser = argparse.ArgumentParser(
        description="Transcribe audio files using OpenAI Whisper API or local models",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Using OpenAI API (requires OPENAI_API_KEY)
  %(prog)s audio.mp3
  %(prog)s audio.mp3 -o transcript.txt --timestamps

  # Using local Whisper model (free, no API key needed)
  %(prog)s audio.mp3 --local --model-size medium

  # Batch processing
  %(prog)s "*.mp3" --batch --local
  %(prog)s "podcasts/**/*.wav" --batch -o transcripts/

  # Translation to English
  %(prog)s spanish_audio.mp3 --translate

  # Specify language for better accuracy
  %(prog)s audio.mp3 --language fr --local
        """
    )

    parser.add_argument(
        "audio_file",
        help="Path to audio file or glob pattern (e.g., '*.mp3', 'folder/**/*.wav')"
    )
    parser.add_argument(
        "-o", "--output",
        help="Output file/directory path (default: prints to stdout)"
    )
    parser.add_argument(
        "--batch",
        action="store_true",
        help="Process multiple files matching the glob pattern"
    )
    parser.add_argument(
        "--local",
        action="store_true",
        help="Use local Whisper model instead of OpenAI API (free, no API key needed)"
    )
    parser.add_argument(
        "--model-size",
        choices=["tiny", "base", "small", "medium", "large"],
        default="base",
        help="Local Whisper model size (default: base). Larger = more accurate but slower"
    )
    parser.add_argument(
        "-k", "--api-key",
        help="OpenAI API key (default: uses OPENAI_API_KEY env var)"
    )
    parser.add_argument(
        "-m", "--model",
        default="whisper-1",
        help="OpenAI model to use (default: whisper-1)"
    )
    parser.add_argument(
        "--language",
        help="Audio language code (e.g., en, es, fr, de, ja, zh). Improves accuracy"
    )
    parser.add_argument(
        "--translate",
        action="store_true",
        help="Translate audio to English"
    )
    parser.add_argument(
        "--timestamps",
        action="store_true",
        help="Include timestamps for each segment"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results in JSON format"
    )

    args = parser.parse_args()

    if args.local and not WHISPER_AVAILABLE:
        print("Error: openai-whisper package not installed.", file=sys.stderr)
        print("Install it with: pip install openai-whisper", file=sys.stderr)
        sys.exit(1)

    if not args.local and not OPENAI_AVAILABLE:
        print("Error: openai package not installed.", file=sys.stderr)
        print("Install it with: pip install openai", file=sys.stderr)
        print("Or use --local flag to use local Whisper models", file=sys.stderr)
        sys.exit(1)

    # Find audio files
    if args.batch:
        audio_files = find_audio_files(args.audio_file)
        if not audio_files:
            print(f"Error: No files found matching pattern: {args.audio_file}", file=sys.stderr)
            sys.exit(1)
        print(f"Found {len(audio_files)} file(s) to process\n")
    else:
        audio_path = Path(args.audio_file)
        if not audio_path.exists():
            print(f"Error: File not found: {args.audio_file}", file=sys.stderr)
            sys.exit(1)
        audio_files = [audio_path]

    # Process files
    results = []
    for audio_file in audio_files:
        try:
            if args.local:
                result = transcribe_with_local_whisper(
                    str(audio_file),
                    model_size=args.model_size,
                    language=args.language,
                    timestamps=args.timestamps,
                    translate=args.translate
                )
            else:
                result = transcribe_with_openai(
                    str(audio_file),
                    api_key=args.api_key,
                    model=args.model,
                    language=args.language,
                    timestamps=args.timestamps,
                    translate=args.translate
                )

            result["file"] = str(audio_file)
            results.append(result)

        except Exception as e:
            print(f"Error processing {audio_file}: {e}", file=sys.stderr)
            if not args.batch:
                sys.exit(1)
            continue

    # Output results
    if not results:
        print("Error: No files were successfully transcribed", file=sys.stderr)
        sys.exit(1)

    if args.output:
        output_path = Path(args.output)

        if args.batch and output_path.is_dir():
            for result in results:
                file_path = Path(result["file"])
                out_file = output_path / f"{file_path.stem}.txt"

                if args.json:
                    out_file = output_path / f"{file_path.stem}.json"
                    out_file.write_text(json.dumps(result, indent=2))
                else:
                    out_file.write_text(format_output(result, args.timestamps))

                print(f"Saved: {out_file}")
        else:
            if args.json:
                output_path.write_text(json.dumps(results if args.batch else results[0], indent=2))
            else:
                content = "\n\n".join([
                    f"=== {result['file']} ===\n{format_output(result, args.timestamps)}"
                    for result in results
                ])
                output_path.write_text(content)

            print(f"\nTranscription saved to: {output_path}")
    else:
        if args.json:
            print(json.dumps(results if args.batch else results[0], indent=2))
        else:
            for result in results:
                if args.batch:
                    print(f"\n{'='*60}")
                    print(f"File: {result['file']}")
                    print('='*60)
                print(format_output(result, args.timestamps))


if __name__ == "__main__":
    main()
