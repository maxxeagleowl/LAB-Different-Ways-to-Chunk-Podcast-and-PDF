from __future__ import annotations

import argparse
from pathlib import Path

from openai import OpenAI

from config import (
    DATA_INPUT_DIR,
    MAX_AUDIO_UPLOAD_BYTES,
    SUPPORTED_AUDIO_EXTENSIONS,
    TRANSCRIPTION_MODEL,
    TRANSCRIPT_FILE_EXTENSION,
    ensure_output_dir,
    require_env,
)


def find_audio_file() -> Path:
    audio_files = sorted(
        path
        for path in DATA_INPUT_DIR.iterdir()
        if path.is_file() and path.suffix.lower() in SUPPORTED_AUDIO_EXTENSIONS
    )

    if not audio_files:
        raise FileNotFoundError(f"No supported audio file found in {DATA_INPUT_DIR}")

    if len(audio_files) > 1:
        names = ", ".join(path.name for path in audio_files)
        raise RuntimeError(f"Multiple audio files found. Pass one with --audio. Found: {names}")

    return audio_files[0]


def _compress_audio(audio_path: Path, output_dir: Path, bitrate: str = "64k") -> Path:
    import shutil
    import subprocess

    compressed_path = output_dir / f"{audio_path.stem}_compressed.m4a"

    if compressed_path.exists():
        print(f"Compressed file already exists, reusing: {compressed_path.name}")
        return compressed_path

    ffmpeg_bin = shutil.which("ffmpeg")
    if not ffmpeg_bin:
        raise RuntimeError("ffmpeg not found on PATH. Install ffmpeg to compress large audio files.")

    size_mb = audio_path.stat().st_size / (1024 * 1024)
    print(f"{audio_path.name} is {size_mb:.1f} MB — compressing to {bitrate} …")
    result = subprocess.run(
        [ffmpeg_bin, "-i", str(audio_path), "-b:a", bitrate, "-y", str(compressed_path)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"ffmpeg compression failed (exit {result.returncode}):\n"
            + result.stderr.decode(errors="replace")
        )
    compressed_mb = compressed_path.stat().st_size / (1024 * 1024)
    print(f"Compressed to {compressed_mb:.1f} MB → {compressed_path.name}")
    return compressed_path


def transcribe_audio(audio_path: Path, model: str) -> Path:
    if not audio_path.exists():
        raise FileNotFoundError(f"Audio file does not exist: {audio_path}")

    output_dir = ensure_output_dir()

    size_bytes = audio_path.stat().st_size
    if size_bytes > MAX_AUDIO_UPLOAD_BYTES:
        audio_path = _compress_audio(audio_path, output_dir)

    require_env("OPENAI_API_KEY")
    client = OpenAI()
    output_path = output_dir / f"{audio_path.stem}{TRANSCRIPT_FILE_EXTENSION}"

    with audio_path.open("rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model=model,
            file=audio_file,
            response_format="text",
        )

    output_path.write_text(str(transcript).strip() + "\n", encoding="utf-8")
    return output_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Transcribe one podcast audio file into data_output/<filename>.txt")
    parser.add_argument(
        "--audio",
        type=Path,
        default=None,
        help="Audio file path. Defaults to the only supported audio file in data_input/.",
    )
    parser.add_argument(
        "--model",
        default=TRANSCRIPTION_MODEL,
        help=f"OpenAI transcription model to use. Default: {TRANSCRIPTION_MODEL}",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    audio_path = args.audio if args.audio else find_audio_file()
    if not audio_path.is_absolute():
        audio_path = audio_path if audio_path.exists() else DATA_INPUT_DIR / audio_path

    output_path = transcribe_audio(audio_path, args.model)
    print(f"Transcript saved to: {output_path}")


if __name__ == "__main__":
    main()
