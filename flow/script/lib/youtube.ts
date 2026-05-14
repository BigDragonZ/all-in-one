/**
 * YouTube operations: title fetch, subtitle download, SRT parsing.
 */

import { dirname, join } from "https://deno.land/std@0.224.0/path/mod.ts";
import { BINARIES, PATHS } from "../config/paths.ts";
import type { SubtitleEntry, VideoMeta } from "../types/video.ts";

const YTDLP = BINARIES.ytDlp;

/** Execute yt-dlp with given args */
async function runYtDlp(args: string[]): Promise<{ code: number; stdout: string; stderr: string }> {
  const cmd = new Deno.Command(YTDLP, {
    args,
    stdout: "piped",
    stderr: "piped",
  });
  const { code, stdout, stderr } = await cmd.output();
  return {
    code,
    stdout: new TextDecoder().decode(stdout),
    stderr: new TextDecoder().decode(stderr),
  };
}

/** Fetch video title from URL */
export async function fetchTitle(url: string): Promise<string> {
  const { code, stdout, stderr } = await runYtDlp([
    "--cookies-from-browser", "chrome",
    "--no-warnings",
    "--print", "%(title)s",
    "--skip-download",
    url,
  ]);
  if (code !== 0) throw new Error(`fetchTitle failed: ${stderr}`);
  return stdout.trim();
}

/** Fetch playlist metadata (title + video list) */
export async function fetchPlaylist(url: string): Promise<{ title: string; videos: VideoMeta[] }> {
  const { code, stdout, stderr } = await runYtDlp([
    "--cookies-from-browser", "chrome",
    "--flat-playlist",
    "-j",
    "--no-warnings",
    url,
  ]);
  if (code !== 0 || !stdout.trim()) {
    throw new Error(`fetchPlaylist failed: ${stderr.slice(0, 200)}`);
  }

  const lines = stdout.trim().split("\n");
  const first = JSON.parse(lines[0]);
  const playlistTitle = first.playlist_title || "Unknown";
  const seen = new Set<string>();
  const videos: VideoMeta[] = [];

  for (const line of lines) {
    if (!line) continue;
    const data = JSON.parse(line);
    const videoUrl = data.url || data.webpage_url || "";
    if (!videoUrl || seen.has(videoUrl)) continue;
    seen.add(videoUrl);
    videos.push({
      id: data.id || "",
      title: data.title || "Unknown",
      url: videoUrl,
      index: videos.length + 1,
    });
  }

  return { title: playlistTitle, videos };
}

/** Download auto-generated English subtitle to temp path, return SRT file path */
export async function downloadSubtitle(
  url: string,
  tempBase: string,
): Promise<string> {
  const { code, stderr } = await runYtDlp([
    "--cookies-from-browser", "chrome",
    "--no-warnings",
    "--write-auto-subs",
    "--skip-download",
    "--sub-langs", "en",
    "--convert-subs", "srt",
    "--output", tempBase,
    url,
  ]);

  if (code !== 0 && !stderr.includes("Downloading")) {
    throw new Error(`yt-dlp exited ${code}: ${stderr}`);
  }

  const srtFile = `${tempBase}.en.srt`;
  try {
    await Deno.stat(srtFile);
    return srtFile;
  } catch {
    const alt = `${tempBase}.srt`;
    await Deno.stat(alt);
    return alt;
  }
}

/** Parse SRT content into structured entries */
export function parseSrt(content: string): SubtitleEntry[] {
  const blocks = content.trim().split(/\n\s*\n/);
  const entries: SubtitleEntry[] = [];

  for (const block of blocks) {
    const lines = block.trim().split("\n");
    if (lines.length < 3) continue;

    const idx = parseInt(lines[0].trim(), 10);
    if (isNaN(idx)) continue;

    const timeMatch = lines[1].match(/(\d{2}:\d{2}:\d{2},\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2},\d{3})/);
    if (!timeMatch) continue;

    const text = lines
      .slice(2)
      .join(" ")
      .replace(/\r/g, "")
      .replace(/<[^>]+>/g, "")
      .replace(/\[music\]|\[Music\]|\[音楽\]|♪/gi, "")
      .trim();

    if (!text) continue;

    entries.push({
      index: idx,
      start: timeMatch[1],
      end: timeMatch[2],
      text,
    });
  }

  return entries;
}

/** Convert subtitle entries to Markdown */
export function toMarkdown(
  entries: SubtitleEntry[],
  meta: { title: string; url: string; course: string; index: number },
): string {
  const lines: string[] = [];

  lines.push(`# ${meta.title}`);
  lines.push("");
  lines.push("## 元信息");
  lines.push("");
  lines.push(`- **序号**: ${meta.index}`);
  lines.push(`- **课程**: ${meta.course}`);
  lines.push(`- **链接**: ${meta.url}`);
  lines.push(`- **处理时间**: ${new Date().toISOString().slice(0, 19).replace("T", " ")}`);
  lines.push(`- **来源**: YouTube 自动生成字幕`);
  lines.push(`- **条目数**: ${entries.length}`);
  lines.push("");
  lines.push("---");
  lines.push("");
  lines.push("## 字幕内容");
  lines.push("");

  for (const e of entries) {
    lines.push(`**[${e.start} - ${e.end}]** ${e.text}`);
    lines.push("");
  }

  return lines.join("\n");
}
