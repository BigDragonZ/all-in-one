# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is a **knowledge-base automation pipeline** that transforms YouTube course playlists into structured, graduate-level academic notes. It consists of two independent pipelines:

1. **Transcription Pipeline** (`flow/script/run_pipeline.py`): YouTube playlist → subtitle extraction → audio transcription → Gemini refinement → raw markdown.
2. **Note Generation Pipeline** (`flow/script/note_pipeline.py`): Raw transcripts → NotebookLM → syllabus → chapter deep-dive notes → MOC / Anki cards.

## Development Environment

- **Python**: 3.12+, managed with `uv`.
- **Virtual env**: `.venv/` (created by `uv sync`). Do not commit it.
- **Dependencies**: listed in `pyproject.toml`.

### Common Commands

```bash
# Install dependencies
uv sync

# Run the transcription pipeline (subtitle-first, audio fallback)
uv run flow/script/run_pipeline.py "PLAYLIST_URL" "CourseName" [MAX_VIDEOS]

# Run the note generation pipeline
uv run flow/script/note_pipeline.py --course "CourseName"
uv run flow/script/note_pipeline.py --course "CourseName" --resume
uv run flow/script/note_pipeline.py --course "CourseName" --dry-run

# Run a single test file
python flow/script/tests/test_syllabus_parser.py
python flow/script/tests/test_note_paths.py
# (Tests are plain Python files with `if __name__ == "__main__"` blocks, not pytest.)
```

## Project Structure

```
flow/script/           # All Python code
  config/              # Path configs, credentials, prompts
  models/              # Domain dataclasses (VideoMeta, Chapter, CourseContext, etc.)
  lib/                 # Core logic modules
    adapters/          # NotebookLM adapter interface + implementations
  tests/               # Unit tests (plain Python, no pytest)
flow/<CourseName>/     # Raw refined transcripts (pipeline 1 output)
01_Permanent/<CourseName>/  # Generated notes: syllabus, chapters, MOC, Anki (pipeline 2 output)
```

## Key Architecture

### Two Pipeline Orchestrators

- **`lib/pipeline.py`** — Orchestrates the transcription pipeline. For each video: tries subtitles first (`lib/youtube.py`), falls back to audio download + transcription (`lib/transcribe.py`), then refines with Gemini (`lib/refine.py`). Raw files are deleted after refinement succeeds.
- **`note_pipeline.py`** — CLI orchestrator for the 3-phase note pipeline. Calls `lib/note_generator.py` for each phase.

### NotebookLM Adapter Pattern

All NotebookLM interactions go through `lib/adapters/base.py` (`NotebookLMAdapter` ABC). Implementations:

- **`CLIAdapter`** (`lib/adapters/cli.py`) — production, wraps the `notebooklm-py` CLI binary (from `.venv/bin/notebooklm`).
- **`MockAdapter`** (`lib/adapters/mock.py`) — dry-run / testing, records calls without external IO.

The adapter is injected into `note_generator.py` functions; never instantiate a concrete adapter inside library code.

### Checkpoint System

`lib/checkpoint.py` persists pipeline state as JSON (`01_Permanent/<course>/.checkpoint.json`). This allows resuming long-running jobs after interruption. Phase auto-detection works from checkpoint first, then falls back to filesystem scanning.

### Prompt Engine

`lib/prompt_engine.py` defines versioned `PromptTemplate` dataclasses with variable binding via `.render(**kwargs)`. Prompts are organized by phase (syllabus, chapter deep dive, 5 pressure-test rounds, MOC, next steps, Anki). The legacy `config/prompts.py` contains the same prompts as raw strings.

### Fault-Tolerant Transcription

`lib/gemini_client.py` provides a unified `generate_content()` that automatically fails over: GCP Vertex AI (`gemini-3.1-pro-preview`) → Gemini Standard API (`gemini-2.5-flash-lite`). Credentials come from environment variables (`gcp-vertex-key`, `GEMINI_API_KEY`).

### Path Conventions

- **Raw transcripts**: `flow/<course_name>/01-Title.md`
- **Chapter notes**: `01_Permanent/<course_name>/Ch_XX_Title.md`
- **Syllabus**: `01_Permanent/<course_name>/<course_name>_课程大纲.md`
- **MOC**: `01_Permanent/<course_name>/<course_name>_知识地图_MOC.md`
- **Anki**: `01_Permanent/<course_name>/Anki_<course_name>_<count>张真题卡.md`

Filenames are sanitized in `config/paths.py` (`build_filename`) and `config/note_paths.py`.

## Important Configuration

- **NotebookLM CLI path**: `config/notebooklm.py` resolves to `.venv/bin/notebooklm`.
- **yt-dlp**: requires Chrome cookies (`--cookies-from-browser chrome`) for subtitle fetch.
- **ffmpeg**: resolved via `shutil.which("ffmpeg")` or hardcoded `/opt/homebrew/bin/ffmpeg`.
- **Environment**: `gcp-vertex-key` and `GEMINI_API_KEY` are read from env vars by `config/transcribe.py`.

## Data Flow

1. `run_pipeline.py` writes refined markdown to `flow/<course>/`.
2. `note_pipeline.py` uploads those markdown files to NotebookLM as sources.
3. Phase 1 generates a syllabus; `lib/syllabus_parser.py` parses it into `Chapter` objects.
4. Phase 2 runs each chapter through multiple "pressure-test" rounds (definition, derivation, case, critique, cross-chapter) via `generate_chapter_note()`.
5. Phase 3 synthesizes MOC, next-steps, and Anki cards.

## Testing

Tests are self-executing Python files in `flow/script/tests/`. Each sets `sys.path` to include `flow/script/` and runs assertions in `if __name__ == "__main__"`. No pytest or test runner is configured. Run them individually with `python flow/script/tests/test_*.py`.
