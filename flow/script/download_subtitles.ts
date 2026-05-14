#!/usr/bin/env -S deno run --allow-net --allow-read --allow-write --allow-run --allow-env
/**
 * Download YouTube video subtitles and convert to Markdown.
 *
 * Usage:
 *   deno run --allow-net --allow-read --allow-write --allow-run --allow-env \
 *     flow/script/download_subtitles.ts <URL> <COURSE_NAME> <INDEX>
 *
 * Example:
 *   deno run ... flow/script/download_subtitles.ts \
 *     "https://www.youtube.com/watch?v=LYGYvN5LUbA" \
 *     "Valuation_Undergrad_2022" 1
 *
 * Output:
 *   all-in-one/flow/Valuation_Undergrad_2022/01-Valuation A Preview.md
 */

import { dirname, join } from "https://deno.land/std@0.224.0/path/mod.ts";

const YTDLP_PATH = new URL("../../.venv/bin/yt-dlp", import.meta.url).pathname;
const PROJECT_ROOT = dirname(dirname(dirname(import.meta.url))).replace("file://", "");

function sanitizeFilename(name: string): string {
  return name.replace(/[<>:"/\\|?*]/g, "_").trim();
}

async function fetchVideoTitle(url: string): Promise<string> {
  const cmd = new Deno.Command(YTDLP_PATH, {
    args: ["--cookies-from-browser", "chrome", "--no-warnings", "--print", "%(title)s", "--skip-download", url],
    stdout: "piped",
    stderr: "piped",
  });
  const { code, stdout, stderr } = await cmd.output();
  if (code !== 0) {
    throw new Error(`Failed to fetch title: ${new TextDecoder().decode(stderr)}`);
  }
  return new TextDecoder().decode(stdout).trim();
}

async function downloadSubtitle(url: string, basePath: string): Promise<string> {
  const cmd = new Deno.Command(YTDLP_PATH, {
    args: [
      "--cookies-from-browser", "chrome",
      "--no-warnings",
      "--write-auto-subs",
      "--skip-download",
      "--sub-langs", "en",
      "--convert-subs", "srt",
      "--output", basePath,
      url,
    ],
    stdout: "piped",
    stderr: "piped",
  });

  const { code, stderr } = await cmd.output();
  const err = new TextDecoder().decode(stderr);

  if (code !== 0 && !err.includes("Downloading")) {
    throw new Error(`yt-dlp exited ${code}: ${err}`);
  }

  // yt-dlp appends .en.srt automatically
  const srtFile = `${basePath}.en.srt`;
  try {
    await Deno.stat(srtFile);
    return srtFile;
  } catch {
    const altFile = `${basePath}.srt`;
    await Deno.stat(altFile);
    return altFile;
  }
}

function parseSrt(content: string): Array<{ index: number; start: string; end: string; text: string }> {
  const blocks = content.trim().split(/\n\s*\n/);
  const entries: Array<{ index: number; start: string; end: string; text: string }> = [];

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

function srtToMarkdown(
  entries: Array<{ index: number; start: string; end: string; text: string }>,
  title: string,
  url: string,
  courseName: string,
  index: number
): string {
  const lines: string[] = [];

  lines.push(`# ${title}`);
  lines.push("");
  lines.push("## 元信息");
  lines.push("");
  lines.push(`- **序号**: ${index}`);
  lines.push(`- **课程**: ${courseName}`);
  lines.push(`- **链接**: ${url}`);
  lines.push(`- **处理时间**: ${new Date().toISOString().slice(0, 19).replace("T", " ")}`);
  lines.push(`- **来源**: YouTube 自动生成字幕`);
  lines.push("");
  lines.push("---");
  lines.push("");
  lines.push("## 字幕内容");
  lines.push("");

  for (const entry of entries) {
    lines.push(`**[${entry.start} - ${entry.end}]** ${entry.text}`);
    lines.push("");
  }

  return lines.join("\n");
}

// ── main ──────────────────────────────────────────────────────────────
const url = Deno.args[0];
const courseName = Deno.args[1];
const indexStr = Deno.args[2];

if (!url || !courseName || !indexStr) {
  console.error("Usage: download_subtitles.ts <URL> <COURSE_NAME> <INDEX>");
  console.error("  URL:          YouTube video or playlist URL");
  console.error("  COURSE_NAME:  Directory name under flow/");
  console.error("  INDEX:        Video sequence number (e.g., 1, 2, 3)");
  Deno.exit(1);
}

const index = parseInt(indexStr, 10);
if (isNaN(index) || index < 1) {
  console.error("[ERROR] INDEX must be a positive integer");
  Deno.exit(1);
}

const outDir = join(PROJECT_ROOT, "flow", courseName);
await Deno.mkdir(outDir, { recursive: true });

console.log(`[INFO] URL: ${url}`);
console.log(`[INFO] Course: ${courseName}`);
console.log(`[INFO] Index: ${index}`);
console.log(`[INFO] Output dir: ${outDir}`);

try {
  const title = await fetchVideoTitle(url);
  const safeTitle = sanitizeFilename(title);
  const filename = `${String(index).padStart(2, "0")}-${safeTitle}.md`;
  const outputPath = join(outDir, filename);

  // Temporary base path for yt-dlp (it auto-adds .en.srt)
  const tempBase = join(outDir, `_tmp_${Date.now()}`);

  console.log(`[INFO] Video title: ${title}`);
  console.log(`[INFO] Downloading subtitle...`);

  const srtFile = await downloadSubtitle(url, tempBase);

  console.log(`[INFO] Converting SRT to Markdown...`);
  const srtContent = await Deno.readTextFile(srtFile);
  const entries = parseSrt(srtContent);
  const markdown = srtToMarkdown(entries, title, url, courseName, index);

  await Deno.writeTextFile(outputPath, markdown);

  // Cleanup temp SRT file
  await Deno.remove(srtFile);
  // Also cleanup .srt if it was renamed
  try {
    await Deno.remove(`${tempBase}.en.srt`);
  } catch { /* ignore */ }

  console.log(`[SUCCESS] Markdown saved to: ${outputPath}`);
  console.log(`[INFO] Total entries: ${entries.length}`);

  Deno.exit(0);
} catch (e: any) {
  console.error(`[ERROR] ${e.message}`);
  Deno.exit(1);
}
