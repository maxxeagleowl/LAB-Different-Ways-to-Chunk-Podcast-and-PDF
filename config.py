from pathlib import Path
import os

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent
DATA_INPUT_DIR = BASE_DIR / "data_input"
DATA_OUTPUT_DIR = BASE_DIR / "data_output"

load_dotenv(BASE_DIR / ".env")


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

SUPPORTED_AUDIO_EXTENSIONS = {
    ".flac",
    ".mp3",
    ".mp4",
    ".mpeg",
    ".mpga",
    ".m4a",
    ".ogg",
    ".wav",
    ".webm",
}
MAX_AUDIO_UPLOAD_BYTES = 25 * 1024 * 1024
TRANSCRIPTION_MODEL = os.getenv("TRANSCRIPTION_MODEL", "gpt-4o-mini-transcribe")
TRANSCRIPT_FILE_EXTENSION = ".txt"


def require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def ensure_output_dir() -> Path:
    DATA_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    return DATA_OUTPUT_DIR
