"""
Generate chapter notes and course artifacts (MOC, Anki).

Orchestrates:
  - Phase 1: Syllabus generation via NotebookLM
  - Phase 2: Chapter deep-dive with pressure-test rounds
  - Phase 3: MOC, next-steps, Anki generation
"""

import time
from pathlib import Path
from typing import Optional

from config.notebooklm import load_config
from config.note_paths import (
    chapter_note_path,
    moc_path,
    anki_path,
    raw_note_dir,
    permanent_note_dir,
)
from config import prompts
from models.note import Chapter, CourseContext, PressureTestRound
from lib import notebooklm_client


# ── Pressure test round definitions ──

PRESSURE_ROUNDS: list[PressureTestRound] = [
    PressureTestRound(
        name="定义与分类",
        prompt_template=prompts.PRESSURE_TEST_DEFINITION,
        focus="definition",
    ),
    PressureTestRound(
        name="数学推导",
        prompt_template=prompts.PRESSURE_TEST_DERIVATION,
        focus="derivation",
    ),
    PressureTestRound(
        name="案例对撞",
        prompt_template=prompts.PRESSURE_TEST_CASE,
        focus="case",
    ),
    PressureTestRound(
        name="学术批判",
        prompt_template=prompts.PRESSURE_TEST_CRITIQUE,
        focus="critique",
    ),
    PressureTestRound(
        name="跨章关联",
        prompt_template=prompts.PRESSURE_TEST_CROSS,
        focus="cross",
    ),
]


# ── Phase 1: Syllabus ──

def generate_syllabus(ctx: CourseContext) -> str:
    """
    Generate course syllabus via NotebookLM.

    Returns raw markdown text from NotebookLM.
    """
    print("\n" + "=" * 60)
    print("Phase 1: Generating Syllabus")
    print("=" * 60)

    notebooklm_client.use_notebook(ctx.notebook_id)
    notebooklm_client.configure_persona(load_config().persona)

    print("[INFO] Asking NotebookLM to generate syllabus...")
    response = notebooklm_client.ask(prompts.SYLLABUS_PROMPT, timeout=300)

    print(f"[OK] Syllabus received: {len(response)} chars")
    return response


# ── Phase 2: Chapter Deep Dive ──

def _build_chapter_prompt(chapter: Chapter, round_idx: int) -> str:
    """Build the prompt for a specific pressure-test round."""
    if round_idx == 0:
        # First round: comprehensive deep-dive
        return prompts.CHAPTER_DEEP_DIVE_PROMPT.format(video_range=chapter.video_range)

    # Subsequent rounds: pressure tests
    round_cfg = PRESSURE_ROUNDS[(round_idx - 1) % len(PRESSURE_ROUNDS)]

    # Extract concepts from thesis/summary for template filling
    prompt = round_cfg.prompt_template.format(
        video_range=chapter.video_range,
        concept_a=chapter.thesis[:50] if chapter.thesis else "核心概念",
        concept_b="相关概念A",
        concept_c="相关概念B",
        theorem=chapter.thesis[:50] if chapter.thesis else "核心定理",
        mechanism=chapter.thesis[:50] if chapter.thesis else "核心机制",
    )
    return prompt


def generate_chapter_note(
    ctx: CourseContext,
    chapter: Chapter,
    max_rounds: int = 5,
) -> Path:
    """
    Generate a chapter note through multiple pressure-test rounds.

    Args:
        ctx: Course context
        chapter: Chapter to process
        max_rounds: Number of pressure-test rounds (default 5)

    Returns:
        Path to saved chapter note file
    """
    print(f"\n{'=' * 60}")
    print(f"Chapter {chapter.index}: {chapter.title}")
    print(f"Video range: {chapter.video_range}")
    print(f"Rounds: {max_rounds}")
    print("=" * 60)

    notebooklm_client.use_notebook(ctx.notebook_id)

    sections: list[str] = []

    # Build header
    header = f"""# Ch.{chapter.index:02d} {chapter.title}

> **Metadata**
> - 署名：DALONG ZHANG
> - 课程：{ctx.course_name}
> - 视频范围：{chapter.video_range}
> - 核心命题：{chapter.thesis}
> - 关联笔记：{' | '.join(chapter.prerequisites) if chapter.prerequisites else '待补充'}

---

"""
    sections.append(header)

    # Execute rounds
    for r in range(max_rounds):
        round_name = (
            "综合深挖" if r == 0 else PRESSURE_ROUNDS[(r - 1) % len(PRESSURE_ROUNDS)].name
        )
        print(f"\n  [Round {r + 1}/{max_rounds}] {round_name}")

        prompt = _build_chapter_prompt(chapter, r)
        try:
            response = notebooklm_client.ask(prompt, timeout=300)
            sections.append(f"## 第{r + 1}轮：{round_name}\n\n{response}\n\n---\n\n")
            print(f"  [OK] Response: {len(response)} chars")
        except Exception as e:
            print(f"  [WARN] Round failed: {e}")
            sections.append(f"## 第{r + 1}轮：{round_name}\n\n[生成失败: {e}]\n\n---\n\n")

        time.sleep(2)  # rate limit between rounds

    # Combine and save
    content = "\n".join(sections)
    output_path = chapter_note_path(ctx.course_name, chapter.index, chapter.title)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding="utf-8")

    print(f"[OK] Saved: {output_path}")
    return output_path


# ── Phase 3: Capstone Synthesis ──

def generate_moc(ctx: CourseContext) -> Path:
    """Generate Map of Contents (MOC)."""
    print("\n" + "=" * 60)
    print("Phase 3.1: Generating MOC")
    print("=" * 60)

    notebooklm_client.use_notebook(ctx.notebook_id)

    prompt = prompts.MOC_PROMPT.format(course_name=ctx.course_name)
    response = notebooklm_client.ask(prompt, timeout=300)

    output_path = moc_path(ctx.course_name)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    header = f"""# {ctx.course_name} 知识地图 (MOC)

> **Metadata**
> - 署名：DALONG ZHANG
> - 生成时间：{time.strftime('%Y-%m-%d %H:%M:%S')}
> - 章节数：{len(ctx.chapters)}

---

"""
    output_path.write_text(header + response, encoding="utf-8")
    print(f"[OK] MOC saved: {output_path}")
    return output_path


def generate_next_steps(ctx: CourseContext) -> str:
    """Generate next steps / advanced learning path."""
    print("\n" + "=" * 60)
    print("Phase 3.2: Generating Next Steps")
    print("=" * 60)

    notebooklm_client.use_notebook(ctx.notebook_id)

    prompt = prompts.NEXT_STEPS_PROMPT.format(course_name=ctx.course_name)
    response = notebooklm_client.ask(prompt, timeout=300)

    # Append to MOC
    moc = moc_path(ctx.course_name)
    if moc.exists():
        existing = moc.read_text(encoding="utf-8")
        moc.write_text(
            existing + "\n\n---\n\n# 进阶学习路径\n\n" + response,
            encoding="utf-8",
        )
        print(f"[OK] Next steps appended to MOC")

    return response


def generate_anki(ctx: CourseContext, card_count: int = 20) -> Path:
    """Generate Anki flashcards."""
    print("\n" + "=" * 60)
    print(f"Phase 3.3: Generating Anki Cards ({card_count})")
    print("=" * 60)

    notebooklm_client.use_notebook(ctx.notebook_id)

    prompt = prompts.ANKI_PROMPT.format(card_count=card_count)
    response = notebooklm_client.ask(prompt, timeout=300)

    output_path = anki_path(ctx.course_name, card_count)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    header = f"""# Anki: {ctx.course_name} ({card_count}张真题卡)

> **Metadata**
> - 署名：DALONG ZHANG
> - 生成时间：{time.strftime('%Y-%m-%d %H:%M:%S')}
> - 难度：研究生/CFA三级

---

"""
    output_path.write_text(header + response, encoding="utf-8")
    print(f"[OK] Anki saved: {output_path}")
    return output_path
