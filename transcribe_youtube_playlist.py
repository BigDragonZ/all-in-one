#!/usr/bin/env python3
"""
YouTube 播放列表音频下载 + MLX Whisper 本地转写脚本
将结果保存为 Obsidian Markdown 笔记

用法:
    python3 transcribe_youtube_playlist.py

依赖安装:
    pip install mlx-whisper yt-dlp
"""

import os
import sys
import json
import re
import subprocess
import time
from pathlib import Path
from urllib.parse import urlparse, parse_qs
from typing import Optional, List, Dict

# ==================== 配置 ====================

# 播放列表 URL
PLAYLIST_URL = "https://www.youtube.com/playlist?list=PLBPbUxsZM4SaA8hFf4krZh_yotY5hSGsJ"

# Obsidian 笔记目录
OBSIDIAN_DIR = Path("/Users/naihe/Documents/all-in-one")

# 资料子目录名
NOTEBOOK_NAME = "期货与期权"

# Whisper 模型
WHISPER_MODEL = "large-v3"

# 音频格式
AUDIO_FORMAT = "mp3"
AUDIO_QUALITY = "5"  # 0=best, 10=worst; 5 is a good balance

# 同时下载数量
CONCURRENT_DOWNLOADS = 3

# 下载音频临时目录
TEMP_DIR = Path("/tmp/youtube_audio_downloads")

# =============================================


def get_playlist_videos(playlist_url: str) -> List[Dict]:
    """使用 yt-dlp 获取播放列表中的所有视频信息"""
    print("📋 正在获取播放列表信息...")
    
    cmd = [
        "yt-dlp",
        "-j", "--flat-playlist",
        "--playlist-start", "1",
        playlist_url
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"❌ 获取播放列表失败: {result.stderr}")
        sys.exit(1)
    
    videos = []
    for line in result.stdout.strip().split('\n'):
        if not line:
            continue
        try:
            data = json.loads(line)
            videos.append({
                'id': data['id'],
                'title': data['title'],
                'url': f"https://www.youtube.com/watch?v={data['id']}"
            })
        except json.JSONDecodeError:
            continue
    
    print(f"✅ 找到 {len(videos)} 个视频")
    return videos


def sanitize_filename(title: str) -> str:
    """清理文件名中的非法字符"""
    # 替换常见非法字符
    title = title.replace('/', '／').replace('\\', '＼')
    title = title.replace(':', '：').replace('*', '＊')
    title = title.replace('?', '？').replace('"', '＂')
    title = title.replace('<', '＜').replace('>', '＞')
    title = title.replace('|', '｜')
    # 移除控制字符
    title = re.sub(r'[\x00-\x1f\x7f]', '', title)
    # 限制长度
    if len(title) > 100:
        title = title[:100]
    return title.strip()


def download_audio(video_id: str, title: str, output_dir: Path) -> Optional[Path]:
    """下载视频的音频"""
    safe_title = sanitize_filename(title)
    output_template = str(output_dir / f"{safe_title}.%(ext)s")
    
    cmd = [
        "yt-dlp",
        "-f", "bestaudio/best",
        "-x", "--audio-format", AUDIO_FORMAT,
        "--audio-quality", AUDIO_QUALITY,
        "-o", output_template,
        "--no-playlist",
        "--progress",
        f"https://www.youtube.com/watch?v={video_id}"
    ]
    
    print(f"   ⬇️  下载音频: {title[:50]}...")
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"   ❌ 下载失败: {result.stderr[:200]}")
        return None
    
    # 找到下载的文件
    expected_file = output_dir / f"{safe_title}.{AUDIO_FORMAT}"
    if expected_file.exists():
        print(f"   ✅ 下载完成: {expected_file.name}")
        return expected_file
    
    # 尝试查找匹配的文件
    for f in output_dir.glob(f"{safe_title}.*"):
        if f.suffix in ['.mp3', '.m4a', '.wav', '.webm']:
            return f
    
    return None


def transcribe_audio(audio_path: Path, model: str = WHISPER_MODEL) -> Optional[Dict]:
    """使用 MLX Whisper 转写音频"""
    print(f"   🎯 开始转写: {audio_path.name}")
    
    try:
        import mlx_whisper
        
        result = mlx_whisper.transcribe(
            str(audio_path),
            path_or_hf_repo="mlx-community/whisper-large-v3-turbo",
            verbose=False,
            word_timestamps=False
        )
        
        print(f"   ✅ 转写完成")
        return result
        
    except Exception as e:
        print(f"   ❌ 转写失败: {str(e)[:200]}")
        return None


def format_timestamp(seconds: float) -> str:
    """将秒数转换为 HH:MM:SS 格式"""
    total = int(seconds)
    h, remainder = divmod(total, 3600)
    m, s = divmod(remainder, 60)
    return f"{h:02d}:{m:02d}:{s:02d}"


import re

def format_transcript_text(text: str) -> str:
    """将转写文本格式化为人类可读的段落形式，添加标点和分段"""
    
    # 步骤1: 基础清理
    # 去除重复的开头（如"请不吝点赞..."）
    text = re.sub(r'请不吝点赞.*?栏目\s*', '', text)
    
    # 步骤2: 添加逗号（短停顿）
    # 在连接词、副词后添加逗号
    comma_words = ['然后', '接着', '接下来', '于是', '因此', '所以', '但是', '然而', '不过', '可是', '另外', '此外', '例如', '比如', '首先', '其次', '最后', '第一', '第二', '第三']
    for word in comma_words:
        text = re.sub(f'(?<=[^，。])\s*{word}(?=\s)', f'，{word}', text)
    
    # 在语气词后添加逗号（短停顿）
    pause_words = ['啊', '呢', '吧', '嘛', '哦', '嗯', '哎', '唉', '哟', '哈']
    for word in pause_words:
        text = re.sub(f'{word}(?=\s+[你我他她它我们你们他们这那这里那里这个那个])', f'{word}，', text)
    
    # 步骤3: 添加句号（长停顿/句子结束）
    # 在句末助词后添加句号
    sentence_endings = ['的', '了', '吗']
    for ending in sentence_endings:
        text = re.sub(f'{ending}(?=\s+[但是所以然后接着接下来首先其次最后另外此外总之这那])', f'{ending}。', text)
    
    # 步骤4: 在问答模式后添加问号
    text = re.sub(r'(是不是|对不对|好不好|可以吗|行吗|对吗|多少|几|什么|为什么|怎么|哪里|谁)(?=\s+[你我他她它我们你们他们])', r'\1？', text)
    
    # 步骤5: 智能分段
    # 先按句号和问号分割
    raw_sentences = re.split(r'[。？]', text)
    
    paragraphs = []
    current_paragraph = []
    current_length = 0
    
    for sentence in raw_sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
        
        # 检查是否是新主题的开始
        is_new_topic = any(sentence.startswith(word) for word in topic_shifts)
        
        # 检查段落长度
        if is_new_topic or current_length > 200:
            if current_paragraph:
                paragraphs.append(''.join(current_paragraph))
                current_paragraph = []
                current_length = 0
        
        # 添加句号回来
        sentence += '。'
        current_paragraph.append(sentence)
        current_length += len(sentence)
    
    # 添加最后一段
    if current_paragraph:
        paragraphs.append(''.join(current_paragraph))
    
    # 步骤7: 后处理
    final_paragraphs = []
    for para in paragraphs:
        # 去除过短的段落（可能是噪音）
        if len(para) > 30:
            # 清理多余的空格
            para = re.sub(r'\s+', ' ', para)
            final_paragraphs.append(para)
    
    return '\n\n'.join(final_paragraphs)


def create_markdown_note(video: Dict, transcript: Dict, note_dir: Path, index: int) -> Path:
    """创建 Obsidian Markdown 笔记"""
    safe_title = sanitize_filename(video['title'])
    filename = f"{index:02d}_{safe_title}.md"
    filepath = note_dir / filename
    
    # 提取纯文本内容
    segments = transcript.get('segments', [])
    raw_text = ' '.join(seg['text'].strip() for seg in segments)
    
    # 格式化文本（添加标点和分段）
    formatted_text = format_transcript_text(raw_text)
    
    # 生成带时间戳的内容
    timestamped_lines = []
    for seg in segments:
        start = seg.get('start', 0)
        text = seg.get('text', '').strip()
        if text:
            timestamped_lines.append(f"[{format_timestamp(start)}] {text}")
    
    # 计算视频时长
    duration = 0
    if segments:
        last_seg = segments[-1]
        duration = last_seg.get('start', 0) + last_seg.get('end', 0) - last_seg.get('start', 0)
    
    # 构建 Markdown 内容
    md_content = f"""# {video['title']}

## 元信息

- **序号**: {index}
- **视频ID**: {video['id']}
- **链接**: https://www.youtube.com/watch?v={video['id']}
- **时长**: {format_timestamp(duration)}
- **转写时间**: {time.strftime('%Y-%m-%d %H:%M:%S')}
- **模型**: MLX Whisper {WHISPER_MODEL}

---

## 完整转写文本

{formatted_text}

---

## 带时间戳的转写

"""
    
    md_content += '\n'.join(timestamped_lines)
    md_content += '\n\n---\n\n*由 MLX Whisper 自动转写生成*\n'
    
    # 写入文件
    filepath.write_text(md_content, encoding='utf-8')
    print(f"   📝 笔记已保存: {filepath.name}")
    
    return filepath


def create_index_note(videos: List[Dict], note_dir: Path, success_indices: List[int]) -> None:
    """创建索引笔记"""
    index_path = note_dir / "_index.md"
    
    content = f"""# {NOTEBOOK_NAME}

> 本笔记由 YouTube 播放列表自动转写生成
> 播放列表: {PLAYLIST_URL}
> 生成时间: {time.strftime('%Y-%m-%d %H:%M:%S')}

## 视频列表

| 序号 | 标题 | 状态 | 链接 |
|------|------|------|------|
"""
    
    for i, video in enumerate(videos, 1):
        status = "✅ 已转写" if i in success_indices else "❌ 失败"
        note_link = f"[[{i:02d}_{sanitize_filename(video['title'])}]]" if i in success_indices else "-"
        content += f"| {i} | {video['title']} | {status} | [{video['id']}](https://www.youtube.com/watch?v={video['id']}) |\n"
    
    content += f"""

## 统计

- 总视频数: {len(videos)}
- 成功转写: {len(success_indices)}
- 失败: {len(videos) - len(success_indices)}

---

*自动生成，请勿手动编辑此索引文件*
"""
    
    index_path.write_text(content, encoding='utf-8')
    print(f"📑 索引笔记已创建: {index_path}")


def main():
    """主流程"""
    print("=" * 60)
    print("🎬 YouTube 播放列表音频下载 + MLX Whisper 转写")
    print("=" * 60)
    
    # 1. 检查依赖
    print("\n🔍 检查依赖...")
    
    # 检查 yt-dlp
    try:
        subprocess.run(["yt-dlp", "--version"], capture_output=True, check=True)
        print("✅ yt-dlp 已安装")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ yt-dlp 未安装，正在安装...")
        subprocess.run(["uv", "pip", "install", "yt-dlp"], check=True)
        print("✅ yt-dlp 安装完成")
    
    # 检查 mlx-whisper
    try:
        import mlx_whisper
        print("✅ mlx-whisper 已安装")
    except ImportError:
        print("❌ mlx-whisper 未安装，正在安装...")
        subprocess.run(["uv", "pip", "install", "mlx-whisper"], check=True)
        import mlx_whisper
        print("✅ mlx-whisper 安装完成")
    
    # 2. 创建目录
    print("\n📁 创建目录...")
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    note_dir = OBSIDIAN_DIR / NOTEBOOK_NAME
    note_dir.mkdir(parents=True, exist_ok=True)
    print(f"✅ 笔记目录: {note_dir}")
    print(f"✅ 临时目录: {TEMP_DIR}")
    
    # 3. 获取播放列表
    print("\n" + "=" * 60)
    videos = get_playlist_videos(PLAYLIST_URL)
    
    if not videos:
        print("❌ 未找到任何视频")
        sys.exit(1)
    
    # 4. 处理每个视频
    print("\n" + "=" * 60)
    print("🚀 开始处理视频...")
    print("=" * 60)
    
    success_indices = []
    failed_videos = []
    
    for i, video in enumerate(videos, 1):
        print(f"\n[{i}/{len(videos)}] 处理: {video['title']}")
        
        # 下载音频
        audio_path = download_audio(video['id'], video['title'], TEMP_DIR)
        if not audio_path:
            failed_videos.append(video)
            continue
        
        # 转写音频
        transcript = transcribe_audio(audio_path)
        if not transcript:
            failed_videos.append(video)
            # 清理音频文件
            audio_path.unlink(missing_ok=True)
            continue
        
        # 创建 Markdown 笔记
        note_path = create_markdown_note(video, transcript, note_dir, i)
        success_indices.append(i)
        
        # 清理音频文件（可选：保留或删除）
        audio_path.unlink(missing_ok=True)
        print(f"   🧹 已清理临时音频文件")
        
        # 间隔一下避免过载
        time.sleep(1)
    
    # 5. 创建索引
    print("\n" + "=" * 60)
    print("📑 创建索引笔记...")
    create_index_note(videos, note_dir, success_indices)
    
    # 6. 完成报告
    print("\n" + "=" * 60)
    print("✨ 处理完成!")
    print("=" * 60)
    print(f"总视频数: {len(videos)}")
    print(f"成功转写: {len(success_indices)}")
    print(f"失败: {len(failed_videos)}")
    print(f"笔记目录: {note_dir}")
    
    if failed_videos:
        print(f"\n失败的视频:")
        for v in failed_videos:
            print(f"  - {v['title']} ({v['id']})")
    
    # 清理临时目录
    if not any(TEMP_DIR.iterdir()):
        TEMP_DIR.rmdir()
        print(f"\n🧹 临时目录已清理")


if __name__ == "__main__":
    main()
