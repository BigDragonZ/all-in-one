#!/usr/bin/env python3
"""
Production-grade Audio/Video Transcription Pipeline
====================================================
Uses google-genai (2026 SDK) via Vertex AI channel with API Key auth.
Targets: gemini-2.5-flash-lite on us-central1.

Flow:
  1. yt-dlp  -> fetch audio stream
  2. ffmpeg  -> re-encode to 64kbps mono MP3
  3. GCS     -> upload to gs://hermes_brain/
  4. Gemini  -> async transcription via Part.from_uri
  5. Cleanup -> delete GCS temp object immediately after success
  6. Archive -> write transcript to Obsidian vault

Concurrency: bounded async semaphore tuned to 300 RPM (Tier 1).
Auth: reads GEMINI_API_KEY from env.
"""

from __future__ import annotations

import asyncio
import hashlib
import json
import logging
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional
from urllib.parse import urlparse

from google.cloud import storage
from google.genai import Client
from google.genai.types import GenerateContentConfig, HttpOptions, Part, Content

# ═══════════════════════════════════════════════════════════════════════════════
# Configuration
# ═══════════════════════════════════════════════════════════════════════════════

PROJECT_ID: str = "gen-lang-client-0385617544"
LOCATION: str = "us-central1"
MODEL_ID: str = "gemini-2.5-flash-lite"
GCS_BUCKET: str = "hermes_brain"
API_VERSION: str = "v1"  # Required for Enterprise Agent Platform API Key auth

# Tier 1 limit = 300 RPM. Leave headroom for safety.
MAX_RPM: int = 280
SEMAPHORE_VALUE: int = 10  # concurrent in-flight requests

# Local paths
OBSIDIAN_VAULT: Path = Path.home() / "Documents" / "all-in-one"
FAILED_LOG: Path = OBSIDIAN_VAULT / "_failed_videos.json"

# Prompt sent to Gemini for transcription + light structuring
TRANSCRIPTION_PROMPT: str = (
    "Please transcribe the following audio into clean, structured Markdown. "
    "Use headers (##) for topic shifts, bullet points for lists, and preserve "
    "any key terminology. Output only the transcript content."
)

# ═══════════════════════════════════════════════════════════════════════════════
# Logging
# ═══════════════════════════════════════════════════════════════════════════════

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("gcp_transcriber")


# ═══════════════════════════════════════════════════════════════════════════════
# Data classes
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class VideoTask:
    url: str
    title: Optional[str] = None
    chapter: Optional[str] = None
    output_path: Optional[Path] = None
    status: str = "pending"  # pending | downloading | uploading | transcribing | done | failed
    error: Optional[str] = None
    attempts: int = 0
    gcs_uri: Optional[str] = None
    local_mp3: Optional[Path] = None
    transcript: Optional[str] = None
    metadata: dict[str, Any] = field(default_factory=dict)


# ═══════════════════════════════════════════════════════════════════════════════
# Helpers: yt-dlp & ffmpeg
# ═══════════════════════════════════════════════════════════════════════════════


def _run_cmd(cmd: list[str], timeout: int = 300) -> subprocess.CompletedProcess:
    """Run a shell command, raise on non-zero exit."""
    logger.debug("Running: %s", " ".join(cmd))
    return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, check=True)


def _slugify(text: str, max_len: int = 80) -> str:
    """Create a filesystem-safe slug."""
    text = re.sub(r"[^\w\s-]", "", text.lower())
    text = re.sub(r"[-\s]+", "-", text).strip("-")
    return text[:max_len]


def _video_id_from_url(url: str) -> str:
    """Extract a stable video identifier from common platforms."""
    parsed = urlparse(url)
    if "youtube" in parsed.netloc or "youtu.be" in parsed.netloc:
        # Try query param v= or path segment
        if "v=" in parsed.query:
            return re.search(r"[?&]v=([^&]+)", parsed.query).group(1)  # type: ignore[union-attr]
        return parsed.path.strip("/").split("/")[-1]
    # Fallback: hash the URL
    return hashlib.sha256(url.encode()).hexdigest()[:12]


def fetch_audio_metadata(url: str) -> dict[str, Any]:
    """Use yt-dlp JSON output to grab title, duration, etc."""
    cmd = [
        "yt-dlp",
        "--no-warnings",
        "--dump-single-json",
        "--skip-download",
        url,
    ]
    result = _run_cmd(cmd, timeout=60)
    return json.loads(result.stdout)


def download_and_compress_audio(
    url: str,
    out_dir: Path,
    video_id: str,
) -> Path:
    """
    Download best audio via yt-dlp, then ffmpeg -> 64kbps mono MP3.
    Returns path to the compressed MP3.
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    temp_base = out_dir / f"{video_id}_raw"
    final_mp3 = out_dir / f"{video_id}.mp3"

    # 1) yt-dlp: best audio only
    ytdlp_cmd = [
        "yt-dlp",
        "--no-warnings",
        "-f", "bestaudio/best",
        "-o", str(temp_base) + ".%(ext)s",
        "--ffmpeg-location", shutil.which("ffmpeg") or "ffmpeg",
        url,
    ]
    _run_cmd(ytdlp_cmd, timeout=600)

    # Find downloaded file (yt-dlp may pick m4a, webm, etc.)
    downloaded = None
    for ext in ("m4a", "webm", "opus", "ogg", "mp3", "mp4"):
        candidate = Path(f"{temp_base}.{ext}")
        if candidate.exists():
            downloaded = candidate
            break

    if not downloaded:
        raise FileNotFoundError(f"yt-dlp did not produce expected audio file for {url}")

    # 2) ffmpeg: 64kbps mono mp3
    ffmpeg_cmd = [
        "ffmpeg",
        "-y",
        "-i", str(downloaded),
        "-vn",                 # no video
        "-ar", "22050",        # sample rate
        "-ac", "1",            # mono
        "-b:a", "64k",         # 64 kbps
        "-f", "mp3",
        str(final_mp3),
    ]
    _run_cmd(ffmpeg_cmd, timeout=300)

    # Clean raw download
    downloaded.unlink(missing_ok=True)

    if not final_mp3.exists():
        raise RuntimeError("ffmpeg failed to produce MP3 output")

    size_mb = final_mp3.stat().st_size / (1024 * 1024)
    logger.info("Compressed audio ready: %s (%.2f MB)", final_mp3.name, size_mb)
    return final_mp3


# ═══════════════════════════════════════════════════════════════════════════════
# GCS helpers
# ═══════════════════════════════════════════════════════════════════════════════


def get_gcs_client() -> storage.Client:
    """Return a GCS client (uses default credentials or ADC)."""
    # For GCS upload we rely on Application Default Credentials (ADC).
    # On local workstations: gcloud auth application-default login
    return storage.Client(project=PROJECT_ID)


def upload_to_gcs(local_path: Path, destination_blob_name: str) -> str:
    """Upload a local file to GCS bucket. Returns gs:// URI."""
    client = get_gcs_client()
    bucket = client.bucket(GCS_BUCKET)
    blob = bucket.blob(destination_blob_name)

    logger.info("Uploading %s -> gs://%s/%s", local_path.name, GCS_BUCKET, destination_blob_name)
    blob.upload_from_filename(str(local_path))

    gs_uri = f"gs://{GCS_BUCKET}/{destination_blob_name}"
    logger.info("Upload complete: %s", gs_uri)
    return gs_uri


def delete_gcs_blob(blob_name: str) -> None:
    """Delete a blob from the GCS bucket."""
    client = get_gcs_client()
    bucket = client.bucket(GCS_BUCKET)
    blob = bucket.blob(blob_name)
    blob.delete()
    logger.info("Deleted GCS blob: gs://%s/%s", GCS_BUCKET, blob_name)


# ═══════════════════════════════════════════════════════════════════════════════
# Gemini / Vertex AI client
# ═══════════════════════════════════════════════════════════════════════════════


def get_genai_client() -> Client:
    """
    Initialize google-genai Client for Vertex AI with API Key auth.
    vertexai=True ensures requests route through Vertex AI and consume
    the project's promotional credits.

    For Gemini Enterprise Agent Platform API Key auth, project/location
    must NOT be passed to the constructor (mutually exclusive with api_key).
    Instead, we set api_version="v1" via http_options.
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "Environment variable GEMINI_API_KEY is not set. "
            "Export it before running this script."
        )

    return Client(
        vertexai=True,
        api_key=api_key,
        http_options=HttpOptions(api_version=API_VERSION),
    )


async def transcribe_audio(gcs_uri: str, client: Client) -> str:
    """
    Send audio (via GCS URI) to Gemini for transcription.
    Returns the generated transcript text.
    """
    part = Part.from_uri(file_uri=gcs_uri, mime_type="audio/mpeg")
    contents = [
        Content(role="user", parts=[Part.from_text(text=TRANSCRIPTION_PROMPT), part])
    ]

    config = GenerateContentConfig(
        temperature=0.0,
        max_output_tokens=8192,
    )

    # Use the async generate_content if available; otherwise run sync in executor
    response = await asyncio.to_thread(
        client.models.generate_content,
        model=MODEL_ID,
        contents=contents,
        config=config,
    )

    if not response.candidates:
        raise RuntimeError("Empty response from Gemini (no candidates)")

    candidate = response.candidates[0]
    if not candidate.content or not candidate.content.parts:
        raise RuntimeError("Empty candidate content from Gemini")

    # Concatenate all text parts
    transcript_parts = [p.text for p in candidate.content.parts if p.text]
    return "\n".join(transcript_parts)


# ═══════════════════════════════════════════════════════════════════════════════
# Persistence
# ═══════════════════════════════════════════════════════════════════════════════


def write_transcript_to_obsidian(task: VideoTask) -> Path:
    """Save transcript as a Markdown note inside the Obsidian vault."""
    vault = OBSIDIAN_VAULT
    vault.mkdir(parents=True, exist_ok=True)

    # Organize by chapter if provided, else fall back to 'Transcripts'
    subdir = task.chapter or "Transcripts"
    target_dir = vault / _slugify(subdir)
    target_dir.mkdir(parents=True, exist_ok=True)

    safe_title = _slugify(task.title or f"video_{_video_id_from_url(task.url)}")
    filename = target_dir / f"{safe_title}.md"

    # Frontmatter
    frontmatter = {
        "title": task.title or "Untitled",
        "source_url": task.url,
        "transcribed_at": datetime.now(timezone.utc).isoformat(),
        "model": MODEL_ID,
        "chapter": task.chapter,
    }
    frontmatter_yaml = "\n".join(f"{k}: {v}" for k, v in frontmatter.items() if v is not None)

    body = f"""---
{frontmatter_yaml}
---

# {task.title or "Transcript"}

**Source:** {task.url}

---

{task.transcript or "(No transcript generated)"}
"""

    filename.write_text(body, encoding="utf-8")
    logger.info("Transcript saved: %s", filename)
    return filename


def log_failed_task(task: VideoTask) -> None:
    """Append failed task info to a JSON log for later retry."""
    entry = {
        "url": task.url,
        "title": task.title,
        "chapter": task.chapter,
        "error": task.error,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    existing: list[dict] = []
    if FAILED_LOG.exists():
        try:
            existing = json.loads(FAILED_LOG.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            existing = []

    existing.append(entry)
    FAILED_LOG.write_text(json.dumps(existing, indent=2, ensure_ascii=False), encoding="utf-8")
    logger.warning("Logged failed task to %s", FAILED_LOG)


# ═══════════════════════════════════════════════════════════════════════════════
# Core pipeline (single task)
# ═══════════════════════════════════════════════════════════════════════════════


async def process_single_task(
    task: VideoTask,
    semaphore: asyncio.Semaphore,
    genai_client: Client,
    temp_dir: Path,
) -> VideoTask:
    """
    End-to-end pipeline for one video:
      download -> compress -> upload -> transcribe -> save -> cleanup
    """
    async with semaphore:
        task.attempts += 1
        video_id = _video_id_from_url(task.url)

        try:
            # ── 1. Metadata ──────────────────────────────────────────────────
            if not task.title:
                logger.info("[%s] Fetching metadata...", video_id)
                meta = await asyncio.to_thread(fetch_audio_metadata, task.url)
                task.title = meta.get("title", "Untitled")
                task.metadata = {
                    "duration": meta.get("duration"),
                    "uploader": meta.get("uploader"),
                    "upload_date": meta.get("upload_date"),
                }

            # ── 2. Download & compress ───────────────────────────────────────
            task.status = "downloading"
            logger.info("[%s] Downloading & compressing audio...", video_id)
            task.local_mp3 = await asyncio.to_thread(
                download_and_compress_audio,
                task.url,
                temp_dir,
                video_id,
            )

            # ── 3. Upload to GCS ─────────────────────────────────────────────
            task.status = "uploading"
            blob_name = f"audio_jobs/{video_id}.mp3"
            task.gcs_uri = await asyncio.to_thread(
                upload_to_gcs,
                task.local_mp3,
                blob_name,
            )

            # ── 4. Transcribe ────────────────────────────────────────────────
            task.status = "transcribing"
            logger.info("[%s] Sending to Gemini for transcription...", video_id)
            task.transcript = await transcribe_audio(task.gcs_uri, genai_client)

            # ── 5. Save locally ──────────────────────────────────────────────
            task.status = "done"
            task.output_path = await asyncio.to_thread(write_transcript_to_obsidian, task)

            # ── 6. Cleanup GCS + local MP3 ───────────────────────────────────
            await asyncio.to_thread(delete_gcs_blob, blob_name)
            if task.local_mp3 and task.local_mp3.exists():
                task.local_mp3.unlink(missing_ok=True)
                logger.info("[%s] Cleaned up local MP3", video_id)

            logger.info("[%s] Pipeline complete.", video_id)

        except Exception as exc:
            task.status = "failed"
            task.error = f"{type(exc).__name__}: {exc}"
            logger.error("[%s] Pipeline failed: %s", video_id, task.error)

            # Attempt GCS cleanup even on failure
            if task.gcs_uri:
                try:
                    blob_name = task.gcs_uri.replace(f"gs://{GCS_BUCKET}/", "")
                    await asyncio.to_thread(delete_gcs_blob, blob_name)
                except Exception as cleanup_exc:
                    logger.warning("[%s] GCS cleanup failed: %s", video_id, cleanup_exc)

            # Log for retry
            await asyncio.to_thread(log_failed_task, task)

        return task


# ═══════════════════════════════════════════════════════════════════════════════
# Batch orchestration
# ═══════════════════════════════════════════════════════════════════════════════


def build_tasks_from_urls(urls: list[str], chapter: Optional[str] = None) -> list[VideoTask]:
    """Create VideoTask objects from raw URLs."""
    return [VideoTask(url=u.strip(), chapter=chapter) for u in urls if u.strip()]


async def run_batch(
    tasks: list[VideoTask],
    max_concurrency: int = SEMAPHORE_VALUE,
) -> list[VideoTask]:
    """Run all tasks with bounded concurrency."""
    genai_client = get_genai_client()
    semaphore = asyncio.Semaphore(max_concurrency)

    with tempfile.TemporaryDirectory(prefix="gcp_transcribe_") as tmp:
        temp_path = Path(tmp)
        coros = [
            process_single_task(task, semaphore, genai_client, temp_path)
            for task in tasks
        ]
        results = await asyncio.gather(*coros, return_exceptions=True)

    # Unwrap any exceptions that leaked through
    final: list[VideoTask] = []
    for task, result in zip(tasks, results):
        if isinstance(result, Exception):
            task.status = "failed"
            task.error = f"UNHANDLED: {type(result).__name__}: {result}"
            final.append(task)
        else:
            final.append(result)
    return final


# ═══════════════════════════════════════════════════════════════════════════════
# CLI / Entrypoint
# ═══════════════════════════════════════════════════════════════════════════════


def print_summary(results: list[VideoTask]) -> None:
    """Pretty-print batch summary."""
    total = len(results)
    ok = sum(1 for r in results if r.status == "done")
    failed = total - ok

    print("\n" + "=" * 60)
    print(" BATCH SUMMARY")
    print("=" * 60)
    print(f"  Total tasks : {total}")
    print(f"  Successful  : {ok}")
    print(f"  Failed      : {failed}")
    print("-" * 60)

    if failed:
        print("\nFailed items:")
        for r in results:
            if r.status == "failed":
                print(f"  - {r.url}")
                print(f"    Error: {r.error}")
        print(f"\nSee {FAILED_LOG} for structured retry data.")

    print("=" * 60)


def main() -> int:
    """
    CLI entrypoint.

    Usage examples:
      # Single URL
      export GEMINI_API_KEY="your-key"
      python gcp_audio_transcriber.py "https://www.youtube.com/watch?v=..."

      # Multiple URLs + chapter tag
      python gcp_audio_transcriber.py \
        --chapter "金融学" \
        url1 url2 url3 ...

      # From file (one URL per line)
      python gcp_audio_transcriber.py --file urls.txt --chapter "投资学"
    """
    import argparse

    parser = argparse.ArgumentParser(
        description="GCP Vertex AI Audio Transcription Pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Environment variables:
  GEMINI_API_KEY   Required. Vertex AI API Key for Gemini.
  GOOGLE_APPLICATION_CREDENTIALS  Optional. ADC for GCS uploads.
        """,
    )
    parser.add_argument("urls", nargs="*", help="Video URLs to transcribe")
    parser.add_argument("--chapter", default=None, help="Obsidian subfolder / chapter tag")
    parser.add_argument("--file", default=None, help="Text file containing one URL per line")
    parser.add_argument("--concurrency", type=int, default=SEMAPHORE_VALUE, help="Max concurrent requests")
    parser.add_argument("--verbose", action="store_true", help="Enable DEBUG logging")

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Collect URLs
    raw_urls: list[str] = list(args.urls)
    if args.file:
        path = Path(args.file)
        if not path.exists():
            logger.error("URL file not found: %s", path)
            return 1
        raw_urls.extend(path.read_text(encoding="utf-8").splitlines())

    raw_urls = [u.strip() for u in raw_urls if u.strip() and not u.strip().startswith("#")]
    if not raw_urls:
        logger.error("No URLs provided. Use positional args or --file.")
        return 1

    # Preflight checks
    for binary in ("yt-dlp", "ffmpeg"):
        if not shutil.which(binary):
            logger.error("Required binary not found in PATH: %s", binary)
            return 1

    if "GEMINI_API_KEY" not in os.environ:
        logger.error("GEMINI_API_KEY environment variable is required.")
        return 1

    tasks = build_tasks_from_urls(raw_urls, chapter=args.chapter)
    logger.info("Starting batch of %d tasks (concurrency=%d)", len(tasks), args.concurrency)

    start = time.monotonic()
    results = asyncio.run(run_batch(tasks, max_concurrency=args.concurrency))
    elapsed = time.monotonic() - start

    print_summary(results)
    logger.info("Batch finished in %.1f seconds", elapsed)
    return 0 if all(r.status == "done" for r in results) else 1


if __name__ == "__main__":
    sys.exit(main())
