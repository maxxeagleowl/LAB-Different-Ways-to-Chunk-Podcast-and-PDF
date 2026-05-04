# LAB: Different Ways to Chunk Podcast and PDF

### --Disclaimer-- Podcast ist due API Limit outcommented

This repository explores multiple chunking strategies for a podcast transcript and a PDF document. It includes an analysis notebook, audio transcription helper, and the necessary project structure to run the lab.

## What is included

- `chunking_strategies.ipynb`
  - The main notebook. It loads podcast and PDF content, applies several chunking methods, compares the results, and creates output plots.
- `transcribe_audio.py`
  - A helper script to transcribe an audio file using OpenAI.
- `config.py`
  - Project configuration, path definitions, and environment variable loading.
- `data_input/`
  - Place your audio and PDF files here.
- `data_output/`
  - Output folder for transcripts, graphs, and recommendation files.
- `lab.md` / `lab_summary.md`
  - Additional documentation and lab summary.

## Requirements

- Python 3.10 or newer
- Global `ffmpeg` installed and available on `PATH`
- OpenAI API key set in a `.env` file

### Install FFmpeg globally

It is recommended to install FFmpeg via `winget` or manually so the notebook and script can use the correct global binary.

Example with Winget:

```powershell
winget install --id Gyan.FFmpeg --exact --silent --scope user
```

Then verify the installation:

```powershell
where.exe ffmpeg
ffmpeg -version
```

If `ffmpeg` is installed at `C:\ffmpeg\bin\ffmpeg.exe`, that will work well.

## Setup

1. Create a virtual environment (optional, but recommended):

```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

2. Install the required Python packages:

```powershell
python -m pip install langchain langchain-community pypdf2 python-dotenv openai tiktoken sentence-transformers matplotlib numpy
```

3. Create a `.env` file in the project root with at least your OpenAI key:

```text
OPENAI_API_KEY=your_api_key
TRANSCRIPTION_MODEL=gpt-4o-mini-transcribe
```

## Prepare your data

- Put your audio file (`.mp3`, `.m4a`, `.wav`, `.flac`, etc.) into `data_input/`
- Put your PDF into `data_input/`

Note: `transcribe_audio.py` will automatically use the only supported audio file in `data_input/`. If more than one supported audio file exists there, the script will raise an error.

## How to run

### 1) Run the notebook

Open `chunking_strategies.ipynb` in Jupyter or VS Code and run the cells in order. The notebook will:

- load the podcast audio file
- transcribe it if needed
- load the PDF document
- compute different chunking outputs
- save charts and recommendations to `data_output/`

### 2) Run transcription directly

If you only need transcription, use the script:

```powershell
python transcribe_audio.py
```

Optionally specify a specific audio file:

```powershell
python transcribe_audio.py --audio data_input/YourPodcast.m4a
```

### 3) Large audio files

The script automatically compresses audio files larger than 25 MB using `ffmpeg` before sending them to OpenAI.

## Important notes

- `data_output/` is created automatically when output is written.
- If transcription fails, check the following first:
  - `OPENAI_API_KEY` is set correctly
  - `ffmpeg` is installed globally and available on `PATH`
  - `data_input/` contains only one supported audio file for automatic mode

## File and folder map

- `chunking_strategies.ipynb` — Notebook for chunking analysis and visualization
- `transcribe_audio.py` — Standalone audio transcription script using OpenAI
- `config.py` — Project settings, paths, and environment variable handling
- `data_input/` — Input files: audio and PDF
- `data_output/` — Output files: transcripts, charts, recommendations
- `lab.md` — Lab documentation
- `lab_summary.md` — Lab summary

## Need help?

If you need assistance, mention the file or step that is causing trouble, and I will help you resolve it.