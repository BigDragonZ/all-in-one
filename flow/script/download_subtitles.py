#!/usr/bin/env python3
"""
Download YouTube video subtitles and convert to Markdown.

Usage:
    python flow/script/download_subtitles.py <URL> <COURSE_NAME> <INDEX>

Example:
    python flow/script/download_subtitles.py \
        "https://www.youtube.com/watch?v=LYGYvN5LUbA" \
        "Valuation_Undergrad_2022" 1
"""

import argparse
import sys
from pathlib import Path

from config.paths import course_dir, build_filename
from lib.youtube import fetch_title, download_subtitle, parse_srt, to_markdown


def main() -> int:
    parser = argparse.ArgumentParser(description="Download YouTube subtitles")
    parser.add_argument("url", help="YouTube video URL")
    parser.add_argument("course", help="Course name (directory under flow/)")
    parser.add_argument("index", type=int, help="Video sequence number")
    args = parser.parse_args()

    out_dir = course_dir(args.course)
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"[INFO] URL: {args.url}")
    print(f"[INFO] Course: {args.course}")
    print(f"[INFO] Index: {args.index}")
    print(f"[INFO] Output dir: {out_dir}")

    try:
        title = fetch_title(args.url)
        filename = build_filename(args.index, title, "md")
        output_path = out_dir / filename

        temp_base = str(out_dir / f"_tmp_{__import__('time').time()}")

        print(f"[INFO] Video title: {title}")
        print("[INFO] Downloading subtitle...")

        srt_file = download_subtitle(args.url, temp_base)

        print("[INFO] Converting SRT to Markdown...")
        srt_content = Path(srt_file).read_text(encoding="utf-8")
        entries = parse_srt(srt_content)
        markdown = to_markdown(
            entries,
            {"title": title, "url": args.url, "course": args.course, "index": args.index},
        )

        output_path.write_text(markdown, encoding="utf-8")

        # Cleanup
        Path(srt_file).unlink(missing_ok=True)
        Path(f"{temp_base}.en.srt").unlink(missing_ok=True)

        print(f"[SUCCESS] Markdown saved to: {output_path}")
        print(f"[INFO] Total entries: {len(entries)}")
        return 0

    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
