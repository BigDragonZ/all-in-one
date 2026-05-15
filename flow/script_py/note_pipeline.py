#!/usr/bin/env python3
"""
Note generation pipeline CLI.

Orchestrates the full knowledge-base workflow:
  Phase 1: Upload transcripts → generate syllabus
  Phase 2: Chapter-by-chapter deep-dive with pressure tests
  Phase 3: MOC, next-steps, Anki synthesis

Usage:
    uv run flow/script_py/note_pipeline.py --course "CourseName" --raw-dir "path/to/transcripts"
    uv run flow/script_py/note_pipeline.py --course "CourseName" --phase 2 --notebook-id "xxx"
    uv run flow/script_py/note_pipeline.py --course "CourseName" --phase 3 --notebook-id "xxx"
"""

import argparse
import sys
from pathlib import Path

# Ensure project root is in path
SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from config.note_paths import raw_note_dir, permanent_note_dir
from config.notebooklm import load_config
from models.note import CourseContext
from lib import notebooklm_client
from lib.course_loader import load_videos, count_raw_files
from lib.syllabus_parser import parse_syllabus, save_syllabus, load_syllabus
from lib.note_generator import (
    generate_syllabus,
    generate_chapter_note,
    generate_moc,
    generate_next_steps,
    generate_anki,
    PRESSURE_ROUNDS,
)


def _build_argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Course knowledge base note generation pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Full pipeline (create notebook, upload, syllabus, chapters, synthesis)
  %(prog)s --course "Valuation" --raw-dir "flow/Valuation"

  # Resume from Phase 2 (syllabus already generated)
  %(prog)s --course "Valuation" --phase 2 --notebook-id "abc123..."

  # Only Phase 3 synthesis
  %(prog)s --course "Valuation" --phase 3 --notebook-id "abc123..."

  # Custom pressure-test rounds
  %(prog)s --course "Valuation" --rounds 7 --notebook-id "abc123..."
        """,
    )

    parser.add_argument(
        "--course",
        required=True,
        help="Course name (used for directory and notebook naming)",
    )
    parser.add_argument(
        "--raw-dir",
        default=None,
        help="Override raw transcription directory (default: flow/<course_name>)",
    )
    parser.add_argument(
        "--phase",
        type=int,
        choices=[1, 2, 3],
        default=None,
        help="Start from specific phase (default: auto-detect from state)",
    )
    parser.add_argument(
        "--notebook-id",
        default=None,
        help="Existing NotebookLM notebook ID (skip creation)",
    )
    parser.add_argument(
        "--rounds",
        type=int,
        default=5,
        help="Number of pressure-test rounds per chapter (default: 5)",
    )
    parser.add_argument(
        "--anki-count",
        type=int,
        default=20,
        help="Number of Anki cards to generate (default: 20)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would be done without executing",
    )
    parser.add_argument(
        "--skip-upload",
        action="store_true",
        help="Skip source upload (assume already uploaded)",
    )

    return parser


def _detect_phase(ctx: CourseContext) -> int:
    """Auto-detect which phase to start from based on existing files."""
    pdir = permanent_note_dir(ctx.course_name)

    # Check for syllabus
    syllabus_path = pdir / f"{ctx.course_name}_课程大纲.md"
    if not syllabus_path.exists():
        return 1

    # Check for chapter notes
    chapter_files = list(pdir.glob("Ch_*.md"))
    if not chapter_files:
        return 2

    # Check for MOC
    moc_file = pdir / f"{ctx.course_name}_知识地图_MOC.md"
    if not moc_file.exists():
        return 3

    # Everything exists
    print("[INFO] All artifacts already exist. Use --phase to force re-run.")
    return 3


def phase1_upload_and_syllabus(ctx: CourseContext, skip_upload: bool = False) -> CourseContext:
    """
    Phase 1: Upload sources and generate syllabus.

    Returns updated context with notebook_id and chapters.
    """
    print("\n" + "=" * 60)
    print("PHASE 1: Upload & Syllabus Generation")
    print("=" * 60)

    # Create or use notebook
    if not ctx.notebook_id:
        print(f"[INFO] Creating notebook: {ctx.course_name}")
        ctx.notebook_id = notebooklm_client.create_notebook(ctx.course_name)
        print(f"[OK] Notebook ID: {ctx.notebook_id}")
    else:
        print(f"[INFO] Using existing notebook: {ctx.notebook_id}")
        notebooklm_client.use_notebook(ctx.notebook_id)

    # Upload sources
    if not skip_upload:
        raw_dir = raw_note_dir(ctx.course_name)
        if not raw_dir.exists():
            raise FileNotFoundError(f"Raw directory not found: {raw_dir}")

        file_count = count_raw_files(ctx.course_name)
        print(f"[INFO] Uploading {file_count} files from {raw_dir}")

        uploaded, skipped = notebooklm_client.upload_sources_dir(raw_dir, "*.md")
        print(f"[OK] Uploaded: {uploaded}, Skipped: {skipped}")

        # Verify
        if not notebooklm_client.verify_upload(file_count):
            print("[WARN] Upload verification failed, continuing anyway...")
    else:
        print("[INFO] Skipping upload (--skip-upload)")

    # Generate syllabus
    syllabus_text = generate_syllabus(ctx)

    # Save syllabus
    pdir = permanent_note_dir(ctx.course_name)
    pdir.mkdir(parents=True, exist_ok=True)
    syllabus_path = save_syllabus(syllabus_text, ctx.course_name, pdir)
    print(f"[OK] Syllabus saved: {syllabus_path}")

    # Parse chapters
    ctx.chapters = parse_syllabus(syllabus_text)
    print(f"[OK] Parsed {len(ctx.chapters)} chapters")
    for ch in ctx.chapters:
        print(f"  Ch.{ch.index:02d}: {ch.title} ({ch.video_range})")

    return ctx


def phase2_chapter_deep_dive(ctx: CourseContext, max_rounds: int = 5) -> None:
    """Phase 2: Chapter-by-chapter deep-dive with pressure tests."""
    print("\n" + "=" * 60)
    print("PHASE 2: Chapter Deep Dive")
    print("=" * 60)

    if not ctx.chapters:
        # Try loading from saved syllabus
        pdir = permanent_note_dir(ctx.course_name)
        syllabus_path = pdir / f"{ctx.course_name}_课程大纲.md"
        if syllabus_path.exists():
            ctx.chapters = load_syllabus(syllabus_path)
            print(f"[OK] Loaded {len(ctx.chapters)} chapters from saved syllabus")
        else:
            raise RuntimeError("No chapters found. Run Phase 1 first.")

    total = len(ctx.chapters)
    for i, chapter in enumerate(ctx.chapters, 1):
        print(f"\n[{i}/{total}] Processing chapter {chapter.index}: {chapter.title}")
        generate_chapter_note(ctx, chapter, max_rounds=max_rounds)

    print(f"\n[OK] All {total} chapters processed")


def phase3_synthesis(ctx: CourseContext, anki_count: int = 20) -> None:
    """Phase 3: Generate MOC, next steps, and Anki cards."""
    print("\n" + "=" * 60)
    print("PHASE 3: Capstone Synthesis")
    print("=" * 60)

    # MOC
    generate_moc(ctx)

    # Next steps
    generate_next_steps(ctx)

    # Anki
    generate_anki(ctx, card_count=anki_count)

    print("\n[OK] Phase 3 complete")


def main() -> int:
    parser = _build_argparser()
    args = parser.parse_args()

    # Validate config
    cfg = load_config()
    cfg.validate()

    # Resolve paths
    raw_dir = Path(args.raw_dir) if args.raw_dir else raw_note_dir(args.course)
    perm_dir = permanent_note_dir(args.course)

    print(f"Course: {args.course}")
    print(f"Raw dir: {raw_dir}")
    print(f"Permanent dir: {perm_dir}")

    # Load videos
    try:
        videos = load_videos(args.course)
        print(f"Videos: {len(videos)}")
    except FileNotFoundError:
        videos = []
        print(f"[WARN] No raw videos found in {raw_dir}")

    # Build context
    ctx = CourseContext(
        course_name=args.course,
        notebook_id=args.notebook_id or "",
        raw_dir=raw_dir,
        permanent_dir=perm_dir,
        videos=videos,
        chapters=[],
    )

    # Determine phase
    phase = args.phase or _detect_phase(ctx)
    print(f"\nStarting from Phase {phase}")

    if args.dry_run:
        print("\n[DRY RUN] Would execute:")
        if phase <= 1:
            print(f"  - Phase 1: Create notebook, upload {len(videos)} files, generate syllabus")
        if phase <= 2:
            print(f"  - Phase 2: Deep-dive {len(ctx.chapters)} chapters with {args.rounds} rounds each")
        if phase <= 3:
            print(f"  - Phase 3: MOC, next-steps, {args.anki_count} Anki cards")
        return 0

    # Execute phases
    try:
        if phase <= 1:
            ctx = phase1_upload_and_syllabus(ctx, skip_upload=args.skip_upload)
            # Save notebook ID for resumption
            print(f"\n[IMPORTANT] Notebook ID for resumption: {ctx.notebook_id}")

        if phase <= 2:
            phase2_chapter_deep_dive(ctx, max_rounds=args.rounds)

        if phase <= 3:
            phase3_synthesis(ctx, anki_count=args.anki_count)

        print("\n" + "=" * 60)
        print("PIPELINE COMPLETE")
        print("=" * 60)
        print(f"Output: {perm_dir}")
        print(f"Notebook ID: {ctx.notebook_id}")
        return 0

    except Exception as e:
        print(f"\n[ERROR] Pipeline failed: {e}")
        print(f"[INFO] To resume, use: --notebook-id {ctx.notebook_id} --phase {phase}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
