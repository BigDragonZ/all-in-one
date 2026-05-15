"""
Parse NotebookLM syllabus output into structured Chapter objects.
"""

import re
from pathlib import Path
from typing import Optional

from models.note import Chapter


def parse_syllabus(text: str) -> list[Chapter]:
    """
    Parse NotebookLM syllabus markdown into Chapter objects.

    Expected format:
      ## 第N章：章节标题
      - **核心命题**：...
      - **视频范围**：XX-XX
      - **前置知识**：[[Ch_XX_...]] | ...
      - **本章概要**：...
    """
    chapters: list[Chapter] = []

    # Split by chapter headers
    chapter_blocks = re.split(r"\n##\s*第\s*(\d+)\s*章\s*[：:]\s*", text)

    # chapter_blocks[0] is preamble, then [1]=index, [2]=content, [3]=index, [4]=content...
    i = 1
    while i < len(chapter_blocks):
        try:
            idx = int(chapter_blocks[i])
        except ValueError:
            i += 2
            continue

        content = chapter_blocks[i + 1] if i + 1 < len(chapter_blocks) else ""

        # Extract title (first line)
        title_match = re.search(r"^(.+?)(?:\n|$)", content.strip())
        title = title_match.group(1).strip() if title_match else f"Chapter {idx}"

        # Extract thesis
        thesis_match = re.search(r"\*\*核心命题\*\*\s*[：:]\s*(.+?)(?:\n|$)", content)
        thesis = thesis_match.group(1).strip() if thesis_match else ""

        # Extract video range
        range_match = re.search(r"\*\*视频范围\*\*\s*[：:]\s*(.+?)(?:\n|$)", content)
        video_range = range_match.group(1).strip() if range_match else ""

        # Extract prerequisites (wikilinks)
        prereq_match = re.search(r"\*\*前置知识\*\*\s*[：:]\s*(.+?)(?:\n|$)", content)
        prerequisites: list[str] = []
        if prereq_match:
            prereq_text = prereq_match.group(1)
            prerequisites = re.findall(r"\[\[(.+?)\]\]", prereq_text)

        # Extract summary
        summary_match = re.search(r"\*\*本章概要\*\*\s*[：:]\s*(.+?)(?=\n##|\Z)", content, re.DOTALL)
        summary = summary_match.group(1).strip() if summary_match else ""

        chapters.append(
            Chapter(
                index=idx,
                title=title,
                thesis=thesis,
                video_range=video_range,
                prerequisites=prerequisites,
                summary=summary,
            )
        )

        i += 2

    return chapters


def save_syllabus(text: str, course_name: str, output_dir: Path) -> Path:
    """Save raw syllabus text to file."""
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / f"{course_name}_课程大纲.md"
    path.write_text(text, encoding="utf-8")
    return path


def load_syllabus(path: Path) -> list[Chapter]:
    """Load and parse syllabus from file."""
    text = path.read_text(encoding="utf-8")
    return parse_syllabus(text)
