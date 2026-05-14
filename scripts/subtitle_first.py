#!/usr/bin/env python3
"""
课程知识库构建 — 阶段零：字幕优先转写
======================================
策略：字幕提取 → Gemini 精修 → Markdown 输出
复用 all-in-one 项目 venv，无需独立环境

用法:
    uv run scripts/subtitle_first.py --playlist "URL" [--note-dir DIR]
    uv run scripts/subtitle_first.py --video "https://www.youtube.com/watch?v=..."
"""

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path
from typing import Optional

from google import genai
from google.genai.types import GenerateContentConfig, HttpOptions
from youtube_transcript_api import YouTubeTranscriptApi

# ═══════════════════════════════════════════════════════════
# 默认配置（可通过命令行覆盖）
# ═══════════════════════════════════════════════════════════

DEFAULT_NOTE_DIR = Path("/Users/naihe/Documents/all-in-one")
DEFAULT_MODEL = "gemini-2.5-flash-lite"
API_VERSION = "v1"

# ═══════════════════════════════════════════════════════════
# 工具函数
# ═══════════════════════════════════════════════════════════


def sanitize_filename(title: str) -> str:
    """清理文件名中的非法字符"""
    invalid = '<>:"/\\|?*'
    for c in invalid:
        title = title.replace(c, '_')
    return title.strip()


def extract_video_id(url: str) -> Optional[str]:
    """从 YouTube URL 提取视频 ID"""
    patterns = [
        r'(?:v=|/v/|/embed/|/shorts/)([A-Za-z0-9_-]{11})',
        r'youtu\.be/([A-Za-z0-9_-]{11})',
    ]
    for p in patterns:
        m = re.search(p, url)
        if m:
            return m.group(1)
    return None


def get_playlist_videos(url: str) -> tuple[str, list[dict]]:
    """使用 yt-dlp 获取播放列表信息"""
    import subprocess

    cmd = [
        sys.executable, "-m", "yt_dlp",
        "--cookies-from-browser", "chrome",
        "-j", "--flat-playlist", url,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    if result.returncode != 0 or not result.stdout.strip():
        print(f"yt-dlp 错误: {result.stderr[:200]}")
        return "Unknown", []

    lines = result.stdout.strip().split("\n")
    first = json.loads(lines[0])
    playlist_title = first.get("playlist_title", "Unknown")
    videos = []
    seen = set()
    for line in lines:
        if not line:
            continue
        data = json.loads(line)
        vid = data.get("id", "")
        if vid in seen:
            continue
        seen.add(vid)
        videos.append({
            "id": vid,
            "title": data.get("title", "Unknown"),
            "url": data.get("url") or data.get("webpage_url", ""),
        })
    return playlist_title, videos


def extract_subtitles(video_id: str, languages: list[str] = None) -> list[dict]:
    """提取字幕，返回带时间戳的段落列表"""
    try:
        ytt_api = YouTubeTranscriptApi()
        transcript = ytt_api.fetch(video_id, languages=languages or ["en"])
        return [{"start": seg.start, "text": seg.text} for seg in transcript]
    except Exception as e:
        print(f"   字幕提取失败: {e}")
        return []


def refine_transcript(raw_text: str, api_key: str, model: str) -> str:
    """使用 Gemini 精修转录文本"""
    client = genai.Client(
        vertexai=True,
        api_key=api_key,
        http_options=HttpOptions(api_version=API_VERSION),
    )

    prompt = f"""You are a professional transcription editor for finance lectures.
Please refine the following raw transcript into clean, well-structured Markdown.

Requirements:
1. Add proper punctuation (periods, commas, apostrophes)
2. Capitalize sentences correctly
3. Break into logical paragraphs (3-5 sentences each)
4. Add ## headers for major topic shifts
5. Preserve all original content - do not summarize or omit
6. Use bullet points for lists if applicable
7. Format financial terms consistently

Raw transcript:
{raw_text}

Output only the refined Markdown content."""

    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=GenerateContentConfig(temperature=0.0, max_output_tokens=8192),
    )

    if not response.candidates:
        raise RuntimeError("Empty response from Gemini")
    return response.candidates[0].content.parts[0].text


def create_note(
    title: str,
    video_id: str,
    refined_text: str,
    segments: list[dict],
    output_dir: Path,
    index: int = 0,
) -> Path:
    """创建 Obsidian 格式的 Markdown 笔记"""
    output_dir.mkdir(parents=True, exist_ok=True)
    safe_title = sanitize_filename(title)
    prefix = f"{index:02d}_" if index > 0 else ""
    note_path = output_dir / f"{prefix}{safe_title}.md"

    # 带时间戳的转写
    timestamped = []
    for seg in segments:
        ts = int(seg["start"])
        mm, ss = divmod(ts, 60)
        timestamped.append(f"[{mm:02d}:{ss:02d}] {seg['text']}")

    content = f"""---
title: {title}
source: https://www.youtube.com/watch?v={video_id}
method: subtitle + gemini-refine
date: {time.strftime('%Y-%m-%d')}
index: {index}
---

# {title}

## 完整转写文本

{refined_text}

---

## 带时间戳的转写

{chr(10).join(timestamped)}

---

*由 youtube-transcript-api + Gemini 自动转写生成*
"""

    note_path.write_text(content, encoding="utf-8")
    return note_path


def create_index(note_dir: Path, videos: list[dict], playlist_url: str):
    """创建索引文件"""
    index_path = note_dir / "_index.md"
    existing = set()
    for f in note_dir.glob("*.md"):
        if f.name == "_index.md":
            continue
        try:
            existing.add(int(f.name[:2]))
        except:
            pass

    lines = [
        f"# {note_dir.name}",
        "",
        f"> 播放列表: {playlist_url}",
        f"> 生成时间: {time.strftime('%Y-%m-%d')}",
        "",
        "## 视频列表",
        "",
        "| 序号 | 标题 | 状态 | 链接 |",
        "|------|------|------|------|",
    ]
    for i, v in enumerate(videos, 1):
        status = "✅ 已处理" if i in existing else "❌ 未处理"
        lines.append(f"| {i:02d} | {v['title']} | {status} | [{v['id']}]({v['url']}) |")

    lines.extend([
        "",
        "## 统计",
        "",
        f"- 总视频数: {len(videos)}",
        f"- 已处理: {len(existing)}",
        f"- 未处理: {len(videos) - len(existing)}",
        "",
        "---",
        "",
        "*自动生成*",
    ])

    index_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"📑 索引已创建: {index_path}")


# ═══════════════════════════════════════════════════════════
# 主流程
# ═══════════════════════════════════════════════════════════


def process_single_video(video_id: str, title: str, note_dir: Path, api_key: str, model: str, index: int = 0) -> bool:
    """处理单个视频"""
    print(f"\n[{index}] {title[:60]}...")

    safe_title = sanitize_filename(title)
    prefix = f"{index:02d}_" if index > 0 else ""
    expected = note_dir / f"{prefix}{safe_title}.md"
    if expected.exists():
        print("   ⏭️  已存在，跳过")
        return True

    # 提取字幕
    print("   🔍 提取字幕...")
    segments = extract_subtitles(video_id)
    if not segments:
        print("   ❌ 无字幕，跳过")
        return False

    print(f"   ✅ 字幕获取成功 ({len(segments)} 段)")
    raw_text = " ".join(seg["text"] for seg in segments)

    # Gemini 精修
    print("   ✨ Gemini 精修中...")
    try:
        refined = refine_transcript(raw_text, api_key, model)
    except Exception as e:
        print(f"   ⚠️  精修失败，使用原始文本: {e}")
        refined = raw_text

    # 保存笔记
    note_path = create_note(title, video_id, refined, segments, note_dir, index)
    print(f"   📝 笔记已保存: {note_path.name}")
    return True


def process_playlist(playlist_url: str, note_dir: Path, api_key: str, model: str):
    """处理播放列表"""
    print(f"\n{'='*60}")
    print("🔗 获取播放列表信息...")
    playlist_title, videos = get_playlist_videos(playlist_url)
    if not videos:
        print("❌ 视频列表为空")
        return

    note_dir = note_dir / sanitize_filename(playlist_title)
    note_dir.mkdir(parents=True, exist_ok=True)

    print(f"{'='*60}")
    print(f"🎬 播放列表: {playlist_title}")
    print(f"📁 笔记目录: {note_dir}")
    print(f"📋 视频数量: {len(videos)}")
    print(f"{'='*60}")

    success = fail = skipped = 0
    for i, video in enumerate(videos, 1):
        safe_title = sanitize_filename(video["title"])
        expected = note_dir / f"{i:02d}_{safe_title}.md"
        if expected.exists():
            print(f"\n[{i}/{len(videos)}] ⏭️  已存在: {video['title'][:50]}...")
            skipped += 1
            continue

        ok = process_single_video(video["id"], video["title"], note_dir, api_key, model, i)
        if ok:
            success += 1
        else:
            fail += 1

        if i < len(videos):
            wait = 5 + (i % 3) * 3
            print(f"   ⏳ 等待 {wait} 秒...")
            time.sleep(wait)

    create_index(note_dir, videos, playlist_url)
    print(f"\n{'='*60}")
    print(f"✅ 完成: {success} 成功, {fail} 失败, {skipped} 跳过")
    print(f"{'='*60}")


# ═══════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════


def main():
    parser = argparse.ArgumentParser(description="课程知识库构建 — 字幕优先转写")
    parser.add_argument("--playlist", help="YouTube 播放列表 URL")
    parser.add_argument("--video", help="单个 YouTube 视频 URL")
    parser.add_argument("--note-dir", type=Path, default=DEFAULT_NOTE_DIR, help="笔记输出目录")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Gemini 模型名称")
    args = parser.parse_args()

    api_key = os.environ.get("GEMINI_API_KEY", "")
    if not api_key:
        print("❌ 未设置 GEMINI_API_KEY 环境变量")
        sys.exit(1)

    print("=" * 60)
    print("🎬 字幕优先转写 — 字幕提取 + Gemini 精修")
    print(f"🤖 模型: {args.model}")
    print("=" * 60)

    if args.playlist:
        process_playlist(args.playlist, args.note_dir, api_key, args.model)
    elif args.video:
        video_id = extract_video_id(args.video)
        if not video_id:
            print("❌ 无法解析视频 ID")
            sys.exit(1)
        process_single_video(video_id, "Single Video", args.note_dir, api_key, args.model)
    else:
        parser.print_help()
        sys.exit(1)

    print("\n" + "=" * 60)
    print("🎉 处理完成!")
    print("=" * 60)


if __name__ == "__main__":
    main()
