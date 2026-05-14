"""
Centralized path configuration for all scripts.
Modify here when project structure changes.
"""

import os
import shutil
from pathlib import Path

# Project root: two levels up from this file
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent

PATHS = {
    "project_root": PROJECT_ROOT,
    "script_dir": PROJECT_ROOT / "flow" / "script_py",
    "venv_bin": PROJECT_ROOT / ".venv" / "bin",
    "flow_dir": PROJECT_ROOT / "flow",
    "download_dir": Path("/tmp/video_audio_downloads"),
}

BINARIES = {
    "yt_dlp": str(PATHS["venv_bin"] / "yt-dlp"),
    "ffmpeg": shutil.which("ffmpeg") or "/opt/homebrew/bin/ffmpeg",
    "ffprobe": shutil.which("ffprobe") or "/opt/homebrew/bin/ffprobe",
    "python": str(PATHS["venv_bin"] / "python3"),
}


def course_dir(course_name: str) -> Path:
    """Resolve course output directory."""
    return PATHS["flow_dir"] / course_name


def build_filename(index: int, title: str, ext: str) -> str:
    """Build standardized filename: {index:02d}-{safe_title}.{ext}"""
    safe = "".join(c if c.isalnum() or c in " _-" else "_" for c in title).strip()
    return f"{index:02d}-{safe}.{ext}"
